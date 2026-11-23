import os
import subprocess
import sys
import tempfile
import unittest
import wave

SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS)

import audio_chain  # noqa: E402
import measure  # noqa: E402

EBUR128 = """[Parsed_ebur128_0 @ 0x79d7448c00] Summary:

  Integrated loudness:
    I:         -21.1 LUFS
    Threshold: -31.1 LUFS

  Loudness range:
    LRA:        20.0 LU
    Threshold: -41.1 LUFS
    LRA low:   -41.1 LUFS
    LRA high:  -21.1 LUFS

  True peak:
    Peak:      -18.1 dBFS
"""

LOUDNORM = """[Parsed_loudnorm_0 @ 0x1]
{
	"input_i" : "-21.05",
	"input_tp" : "-18.06",
	"input_lra" : "0.00",
	"input_thresh" : "-31.05",
	"output_i" : "-13.95",
	"output_tp" : "-10.97",
	"output_lra" : "0.00",
	"output_thresh" : "-23.95",
	"normalization_type" : "dynamic",
	"target_offset" : "-0.05"
}
[out#0/null @ 0x2] video:0KiB audio:1125KiB
"""


def make_mp4(path, tracks, seconds):
    """Black video plus `tracks` audio tracks. Track 2 is a 1 kHz sine with
    pauses (so it reads as speech-like for loudness gating); the rest are
    silent."""
    args = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "lavfi", "-i", f"color=c=black:s=320x180:r=24000/1001:d={seconds}"]
    for t in range(1, tracks + 1):
        if t == 2:
            src = (f"sine=f=1000:d={seconds},volume='if(lt(mod(t,1),0.7),0.3,0)':eval=frame,"
                   "aformat=channel_layouts=stereo")
        else:
            src = f"anullsrc=r=48000:cl=stereo:d={seconds}"
        args += ["-f", "lavfi", "-i", src]
    args += ["-map", "0:v"] + sum((["-map", f"{i}:a"] for i in range(1, tracks + 1)), [])
    args += ["-c:v", "libx264", "-c:a", "aac", "-shortest", path]
    subprocess.run(args, check=True)


class ParseTest(unittest.TestCase):
    def test_parse_ebur128(self):
        self.assertEqual(measure.parse_ebur128(EBUR128), {"I": -21.1, "LRA": 20.0, "TP": -18.1})

    def test_parse_loudnorm(self):
        d = measure.parse_loudnorm(LOUDNORM)
        self.assertEqual(d["input_i"], "-21.05")
        self.assertEqual(d["target_offset"], "-0.05")


class RenderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.two = os.path.join(cls.tmp.name, "two tracks, x.mp4")
        cls.six = os.path.join(cls.tmp.name, "six  tracks, x.mp4")
        make_mp4(cls.two, 2, 10)
        make_mp4(cls.six, 6, 10)
        cls.chain = audio_chain.load_chain(os.path.join(SCRIPTS, "chain.json"))
        cls.out = os.path.join(cls.tmp.name, "out.wav")
        audio_chain.render_stretch(cls.six, 2, 5, cls.chain, cls.out)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_render_stretch_rejects_wrong_track_count(self):
        with self.assertRaises(ValueError) as cm:
            audio_chain.render_stretch(self.two, 2, 5, self.chain, os.path.join(self.tmp.name, "x.wav"))
        self.assertEqual(str(cm.exception), "expected 6 audio tracks, found 2")

    def test_render_stretch_rejects_out_of_range(self):
        with self.assertRaises(ValueError) as cm:
            audio_chain.render_stretch(self.six, 8, 5, self.chain, os.path.join(self.tmp.name, "y.wav"))
        self.assertIn("past the end", str(cm.exception))

    def test_render_stretch_sine_roundtrip(self):
        with wave.open(self.out) as w:
            self.assertEqual(w.getframerate(), 48000)
            self.assertEqual(w.getnchannels(), 2)
            self.assertAlmostEqual(w.getnframes() / 48000, 5, delta=0.05)
        self.assertAlmostEqual(measure.measure(self.out)["I"], self.chain["loudness"]["I"], delta=1.5)

    def test_measure_bands_peak_at_1k(self):
        bands = measure.measure(self.out)["bands"]
        self.assertEqual(sorted(bands), measure.BANDS)
        self.assertEqual(max(bands, key=bands.get), 1000)


if __name__ == "__main__":
    unittest.main()
