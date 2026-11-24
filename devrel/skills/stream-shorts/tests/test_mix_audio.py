import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "scripts")
sys.path.insert(0, os.path.join(HERE, "..", "..", "stream-trim", "tests"))

from test_measure import make_mp4  # noqa: E402

RENDER = os.path.join(SCRIPTS, "render-short.sh")
SHORTS = os.path.join(SCRIPTS, "shorts.py")
FONT = any(os.path.exists(p) for p in (os.path.expanduser("~/Library/Fonts/Jost-SemiBold.ttf"),
                                       "/Library/Fonts/Jost-SemiBold.ttf"))
LIBASS = " ass " in subprocess.run(["ffmpeg", "-hide_banner", "-filters"],
                                   capture_output=True, text=True).stdout


@unittest.skipUnless(FONT and LIBASS, "needs the Jost font and an ffmpeg with libass")
class MixAudioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        d = cls.tmp.name
        cls.raw = os.path.join(d, "raw.mp4")
        cls.edit = os.path.join(d, "edit.mp4")
        make_mp4(cls.raw, 6, 6)
        make_mp4(cls.edit, 4, 6)
        cls.words = os.path.join(d, "words.json")
        with open(cls.words, "w") as f:
            json.dump([[1.0, 1.4, "hello"], [1.5, 2.0, "world"]], f)
        cls.out = os.path.join(d, "01-x.mp4")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def run_render(self, *flags, raw=None):
        r = subprocess.run(["bash", RENDER, "--dry-run", *flags, raw or self.raw, self.words,
                            "1", "3", self.out], capture_output=True, text=True)
        # The dry run prints with printf %q, which backslash-escapes brackets.
        r.stdout = r.stdout.replace("\\", "")
        return r

    def test_default_unchanged(self):
        r = self.run_render()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("[1:a:1]loudnorm=I=-14:TP=-1.5:LRA=11", r.stdout)
        self.assertNotIn("audio.wav", r.stdout)

    def test_mix_audio_command(self):
        r = self.run_render("--mix-audio", "/x/short_audio.py")
        self.assertEqual(r.returncode, 0, r.stderr)
        lines = r.stdout.splitlines()
        py = next(l for l in lines if l.startswith("python3 /x/short_audio.py"))
        parts = py.split()
        vs = 0.8 - 9 * 1001 / 24000
        self.assertAlmostEqual(float(parts[3]), vs, places=3)
        self.assertAlmostEqual(float(parts[4]), 2.6, places=3)
        self.assertTrue(parts[5].endswith("audio.wav"))
        ff = next(l for l in lines if l.startswith("ffmpeg"))
        self.assertIn("-i " + parts[5], ff)
        self.assertIn("-map 1:a", ff)
        self.assertNotIn("loudnorm", ff)

    def test_mix_audio_needs_raw(self):
        r = self.run_render("--mix-audio", "/x/short_audio.py", raw=self.edit)
        self.assertEqual(r.returncode, 1)
        self.assertIn("6 audio tracks", r.stderr)

    def test_shorts_py_passes_mix_audio(self):
        manifest = os.path.join(self.tmp.name, "shorts.json")
        with open(manifest, "w") as f:
            json.dump({"recording": self.raw, "words": self.words, "mix_audio": "/x/short_audio.py",
                       "clips": [{"file": "01-x.mp4", "start": 1, "end": 3}]}, f)
        r = subprocess.run([sys.executable, SHORTS, "--dry-run", manifest, "1"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("python3 /x/short_audio.py", r.stdout)


if __name__ == "__main__":
    unittest.main()
