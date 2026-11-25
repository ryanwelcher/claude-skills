"""The transcript window: chapters for an edit of the recording (stream-trim's
In/Out) from the recording's cached transcript, with In as 00:00.

fixture.srt: speech 5-200 s, no speech to 320 s, "thanks for watching" looped
320-390 s, speech 400-600 s. fixture-condensed-120.txt and fixture-quality.txt
are the output from before the window existed."""
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "scripts")
SRT = os.path.join(HERE, "fixture.srt")


def run(script, *args, env=None):
    r = subprocess.run([sys.executable if script.endswith(".py") else "bash", os.path.join(SCRIPTS, script), *args],
                       capture_output=True, text=True, env=env)
    return r


def fixture(name):
    with open(os.path.join(HERE, name)) as f:
        return f.read()


class WindowTest(unittest.TestCase):
    def test_no_window_unchanged(self):
        self.assertEqual(run("condense.py", SRT, "120").stdout, fixture("fixture-condensed-120.txt"))
        self.assertEqual(run("check-transcript.py", SRT, "600").stdout, fixture("fixture-quality.txt"))

    def test_window_condense(self):
        lines = run("condense.py", SRT, "120", "--window", "300.25", "560").stdout.splitlines()
        self.assertTrue(lines[0].startswith("[00:00:00] thanks for watching"), lines[0])
        self.assertTrue(any(l.startswith("[00:02:00] more at 420") for l in lines), lines)
        text = " ".join(lines)
        self.assertNotIn("talk at", text)
        self.assertIn("more at 550", text)
        self.assertNotIn("more at 560", text)

    def test_window_quality(self):
        out = run("check-transcript.py", SRT, "600", "--window", "300.25", "560").stdout
        # The 20 s of silence left before the loop is too short to flag.
        self.assertEqual(out.splitlines(), ["COVERAGE: 73%", 'SUSPECT: 00:00:20-00:01:30 repeated "thanks for watching"'])

    def test_window_clips_a_gap(self):
        out = run("check-transcript.py", SRT, "600", "--window", "150", "450").stdout.splitlines()
        self.assertEqual(out[1:], ["SUSPECT: 00:00:49-00:02:50 no speech",
                                   'SUSPECT: 00:02:50-00:04:00 repeated "thanks for watching"'])

    def test_print_dir(self):
        """TRANSCRIBE_PRINT_DIR prints the cache folder a run would use, so
        stream-trim can show progress, and creates nothing."""
        with tempfile.TemporaryDirectory() as tmp:
            media = os.path.join(tmp, "rec.mp4")
            with open(media, "w") as f:
                f.write("not media")
            env = {**os.environ, "STREAM_TRANSCRIPT_CACHE": os.path.join(tmp, "cache"), "TRANSCRIBE_WAIT": "30"}
            r = run("transcribe-file.sh", media, "60", env={**env, "TRANSCRIBE_PRINT_DIR": "1"})
            self.assertEqual(r.returncode, 0, r.stderr)
            printed = re.fullmatch(r"DIR: (.+)\n", r.stdout).group(1)
            self.assertFalse(os.path.exists(os.path.join(tmp, "cache")))
            first = run("transcribe-file.sh", media, env=env)
            self.assertEqual(re.search(r"\(cache: (.+?)\)", first.stderr).group(1), printed)

    def test_transcribe_file_window(self):
        """transcribe-file.sh passes TRANSCRIPT_WINDOW on, and keeps the
        windowed files apart from the whole-recording ones."""
        with tempfile.TemporaryDirectory() as tmp:
            media = os.path.join(tmp, "rec.mp4")
            with open(media, "w") as f:
                f.write("not media")
            env = {**os.environ, "STREAM_TRANSCRIPT_CACHE": os.path.join(tmp, "cache"), "TRANSCRIBE_WAIT": "30"}
            first = run("transcribe-file.sh", media, env=env)  # the worker fails on the fake file
            cache = re.search(r"\(cache: (.+?)\)", first.stderr).group(1)
            with open(SRT) as src, open(os.path.join(cache, "audio.srt"), "w") as dst:
                dst.write(src.read())
            open(os.path.join(cache, "done"), "w").close()
            whole = run("transcribe-file.sh", media, env=env)
            self.assertEqual(whole.returncode, 0, whole.stderr)
            win = run("transcribe-file.sh", media, env={**env, "TRANSCRIPT_WINDOW": "300.25 560"})
            self.assertEqual(win.returncode, 0, win.stderr)
            path = re.search(r"CONDENSED: (.+)", win.stdout).group(1)
            with open(path) as f:
                self.assertTrue(f.read().startswith("[00:00:00] thanks for watching"))
            self.assertIn("COVERAGE: 73%", win.stdout)
            path = re.search(r"CONDENSED: (.+)", whole.stdout).group(1)
            with open(path) as f:
                self.assertEqual(f.read(), fixture("fixture-condensed-120.txt"))
            bad = run("transcribe-file.sh", media, env={**env, "TRANSCRIPT_WINDOW": "560 300"})
            self.assertEqual(bad.returncode, 1)
            self.assertIn("ERROR:", bad.stderr)


if __name__ == "__main__":
    unittest.main()
