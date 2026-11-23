import array
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
sys.path.insert(0, HERE)

import audio_chain  # noqa: E402
import prepare  # noqa: E402
from test_measure import make_mp4  # noqa: E402

CHAIN = audio_chain.load_chain(os.path.join(HERE, "..", "scripts", "chain.json"))

STDERR = """[silencedetect @ 0x1] silence_start: 0
[silencedetect @ 0x1] silence_end: 300.5 | silence_duration: 300.5
[silencedetect @ 0x1] silence_start: 1000
[silencedetect @ 0x1] silence_end: 1003 | silence_duration: 3
[silencedetect @ 0x1] silence_start: 5300
"""


class PureTest(unittest.TestCase):
    def test_parse_silences(self):
        self.assertEqual(prepare.parse_silences(STDERR, 5400),
                         [(0, 300.5), (1000, 1003), (5300, 5400)])

    def test_defaults_normal(self):
        d = prepare.defaults(prepare.parse_silences(STDERR, 5400), 5400)
        self.assertEqual((d["voice_start"], d["in"], d["voice_end"], d["out"]),
                         (300.5, 300.0, 5300, 5301.0))

    def test_defaults_no_intro(self):
        for silences in ([(0, 30), (5300, 5400)], [(10, 400), (5300, 5400)], []):
            d = prepare.defaults(silences, 5400)
            self.assertEqual((d["voice_start"], d["in"]), (0, 0))

    def test_defaults_no_outro(self):
        d = prepare.defaults([(0, 300.5), (1000, 1003)], 5400)
        self.assertEqual((d["voice_end"], d["out"]), (5400, 5400))
        d = prepare.defaults([(0, 300.5), (5399.6, 5400)], 5400)
        self.assertEqual(d["out"], 5400)

    def test_peaks_from_pcm(self):
        samples = array.array("h", [0] * 2000)
        samples[3 * 50 + 7] = -32768
        peaks = prepare.peaks_from_pcm(samples.tobytes(), 1000, 20)
        self.assertEqual(len(peaks), 40)
        self.assertEqual(peaks[3], 1.0)
        self.assertEqual(peaks[0], 0.0)

    def test_cache_dir_stable(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as f:
            a = prepare.cache_dir(f.name)
            self.assertEqual(a, prepare.cache_dir(f.name))
            self.assertTrue(a.startswith(os.path.expanduser("~/Library/Caches/stream-trim/")))
            st = os.stat(f.name)
            os.utime(f.name, (st.st_atime, st.st_mtime + 10))
            self.assertNotEqual(a, prepare.cache_dir(f.name))


class EndToEndTest(unittest.TestCase):
    def test_prepare_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw = os.path.join(tmp, "raw, stream.mp4")
            make_mp4(raw, 6, 100, tone_from=70, tone_to=90)
            cache = os.path.join(tmp, "cache")
            with mock.patch.object(prepare, "cache_dir", return_value=cache):
                a = prepare.prepare(raw, CHAIN)
                # Tone on the mic track at file time 70.0 to 89.7; the mic is
                # 9 frames (0.375 s) late, so on the video clock it's 69.625
                # to 89.325. In = start - 0.5, Out = end + 1.0.
                self.assertAlmostEqual(a["in"], 69.125, delta=0.1)
                self.assertAlmostEqual(a["out"], 90.325, delta=0.1)
                proxy = os.path.join(cache, "proxy.mp4")
                out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                      "stream=codec_type,height", "-of", "csv=p=0", proxy],
                                     capture_output=True, text=True, check=True).stdout.split()
                self.assertEqual(sorted(x.rstrip(",") for x in out), ["audio", "video,720"])
                with open(os.path.join(cache, "peaks.json")) as f:
                    peaks = json.load(f)
                self.assertEqual(peaks["per_s"], 20)
                self.assertAlmostEqual(len(peaks["peaks"]), 1992, delta=10)
                # The 1 kHz tone (amplitude 0.125 * 0.3) must show up in the
                # waveform: peaks are taken before any downsampling.
                voiced = peaks["peaks"][75 * 20:85 * 20]
                self.assertGreater(max(voiced), 0.02)
                self.assertLess(max(peaks["peaks"][10 * 20:60 * 20]), 0.001)
                t = time.time()
                self.assertEqual(prepare.prepare(raw, CHAIN), a)
                self.assertLess(time.time() - t, 1)


if __name__ == "__main__":
    unittest.main()
