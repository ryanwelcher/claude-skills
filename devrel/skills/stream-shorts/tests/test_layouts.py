"""Layouts: "Code + me" (coding-rebrand), and two "Just me" looks for talking
shorts: me (a 9:16 slice of the camera) and me-square (a square of the
camera on a blurred copy of it)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

from test_mix_audio import FONT, LIBASS, RENDER, SCRIPTS, make_mp4

LAYOUT = os.path.join(SCRIPTS, "layout.py")


def layout(*args, env=None):
    return subprocess.run([sys.executable, LAYOUT, *args], capture_output=True, text=True, env=env)


class LayoutTest(unittest.TestCase):
    def test_labels(self):
        with open(os.path.join(SCRIPTS, "layouts.json")) as f:
            data = json.load(f)["layouts"]
        self.assertEqual({k: v.get("label") for k, v in data.items() if v.get("label")},
                         {"coding-rebrand": "Code + me", "me": "Just me", "me-square": "Just me (square)"})

    def test_me(self):
        r = layout("me")
        self.assertEqual(r.returncode, 0, r.stderr)
        chain, cap = r.stdout.splitlines()
        self.assertEqual(chain, "[0:v]crop=iw*243/1920:ih*432/1080:iw*1650/1920:ih*588/1080,scale=1080:1920")
        self.assertEqual(int(cap), 1450)
        self.assertIn("iw*1500/1920", layout("me", "1500").stdout)
        self.assertEqual(layout("me", "1700").returncode, 1)  # runs off the camera

    def test_me_square(self):
        r = layout("me-square")
        self.assertEqual(r.returncode, 0, r.stderr)
        chain, cap = r.stdout.splitlines()
        self.assertEqual(int(cap), 1500)
        # The background: the same box, scaled to cover the frame, blurred and dimmed.
        self.assertIn("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:2,eq=brightness=-0.25", chain)
        self.assertIn("crop=iw*420/1920:ih*420/1080:iw*1490/1920:ih*600/1080,scale=1080:1080", chain)
        self.assertIn("overlay=0:300", chain)
        # pan_x moves the square, not the blurred background.
        moved = layout("me-square", "1460").stdout
        self.assertIn("iw*1460/1920", moved)
        self.assertEqual(moved.count("iw*1490/1920"), 1)

    def test_background_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = os.path.join(tmp, "bad.json")
            for band in ({"name": "a", "crop": [420, 420, 0, 0], "height": 1080, "top": 900},  # runs off the bottom
                         {"name": "a", "crop": [420, 420, 0, 0], "height": 1080}):  # no top
                with open(bad, "w") as f:
                    json.dump({"layouts": {"x": {"background": {"crop": [420, 420, 0, 0]}, "bands": [band],
                                                 "caption_y": 1500}}}, f)
                r = layout("x", env={**os.environ, "SHORTS_LAYOUTS": bad})
                self.assertEqual(r.returncode, 1, band)
                self.assertIn("ERROR", r.stderr)

    def test_coding_rebrand_unchanged(self):
        r = layout("coding-rebrand")
        self.assertEqual(r.stdout.splitlines()[0],
                         "[0:v]split=2[b0][b1];[b0]crop=iw*600/1920:ih*500/1080:iw*1320/1920:ih*520/1080,scale=1080:900[o0];"
                         "[b1]crop=iw*1038/1920:ih*980/1080:iw*200/1920:ih*20/1080,scale=1080:1020[o1];[o0][o1]vstack=inputs=2")


@unittest.skipUnless(FONT and LIBASS, "needs the Jost font and an ffmpeg with libass")
class LayoutRenderTest(unittest.TestCase):
    def test_previews(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw = os.path.join(tmp, "six.mp4")
            make_mp4(raw, 6, 4)
            words = os.path.join(tmp, "words.json")
            with open(words, "w") as f:
                json.dump([[1.0, 1.4, "hello"]], f)
            for name in ("me", "me-square"):
                out = os.path.join(tmp, name + ".jpg")
                r = subprocess.run(["bash", RENDER, "--preview", "--layout", name, raw, words, "1", "2", out],
                                   capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stderr)
                dims = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-of", "csv=p=0", out],
                                      capture_output=True, text=True).stdout.strip()
                self.assertEqual(dims, "1080,1920", name)


if __name__ == "__main__":
    unittest.main()
