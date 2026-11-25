import json
import shutil
import os
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from unittest import mock

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import prepare  # noqa: E402
import profiles  # noqa: E402
import server  # noqa: E402
from test_measure import make_mp4  # noqa: E402


STUB = """import json, os, sys, time
args = sys.argv[1:]
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps(args) + "\\n")
if os.environ.get("STUB_PROFILE_LOG"):
    with open(os.environ["STUB_PROFILE_LOG"], "a") as f:
        f.write(os.environ.get("STREAM_TRIM_PROFILE", "-") + "\\n")
mode = args.pop(0) if args[0].startswith("--") else None
manifest, n = args
m = json.load(open(manifest))
clip = next(c for c in m["clips"] if int(c["file"].split("-")[0]) == int(n))
out = os.path.join(os.path.dirname(manifest), clip["file"])
if mode == "--preview":
    open(os.path.splitext(out)[0] + ".jpg", "wb").write(b"JPG")
    print("PREVIEW: x")
elif mode == "--draft":
    open(os.path.splitext(out)[0] + ".draft.mp4", "wb").write(b"DRAFTMP4")
    print("SHORT: x")
elif mode == "--captions":
    print("== " + clip["file"])
    print("HELLO WORLD")
elif clip.get("hook") == "fail":
    print("ERROR: render broke", file=sys.stderr)
    print("ERROR: failed: " + clip["file"], file=sys.stderr)
    sys.exit(1)
else:
    if os.environ.get("STUB_PROGRESS"):
        time.sleep(float(os.environ["STUB_PROGRESS"]))
        sys.stderr.write("frame=  10 fps=0.0 q=-0.0 size=       0KiB time=00:00:05.30 bitrate=N/A speed=0x\\r")
        sys.stderr.flush()
    time.sleep(float(os.environ.get("STUB_SLEEP", "0")))
    open(out, "wb").write(b"MP4")
    print("SHORT: " + out)
"""

ANALYSIS = {"raw": "x", "duration": 100.0, "fps": 23.976, "silences": [[0, 70]],
            "voice_start": 70, "voice_end": 90, "in": 69.5, "out": 91.0}


class ServerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raw = os.path.join(self.tmp.name, "raw, stream.mp4")
        open(self.raw, "wb").close()
        self.cache = os.path.join(self.tmp.name, "cache")
        os.makedirs(self.cache)
        self.proxy_bytes = bytes(range(256)) * 8
        with open(os.path.join(self.cache, "proxy.mp4"), "wb") as f:
            f.write(self.proxy_bytes)
        with open(os.path.join(self.cache, "analysis.json"), "w") as f:
            json.dump(ANALYSIS, f)
        with open(os.path.join(self.cache, "peaks.json"), "w") as f:
            json.dump({"per_s": 20, "peaks": [0.0, 0.5, 1.0]}, f)
        patcher = mock.patch.object(prepare, "cache_dir", return_value=self.cache)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.stub = os.path.join(self.tmp.name, "stub_shorts.py")
        with open(self.stub, "w") as f:
            f.write(STUB)
        self.log = os.path.join(self.tmp.name, "stub.log")
        env = mock.patch.dict(os.environ, {"STUB_LOG": self.log})
        env.start()
        self.addCleanup(env.stop)
        self.shorts = os.path.join(self.tmp.name, "shorts")
        self.srv = server.make_server(self.raw, profiles.load("ryan-obs"), port=0, shorts_py=self.stub)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.srv.server_address[1]}"

    def tearDown(self):
        self.srv.shutdown()
        self.srv.server_close()
        self.tmp.cleanup()

    def get(self, path, headers=None):
        req = urllib.request.Request(self.base + path, headers=headers or {})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, dict(r.headers), r.read()
        except urllib.error.HTTPError as e:
            with e:
                return e.code, dict(e.headers), e.read()

    def post(self, path, body=None):
        data = json.dumps(body).encode() if body is not None else b""
        req = urllib.request.Request(self.base + path, data=data, method="POST",
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            with e:
                return e.code, json.loads(e.read() or b"{}")

    def state(self):
        return json.loads(self.get("/api/state")[2])

    def wait_for(self, want):
        for _ in range(100):
            s = json.loads(self.get("/api/render")[2])
            if s["state"] == want:
                return s
            time.sleep(0.02)
        self.fail(f"render never reached {want}: {s}")

    def test_state(self):
        s = self.state()
        self.assertEqual((s["in"], s["out"]), (69.5, 91.0))
        self.assertEqual(s["peaks"], [0.0, 0.5, 1.0])
        self.assertEqual(s["per_s"], 20)
        self.assertEqual(s["render"]["state"], "idle")
        self.assertTrue(s["output"].endswith(os.path.join("renders", "raw, stream-final.mp4")))
        self.assertFalse(s["exists"])

    def test_proxy_range(self):
        size = len(self.proxy_bytes)
        code, h, body = self.get("/proxy.mp4", {"Range": "bytes=10-19"})
        self.assertEqual(code, 206)
        self.assertEqual(h["Content-Range"], f"bytes 10-19/{size}")
        self.assertEqual(body, self.proxy_bytes[10:20])
        code, h, body = self.get("/proxy.mp4", {"Range": "bytes=10-"})
        self.assertEqual((code, body), (206, self.proxy_bytes[10:]))
        code, h, body = self.get("/proxy.mp4")
        self.assertEqual((code, len(body)), (200, size))
        self.assertEqual(h["Accept-Ranges"], "bytes")

    def test_render_validation(self):
        with mock.patch.object(server.render, "render_final") as rf:
            for body in ({"in": 5, "out": 2}, {"in": "a", "out": 2}, {"in": -1, "out": 2},
                         {"in": 0, "out": 1e9}, None):
                code, resp = self.post("/api/render", body)
                self.assertEqual(code, 400, body)
                self.assertIn("error", resp)
            rf.assert_not_called()
        self.assertEqual(self.state()["render"]["state"], "idle")

    def test_render_conflict(self):
        release = threading.Event()

        def fake(raw, a, b, chain, progress=None, stop=None):
            release.wait(5)
            return "/out/final.mp4"

        with mock.patch.object(server.render, "render_final", side_effect=fake):
            self.assertEqual(self.post("/api/render", {"in": 1, "out": 50})[0], 202)
            self.assertEqual(self.post("/api/render", {"in": 1, "out": 50})[0], 409)
            release.set()
            s = self.wait_for("done")
        self.assertEqual(s["output"], "/out/final.mp4")

    def test_render_error_reported(self):
        with mock.patch.object(server.render, "render_final", side_effect=RuntimeError("boom")):
            self.assertEqual(self.post("/api/render", {"in": 1, "out": 50})[0], 202)
            s = self.wait_for("error")
        self.assertEqual(s["error"], "boom")

    def test_stop(self):
        self.assertEqual(self.post("/api/stop")[0], 409)

        def fake(raw, a, b, chain, progress=None, stop=None):
            stop.wait(5)
            raise RuntimeError("stopped")

        with mock.patch.object(server.render, "render_final", side_effect=fake):
            self.post("/api/render", {"in": 1, "out": 50})
            self.assertEqual(self.post("/api/stop")[0], 200)
            self.assertEqual(self.wait_for("error")["error"], "stopped")

    def test_existing_output_conflict(self):
        os.makedirs(os.path.join(self.tmp.name, "renders"))
        open(os.path.join(self.tmp.name, "renders", "raw, stream-final.mp4"), "wb").close()
        self.assertTrue(self.state()["exists"])
        self.assertEqual(self.post("/api/render", {"in": 1, "out": 50})[0], 409)

    def test_binds_localhost(self):
        self.assertEqual(self.srv.server_address[0], "127.0.0.1")

    # -- shorts --

    SHIFT = round(9 / 23.976, 6)

    def write_edit(self, edit=None):
        with open(os.path.join(self.cache, "edit.json"), "w") as f:
            json.dump(edit or {"in": 10.0, "out": 90.0, "output": "/x-final.mp4"}, f)

    def write_candidates(self, text=None):
        os.makedirs(self.shorts, exist_ok=True)
        self.cand_path = os.path.join(self.shorts, "candidates.json")
        with open(self.cand_path, "w") as f:
            f.write(text if text is not None else json.dumps({
                "recording": self.raw, "words": "/w.json",
                "clips": [{"file": "01-one.mp4", "start": 20, "end": 30, "hook": "one", "layout": "center"},
                          {"file": "02-two.mp4", "start": 40, "end": 50, "hook": "two"},
                          {"file": "03-out.mp4", "start": 5, "end": 15, "hook": "out"}]}))

    def shorts_state(self):
        return json.loads(self.get("/api/shorts")[2])

    def wait_shorts(self, want):
        for _ in range(200):
            s = self.shorts_state()["render"]
            if s["state"] == want:
                return s
            time.sleep(0.02)
        self.fail(f"shorts render never reached {want}: {s}")

    def stub_calls(self):
        if not os.path.exists(self.log):
            return []
        with open(self.log) as f:
            return [json.loads(line) for line in f]

    def test_render_writes_edit(self):
        with mock.patch.object(server.render, "render_final", return_value="/out/final.mp4"):
            self.post("/api/render", {"in": 10.01, "out": 50.02})
            self.wait_for("done")
        with open(os.path.join(self.cache, "edit.json")) as f:
            edit = json.load(f)
        self.assertAlmostEqual(edit["in"] * 23.976, round(edit["in"] * 23.976), places=6)
        self.assertLessEqual(abs(edit["in"] - 10.01), 0.5 / 23.976)
        self.assertEqual(edit["output"], "/out/final.mp4")
        self.assertEqual(self.state()["edit"]["in"], edit["in"])

    def test_edit_survives_restart(self):
        self.assertIsNone(self.state()["edit"])
        self.write_edit()
        srv = server.make_server(self.raw, profiles.load("ryan-obs"), port=0, shorts_py=self.stub)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        self.addCleanup(srv.server_close)
        self.addCleanup(srv.shutdown)
        base = f"http://127.0.0.1:{srv.server_address[1]}"
        with urllib.request.urlopen(base + "/api/state") as r:
            self.assertEqual(json.loads(r.read())["edit"]["in"], 10.0)
        with urllib.request.urlopen(base + "/api/shorts") as r:
            self.assertEqual(json.loads(r.read())["edit"]["out"], 90.0)

    def test_shorts_no_candidates(self):
        self.write_edit()
        s = self.shorts_state()
        self.assertIsNone(s["candidates"])
        self.assertIsNone(s["error"])
        self.assertEqual(s["render"]["state"], "idle")
        self.assertAlmostEqual(s["shift"], self.SHIFT)

    def test_shorts_bad_candidates(self):
        self.write_edit()
        self.write_candidates('{"clips": [')
        code, _, body = self.get("/api/shorts")
        s = json.loads(body)
        self.assertEqual(code, 200)
        self.assertIsNone(s["candidates"])
        self.assertTrue(s["error"])

    def test_shorts_candidates_listed(self):
        self.write_edit()
        self.write_candidates()
        c = self.shorts_state()["candidates"]
        self.assertEqual([x["n"] for x in c], [1, 2, 3])
        self.assertEqual([x["inside"] for x in c], [True, True, False])
        self.assertAlmostEqual(c[0]["edit_start"], 20 - self.SHIFT - 10)
        with open(os.path.join(self.shorts, "layouts.json"), "w") as f:
            json.dump({"default": "wide", "layouts": {
                "wide": {"bands": [{"name": "a", "crop": [10, 10, 300, 0], "height": 1920, "pan": [0, 900]}]},
                "fixed": {"bands": [{"name": "a", "crop": [10, 10, 0, 0], "height": 1920}]}}}, f)
        s = self.shorts_state()
        self.assertEqual(s["layouts"]["wide"], {"label": None, "pan": [0, 900], "x": 300})
        self.assertEqual(s["layouts"]["fixed"], {"label": None, "pan": None, "x": None})
        # Ryan's built-in layouts carry the names the card's switch shows.
        self.builtin_layouts()
        s = self.shorts_state()
        self.assertEqual(s["layouts"]["me"]["label"], "Just me")
        self.assertEqual(s["layouts"]["coding-rebrand"]["label"], "Code + me")
        self.assertEqual(s["default_layout"], "wide")

    def test_shorts_preview_and_captions(self):
        self.write_edit()
        self.write_candidates()
        code, body = self.post("/api/shorts/preview", {"n": 1, "start": 20, "end": 30, "pan_x": 100})
        self.assertEqual(code, 200, body)
        status, headers, data = self.get(body["url"])
        self.assertEqual((status, data), (200, b"JPG"))
        self.assertEqual(headers["Content-Type"], "image/jpeg")
        call = self.stub_calls()[-1]
        self.assertEqual(call[0], "--preview")
        self.assertTrue(os.path.realpath(call[1]).startswith(os.path.realpath(self.cache)))
        with open(call[1]) as f:
            m = json.load(f)
        self.assertEqual(m["clips"][0]["pan_x"], 100)
        self.assertEqual(m["clips"][0]["layout"], "center")
        self.assertFalse(os.path.exists(os.path.join(self.shorts, "01-one.jpg")))
        code, body = self.post("/api/shorts/captions", {"n": 1, "start": 20, "end": 30, "fixes": {"a": "b"}})
        self.assertEqual(code, 200, body)
        self.assertEqual(body["text"].strip(), "HELLO WORLD")
        with open(self.stub_calls()[-1][1]) as f:
            self.assertEqual(json.load(f)["clips"][0]["fixes"], {"a": "b"})

    def test_shorts_draft(self):
        self.write_edit()
        self.write_candidates()
        self.assertEqual(self.get("/shorts/draft/1.mp4")[0], 404)
        code, body = self.post("/api/shorts/draft", {"n": 1, "start": 20, "end": 30, "fixes": {"a": "b"}})
        self.assertEqual(code, 200, body)
        self.assertRegex(body["url"], r"^/shorts/draft/1\.mp4\?v=")
        call = self.stub_calls()[-1]
        self.assertEqual(call[0], "--draft")
        self.assertTrue(os.path.realpath(call[1]).startswith(os.path.realpath(self.cache)))
        status, headers, data = self.get(body["url"], {"Range": "bytes=0-4"})
        self.assertEqual((status, data), (206, b"DRAFT"))
        self.assertEqual(headers["Content-Type"], "video/mp4")
        self.assertFalse(os.path.exists(os.path.join(self.shorts, "01-one.draft.mp4")))
        code, body = self.post("/api/shorts/draft", {"n": 9, "start": 20, "end": 30})
        self.assertEqual(code, 400)

    def test_state_has_profile(self):
        self.assertEqual(self.state()["profile"], "ryan-obs")
        self.write_edit()
        self.assertEqual(self.shorts_state()["profile"], "ryan-obs")

    def test_shorts_json_has_profile_fields(self):
        self.write_edit()
        self.write_candidates()
        self.post("/api/shorts/render", {"picks": [{"n": 1, "start": 20, "end": 30}]})
        self.wait_shorts("done")
        with open(os.path.join(self.shorts, "shorts.json")) as f:
            m = json.load(f)
        self.assertEqual((m["mic_track"], m["mic_lag_frames"], m["transcript_lag_frames"]), (2, 9, 9))
        self.assertEqual(m["profile"], "ryan-obs")
        self.assertEqual(m["caption_font"], {"name": "Jost SemiBold", "file": "Jost-SemiBold.ttf"})
        self.assertNotIn("layouts", m)

    def test_work_manifest_has_profile_fields(self):
        self.write_edit()
        self.write_candidates()
        self.post("/api/shorts/preview", {"n": 1, "start": 20, "end": 30})
        with open(self.stub_calls()[-1][1]) as f:
            m = json.load(f)
        self.assertEqual(m["mic_track"], 2)
        self.assertEqual(m["caption_font"]["name"], "Jost SemiBold")

    def test_shorts_env_profile(self):
        log = os.path.join(self.tmp.name, "profile.log")
        self.write_edit()
        self.write_candidates()
        with mock.patch.dict(os.environ, {"STUB_PROFILE_LOG": log}):
            self.post("/api/shorts/preview", {"n": 1, "start": 20, "end": 30})
            self.post("/api/shorts/render", {"picks": [{"n": 1, "start": 20, "end": 30}]})
            self.wait_shorts("done")
        with open(log) as f:
            self.assertEqual(set(f.read().split()), {"ryan-obs"})

    def test_profile_layouts_overlay(self):
        config = os.path.join(self.tmp.name, "config", "profiles")
        os.makedirs(config)
        band = {"bands": [{"name": "a", "crop": [10, 10, 300, 0], "height": 1920, "pan": [0, 900]}]}
        with open(os.path.join(config, "mate-layouts.json"), "w") as f:
            json.dump({"default": "cam", "layouts": {"cam": band}}, f)
        with open(profiles.find("ryan-obs")) as f:
            mate = json.load(f)
        mate.update(name="mate", layouts="mate-layouts.json", chain=os.path.abspath(
            os.path.join(HERE, "..", "scripts", "chain.json")))
        with open(os.path.join(config, "mate.json"), "w") as f:
            json.dump(mate, f)
        with mock.patch.dict(os.environ, {"STREAM_TRIM_CONFIG": os.path.dirname(config)}):
            p = profiles.load("mate")
        with open(os.path.join(self.cache, "analysis.json"), "w") as f:
            json.dump({**ANALYSIS, "profile": "mate", "profile_key": profiles.cache_key(p)}, f)
        srv = server.make_server(self.raw, p, port=0, shorts_py=self.stub)
        self.addCleanup(srv.server_close)
        layouts, default = srv.layouts()
        self.assertEqual((layouts["cam"]["x"], default), (300, "cam"))
        os.makedirs(self.shorts, exist_ok=True)
        band2 = {"bands": [{"name": "a", "crop": [10, 10, 500, 0], "height": 1920, "pan": [0, 900]}]}
        with open(os.path.join(self.shorts, "layouts.json"), "w") as f:
            json.dump({"layouts": {"cam": band2}}, f)
        self.assertEqual(srv.layouts()[0]["cam"]["x"], 500)

    def test_streams_list(self):
        s = json.loads(self.get("/api/streams")[2])
        self.assertEqual(s["current"], "cache")
        self.assertIn("cache", [x["id"] for x in s["streams"]])

    def test_reveal(self):
        calls = []
        self.srv.open_cmd = calls.append
        # The current stream's raw (the cache's analysis names "x", which doesn't exist).
        with open(os.path.join(self.cache, "analysis.json"), "w") as f:
            json.dump({**ANALYSIS, "raw": self.raw}, f)
        self.assertEqual(self.post("/api/reveal", {"target": "raw"})[0], 200)
        self.assertEqual(calls, [["open", "-R", self.raw]])
        self.assertEqual(self.post("/api/reveal", {"stream": "cache", "target": "final"})[0], 404)
        self.assertEqual(self.post("/api/reveal", {"stream": "nope", "target": "raw"})[0], 404)
        self.assertEqual(self.post("/api/reveal", {"target": "/etc/passwd"})[0], 400)
        self.assertEqual(self.post("/api/reveal", ["raw"])[0], 400)
        self.assertEqual(len(calls), 1)

    def test_cache_from_other_profile(self):
        p = profiles.load("ryan-obs")
        for over in ({"profile": "laptop"}, {"profile": "ryan-obs", "profile_key": "0" * 16}):
            with open(os.path.join(self.cache, "analysis.json"), "w") as f:
                json.dump({**ANALYSIS, **over}, f)
            with self.assertRaises(profiles.ProfileError) as cm:
                server.make_server(self.raw, p, port=0, shorts_py=self.stub)
            self.assertIn("prepare.py", str(cm.exception))
        with open(os.path.join(self.cache, "analysis.json"), "w") as f:
            json.dump({**ANALYSIS, "profile": "ryan-obs", "profile_key": profiles.cache_key(p)}, f)
        server.make_server(self.raw, p, port=0, shorts_py=self.stub).server_close()

    def test_server_cli_mismatch(self):
        raw = os.path.join(self.tmp.name, "two.mp4")
        make_mp4(raw, 2, 2)
        config = os.path.join(self.tmp.name, "cfg")
        os.makedirs(config)
        with open(os.path.join(config, "default"), "w") as f:
            f.write("ryan-obs\n")
        r = subprocess.run([sys.executable, os.path.join(HERE, "..", "scripts", "server.py"), raw],
                           capture_output=True, text=True, timeout=30,
                           env={**os.environ, "STREAM_TRIM_CONFIG": config})
        self.assertEqual(r.returncode, 1)
        self.assertIn("ERROR: this recording has 2 audio tracks", r.stderr)
        self.assertNotIn("READY", r.stdout)

    def test_shorts_render(self):
        self.write_edit()
        self.write_candidates()
        with open(self.cand_path, "rb") as f:
            before = f.read()
        picks = [{"n": 1, "start": 21, "end": 30, "pan_x": 50, "fixes": {"x": "y"}},
                 {"n": 2, "start": 40, "end": 50, "pan_x": None, "fixes": {}}]
        self.assertEqual(self.post("/api/shorts/render", {"picks": picks})[0], 202)
        s = self.wait_shorts("done")
        self.assertEqual([s["clips"][k]["state"] for k in ("1", "2")], ["done", "done"])
        self.assertTrue(s["clips"]["1"]["output"].endswith("01-one.mp4"))
        with open(os.path.join(self.shorts, "shorts.json")) as f:
            m = json.load(f)
        self.assertEqual([c["file"] for c in m["clips"]], ["01-one.mp4", "02-two.mp4"])
        self.assertEqual(m["clips"][0]["start"], "00:00:21.00")
        self.assertEqual(m["clips"][0]["fixes"], {"x": "y"})
        self.assertNotIn("pan_x", m["clips"][1])
        self.assertTrue(m["mix_audio"].endswith("short_audio.py"))
        self.assertEqual(m["words"], "/w.json")
        with open(self.cand_path, "rb") as f:
            self.assertEqual(f.read(), before)

    def test_shorts_render_progress(self):
        self.write_edit()
        self.write_candidates()
        with mock.patch.dict(os.environ, {"STUB_PROGRESS": "0.6", "STUB_SLEEP": "1.5"}):
            self.post("/api/shorts/render", {"picks": [{"n": 1, "start": 20, "end": 30}]})
            seen = []
            stop = time.time() + 10
            while time.time() < stop:
                c = self.shorts_state()["render"]["clips"]["1"]
                if c["state"] == "rendering":
                    seen.append((c.get("phase"), c.get("percent")))
                if c["state"] == "done":
                    break
                time.sleep(0.02)
        # 5.3 s into a 10.6 s clip (0.2 s before, 0.4 s after the words).
        self.assertIn(("audio", None), seen)
        enc = [p for ph, p in seen if ph == "encoding"]
        self.assertTrue(enc, seen)
        self.assertAlmostEqual(enc[-1], 50.0, delta=0.5)
        self.assertEqual(c["state"], "done")

    def test_shorts_render_error_reported(self):
        self.write_edit()
        self.write_candidates(json.dumps({"recording": self.raw, "words": "/w.json", "clips": [
            {"file": "01-bad.mp4", "start": 20, "end": 30, "hook": "fail"}]}))
        self.post("/api/shorts/render", {"picks": [{"n": 1, "start": 20, "end": 30}]})
        s = self.wait_shorts("error")
        self.assertEqual(s["clips"]["1"]["error"], "ERROR: render broke")

    def test_shorts_render_number_collision(self):
        self.write_edit()
        self.write_candidates()
        with open(os.path.join(self.shorts, "shorts.json"), "w") as f:
            json.dump({"recording": self.raw, "words": "/w.json",
                       "clips": [{"file": "01-older.mp4", "start": 1, "end": 2}]}, f)
        code, body = self.post("/api/shorts/render", {"picks": [{"n": 1, "file": "01-one.mp4", "start": 20, "end": 30}]})
        self.assertEqual(code, 400)
        self.assertIn("01-older.mp4", body["error"])
        self.assertEqual(self.stub_calls(), [])

    def test_shorts_render_file_mismatch(self):
        self.write_edit()
        self.write_candidates()
        code, body = self.post("/api/shorts/render", {"picks": [{"n": 1, "file": "01-stale.mp4", "start": 20, "end": 30}]})
        self.assertEqual(code, 400)
        self.assertIn("changed", body["error"])

    def builtin_layouts(self):
        """The real shorts.py sits next to stream-shorts' layouts.json; the stub doesn't."""
        shutil.copyfile(os.path.join(HERE, "..", "..", "stream-shorts", "scripts", "layouts.json"),
                        os.path.join(os.path.dirname(self.stub), "layouts.json"))

    def test_pick_layout(self):
        """The card's Code + me / Just me switch sends a layout with the pick."""
        self.builtin_layouts()
        self.write_candidates()
        self.assertEqual(self.post("/api/shorts/preview", {"n": 1, "start": 20, "end": 30, "layout": "me"})[0], 200)
        with open(os.path.join(self.cache, "shorts-work", "manifest.json")) as f:
            self.assertEqual(json.load(f)["clips"][0]["layout"], "me")
        code, body = self.post("/api/shorts/preview", {"n": 1, "start": 20, "end": 30, "layout": "nope"})
        self.assertEqual(code, 400)
        self.assertIn("nope", body["error"])
        # No layout in the pick keeps Claude's (candidate 1 says "center").
        self.post("/api/shorts/preview", {"n": 1, "start": 20, "end": 30})
        with open(os.path.join(self.cache, "shorts-work", "manifest.json")) as f:
            self.assertEqual(json.load(f)["clips"][0]["layout"], "center")
        self.assertEqual(self.post("/api/shorts/render", {"picks": [{"n": 2, "start": 40, "end": 50, "layout": "me-square"}]})[0], 202)
        self.wait_shorts("done")
        with open(os.path.join(self.shorts, "shorts.json")) as f:
            self.assertEqual(json.load(f)["clips"][0]["layout"], "me-square")

    # -- the overhauled Shorts tab: rendered, dismissed --

    def test_shorts_rendered_and_dismissed(self):
        self.write_candidates()
        st = self.shorts_state()
        self.assertEqual((st["rendered"], st["dismissed"]), ({}, []))
        self.post("/api/shorts/render", {"picks": [{"n": 1, "start": 21, "end": 30}]})
        self.wait_shorts("done")
        r = self.shorts_state()["rendered"]["1"]
        self.assertEqual((r["file"], r["start"], r["end"], r["exists"]), ("01-one.mp4", "00:00:21.00", "00:00:30.00", True))
        self.assertEqual(r["layout"], "center")
        # Saved across a server restart, like the page reloading.
        self.assertEqual(self.post("/api/shorts/dismiss", {"n": 2, "dismissed": True})[0], 200)
        self.assertEqual(self.post("/api/shorts/dismiss", {"n": 3, "dismissed": True})[0], 200)
        srv = server.make_server(self.raw, profiles.load("ryan-obs"), port=0, shorts_py=self.stub)
        self.addCleanup(srv.server_close)
        self.assertEqual(srv.shorts_state()["dismissed"], [2, 3])
        self.assertEqual(self.post("/api/shorts/dismiss", {"n": 3, "dismissed": False})[0], 200)
        self.assertEqual(self.shorts_state()["dismissed"], [2])
        for bad in ({"n": 9, "dismissed": True}, {"n": 1}, {"n": "1", "dismissed": True}, [1]):
            self.assertEqual(self.post("/api/shorts/dismiss", bad)[0], 400, bad)
        # A rendered file that's gone (deleted in Finder) shows as not there.
        os.remove(os.path.join(self.shorts, "01-one.mp4"))
        self.assertFalse(self.shorts_state()["rendered"]["1"]["exists"])

    def test_rendered_file_served_and_revealed(self):
        self.write_candidates()
        self.post("/api/shorts/render", {"picks": [{"n": 1, "start": 21, "end": 30}]})
        self.wait_shorts("done")
        code, _, body = self.get("/shorts/file/1.mp4")
        self.assertEqual((code, body), (200, b"MP4"))
        self.assertEqual(self.get("/shorts/file/2.mp4")[0], 404)
        calls = []
        self.srv.open_cmd = calls.append
        self.assertEqual(self.post("/api/reveal", {"target": "short", "n": 1})[0], 200)
        self.assertEqual(calls, [["open", "-R", os.path.join(self.shorts, "01-one.mp4")]])
        self.assertEqual(self.post("/api/reveal", {"target": "short", "n": 2})[0], 404)

    def test_rendered_from_an_earlier_shortlist(self):
        """Shorts rendered from an earlier shortlist still show (under Rendered), and can be re-rendered."""
        self.write_candidates()
        with open(os.path.join(self.shorts, "shorts.json"), "w") as f:
            json.dump({"recording": self.raw, "words": "/w.json", "clips": [
                {"file": "07 - Old one.mp4", "start": "00:01:00.00", "end": "00:01:10.00", "hook": "old", "layout": "center"}]}, f)
        open(os.path.join(self.shorts, "07 - Old one.mp4"), "wb").close()
        c = {x["n"]: x for x in self.shorts_state()["candidates"]}
        self.assertEqual(sorted(c), [1, 2, 3, 7])
        self.assertTrue(c[7]["earlier"])
        self.assertNotIn("earlier", c[1])
        self.assertEqual(c[7]["file"], "07 - Old one.mp4")
        self.assertEqual(self.post("/api/shorts/preview", {"n": 7, "start": 60, "end": 70})[0], 200)
        self.assertEqual(self.post("/api/shorts/render", {"picks": [{"n": 7, "start": 61, "end": 70}]})[0], 202)
        self.assertTrue(self.wait_shorts("done")["clips"]["7"]["output"].endswith("07 - Old one.mp4"))
        # With no shortlist at all, the rendered ones still show.
        os.remove(self.cand_path)
        self.assertEqual([x["n"] for x in self.shorts_state()["candidates"]], [7])

    def test_shorts_render_checks(self):
        self.write_edit()
        self.write_candidates()
        for picks in ([{"n": 1, "start": 30, "end": 20}], [{"n": 9, "start": 20, "end": 30}], [], "x"):
            code, body = self.post("/api/shorts/render", {"picks": picks})
            self.assertEqual(code, 400, picks)
            self.assertIn("error", body)
        with mock.patch.dict(os.environ, {"STUB_SLEEP": "0.5"}):
            self.assertEqual(self.post("/api/shorts/render", {"picks": [{"n": 1, "start": 20, "end": 30}]})[0], 202)
            self.assertEqual(self.post("/api/shorts/render", {"picks": [{"n": 2, "start": 40, "end": 50}]})[0], 409)
            self.wait_shorts("done")

    # -- shorts before the final, and while it renders --

    def test_shorts_before_final(self):
        """Shorts are standalone: no final render needed, and a short outside
        the trim is flagged, not refused."""
        self.write_candidates()
        s = self.shorts_state()
        self.assertEqual([x["n"] for x in s["candidates"]], [1, 2, 3])
        # Without an edit, inside is judged against prepare's default In/Out (69.5-91).
        self.assertEqual([x["inside"] for x in s["candidates"]], [False, False, False])
        self.assertEqual(self.post("/api/shorts/preview", {"n": 3, "start": 5, "end": 15})[0], 200)
        self.assertEqual(self.post("/api/shorts/render", {"picks": [{"n": 3, "start": 5, "end": 15}]})[0], 202)
        self.assertEqual(self.wait_shorts("done")["clips"]["3"]["state"], "done")

    def test_shorts_render_during_final(self):
        self.write_candidates()
        with self.srv.lock:
            self.srv.status["state"] = "running"
        try:
            self.assertEqual(self.post("/api/shorts/render", {"picks": [{"n": 1, "start": 20, "end": 30}]})[0], 202)
            self.wait_shorts("done")
        finally:
            with self.srv.lock:
                self.srv.status["state"] = "idle"

    # -- finding shorts: transcription progress --

    def test_finding_progress(self):
        t = os.path.join(self.tmp.name, "transcript")
        self.srv.transcript_dir = lambda: t
        finding = lambda: self.shorts_state()["finding"]
        self.assertEqual(finding()["stage"], "waiting")
        os.makedirs(t)
        log = os.path.join(t, "log")
        with open(log, "w") as f:
            f.write("Extracting audio from raw.mp4...\n")
        self.assertEqual(finding()["stage"], "audio")
        with open(log, "a") as f:
            f.write("Transcribing with m...\n[00:50.000 --> 00:55.500]  hi\n[01:10.000 --> 01:15.000]  there\n")
        f2 = finding()
        self.assertEqual((f2["stage"], f2["at"], f2["percent"]), ("transcribing", 75.0, 75.0))
        with open(log, "a") as f:
            f.write("[01:00:01.000 --> 01:00:02.500]  past the end\n")
        self.assertEqual(finding()["percent"], 99.9)
        with open(log, "a") as f:
            f.write("Re-transcribing looped range 00:01:00-00:02:00...\n")
        self.assertEqual(finding()["stage"], "checking")
        open(os.path.join(t, "done"), "w").close()
        f3 = finding()
        self.assertEqual(f3["stage"], "picking")
        self.assertIsInstance(f3["since"], float)
        self.write_candidates()
        self.assertEqual(finding()["stage"], "ready")
        os.remove(self.cand_path)
        os.remove(os.path.join(t, "done"))
        with open(os.path.join(t, "failed"), "w") as f:
            f.write("ffmpeg could not extract audio\n")
        self.assertEqual(finding(), {"stage": "error", "error": "ffmpeg could not extract audio"})

    def test_transcript_dir_found(self):
        d = self.srv.transcript_dir()
        self.assertTrue(d and os.path.isabs(d), d)
        self.assertFalse(os.path.exists(d))  # finding it never creates it

    # -- titles --

    def post_titles(self, body):
        return self.post("/api/titles", body)

    def test_titles_options(self):
        opts = {"final": [{"title": "One", "score": 82}, {"title": "Two", "score": None}],
                "shorts": {"1": [{"title": "Short one", "score": 70}]}}
        self.assertEqual(self.post_titles(opts)[0], 200)
        self.assertEqual(self.post_titles({"shorts": {"2": [{"title": "Short two"}]}})[0], 200)
        t = json.loads(self.get("/api/titles")[2])
        self.assertEqual([o["title"] for o in t["options"]["final"]], ["One", "Two"])
        self.assertEqual(sorted(t["options"]), ["1", "2", "final"])
        self.assertEqual(t["picked"], {})
        self.assertIn("titles", self.shorts_state())
        for bad in ({"final": "x"}, {"final": [{"title": ""}]}, {"final": [{"title": "a", "score": "9"}]},
                    {"shorts": {"x": []}}, [1]):
            self.assertEqual(self.post_titles(bad)[0], 400, bad)

    def write_final(self):
        out = os.path.join(self.tmp.name, "renders", "raw, stream-final.mp4")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "wb") as f:
            f.write(b"FINAL")
        self.write_edit({"in": 10.0, "out": 90.0, "output": out})
        return out

    def test_title_final_renames(self):
        self.assertEqual(self.post("/api/title", {"target": "final", "title": "A"})[0], 409)
        out = self.write_final()
        code, body = self.post("/api/title", {"target": "final", "title": "Contributor Toolkit: Open / Debug "})
        self.assertEqual(code, 200, body)
        new = os.path.join(self.tmp.name, "renders", "Contributor Toolkit - Open - Debug.mp4")
        self.assertEqual(body["path"], new)
        self.assertFalse(os.path.exists(out))
        with open(new, "rb") as f:
            self.assertEqual(f.read(), b"FINAL")
        st = self.state()
        self.assertEqual((st["output"], st["exists"], st["edit"]["output"]), (new, True, new))
        self.assertEqual(json.loads(self.get("/api/titles")[2])["picked"]["final"], "Contributor Toolkit: Open / Debug")
        # The renamed final still counts: no second render.
        self.assertEqual(self.post("/api/render", {"in": 1, "out": 50})[0], 409)
        # Picking again renames from the current name; a taken name is refused.
        open(os.path.join(self.tmp.name, "renders", "Taken.mp4"), "wb").close()
        self.assertEqual(self.post("/api/title", {"target": "final", "title": "Taken"})[0], 409)
        self.assertEqual(self.post("/api/title", {"target": "final", "title": "Again"})[0], 200)
        self.assertTrue(os.path.exists(os.path.join(self.tmp.name, "renders", "Again.mp4")))
        for bad in ({"target": "final", "title": " :/ "}, {"target": "final"}, {"target": "x", "title": "a"}, "x"):
            self.assertEqual(self.post("/api/title", bad)[0], 400, bad)

    def test_title_short_renames(self):
        self.write_candidates()
        self.assertEqual(self.post("/api/title", {"target": 1, "title": "My Title"})[0], 409)  # not rendered
        self.assertEqual(self.post("/api/shorts/render", {"picks": [{"n": 1, "start": 20, "end": 30}]})[0], 202)
        self.wait_shorts("done")
        code, body = self.post("/api/title", {"target": 1, "title": "My Title?"})
        self.assertEqual(code, 200, body)
        new = os.path.join(self.shorts, "01 - My Title?.mp4")
        self.assertEqual(body["path"], new)
        self.assertTrue(os.path.exists(new))
        self.assertFalse(os.path.exists(os.path.join(self.shorts, "01-one.mp4")))
        with open(os.path.join(self.shorts, "shorts.json")) as f:
            self.assertEqual([c["file"] for c in json.load(f)["clips"]], ["01 - My Title?.mp4"])
        # Re-rendering it from the page writes to the new name, not the old one.
        self.assertEqual(self.post("/api/shorts/render", {"picks": [{"n": 1, "file": "01-one.mp4", "start": 21, "end": 30}]})[0], 202)
        self.assertTrue(self.wait_shorts("done")["clips"]["1"]["output"].endswith("01 - My Title?.mp4"))
        self.assertFalse(os.path.exists(os.path.join(self.shorts, "01-one.mp4")))
        with open(os.path.join(self.shorts, "shorts.json")) as f:
            self.assertEqual([c["file"] for c in json.load(f)["clips"]], ["01 - My Title?.mp4"])


if __name__ == "__main__":
    unittest.main()
