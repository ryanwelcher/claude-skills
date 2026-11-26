import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import thumbs  # noqa: E402
import vision  # noqa: E402

FACE = os.path.join(HERE, "fixtures", "face.jpg")
SWIFT = shutil.which("swiftc")


def yellow(px):
    r, g, b = px[:3]
    return r > 200 and g > 180 and b < 80


class FrameTimesTest(unittest.TestCase):
    def test_frame_times(self):
        self.assertEqual(thumbs.frame_times(10, 40, 3), [15.0, 25.0, 35.0])

    def test_parse_time(self):
        self.assertEqual(thumbs.parse_time("71.5"), 71.5)
        self.assertEqual(thumbs.parse_time("00:01:10.50"), 70.5)
        self.assertEqual(thumbs.parse_time("1:02:03"), 3723.0)

    def test_frames_cli_shift(self):
        with mock.patch.object(thumbs, "frames", return_value=[]) as f:
            thumbs.main(["frames", "/x/raw.mp4", "00:01:10.00", "00:01:20.00", "/tmp/o", "--shift", "0.5"])
        f.assert_called_once_with("/x/raw.mp4", 69.5, 79.5, "/tmp/o")

    def test_frames_refuses_cloud_only(self):
        with mock.patch.object(thumbs.profiles, "cloud_only", return_value=True), \
                mock.patch.object(thumbs.subprocess, "run") as run:
            with self.assertRaisesRegex(ValueError, "cloud"):
                thumbs.frames("/x/raw.mp4", 0, 10, "/tmp/nowhere")
            run.assert_not_called()


@unittest.skipUnless(SWIFT, "needs the Xcode command-line tools")
class ThumbsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.box = vision.faces([FACE])[0]["faces"][0]["box"]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def path(self, name):
        return os.path.join(self.tmp.name, name)

    def test_frames_ranks(self):
        grey = self.path("grey.jpg")
        Image.new("RGB", (640, 360), (128, 128, 128)).save(grey)
        mp4 = self.path("clip.mp4")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y",
                        "-loop", "1", "-t", "2", "-i", FACE, "-loop", "1", "-t", "2", "-i", grey,
                        "-filter_complex", "[0:v][1:v]concat=n=2:v=1[v]", "-map", "[v]",
                        "-r", "24", "-pix_fmt", "yuv420p", mp4], check=True)
        out = self.path("frames")
        got = thumbs.frames(mp4, 0, 4, out, count=4, keep=8)
        self.assertEqual([round(g["t"], 1) for g in got if g["t"] >= 2], [])
        self.assertTrue(got)
        self.assertEqual(got, sorted(got, key=lambda g: -g["quality"]))
        for g in got:
            self.assertTrue(os.path.exists(g["path"]))
            self.assertEqual(len(g["box"]), 4)

    def test_compose_landscape(self):
        out = thumbs.compose(FACE, self.box, ["Finding", "core bugs!"], "landscape", self.path("l.jpg"))
        im = Image.open(out)
        self.assertEqual(im.format, "JPEG")
        self.assertEqual(im.size, (1280, 720))
        self.assertLess(os.path.getsize(out), 2 * 1024 * 1024)
        # Text goes opposite the person; the fixture's face is on the right.
        left = im.crop((0, 0, 640, 360)).convert("RGB")
        self.assertTrue(any(yellow(p) for p in left.get_flattened_data()))

    def test_compose_portrait(self):
        out = thumbs.compose(FACE, self.box, ["No docker!"], "portrait", self.path("p.jpg"))
        im = Image.open(out).convert("RGB")
        self.assertEqual(im.size, (1080, 1920))
        # The person fills the bottom: its pixels aren't the tinted background.
        bottom = im.crop((0, 1344, 1080, 1920))
        bg = Image.open(out).convert("RGB").crop((0, 900, 60, 960)).resize((1, 1)).getpixel((0, 0))
        far = [p for p in bottom.get_flattened_data() if sum(abs(a - b) for a, b in zip(p, bg)) > 120]
        self.assertGreater(len(far), 1080 * 576 * 0.1)

    def test_compose_long_text_fits(self):
        out = thumbs.compose(FACE, self.box, ["CONTRIBUTORTOOLKIT", "IS", "HERE"], "landscape",
                             self.path("long.jpg"))
        im = Image.open(out).convert("RGB")
        w, h = im.size
        border = [im.getpixel((x, y)) for x in range(w) for y in (*range(8), *range(h - 8, h))]
        border += [im.getpixel((x, y)) for y in range(h) for x in (*range(8), *range(w - 8, w))]
        self.assertFalse(any(yellow(p) for p in border))


if __name__ == "__main__":
    unittest.main()
