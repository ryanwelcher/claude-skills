import json
import os
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
import server  # noqa: E402


STUB = """import json, os, sys, time
args = sys.argv[1:]
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps(args) + "\\n")
mode = args.pop(0) if args[0].startswith("--") else None
manifest, n = args
m = json.load(open(manifest))
clip = next(c for c in m["clips"] if int(c["file"].split("-")[0]) == int(n))
out = os.path.join(os.path.dirname(manifest), clip["file"])
if mode == "--preview":
    open(os.path.splitext(out)[0] + ".jpg", "wb").write(b"JPG")
    print("PREVIEW: x")
elif mode == "--captions":
    print("== " + clip["file"])
    print("HELLO WORLD")
elif clip.get("hook") == "fail":
    print("ERROR: render broke", file=sys.stderr)
    sys.exit(1)
else:
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
        self.srv = server.make_server(self.raw, {"loudness": {}}, port=0, shorts_py=self.stub)
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
        self.assertTrue(s["output"].endswith("raw, stream-final.mp4"))
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
        open(os.path.join(self.tmp.name, "raw, stream-final.mp4"), "wb").close()
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
        srv = server.make_server(self.raw, {"loudness": {}}, port=0, shorts_py=self.stub)
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

    def test_shorts_render_error_reported(self):
        self.write_edit()
        self.write_candidates(json.dumps({"recording": self.raw, "words": "/w.json", "clips": [
            {"file": "01-bad.mp4", "start": 20, "end": 30, "hook": "fail"}]}))
        self.post("/api/shorts/render", {"picks": [{"n": 1, "start": 20, "end": 30}]})
        s = self.wait_shorts("error")
        self.assertEqual(s["clips"]["1"]["error"], "ERROR: render broke")

    def test_shorts_render_rejects_outside(self):
        self.write_candidates()
        self.assertEqual(self.post("/api/shorts/render", {"picks": [{"n": 1, "start": 20, "end": 30}]})[0], 409)
        self.write_edit()
        for picks in ([{"n": 1, "start": 30, "end": 20}], [{"n": 3, "start": 5, "end": 15}],
                      [{"n": 9, "start": 20, "end": 30}], [], "x"):
            code, body = self.post("/api/shorts/render", {"picks": picks})
            self.assertEqual(code, 400, picks)
            self.assertIn("error", body)
        with mock.patch.dict(os.environ, {"STUB_SLEEP": "0.5"}):
            self.assertEqual(self.post("/api/shorts/render", {"picks": [{"n": 1, "start": 20, "end": 30}]})[0], 202)
            self.assertEqual(self.post("/api/shorts/render", {"picks": [{"n": 2, "start": 40, "end": 50}]})[0], 409)
            self.wait_shorts("done")


if __name__ == "__main__":
    unittest.main()
