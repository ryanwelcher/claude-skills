"""The Streams tab: every recording with a stream-trim cache, and what's
been made from it."""
import json
import os
import sys
import tempfile
import time
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import streams  # noqa: E402


def write(path, data=b""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if isinstance(data, bytes) else "w") as f:
        f.write(data if isinstance(data, bytes) else json.dumps(data))


class StreamsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        t = self.tmp.name
        self.root = os.path.join(t, "caches")
        # A: everything made. B: a cache from before profiles, raw gone. C: no analysis yet.
        self.raw_a = os.path.join(t, "Nov 12", "rec-a.mp4")
        write(self.raw_a)
        self.final_a = os.path.join(t, "Nov 12", "renders", "rec-a-final.mp4")
        write(self.final_a)
        write(os.path.join(t, "Nov 12", "renders", "youtube-description.txt"), b"Title:")
        write(os.path.join(t, "Nov 12", "shorts", "shorts.json"),
              {"clips": [{"file": "01-a.mp4"}, {"file": "02-b.mp4"}]})
        write(os.path.join(t, "Nov 12", "shorts", "01-a.mp4"))
        a = os.path.join(self.root, "aaaa")
        write(os.path.join(a, "analysis.json"), {"raw": self.raw_a, "profile": "ryan-obs"})
        write(os.path.join(a, "edit.json"), {"in": 1, "out": 2, "output": self.final_a})
        write(os.path.join(a, "proxy.mp4"), b"x" * 2_000_000)
        b = os.path.join(self.root, "bbbb")
        write(os.path.join(b, "analysis.json"), {"raw": os.path.join(t, "gone", "rec-b.mp4")})
        old = time.time() - 86400
        for f in os.listdir(b):
            os.utime(os.path.join(b, f), (old, old))
        os.makedirs(os.path.join(self.root, "cccc"))

    def test_list(self):
        got = streams.list_streams(self.root)
        self.assertEqual([s["id"] for s in got], ["aaaa", "bbbb"])
        a, b = got
        self.assertEqual((a["name"], a["state"], a["profile"]), ("rec-a.mp4", "local", "ryan-obs"))
        self.assertEqual(a["final"], self.final_a)
        self.assertEqual(a["shorts"], {"picked": 2, "rendered": 1})
        self.assertTrue(a["description"].endswith(os.path.join("renders", "youtube-description.txt")))
        self.assertGreaterEqual(a["cache_bytes"], 2_000_000)
        self.assertEqual((b["state"], b["profile"], b["final"], b["shorts"], b["description"]),
                         ("missing", "ryan-obs", None, None, None))
        self.assertGreater(a["last_used"], b["last_used"])

    def test_cloud_only(self):
        with mock.patch.object(streams.profiles, "cloud_only", return_value=True):
            self.assertEqual(streams.list_streams(self.root)[0]["state"], "cloud-only")

    def test_final_from_before_renders(self):
        """A final made before renders/ existed sits next to the raw, and the
        edit records where it went."""
        moved = os.path.join(self.tmp.name, "Nov 12", "rec-a-final.mp4")
        os.replace(self.final_a, moved)
        write(os.path.join(self.root, "aaaa", "edit.json"), {"in": 1, "out": 2, "output": moved})
        self.assertEqual(streams.list_streams(self.root)[0]["final"], moved)

    def test_reveal_target(self):
        a = streams.list_streams(self.root)[0]
        self.assertEqual(streams.reveal_target(a, "raw"), ["open", "-R", self.raw_a])
        self.assertEqual(streams.reveal_target(a, "final"), ["open", "-R", self.final_a])
        self.assertEqual(streams.reveal_target(a, "shorts"), ["open", os.path.join(self.tmp.name, "Nov 12", "shorts")])
        self.assertEqual(streams.reveal_target(a, "description")[:2], ["open", "-R"])
        b = streams.list_streams(self.root)[1]
        for target in ("raw", "final", "shorts", "description"):
            self.assertIsNone(streams.reveal_target(b, target), target)
        with self.assertRaises(ValueError):
            streams.reveal_target(a, "../../etc")


if __name__ == "__main__":
    unittest.main()
