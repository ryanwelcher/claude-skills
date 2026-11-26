"""Local server for the stream-trim page: the page, the ranged preview, and
a small JSON API to read state and start/stop the final render, and the
Shorts view: previews, drafts, captions and renders through stream-shorts.

  python3 server.py <raw.mp4>     prints: READY http://127.0.0.1:<port>/
Run prepare.py on the recording first."""
import json
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import attention
import audio_chain
import prepare
import profiles
import streams
import render
import shorts_view

HERE = os.path.dirname(os.path.abspath(__file__))
CHUNK = 1 << 20
SHORTS_PY = os.path.normpath(os.path.join(HERE, "..", "..", "stream-shorts", "scripts", "shorts.py"))
SHORT_AUDIO = os.path.join(HERE, "short_audio.py")
TRANSCRIBE = os.path.normpath(os.path.join(HERE, "..", "..", "analyze-stream-recording", "scripts",
                                           "transcribe-file.sh"))
# The end time of a transcribed line in the worker's log: [MM:SS.mmm --> HH:MM:SS.mmm]
CUE_END = re.compile(r"--> (?:(\d+):)?(\d+):(\d+(?:\.\d+)?)\]")


def safe_title(title):
    """A title as a file name: Finder won't take ":" or "/", so ":" becomes
    " -" (like Ryan's Premiere exports) and "/" becomes "-"."""
    if not isinstance(title, str):
        raise ValueError("title must be text")
    t = title.replace(":", " -").replace("/", "-")
    t = re.sub(r"[\x00-\x1f]", "", t)
    t = re.sub(r"\s+", " ", t).strip().strip(".").strip()
    if not re.search(r"\w", t):
        raise ValueError("the title needs some letters or numbers")
    return t[:180].strip()


class TrimServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, raw, profile, port, shorts_py=SHORTS_PY):
        if not os.path.exists(shorts_py):
            raise FileNotFoundError(f"stream-shorts not found at {shorts_py}")
        self.raw = raw
        self.shorts_py = shorts_py
        self.shorts_dir = os.path.join(os.path.dirname(os.path.abspath(raw)), "shorts")
        self.profile = profile
        self.cache = prepare.cache_dir(raw)
        with open(os.path.join(self.cache, "analysis.json")) as f:
            self.analysis = json.load(f)
        # Same rule as prepare.py's cache reuse: a cache from before profiles is ryan-obs.
        cached = self.analysis.get("profile", "ryan-obs")
        key = self.analysis.get("profile_key", profiles.cache_key(profile))
        if cached != profile["name"] or key != profiles.cache_key(profile):
            raise profiles.ProfileError(
                f"the prepared cache was made with profile {cached}"
                f"{'' if cached != profile['name'] else ' before it was edited'}; "
                f"run prepare.py --profile {profile['name']} first")
        with open(os.path.join(self.cache, "peaks.json")) as f:
            self.peaks = json.load(f)
        self.work = os.path.join(self.cache, "shorts-work")
        self.edit_path = os.path.join(self.cache, "edit.json")
        self.titles_path = os.path.join(self.cache, "titles.json")
        self.thumbs_path = os.path.join(self.cache, "thumbs.json")
        self.dismissed_path = os.path.join(self.cache, "dismissed.json")
        self._transcript_dir = False  # not looked up yet
        # Transcript clock -> video clock (the shortlist's times are transcript times).
        self.shift = profiles.transcript_shift(profile, self.analysis["fps"])
        self.lock = threading.Lock()
        self.work_lock = threading.Lock()  # one preview/captions run at a time
        self.shorts_status = {"state": "idle", "clips": {}}
        # Show in Finder. Tests swap it for a list's append.
        self.open_cmd = lambda args: subprocess.run(args, check=False)
        # Set by Claude Code hooks (attention.py) while Claude waits on Ryan in the terminal.
        self.attention = {"waiting": False, "reason": None, "since": None}
        self.stop_event = threading.Event()
        self.status = {"state": "idle", "phase": None, "percent": 0, "output": None, "error": None}
        super().__init__(("127.0.0.1", port), Handler)

    # -- the Shorts tab's states: rendered and dismissed survive a reload --

    def rendered(self):
        """{n: the clip as rendered (shorts.json) and whether its file is there}."""
        try:
            with open(os.path.join(self.shorts_dir, "shorts.json")) as f:
                m = json.load(f)
        except (OSError, ValueError):
            return {}
        clips = m.get("clips", []) if isinstance(m, dict) else m if isinstance(m, list) else []
        out = {}
        for c in clips:
            n = shorts_view.number(c) if isinstance(c, dict) else None
            if n is None:
                continue
            out[str(n)] = {**{k: c.get(k) for k in ("file", "start", "end", "layout", "pan_x", "fixes")},
                           "exists": os.path.exists(os.path.join(self.shorts_dir, c["file"]))}
        return out

    def dismissed(self):
        try:
            with open(self.dismissed_path) as f:
                return sorted(n for n in json.load(f) if isinstance(n, int))
        except (OSError, ValueError, TypeError):
            return []

    def dismiss(self, body):
        """Ryan's "Not this one" (dismissed: true) and Restore (false)."""
        if not isinstance(body, dict) or isinstance(body.get("n"), bool) or not isinstance(body.get("n"), int) \
                or not isinstance(body.get("dismissed"), bool):
            return 400, {"error": "expected {\"n\": number, \"dismissed\": true|false}"}
        clips, _, _ = self.candidates()
        if not any(c["n"] == body["n"] for c in clips or []):
            return 400, {"error": f"no short numbered {body['n']}"}
        with self.lock:
            now = set(self.dismissed())
            (now.add if body["dismissed"] else now.discard)(body["n"])
            write_json(self.dismissed_path, sorted(now))
        return 200, {"dismissed": sorted(now)}

    def set_attention(self, body):
        if not isinstance(body, dict) or not isinstance(body.get("waiting"), bool) \
                or not isinstance(body.get("reason", ""), (str, type(None))):
            return 400, {"error": "expected {\"waiting\": true|false, \"reason\": text}"}
        with self.lock:
            if body["waiting"]:
                self.attention = {"waiting": True, "reason": (body.get("reason") or "Claude needs you in the terminal")[:200],
                                  "since": self.attention["since"] or time.time()}
            else:
                self.attention = {"waiting": False, "reason": None, "since": None}
        return 200, {"ok": True}

    def streams(self):
        """Every stream with a cache next to this one's, and this one's id."""
        return {"current": os.path.basename(self.cache),
                "streams": streams.list_streams(os.path.dirname(self.cache))}

    def reveal(self, body):
        """Show a stream's raw, final, shorts folder or description in Finder.
        The page names the stream and the item, never a path."""
        if not isinstance(body, dict):
            return 400, {"error": "expected a JSON object"}
        if body.get("target") == "thumb":
            if not self.thumb_known(body.get("path")):
                return 404, {"error": "no such thumbnail"}
            self.open_cmd(["open", "-R", body["path"]])
            return 200, {"path": body["path"]}
        if body.get("target") == "short":
            r = self.rendered().get(str(body.get("n")))
            if not r or not r["exists"]:
                return 404, {"error": "that short isn't rendered"}
            path = os.path.join(self.shorts_dir, r["file"])
            self.open_cmd(["open", "-R", path])
            return 200, {"path": path}
        want = body.get("stream") or os.path.basename(self.cache)
        target = body.get("target")
        if target not in streams.TARGETS:
            return 400, {"error": f"target must be one of {', '.join(streams.TARGETS)}"}
        stream = next((x for x in self.streams()["streams"] if x["id"] == want), None)
        if stream is None:
            return 404, {"error": "no such stream"}
        cmd = streams.reveal_target(stream, target)
        if cmd is None:
            return 404, {"error": f"this stream has no {target} yet"}
        self.open_cmd(cmd)
        return 200, {"path": cmd[-1]}

    def final_output(self):
        """The final's path: where the edit says it went (it may have been
        renamed to its title), else where a render would write it."""
        edit = self.edit()
        if edit and edit.get("output") and os.path.exists(edit["output"]):
            return edit["output"]
        return render.final_path(self.raw)

    # -- finding shorts --

    def transcript_dir(self):
        """The transcriber's cache folder for this recording (find-stream-shorts'
        run), or None. Looked up once; looking creates nothing."""
        if self._transcript_dir is False:
            self._transcript_dir = None
            try:
                r = subprocess.run(["bash", TRANSCRIBE, self.raw, "60"], capture_output=True, text=True, timeout=20,
                                   env={**os.environ, "TRANSCRIBE_PRINT_DIR": "1"})
                m = re.match(r"DIR: (.+)", r.stdout)
                self._transcript_dir = m.group(1).strip() if m else None
            except (OSError, subprocess.SubprocessError):
                pass
        return self._transcript_dir

    def finding(self):
        """Where finding the shorts is up to, for the page."""
        if os.path.exists(os.path.join(self.shorts_dir, "candidates.json")):
            return {"stage": "ready"}
        d = self.transcript_dir()
        if not d or not os.path.isdir(d):
            return {"stage": "waiting"}
        if os.path.exists(os.path.join(d, "failed")):
            with open(os.path.join(d, "failed")) as f:
                return {"stage": "error", "error": f.read().strip()}
        if os.path.exists(os.path.join(d, "done")):
            return {"stage": "picking", "since": os.path.getmtime(os.path.join(d, "done"))}
        try:
            with open(os.path.join(d, "log"), "rb") as f:
                f.seek(max(0, os.path.getsize(f.name) - 65536))
                tail = f.read().decode(errors="replace")
        except OSError:
            return {"stage": "waiting"}
        if "Re-transcribing" in tail:
            return {"stage": "checking"}
        cues = CUE_END.findall(tail)
        if cues or "Transcribing with" in tail:
            at, duration = 0.0, self.analysis["duration"]
            if cues:
                h, m, s = cues[-1]
                at = int(h or 0) * 3600 + int(m) * 60 + float(s)
            return {"stage": "transcribing", "at": at, "duration": duration,
                    "percent": round(min(99.9, at / duration * 100), 1)}
        return {"stage": "audio"} if "Extracting audio" in tail else {"stage": "waiting"}

    # -- titles --

    def titles(self):
        try:
            with open(self.titles_path) as f:
                t = json.load(f)
        except (OSError, ValueError):
            t = {}
        return {"options": t.get("options", {}), "picked": t.get("picked", {}), "files": t.get("files", {})}

    def post_titles(self, body):
        """Claude's title options: {"final": [...], "shorts": {"<n>": [...]}},
        each option {"title": str, "score": number or null}. Merged in."""
        def options(lst):
            if not isinstance(lst, list):
                raise ValueError("options must be a list")
            out = []
            for o in lst:
                if not isinstance(o, dict) or not isinstance(o.get("title"), str) or not o["title"].strip():
                    raise ValueError("each option needs a \"title\"")
                score = o.get("score")
                if score is not None and (isinstance(score, bool) or not isinstance(score, (int, float))):
                    raise ValueError("score must be a number or null")
                out.append({"title": o["title"].strip()[:200], "score": score})
            return out

        if not isinstance(body, dict) or not set(body) <= {"final", "shorts"}:
            return 400, {"error": "expected {\"final\": [...], \"shorts\": {\"<n>\": [...]}}"}
        try:
            new = {}
            if "final" in body:
                new["final"] = options(body["final"])
            shorts = body.get("shorts", {})
            if not isinstance(shorts, dict) or not all(str(k).isdigit() for k in shorts):
                raise ValueError("shorts must be {\"<number>\": [...]}")
            for k, v in shorts.items():
                new[str(int(k))] = options(v)
        except ValueError as e:
            return 400, {"error": str(e)}
        with self.lock:
            t = self.titles()
            t["options"].update(new)
            write_json(self.titles_path, t)
        return 200, {"ok": True}

    def pick_title(self, body):
        """Ryan's pick: rename the final, or short n, to the title."""
        if not isinstance(body, dict):
            return 400, {"error": "expected a JSON object"}
        target, title = body.get("target"), body.get("title")
        if target != "final" and (isinstance(target, bool) or not isinstance(target, int) or target < 0):
            return 400, {"error": "target must be \"final\" or a short's number"}
        try:
            name = safe_title(title)
        except ValueError as e:
            return 400, {"error": str(e)}
        with self.lock:
            if target == "final":
                if self.status["state"] == "running":
                    return 409, {"error": "the final is still rendering"}
                edit = self.edit()
                old = edit and edit.get("output")
                if not old or not os.path.exists(old):
                    return 409, {"error": "render the final first"}
                new = os.path.join(os.path.dirname(old), name + ".mp4")
            else:
                if self.shorts_status["state"] == "running":
                    return 409, {"error": "wait for the shorts to finish rendering"}
                manifest = os.path.join(self.shorts_dir, "shorts.json")
                try:
                    with open(manifest) as f:
                        m = json.load(f)
                except (OSError, ValueError):
                    m = {}
                clips = m.get("clips", []) if isinstance(m, dict) else []
                clip = next((c for c in clips if shorts_view.number(c) == target), None)
                old = clip and os.path.join(self.shorts_dir, clip["file"])
                if not old or not os.path.exists(old):
                    return 409, {"error": f"render short {target} first"}
                new = os.path.join(self.shorts_dir, f"{target:02d} - {name}.mp4")
            if new != old:
                if os.path.exists(new):
                    return 409, {"error": f"{os.path.basename(new)} already exists"}
                os.rename(old, new)
                self.rename_thumbs("final" if target == "final" else str(target), old, new)
            t = self.titles()
            if target == "final":
                write_json(self.edit_path, {**edit, "output": new})
                t["picked"]["final"] = title.strip()
            else:
                clip["file"] = os.path.basename(new)
                write_json(manifest, m)
                t["picked"][str(target)] = title.strip()
                t["files"][str(target)] = clip["file"]
            write_json(self.titles_path, t)
        return 200, {"path": new}

    # -- thumbnails --

    def thumbs(self):
        try:
            with open(self.thumbs_path) as f:
                t = json.load(f)
        except (OSError, ValueError):
            t = {}
        return {"options": t.get("options", {}), "picked": t.get("picked", {}),
                "picked_from": t.get("picked_from", {}),
                "requests": t.get("requests", []), "next_id": t.get("next_id", 1)}

    def thumbs_public(self):
        t = self.thumbs()
        return {"options": t["options"], "picked": t["picked"], "picked_from": t["picked_from"],
                "requests": t["requests"]}

    def post_thumbs(self, body):
        """Claude's thumbnail options: {"final": [...], "shorts": {"<n>": [...]}},
        each {"file": abs path to a .jpg, "kind": "plain"|"vidiq"}. Appended."""
        def options(lst):
            if not isinstance(lst, list):
                raise ValueError("options must be a list")
            out = []
            for o in lst:
                if not isinstance(o, dict) or not isinstance(o.get("file"), str):
                    raise ValueError("each option needs a \"file\"")
                if o.get("kind") not in ("plain", "vidiq"):
                    raise ValueError("kind must be plain or vidiq")
                f = o["file"]
                if not os.path.isabs(f) or not f.lower().endswith(".jpg") or not os.path.isfile(f):
                    raise ValueError(f"no such .jpg: {f}")
                out.append({"file": f, "kind": o["kind"]})
            return out

        if not isinstance(body, dict) or not set(body) <= {"final", "shorts"}:
            return 400, {"error": "expected {\"final\": [...], \"shorts\": {\"<n>\": [...]}}"}
        try:
            new = {}
            if "final" in body:
                new["final"] = options(body["final"])
            shorts = body.get("shorts", {})
            if not isinstance(shorts, dict) or not all(str(k).isdigit() for k in shorts):
                raise ValueError("shorts must be {\"<number>\": [...]}")
            for k, v in shorts.items():
                new[str(int(k))] = options(v)
        except ValueError as e:
            return 400, {"error": str(e)}
        with self.lock:
            t = self.thumbs()
            for k, opts in new.items():
                have = t["options"].setdefault(k, [])
                for o in opts:
                    if all(h["file"] != o["file"] for h in have):
                        have.append(o)
            write_json(self.thumbs_path, t)
        return 200, {"ok": True}

    def video_for(self, target):
        """The rendered video for "final" or a short's number, or None."""
        if target == "final":
            edit = self.edit()
            out = edit and edit.get("output")
        else:
            out = None
            clip = self.rendered().get(str(target))
            if clip and clip.get("exists"):
                out = os.path.join(self.shorts_dir, clip["file"])
        return out if out and os.path.exists(out) else None

    def thumb_action(self, body):
        """Ryan on the page: pick an option, or queue a change or a polish for Claude."""
        if not isinstance(body, dict):
            return 400, {"error": "expected a JSON object"}
        target, f = body.get("target"), body.get("file")
        if target != "final" and (isinstance(target, bool) or not isinstance(target, int) or target < 0):
            return 400, {"error": "target must be \"final\" or a short's number"}
        change, polish = body.get("change"), body.get("polish", False)
        if change is not None and (not isinstance(change, str) or not 1 <= len(change.strip()) <= 500):
            return 400, {"error": "say what to change (up to 500 characters)"}
        if polish not in (True, False) or (polish and change is not None):
            return 400, {"error": "polish is true or left out, without a change"}
        key = "final" if target == "final" else str(target)
        with self.lock:
            video = self.video_for(target)
            if not video:
                return 409, {"error": "render it first"}
            t = self.thumbs()
            opt = next((o for o in t["options"].get(key, []) if o["file"] == f), None)
            if not opt or not os.path.isfile(f):
                return 409, {"error": "that thumbnail isn't there any more"}
            if polish and opt["kind"] != "plain":
                return 400, {"error": "only a plain thumbnail can be polished"}
            if change is None and not polish:
                dest = os.path.splitext(video)[0] + ".jpg"
                shutil.copyfile(f, dest)
                t["picked"][key] = dest
                t["picked_from"][key] = f
                write_json(self.thumbs_path, t)
                return 200, {"path": dest}
            rid = t["next_id"]
            t["next_id"] = rid + 1
            t["requests"].append({"id": rid, "target": target, "file": f,
                                  "change": change.strip() if change else None, "polish": bool(polish)})
            write_json(self.thumbs_path, t)
        return 200, {"id": rid}

    def thumb_known(self, path):
        """True if path is a current thumbnail option or pick (the page may
        only see or reveal those)."""
        t = self.thumbs()
        known = {o["file"] for opts in t["options"].values() for o in opts} | set(t["picked"].values())
        return isinstance(path, str) and path in known and os.path.isfile(path)

    def thumbs_done(self, body):
        rid = body.get("id") if isinstance(body, dict) else None
        with self.lock:
            t = self.thumbs()
            left = [r for r in t["requests"] if r["id"] != rid]
            if len(left) == len(t["requests"]):
                return 404, {"error": "no such request"}
            t["requests"] = left
            write_json(self.thumbs_path, t)
        return 200, {"ok": True}

    def rename_thumbs(self, key, old_video, new_video):
        """A title pick renamed a video: its picked .jpg and its options
        (thumbnails/<stem>-*.jpg) follow. Call with the lock held."""
        old_stem, new_stem = (os.path.splitext(os.path.basename(v))[0] for v in (old_video, new_video))
        moved = {}
        old_jpg = os.path.splitext(old_video)[0] + ".jpg"
        if os.path.exists(old_jpg):
            moved[old_jpg] = os.path.splitext(new_video)[0] + ".jpg"
        t = self.thumbs()
        # Only this video's listed options move, never another file that
        # happens to share the prefix.
        for o in t["options"].get(key, []):
            d, name = os.path.split(o["file"])
            if name.startswith(old_stem + "-") and os.path.exists(o["file"]):
                moved[o["file"]] = os.path.join(d, new_stem + name[len(old_stem):])
        for a, b in list(moved.items()):
            if os.path.exists(b):
                del moved[a]
            else:
                os.rename(a, b)
        for o in t["options"].get(key, []):
            o["file"] = moved.get(o["file"], o["file"])
        if key in t["picked"]:
            t["picked"][key] = moved.get(t["picked"][key], t["picked"][key])
        if key in t["picked_from"]:
            t["picked_from"][key] = moved.get(t["picked_from"][key], t["picked_from"][key])
        for r in t["requests"]:
            r["file"] = moved.get(r["file"], r["file"])
        write_json(self.thumbs_path, t)

    def render_status(self):
        with self.lock:
            return dict(self.status)

    def start_render(self, in_s, out_s):
        """Returns (http code, body)."""
        with self.lock:
            if self.status["state"] == "running":
                return 409, {"error": "a render is already running"}
            if os.path.exists(self.final_output()):
                return 409, {"error": f"{os.path.basename(self.final_output())} already exists"}
            self.stop_event.clear()
            self.status = {"state": "running", "phase": "measuring", "percent": 0,
                           "output": None, "error": None}
        threading.Thread(target=self._render, args=(in_s, out_s), daemon=True).start()
        return 202, {"ok": True}

    def _render(self, in_s, out_s):
        def progress(percent, phase):
            with self.lock:
                self.status.update(percent=round(percent, 1), phase=phase)

        try:
            out = render.render_final(self.raw, in_s, out_s, self.profile,
                                      progress=progress, stop=self.stop_event)
            a = self.analysis
            snapped = render.snap_range(in_s, out_s, a["fps"], a["duration"])
            write_json(self.edit_path, {"in": snapped[0], "out": snapped[1], "output": out})
            update = {"state": "done", "percent": 100, "output": out}
        except Exception as e:  # report anything to the page
            update = {"state": "error", "error": str(e)}
        with self.lock:
            self.status.update(update)


    # -- shorts --

    def edit(self):
        try:
            with open(self.edit_path) as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def candidates(self):
        """(candidate list or None, words path or None, error or None)."""
        path = os.path.join(self.shorts_dir, "candidates.json")
        # Shorts don't need the final: before it, judge "inside" against
        # prepare's default In/Out. The page flags, never hides, the rest.
        trim = self.edit() or {"in": self.analysis["in"], "out": self.analysis["out"]}
        # Shorts rendered from an earlier shortlist (in shorts.json, not in
        # candidates.json) still show, under Rendered, marked "earlier".
        try:
            with open(os.path.join(self.shorts_dir, "shorts.json")) as f:
                m = json.load(f)
        except (OSError, ValueError):
            m = {}
        done = m.get("clips", []) if isinstance(m, dict) else []
        done = [c for c in done if isinstance(c, dict) and all(k in c for k in ("file", "start", "end"))
                and shorts_view.number(c) is not None and os.path.exists(os.path.join(self.shorts_dir, c["file"]))]
        if not os.path.exists(path):
            if not done:
                return None, None, None
            return [{**shorts_view.describe(c, trim, self.shift), "earlier": True} for c in done], m.get("words"), None
        try:
            clips = shorts_view.load_candidates(path, trim, self.shift)
            with open(path) as f:
                words = json.load(f).get("words")
        except (OSError, ValueError) as e:
            return None, None, str(e)
        have = {c["n"] for c in clips}
        clips += [{**shorts_view.describe(c, trim, self.shift), "earlier": True}
                  for c in done if shorts_view.number(c) not in have]
        return clips, words, None

    def layouts(self):
        """({name: {"label": text or None, "pan": [lo, hi] or None, "x": default x or None}}, default name),
        from stream-shorts' layouts.json overlaid with the profile's layouts
        file and then shorts/layouts.json."""
        data, default = {}, None
        for path in (os.path.join(os.path.dirname(self.shorts_py), "layouts.json"),
                     self.profile.get("layouts_path"),
                     os.path.join(self.shorts_dir, "layouts.json")):
            if not path:
                continue
            try:
                with open(path) as f:
                    more = json.load(f)
            except (OSError, ValueError):
                continue
            data.update(more.get("layouts", {}))
            default = more.get("default", default)
        out = {}
        for name, layout in data.items():
            band = next((b for b in layout.get("bands", []) if "pan" in b), None)
            out[name] = {"label": layout.get("label"), "pan": band and band["pan"], "x": band and band["crop"][2]}
        return out, default

    def shorts_state(self):
        clips, _, error = self.candidates()
        with self.lock:
            render_state = json.loads(json.dumps(self.shorts_status))
        layouts, default = self.layouts()
        return {"profile": self.profile["name"], "edit": self.edit(), "shift": self.shift,
                "candidates": clips, "error": error, "finding": self.finding(), "titles": self.titles(), "thumbs": self.thumbs_public(),
                "rendered": self.rendered(), "dismissed": self.dismissed(),
                "layouts": layouts, "default_layout": default, "render": render_state}

    def build_clip(self, pick):
        """The shorts.json clip for one pick from the page, and the words path.
        Raises ValueError with a reason for the page."""
        clips, words, error = self.candidates()
        if clips is None:
            raise ValueError(error or "no candidates yet")
        if not words:
            raise ValueError("candidates.json has no \"words\"")
        if not isinstance(pick, dict):
            raise ValueError("a pick must be an object")
        cand = next((c for c in clips if c["n"] == pick.get("n")), None)
        if cand is None:
            raise ValueError(f"no candidate numbered {pick.get('n')}")
        if "file" in pick and pick["file"] != cand["file"]:
            raise ValueError("the shortlist changed since the page loaded it. Reload the page.")
        try:
            start, end = (shorts_view.to_secs(pick.get(k, cand[k])) for k in ("start", "end"))
        except (TypeError, ValueError):
            raise ValueError("start and end must be times")
        if not start < end:
            raise ValueError(f"clip {cand['n']}: start has to be before end")
        clip = {k: cand[k] for k in ("file", "hook", "layout") if k in cand}
        # The card's Code + me / Just me switch.
        if pick.get("layout") is not None:
            if pick["layout"] not in self.layouts()[0]:
                raise ValueError(f"no layout named {pick['layout']}")
            clip["layout"] = pick["layout"]
        clip.update(start=shorts_view.fmt(start), end=shorts_view.fmt(end))
        if pick.get("pan_x") is not None:
            clip["pan_x"] = pick["pan_x"]
        if pick.get("fixes"):
            if not isinstance(pick["fixes"], dict):
                raise ValueError("fixes must be {heard: meant}")
            clip["fixes"] = pick["fixes"]
        return clip, words

    def run_work(self, mode, pick):
        """Run shorts.py --preview, --draft or --captions on a one-clip manifest in
        the cache. Returns (clip, stdout). Raises ValueError on a failure."""
        clip, words = self.build_clip(pick)
        with self.work_lock:
            os.makedirs(self.work, exist_ok=True)
            layouts = os.path.join(self.shorts_dir, "layouts.json")
            local = os.path.join(self.work, "layouts.json")
            if os.path.exists(layouts):
                shutil.copyfile(layouts, local)
            elif os.path.exists(local):
                os.remove(local)
            manifest = os.path.join(self.work, "manifest.json")
            write_json(manifest, {"recording": self.raw, "words": words,
                                  **shorts_view.profile_fields(self.profile), "clips": [clip]})
            r = subprocess.run([sys.executable, self.shorts_py, mode, manifest,
                                str(shorts_view.number(clip))], env=self.shorts_env(),
                               capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            raise ValueError(error_line(r.stderr) or f"{mode} failed")
        return clip, r.stdout

    def shorts_env(self):
        """shorts.py's environment: short_audio.py reads the profile from it."""
        return {**os.environ, "STREAM_TRIM_PROFILE": self.profile["name"]}

    def preview_path(self, n, ext=".jpg"):
        """The still (.jpg) or draft (.draft.mp4) for candidate n in the cache."""
        clips, _, _ = self.candidates()
        cand = next((c for c in clips or [] if c["n"] == n), None)
        return cand and os.path.join(self.work, os.path.splitext(cand["file"])[0] + ext)

    def start_shorts(self, picks):
        """Returns (http code, body)."""
        if not isinstance(picks, list) or not picks:
            return 400, {"error": "pick at least one clip"}
        try:
            built = [self.build_clip(p) for p in picks]
        except ValueError as e:
            return 400, {"error": str(e)}
        manifest = os.path.join(self.shorts_dir, "shorts.json")
        existing = None
        if os.path.exists(manifest):
            try:
                with open(manifest) as f:
                    existing = json.load(f)
            except ValueError as e:
                return 400, {"error": f"shorts/shorts.json can't be read, so it isn't overwritten: {e}"}
        # shorts.py picks clips by number, so a kept clip with the same
        # number would be rendered (and overwritten) too.
        kept = existing.get("clips", []) if isinstance(existing, dict) else existing or []
        # A short renamed to its title keeps that name when it's re-rendered.
        files = self.titles()["files"]
        for clip, _ in built:
            renamed = files.get(str(shorts_view.number(clip)))
            if renamed and any(k.get("file") == renamed for k in kept):
                clip["file"] = renamed
        for clip, _ in built:
            clash = next((k.get("file") for k in kept if shorts_view.number(k) == shorts_view.number(clip)
                          and k.get("file") != clip["file"]), None)
            if clash:
                return 400, {"error": f"{clip['file']} has the same number as {clash} in shorts/shorts.json. "
                                      "Ask Claude to renumber the shortlist."}
        with self.lock:
            if self.shorts_status["state"] == "running":
                return 409, {"error": "shorts are already rendering"}
            clips = [c for c, _ in built]
            self.shorts_status = {"state": "running", "clips": {
                str(shorts_view.number(c)): {"state": "queued", "output": None, "error": None,
                                             "phase": None, "percent": None}
                for c in clips}}
        os.makedirs(self.shorts_dir, exist_ok=True)
        write_json(manifest, shorts_view.merge_picks(existing, self.raw, built[0][1], SHORT_AUDIO, clips,
                                                     self.profile))
        threading.Thread(target=self._render_shorts, args=(manifest, clips), daemon=True).start()
        return 202, {"ok": True}

    def _run_short(self, manifest, key, clip):
        """Run shorts.py for one clip. The audio step prints nothing; then
        ffmpeg's -stats lines ("time=HH:MM:SS.ss", ended by \\r) give the
        encoding percent. Returns (exit code, stdout, stderr)."""
        dur = shorts_view.to_secs(clip["end"]) - shorts_view.to_secs(clip["start"]) + 0.6
        p = subprocess.Popen([sys.executable, self.shorts_py, manifest, key], env=self.shorts_env(),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err, buf = [], b""
        while True:
            chunk = p.stderr.read1(4096)
            if not chunk:
                break
            err.append(chunk)
            buf = (buf + chunk)[-4096:]
            times = re.findall(rb"time=(\d+):(\d+):(\d+(?:\.\d+)?)", buf)
            if times:
                h, m, s = times[-1]
                t = int(h) * 3600 + int(m) * 60 + float(s)
                with self.lock:
                    self.shorts_status["clips"][key].update(
                        phase="encoding", percent=round(min(99.9, max(0.0, t / dur * 100)), 1))
        stdout = p.stdout.read().decode(errors="replace")
        p.wait()
        stderr = b"".join(err).decode(errors="replace").replace("\r", "\n")
        return p.returncode, stdout, stderr

    def _render_shorts(self, manifest, clips):
        failed = False
        for clip in clips:
            key = str(shorts_view.number(clip))
            with self.lock:
                self.shorts_status["clips"][key].update(state="rendering", phase="audio", percent=None)
            try:
                code, stdout, stderr = self._run_short(manifest, key, clip)
                out = next((l[len("SHORT: "):] for l in stdout.splitlines() if l.startswith("SHORT: ")), None)
                update = ({"state": "done", "output": out} if code == 0 and out else
                          {"state": "error", "error": error_line(stderr) or "render failed"})
            except Exception as e:  # report anything to the page
                update = {"state": "error", "error": str(e)}
            failed = failed or update["state"] == "error"
            with self.lock:
                self.shorts_status["clips"][key].update(update)
        with self.lock:
            self.shorts_status["state"] = "error" if failed else "done"


def write_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)


def error_line(stderr):
    """The line that says what went wrong. shorts.py ends with its own
    "ERROR: failed: <file>" summary after the real error, so skip that."""
    lines = [l for l in stderr.strip().splitlines() if l.strip()]
    errors = [l for l in lines if l.startswith("ERROR:")]
    real = [l for l in errors if not l.startswith("ERROR: failed:")]
    return (real or errors or lines or [""])[-1]


class Handler(BaseHTTPRequestHandler):
    server: TrimServer

    def log_message(self, *args):
        pass

    def send_json(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        s = self.server
        path = self.path.split("?", 1)[0]
        m = re.fullmatch(r"/shorts/preview/(\d+)\.jpg", path)
        d = re.fullmatch(r"/shorts/draft/(\d+)\.mp4", path)
        rf = re.fullmatch(r"/shorts/file/(\d+)\.mp4", path)
        if path == "/thumb":
            from urllib.parse import parse_qs, urlsplit
            want = parse_qs(urlsplit(self.path).query).get("path", [None])[0]
            if s.thumb_known(want):
                self.send_file(want, "image/jpeg")
            else:
                self.send_json(404, {"error": "no such thumbnail"})
        elif rf:
            r = s.rendered().get(str(int(rf.group(1))))
            if r and r["exists"]:
                self.send_ranged(os.path.join(s.shorts_dir, r["file"]))
            else:
                self.send_json(404, {"error": "no such rendered short"})
        elif d:
            mp4 = s.preview_path(int(d.group(1)), ".draft.mp4")
            if mp4 and os.path.exists(mp4):
                self.send_ranged(mp4)
            else:
                self.send_json(404, {"error": "no such draft"})
        elif m:
            jpg = s.preview_path(int(m.group(1)))
            if jpg:
                self.send_file(jpg, "image/jpeg")
            else:
                self.send_json(404, {"error": "no such preview"})
        elif self.path == "/":
            self.send_file(os.path.join(HERE, "page.html"), "text/html; charset=utf-8")
        elif self.path == "/proxy.mp4":
            self.send_ranged(os.path.join(s.cache, "proxy.mp4"))
        elif self.path == "/api/state":
            out = s.final_output()
            self.send_json(200, {**s.analysis, "peaks": s.peaks["peaks"], "per_s": s.peaks["per_s"],
                                 "name": os.path.basename(s.raw), "profile": s.profile["name"],
                                 "render": s.render_status(),
                                 "output": out, "exists": os.path.exists(out), "edit": s.edit()})
        elif self.path == "/api/shorts":
            self.send_json(200, s.shorts_state())
        elif self.path == "/api/render":
            self.send_json(200, s.render_status())
        elif self.path == "/api/streams":
            self.send_json(200, s.streams())
        elif self.path == "/api/titles":
            self.send_json(200, s.titles())
        elif self.path == "/api/thumbs":
            self.send_json(200, s.thumbs_public())
        elif self.path == "/api/attention":
            with s.lock:
                self.send_json(200, dict(s.attention))
        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        s = self.server
        length = int(self.headers.get("Content-Length") or 0)
        raw_body = self.rfile.read(length) if length else b""
        if self.path == "/api/render":
            try:
                body = json.loads(raw_body)
                in_s, out_s = body["in"], body["out"]
                if not all(isinstance(x, (int, float)) and not isinstance(x, bool)
                           and math.isfinite(x) for x in (in_s, out_s)):
                    raise ValueError("in and out must be numbers")
                if not 0 <= in_s < out_s <= s.analysis["duration"]:
                    raise ValueError(f"need 0 <= in < out <= {s.analysis['duration']:.2f}")
            except (ValueError, KeyError, TypeError) as e:
                self.send_json(400, {"error": str(e) or "bad request"})
                return
            self.send_json(*s.start_render(float(in_s), float(out_s)))
        elif self.path in ("/api/shorts/preview", "/api/shorts/draft", "/api/shorts/captions",
                           "/api/shorts/render"):
            try:
                body = json.loads(raw_body)
                if not isinstance(body, dict):
                    raise ValueError("expected a JSON object")
            except ValueError as e:
                self.send_json(400, {"error": str(e) or "bad request"})
                return
            if self.path == "/api/shorts/render":
                self.send_json(*s.start_shorts(body.get("picks")))
                return
            mode = "--" + self.path.rsplit("/", 1)[1]
            try:
                clip, stdout = s.run_work(mode, body)
            except ValueError as e:
                self.send_json(400, {"error": str(e)})
                return
            if mode == "--captions":
                text = "\n".join(l for l in stdout.splitlines() if not l.startswith("== "))
                self.send_json(200, {"text": text})
            elif mode == "--draft":
                n = shorts_view.number(clip)
                mtime = os.path.getmtime(s.preview_path(n, ".draft.mp4"))
                self.send_json(200, {"url": f"/shorts/draft/{n}.mp4?v={mtime}"})
            else:
                n = shorts_view.number(clip)
                mtime = os.path.getmtime(s.preview_path(n))
                self.send_json(200, {"url": f"/shorts/preview/{n}.jpg?v={mtime}"})
        elif self.path == "/api/shorts/dismiss":
            try:
                body = json.loads(raw_body)
            except ValueError:
                self.send_json(400, {"error": "bad request"})
                return
            self.send_json(*s.dismiss(body))
        elif self.path == "/api/attention":
            try:
                body = json.loads(raw_body)
            except ValueError:
                self.send_json(400, {"error": "bad request"})
                return
            self.send_json(*s.set_attention(body))
        elif self.path in ("/api/titles", "/api/title"):
            try:
                body = json.loads(raw_body)
            except ValueError:
                self.send_json(400, {"error": "bad request"})
                return
            self.send_json(*(s.post_titles(body) if self.path == "/api/titles" else s.pick_title(body)))
        elif self.path in ("/api/thumbs", "/api/thumb", "/api/thumbs/done"):
            try:
                body = json.loads(raw_body)
            except ValueError:
                self.send_json(400, {"error": "bad request"})
                return
            fn = {"/api/thumbs": s.post_thumbs, "/api/thumb": s.thumb_action, "/api/thumbs/done": s.thumbs_done}
            self.send_json(*fn[self.path](body))
        elif self.path == "/api/reveal":
            try:
                body = json.loads(raw_body)
            except ValueError:
                self.send_json(400, {"error": "bad request"})
                return
            self.send_json(*s.reveal(body))
        elif self.path == "/api/stop":
            if s.render_status()["state"] != "running":
                self.send_json(409, {"error": "no render is running"})
            else:
                s.stop_event.set()
                self.send_json(200, {"ok": True})
        else:
            self.send_json(404, {"error": "not found"})

    def send_file(self, path, ctype):
        if not os.path.exists(path):
            self.send_json(404, {"error": f"{os.path.basename(path)} missing"})
            return
        with open(path, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_ranged(self, path):
        size = os.path.getsize(path)
        start, end, code = 0, size - 1, 200
        m = re.fullmatch(r"bytes=(\d+)-(\d*)", self.headers.get("Range", ""))
        if m:
            start = int(m.group(1))
            end = min(int(m.group(2)), size - 1) if m.group(2) else size - 1
            if start > end:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return
            code = 206
        self.send_response(code)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        if code == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        try:
            with open(path, "rb") as f:
                f.seek(start)
                left = end - start + 1
                while left > 0:
                    chunk = f.read(min(CHUNK, left))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    left -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass  # the browser cancels range requests while seeking


def make_server(raw, profile, port=0, shorts_py=SHORTS_PY):
    return TrimServer(raw, profile, port, shorts_py)


if __name__ == "__main__":
    args = sys.argv[1:]
    name = None
    if "--profile" in args:
        i = args.index("--profile")
        name = args[i + 1] if i + 1 < len(args) else ""
        del args[i:i + 2]
    if len(args) != 1 or name == "":
        sys.exit("usage: server.py <raw.mp4> [--profile NAME]")
    try:
        profile = profiles.load(name)
        profiles.check_recording(profile, audio_chain.probe(args[0], video=False)[0])
    except (profiles.ProfileError, OSError, subprocess.CalledProcessError) as e:
        sys.exit(f"ERROR: {e}")
    try:
        srv = make_server(args[0], profile)
    except profiles.ProfileError as e:
        sys.exit(f"ERROR: {e}")
    except FileNotFoundError as e:
        if "stream-shorts" in str(e):
            sys.exit(f"ERROR: {e}")
        sys.exit("ERROR: no prepared cache for this recording, run prepare.py first")
    print(f"READY http://127.0.0.1:{srv.server_address[1]}/", flush=True)
    # So Claude Code hooks (attention.py) can find this page.
    attention.register(srv.server_address[1], os.getpid(), os.path.realpath(args[0]),
                       session=os.environ.get("CLAUDE_CODE_SESSION_ID"))
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))  # stopping the task still unregisters
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        attention.unregister(srv.server_address[1])
