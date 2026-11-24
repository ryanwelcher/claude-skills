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
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import audio_chain
import prepare
import profiles
import render
import shorts_view

HERE = os.path.dirname(os.path.abspath(__file__))
CHUNK = 1 << 20
SHORTS_PY = os.path.normpath(os.path.join(HERE, "..", "..", "stream-shorts", "scripts", "shorts.py"))
SHORT_AUDIO = os.path.join(HERE, "short_audio.py")


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
        with open(os.path.join(self.cache, "peaks.json")) as f:
            self.peaks = json.load(f)
        self.work = os.path.join(self.cache, "shorts-work")
        self.edit_path = os.path.join(self.cache, "edit.json")
        # Transcript clock -> video clock (the shortlist's times are transcript times).
        self.shift = profiles.transcript_shift(profile, self.analysis["fps"])
        self.lock = threading.Lock()
        self.work_lock = threading.Lock()  # one preview/captions run at a time
        self.shorts_status = {"state": "idle", "clips": {}}
        self.stop_event = threading.Event()
        self.status = {"state": "idle", "phase": None, "percent": 0, "output": None, "error": None}
        super().__init__(("127.0.0.1", port), Handler)

    def render_status(self):
        with self.lock:
            return dict(self.status)

    def start_render(self, in_s, out_s):
        """Returns (http code, body)."""
        with self.lock:
            if self.status["state"] == "running":
                return 409, {"error": "a render is already running"}
            if os.path.exists(render.final_path(self.raw)):
                return 409, {"error": f"{os.path.basename(render.final_path(self.raw))} already exists"}
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
        edit = self.edit()
        if edit is None or not os.path.exists(path):
            return None, None, None
        try:
            clips = shorts_view.load_candidates(path, edit, self.shift)
            with open(path) as f:
                words = json.load(f).get("words")
        except (OSError, ValueError) as e:
            return None, None, str(e)
        return clips, words, None

    def layouts(self):
        """({name: {"pan": [lo, hi], "x": default x} or None}, default name),
        from stream-shorts' layouts.json overlaid with shorts/layouts.json."""
        data, default = {}, None
        for path in (os.path.join(os.path.dirname(self.shorts_py), "layouts.json"),
                     os.path.join(self.shorts_dir, "layouts.json")):
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
            out[name] = band and {"pan": band["pan"], "x": band["crop"][2]}
        return out, default

    def shorts_state(self):
        clips, _, error = self.candidates()
        with self.lock:
            render_state = json.loads(json.dumps(self.shorts_status))
        layouts, default = self.layouts()
        return {"edit": self.edit(), "shift": self.shift, "candidates": clips, "error": error,
                "layouts": layouts, "default_layout": default, "render": render_state}

    def build_clip(self, pick, require_inside):
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
        clip.update(start=shorts_view.fmt(start), end=shorts_view.fmt(end))
        if pick.get("pan_x") is not None:
            clip["pan_x"] = pick["pan_x"]
        if pick.get("fixes"):
            if not isinstance(pick["fixes"], dict):
                raise ValueError("fixes must be {heard: meant}")
            clip["fixes"] = pick["fixes"]
        if require_inside and not shorts_view.inside(clip, self.edit(), self.shift):
            raise ValueError(f"clip {cand['n']} runs outside the edit")
        return clip, words

    def run_work(self, mode, pick):
        """Run shorts.py --preview, --draft or --captions on a one-clip manifest in
        the cache. Returns (clip, stdout). Raises ValueError on a failure."""
        clip, words = self.build_clip(pick, require_inside=False)
        with self.work_lock:
            os.makedirs(self.work, exist_ok=True)
            layouts = os.path.join(self.shorts_dir, "layouts.json")
            local = os.path.join(self.work, "layouts.json")
            if os.path.exists(layouts):
                shutil.copyfile(layouts, local)
            elif os.path.exists(local):
                os.remove(local)
            manifest = os.path.join(self.work, "manifest.json")
            write_json(manifest, {"recording": self.raw, "words": words, "clips": [clip]})
            r = subprocess.run([sys.executable, self.shorts_py, mode, manifest,
                                str(shorts_view.number(clip))],
                               capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            raise ValueError(error_line(r.stderr) or f"{mode} failed")
        return clip, r.stdout

    def preview_path(self, n, ext=".jpg"):
        """The still (.jpg) or draft (.draft.mp4) for candidate n in the cache."""
        clips, _, _ = self.candidates()
        cand = next((c for c in clips or [] if c["n"] == n), None)
        return cand and os.path.join(self.work, os.path.splitext(cand["file"])[0] + ext)

    def start_shorts(self, picks):
        """Returns (http code, body)."""
        if self.edit() is None:
            return 409, {"error": "render the final edit first"}
        if not isinstance(picks, list) or not picks:
            return 400, {"error": "pick at least one clip"}
        try:
            built = [self.build_clip(p, require_inside=True) for p in picks]
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
        for clip, _ in built:
            clash = next((k.get("file") for k in kept if shorts_view.number(k) == shorts_view.number(clip)
                          and k.get("file") != clip["file"]), None)
            if clash:
                return 400, {"error": f"{clip['file']} has the same number as {clash} in shorts/shorts.json. "
                                      "Ask Claude to renumber the shortlist."}
        with self.lock:
            if self.status["state"] == "running":
                return 409, {"error": "the final render is still running"}
            if self.shorts_status["state"] == "running":
                return 409, {"error": "shorts are already rendering"}
            clips = [c for c, _ in built]
            self.shorts_status = {"state": "running", "clips": {
                str(shorts_view.number(c)): {"state": "queued", "output": None, "error": None,
                                             "phase": None, "percent": None}
                for c in clips}}
        os.makedirs(self.shorts_dir, exist_ok=True)
        write_json(manifest, shorts_view.merge_picks(existing, self.raw, built[0][1], SHORT_AUDIO, clips))
        threading.Thread(target=self._render_shorts, args=(manifest, clips), daemon=True).start()
        return 202, {"ok": True}

    def _run_short(self, manifest, key, clip):
        """Run shorts.py for one clip. The audio step prints nothing; then
        ffmpeg's -stats lines ("time=HH:MM:SS.ss", ended by \\r) give the
        encoding percent. Returns (exit code, stdout, stderr)."""
        dur = shorts_view.to_secs(clip["end"]) - shorts_view.to_secs(clip["start"]) + 0.6
        p = subprocess.Popen([sys.executable, self.shorts_py, manifest, key],
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
        if d:
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
            out = render.final_path(s.raw)
            self.send_json(200, {**s.analysis, "peaks": s.peaks["peaks"], "per_s": s.peaks["per_s"],
                                 "name": os.path.basename(s.raw), "render": s.render_status(),
                                 "output": out, "exists": os.path.exists(out), "edit": s.edit()})
        elif self.path == "/api/shorts":
            self.send_json(200, s.shorts_state())
        elif self.path == "/api/render":
            self.send_json(200, s.render_status())
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
    except profiles.ProfileError as e:
        sys.exit(f"ERROR: {e}")
    try:
        srv = make_server(args[0], profile)
    except FileNotFoundError as e:
        if "stream-shorts" in str(e):
            sys.exit(f"ERROR: {e}")
        sys.exit("ERROR: no prepared cache for this recording, run prepare.py first")
    print(f"READY http://127.0.0.1:{srv.server_address[1]}/", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
