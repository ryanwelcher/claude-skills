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
        self.srv = server.make_server(self.raw, {"loudness": {}}, port=0)
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


if __name__ == "__main__":
    unittest.main()
