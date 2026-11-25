"""The "Claude needs you in the terminal" banner: Claude Code hooks run
attention.py, which tells every running stream-trim page."""
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.request
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "scripts")
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)

import attention  # noqa: E402
import prepare  # noqa: E402
import profiles  # noqa: E402
import server  # noqa: E402
from test_server import ANALYSIS, STUB  # noqa: E402

CLI = os.path.join(SCRIPTS, "attention.py")


class AttentionTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        t = self.tmp.name
        self.servers = os.path.join(t, "servers")
        env = mock.patch.dict(os.environ, {"STREAM_TRIM_SERVERS": self.servers})
        env.start()
        self.addCleanup(env.stop)
        cache = os.path.join(t, "cache")
        os.makedirs(cache)
        for name, data in (("analysis.json", ANALYSIS), ("peaks.json", {"per_s": 20, "peaks": [0.0]})):
            with open(os.path.join(cache, name), "w") as f:
                json.dump(data, f)
        stub = os.path.join(t, "stub.py")
        with open(stub, "w") as f:
            f.write(STUB)
        self.raw = os.path.join(t, "raw.mp4")
        open(self.raw, "wb").close()
        with mock.patch.object(prepare, "cache_dir", return_value=cache):
            self.srv = server.make_server(self.raw, profiles.load("ryan-obs"), port=0, shorts_py=stub)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.addCleanup(self.srv.server_close)
        self.addCleanup(self.srv.shutdown)
        self.port = self.srv.server_address[1]

    def state(self):
        with urllib.request.urlopen(f"http://127.0.0.1:{self.port}/api/attention") as r:
            return json.loads(r.read())

    def cli(self, *args, stdin=""):
        return subprocess.run([sys.executable, CLI, *args], input=stdin, capture_output=True, text=True, timeout=20)

    def test_registry(self):
        attention.register(self.port, os.getpid(), self.raw)
        attention.register(1, 999999, "/gone.mp4")  # a server that died without cleaning up
        self.assertEqual([s["port"] for s in attention.live_servers()], [self.port])
        self.assertFalse(os.path.exists(os.path.join(self.servers, "1.json")))
        attention.unregister(self.port)
        self.assertEqual(attention.live_servers(), [])

    def test_set_and_clear(self):
        self.assertEqual(self.state()["waiting"], False)
        attention.register(self.port, os.getpid(), self.raw)
        r = self.cli("set", "Claude asked you a question in the terminal", stdin='{"tool_name": "AskUserQuestion"}')
        self.assertEqual(r.returncode, 0, r.stderr)
        s = self.state()
        self.assertEqual((s["waiting"], s["reason"]), (True, "Claude asked you a question in the terminal"))
        self.assertIsInstance(s["since"], float)
        self.assertEqual(self.cli("clear").returncode, 0)
        self.assertEqual(self.state(), {"waiting": False, "reason": None, "since": None})

    def test_notify(self):
        attention.register(self.port, os.getpid(), self.raw)
        for kind, word in (("permission_prompt", "approve"), ("idle_prompt", "reply"), ("elicitation_dialog", "terminal")):
            self.cli("notify", stdin=json.dumps({"hook_event_name": "Notification", "notification_type": kind}))
            s = self.state()
            self.assertTrue(s["waiting"], kind)
            self.assertIn(word, s["reason"], kind)
        self.cli("clear")
        self.cli("notify", stdin='{"notification_type": "auth_success"}')
        self.assertFalse(self.state()["waiting"])

    def test_never_fails(self):
        """A hook must never get in Claude's way: no servers, junk input, a dead port."""
        for args, stdin in ((["set", "x"], ""), (["notify"], "not json"), (["clear"], ""), ([], ""), (["bogus"], "")):
            r = self.cli(*args, stdin=stdin)
            self.assertEqual((r.returncode, r.stdout), (0, ""), args)
        attention.register(9, os.getpid(), "/x.mp4")  # alive pid, nothing listening
        self.assertEqual(self.cli("set", "x").returncode, 0)

    def test_bad_post(self):
        req = urllib.request.Request(f"http://127.0.0.1:{self.port}/api/attention", data=b'{"waiting": "yes"}',
                                     method="POST", headers={"Content-Type": "application/json"})
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(req)
        cm.exception.close()
        self.assertEqual(cm.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
