import copy
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS)

import audio_chain  # noqa: E402
import measure  # noqa: E402
import short_audio  # noqa: E402
from test_measure import make_mp4  # noqa: E402

CLI = os.path.join(SCRIPTS, "short_audio.py")


class ShortAudioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.raw = os.path.join(cls.tmp.name, "raw.mp4")
        make_mp4(cls.raw, 6, 12)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_shorts_chain(self):
        chain = audio_chain.load_chain(os.path.join(SCRIPTS, "chain.json"))
        before = copy.deepcopy(chain)
        out = short_audio.shorts_chain(chain)
        self.assertEqual(out["loudness"]["I"], -14)
        self.assertEqual(out["loudness"]["TP"], -1.5)
        self.assertEqual(out["loudness"]["LRA"], chain["loudness"]["LRA"])
        self.assertEqual(chain, before)

    def test_cli_renders_clip(self):
        wav = os.path.join(self.tmp.name, "out.wav")
        subprocess.run([sys.executable, CLI, self.raw, "2", "4", wav], check=True)
        info = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                               "stream=sample_rate,channels:format=duration", "-of", "csv=p=0", wav],
                              capture_output=True, text=True, check=True).stdout.split()
        rate, channels = info[0].split(",")
        self.assertEqual((rate, channels), ("48000", "2"))
        self.assertAlmostEqual(float(info[1]), 4, delta=0.01)
        self.assertAlmostEqual(measure.measure(wav)["I"], -14, delta=1)

    def test_cli_error(self):
        wav = os.path.join(self.tmp.name, "bad.wav")
        r = subprocess.run([sys.executable, CLI, self.raw, "11", "4", wav], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertTrue(r.stderr.startswith("ERROR:"), r.stderr)


if __name__ == "__main__":
    unittest.main()
