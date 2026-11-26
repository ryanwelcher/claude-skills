import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import vision  # noqa: E402

FACE = os.path.join(HERE, "fixtures", "face.jpg")


@unittest.skipUnless(shutil.which("swiftc"), "needs the Xcode command-line tools")
class VisionTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_faces_finds_one(self):
        [r] = vision.faces([FACE])
        self.assertEqual(r["path"], FACE)
        self.assertEqual(len(r["faces"]), 1)
        f = r["faces"][0]
        self.assertGreater(f["quality"], 0)
        x, y, w, h = f["box"]
        self.assertGreater(x + w / 2, 320)

    def test_faces_none(self):
        grey = os.path.join(self.tmp.name, "grey.jpg")
        Image.new("RGB", (640, 360), (128, 128, 128)).save(grey)
        self.assertEqual(vision.faces([grey])[0]["faces"], [])

    def test_cutout_alpha(self):
        box = vision.faces([FACE])[0]["faces"][0]["box"]
        out = os.path.join(self.tmp.name, "cut.png")
        cx, cy, cw, ch = vision.cutout(FACE, box, out)
        im = Image.open(out)
        self.assertEqual(im.mode, "RGBA")
        alphas = set(im.getchannel("A").get_flattened_data())
        self.assertIn(0, alphas)
        self.assertIn(255, alphas)
        x, y, w, h = box
        self.assertLessEqual(cx, x)
        self.assertLessEqual(cy, y)
        self.assertGreaterEqual(cx + cw, x + w)
        self.assertGreaterEqual(cy + ch, y + h)

    def test_cutout_two_people(self):
        two = os.path.join(self.tmp.name, "two.jpg")
        src = Image.open(FACE)
        canvas = Image.new("RGB", (1280, 360))
        canvas.paste(ImageOps.mirror(src), (0, 0))
        canvas.paste(src, (640, 0))
        canvas.save(two)
        faces = vision.faces([two])[0]["faces"]
        right = max(faces, key=lambda f: f["box"][0])["box"]
        self.assertGreater(right[0], 640)
        cx, _, _, _ = vision.cutout(two, right, os.path.join(self.tmp.name, "cut.png"))
        self.assertGreaterEqual(cx, 640)

    def test_binary_cached(self):
        first = vision.binary()
        with mock.patch.object(vision.subprocess, "run") as run:
            self.assertEqual(vision.binary(), first)
            run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
