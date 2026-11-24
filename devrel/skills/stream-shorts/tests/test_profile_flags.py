import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

from test_mix_audio import FONT, LIBASS, RENDER, SCRIPTS, SHORTS, make_mp4

LAYOUT = os.path.join(SCRIPTS, "layout.py")
CAPTIONS = os.path.join(SCRIPTS, "make-captions.py")
LAG = 9 * 1001 / 24000


def band_layout(x):
    return {"bands": [{"name": "cam", "crop": [1080, 960, 0, 0], "height": 960},
                      {"name": "screen", "crop": [1080, 960, x, 0], "height": 960}], "caption_y": 960}


@unittest.skipUnless(FONT and LIBASS, "needs the Jost font and an ffmpeg with libass")
class ProfileFlagsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        d = cls.tmp.name
        cls.six = os.path.join(d, "six.mp4")
        cls.two = os.path.join(d, "two.mp4")
        make_mp4(cls.six, 6, 6)
        make_mp4(cls.two, 2, 6)
        cls.words = os.path.join(d, "words.json")
        with open(cls.words, "w") as f:
            json.dump([[1.0, 1.4, "hello"], [1.5, 2.0, "world"]], f)
        cls.out = os.path.join(d, "01-x.mp4")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def dry(self, raw, *flags):
        r = subprocess.run(["bash", RENDER, "--dry-run", *flags, raw, self.words, "1", "3", self.out],
                           capture_output=True, text=True)
        r.stdout = r.stdout.replace("\\", "")
        return r

    def ss_inputs(self, text):
        """(seek, input) pairs of the ffmpeg line."""
        ff = next(l for l in text.splitlines() if l.startswith("ffmpeg"))
        return [float(s) for s in re.findall(r"-ss (\S+) -t \S+ -i ", ff)], ff

    def test_two_track_dry_run(self):
        r = self.dry(self.two, "--mic-track", "1", "--mic-lag-frames", "0", "--transcript-lag-frames", "0")
        self.assertEqual(r.returncode, 0, r.stderr)
        seeks, ff = self.ss_inputs(r.stdout)
        self.assertIn("[1:a:0]loudnorm", ff)
        self.assertEqual(len(seeks), 2)
        for s in seeks:
            self.assertAlmostEqual(s, 0.8, places=5)

    def test_mic_lag_differs(self):
        r = self.dry(self.six, "--mic-track", "2", "--mic-lag-frames", "9", "--transcript-lag-frames", "0")
        self.assertEqual(r.returncode, 0, r.stderr)
        seeks, ff = self.ss_inputs(r.stdout)
        self.assertIn("[1:a:1]loudnorm", ff)
        self.assertAlmostEqual(seeks[0], 0.8, places=5)
        self.assertAlmostEqual(seeks[1], 0.8 + LAG, places=5)

    def test_font_file_missing(self):
        r = self.dry(self.six, "--font-name", "Inter Bold", "--font-file", "NoSuch-Font-Here.ttf")
        self.assertEqual(r.returncode, 1)
        self.assertIn("NoSuch-Font-Here.ttf", r.stderr)

    def test_font_name_reaches_captions(self):
        r = self.dry(self.six, "--font-name", "Inter Bold", "--font-file", "Jost-SemiBold.ttf")
        self.assertEqual(r.returncode, 0, r.stderr)
        ass = re.search(r"ass=(\S+?/captions\.ass)", r.stdout).group(1)
        with open(ass) as f:
            self.assertIn(",Inter Bold,", f.read())

    def test_make_captions_font(self):
        ass = os.path.join(self.tmp.name, "c.ass")
        for flags, font in ((["--font", "Inter Bold"], "Inter Bold"), ([], "Jost SemiBold")):
            r = subprocess.run([sys.executable, CAPTIONS, *flags, self.words, "0.8", "2.4", ass],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            with open(ass) as f:
                self.assertIn("," + font + ",", f.read())

    def test_layouts_files_in_order(self):
        a, b = (os.path.join(self.tmp.name, n) for n in ("a.json", "b.json"))
        with open(a, "w") as f:
            json.dump({"default": "cam-a", "layouts": {"cam": band_layout(100), "cam-a": band_layout(300)}}, f)
        with open(b, "w") as f:
            json.dump({"default": "cam", "layouts": {"cam": band_layout(200)}}, f)
        env = {**os.environ, "SHORTS_LAYOUTS": os.pathsep.join([a, b])}
        r = subprocess.run([sys.executable, LAYOUT, ""], capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("iw*200/1920", r.stdout)
        r = subprocess.run([sys.executable, LAYOUT, "cam-a"], capture_output=True, text=True, env=env)
        self.assertIn("iw*300/1920", r.stdout)

    def test_shorts_py_passes_profile(self):
        d = os.path.join(self.tmp.name, "rec")
        os.makedirs(d, exist_ok=True)
        prof_layouts = os.path.join(self.tmp.name, "teammate-layouts.json")
        with open(prof_layouts, "w") as f:
            json.dump({"default": "mine", "layouts": {"mine": band_layout(400)}}, f)
        manifest = os.path.join(d, "shorts.json")
        with open(manifest, "w") as f:
            json.dump({"recording": self.two, "words": self.words, "mic_track": 1,
                       "mic_lag_frames": 0, "transcript_lag_frames": 0,
                       "caption_font": {"name": "Inter Bold", "file": "Jost-SemiBold.ttf"},
                       "layouts": prof_layouts,
                       "clips": [{"file": "01-x.mp4", "start": 1, "end": 3}]}, f)
        for mode in ([], ["--draft"], ["--preview"]):
            r = subprocess.run([sys.executable, SHORTS, *mode, "--dry-run", manifest, "1"],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            out = r.stdout.replace("\\", "")
            self.assertIn("iw*400/1920", out, mode)
            if mode != ["--preview"]:
                self.assertIn("[1:a:0]loudnorm", out, mode)
        # A per-recording layouts.json still wins over the profile's file.
        with open(os.path.join(d, "layouts.json"), "w") as f:
            json.dump({"layouts": {"mine": band_layout(500)}}, f)
        r = subprocess.run([sys.executable, SHORTS, "--dry-run", manifest, "1"], capture_output=True, text=True)
        self.assertIn("iw*500/1920", r.stdout.replace("\\", ""))

    def test_shorts_py_exports_profile(self):
        d = os.path.join(self.tmp.name, "rec2")
        os.makedirs(d, exist_ok=True)
        seen = os.path.join(d, "seen.txt")
        stub = os.path.join(d, "stub_audio.py")
        with open(stub, "w") as f:
            f.write("import os, sys\nopen(%r, 'w').write(os.environ.get('STREAM_TRIM_PROFILE', '-'))\nsys.exit(1)\n" % seen)
        manifest = os.path.join(d, "shorts.json")
        with open(manifest, "w") as f:
            json.dump({"recording": self.two, "words": self.words, "mix_audio": stub, "profile": "laptop",
                       "mic_track": 1, "clips": [{"file": "01-x.mp4", "start": 1, "end": 3}]}, f)
        env = {k: v for k, v in os.environ.items() if k != "STREAM_TRIM_PROFILE"}
        subprocess.run([sys.executable, SHORTS, manifest, "1"], capture_output=True, text=True, env=env)
        with open(seen) as f:
            self.assertEqual(f.read(), "laptop")

    def test_mix_audio_with_profile_flags(self):
        r = self.dry(self.two, "--mic-track", "1", "--mic-lag-frames", "0", "--transcript-lag-frames", "0",
                     "--mix-audio", "/x/short_audio.py")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("python3 /x/short_audio.py", r.stdout)


if __name__ == "__main__":
    unittest.main()
