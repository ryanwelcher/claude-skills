import os
import subprocess
import sys
import tempfile
import threading
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
sys.path.insert(0, HERE)

import audio_chain  # noqa: E402
import render  # noqa: E402
from test_measure import make_mp4  # noqa: E402

CHAIN = audio_chain.load_chain(os.path.join(HERE, "..", "scripts", "chain.json"))


def streams(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=codec_type,codec_name,channels,sample_rate:format=duration",
                          "-of", "json", path], capture_output=True, text=True, check=True).stdout
    import json
    return json.loads(out)


class PureTest(unittest.TestCase):
    def test_final_path(self):
        self.assertEqual(render.final_path("/x/Nov 12/2026-11-12 10-24-27.mp4"),
                         "/x/Nov 12/2026-11-12 10-24-27-final.mp4")

    def test_parse_progress(self):
        self.assertEqual(render.parse_progress("out_time_us=5000000", 10), 50.0)
        self.assertIsNone(render.parse_progress("progress=end", 10))
        self.assertIsNone(render.parse_progress("out_time_us=N/A", 10))
        self.assertIsNone(render.parse_progress("garbage", 10))


class RenderTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raw = os.path.join(self.tmp.name, "raw, stream.mp4")
        make_mp4(self.raw, 6, 12)
        self.out = render.final_path(self.raw)
        self.partial = self.out.replace("-final.mp4", "-final.partial.mp4")

    def tearDown(self):
        self.tmp.cleanup()

    def test_render_final_trims_exactly(self):
        self.assertEqual(render.render_final(self.raw, 2, 8, CHAIN), self.out)
        info = streams(self.out)
        self.assertAlmostEqual(float(info["format"]["duration"]), 6, delta=1001 / 24000 + 0.03)
        kinds = sorted(s["codec_type"] for s in info["streams"])
        self.assertEqual(kinds, ["audio", "video"])
        audio = next(s for s in info["streams"] if s["codec_type"] == "audio")
        video = next(s for s in info["streams"] if s["codec_type"] == "video")
        self.assertEqual((audio["codec_name"], audio["channels"], audio["sample_rate"]), ("aac", 2, "48000"))
        self.assertEqual(video["codec_name"], "h264")
        self.assertFalse(os.path.exists(self.partial))

    def test_render_final_refuses_existing(self):
        render.render_final(self.raw, 2, 4, CHAIN)
        mtime = os.stat(self.out).st_mtime
        with self.assertRaises(FileExistsError):
            render.render_final(self.raw, 2, 4, CHAIN)
        self.assertEqual(os.stat(self.out).st_mtime, mtime)

    def test_render_final_bad_range(self):
        for a, b in ((8, 2), (-1, 3), (2, 99)):
            with self.assertRaises(ValueError):
                render.render_final(self.raw, a, b, CHAIN)

    def test_render_final_stop_cleans_up(self):
        stop = threading.Event()

        def progress(percent, phase):
            if phase == "encoding":
                stop.set()

        with self.assertRaises(RuntimeError) as cm:
            render.render_final(self.raw, 0, 11, CHAIN, progress=progress, stop=stop)
        self.assertEqual(str(cm.exception), "stopped")
        self.assertFalse(os.path.exists(self.out))
        self.assertFalse(os.path.exists(self.partial))


if __name__ == "__main__":
    unittest.main()
