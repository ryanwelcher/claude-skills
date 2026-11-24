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

import profiles  # noqa: E402

CHAIN = profiles.load("ryan-obs")  # the profile; the name is kept from before profiles


def streams(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=codec_type,codec_name,codec_tag_string,channels,sample_rate:format=duration",
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


class SnapRangeTest(unittest.TestCase):
    def test_snap_range(self):
        fps, dur = 24000 / 1001, 5706.45
        i, o = render.snap_range(343.83, 5699.66, fps, dur)
        for t, want in ((i, 343.83), (o, 5699.66)):
            self.assertAlmostEqual(t * fps, round(t * fps), places=6)
            self.assertLessEqual(abs(t - want), 0.5 / fps)
        self.assertEqual(render.snap_range(10, dur, fps, dur)[1], dur)


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
        self.assertEqual((video["codec_name"], video.get("codec_tag_string")), ("hevc", "hvc1"))
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


FPS = 24000 / 1001
FLASH = 120  # frame with a white flash; a beep starts at the same instant on the theme track


def make_sync_mp4(path):
    """12 s, 6 tracks. Frames 120-122 are white; track 5 (theme, no voice
    chain) beeps for exactly those frames. Everything else is silent/black."""
    t0, t1 = FLASH / FPS, (FLASH + 3) / FPS
    args = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
            f"color=c=black:s=320x180:r=24000/1001:d=12,"
            f"drawbox=c=white:t=fill:enable='between(n,{FLASH},{FLASH + 2})'"]
    for t in range(1, 7):
        src = (f"sine=f=1000:d=12,volume='between(t,{t0},{t1})':eval=frame,aformat=channel_layouts=stereo"
               if t == 5 else "anullsrc=r=48000:cl=stereo:d=12")
        args += ["-f", "lavfi", "-i", src]
    args += ["-map", "0:v"] + sum((["-map", f"{i}:a"] for i in range(1, 7)), [])
    subprocess.run(args + ["-c:v", "libx264", "-c:a", "pcm_s16le", "-shortest",
                           path.replace(".mp4", ".mov")], check=True)
    return path.replace(".mp4", ".mov")


def flash_minus_beep(path):
    """Seconds from the beep onset to the first white frame in `path`."""
    import re
    err = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", path, "-vf",
                          "signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-an", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    frames = re.findall(r"pts_time:([\d.]+)\s*\n.*?YAVG=([\d.]+)", err)
    flash = next(float(t) for t, y in frames if float(y) > 128)
    err = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", path, "-vn", "-af",
                          "silencedetect=noise=-50dB:d=0.05", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    beep = float(re.findall(r"silence_end: ([\d.]+)", err)[0])
    return flash - beep


class SyncTest(unittest.TestCase):
    def test_off_grid_in_stays_in_sync(self):
        with tempfile.TemporaryDirectory() as tmp:
            offsets = []
            for name, in_frames in (("grid", 72), ("off", 72.6)):
                raw = make_sync_mp4(os.path.join(tmp, f"{name}.mp4"))
                out = render.render_final(raw, in_frames / FPS, 10.0, CHAIN)
                offsets.append(flash_minus_beep(out))
            # The off-grid In must give the same A/V offset as the on-grid one.
            self.assertAlmostEqual(offsets[1], offsets[0], delta=0.005, msg=offsets)
