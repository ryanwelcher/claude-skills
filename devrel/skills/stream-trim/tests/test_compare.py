import contextlib
import io
import json
import os
import re
import sys
import tempfile
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
sys.path.insert(0, HERE)

import compare  # noqa: E402
from test_measure import make_mp4  # noqa: E402

CHAIN = os.path.join(HERE, "..", "scripts", "chain.json")


class ParseStretchTest(unittest.TestCase):
    def test_parse_stretch(self):
        self.assertEqual(compare.parse_stretch("300:150"), (300.0, 150.0))
        with self.assertRaises(ValueError):
            compare.parse_stretch("5:00")


class CliTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.raw = os.path.join(cls.tmp.name, "raw, 1.mp4")
        cls.ref = os.path.join(cls.tmp.name, "ref  render.mp4")
        make_mp4(cls.raw, 6, 8)
        make_mp4(cls.ref, 1, 8, level=0.05)
        cls.long_raw = os.path.join(cls.tmp.name, "long raw.mp4")
        cls.two = os.path.join(cls.tmp.name, "two.mp4")
        cls.silent = os.path.join(cls.tmp.name, "silent mic.mp4")
        make_mp4(cls.long_raw, 6, 14)
        make_mp4(cls.two, 2, 8)
        make_mp4(cls.silent, 6, 8, tone=False)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def args(self, out, *extra, raw=None):
        return ["--raw", raw or self.raw, "--reference", self.ref, "--offset", "0",
                "--chain", CHAIN, "--out", out, *extra]

    def run_cli(self, argv):
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            code = compare.main(argv)
        return code, err.getvalue()

    def test_reference_too_short_fails_before_work(self):
        out = os.path.join(self.tmp.name, "short-ref")
        code, err = self.run_cli(self.args(out, "6:5", raw=self.long_raw))
        self.assertEqual(code, 1)
        self.assertIn("ERROR: stretch 1 runs past the end of the reference", err)
        self.assertFalse(os.path.exists(out))

    def test_wrong_track_count_leaves_no_folder(self):
        out = os.path.join(self.tmp.name, "two-tracks")
        code, err = self.run_cli(self.args(out, "1:3", raw=self.two))
        self.assertEqual(code, 1)
        self.assertIn("ERROR: this recording has 2 audio tracks; profile ryan-obs expects 6\n", err)
        self.assertFalse(os.path.exists(out))

    def test_silent_mic_refused(self):
        out = os.path.join(self.tmp.name, "silent")
        code, err = self.run_cli(self.args(out, "1:3", raw=self.silent))
        self.assertEqual(code, 1)
        self.assertIn("ERROR: stretch 1: the mic is silent", err)
        self.assertFalse(os.path.exists(out))

    def test_force_keeps_other_files(self):
        out = os.path.join(self.tmp.name, "forced")
        self.assertEqual(self.run_cli(self.args(out, "1:3"))[0], 0)
        with open(os.path.join(out, "notes.md"), "w") as f:
            f.write("round notes")
        self.assertEqual(self.run_cli(self.args(out, "1:3", "--force"))[0], 0)
        self.assertTrue(os.path.exists(os.path.join(out, "notes.md")))

    def test_force_refuses_source_folder(self):
        code, err = self.run_cli(self.args(self.tmp.name, "1:3", "--force"))
        self.assertEqual(code, 1)
        self.assertIn("holds the raw recording or the reference", err)
        self.assertTrue(os.path.exists(self.raw))

    def test_refuses_existing_out(self):
        out = os.path.join(self.tmp.name, "exists")
        os.mkdir(out)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = compare.main(self.args(out, "1:3"))
        self.assertEqual(code, 1)
        self.assertIn(f"ERROR: {out} exists, pass --force to overwrite", err.getvalue())

    def test_ab_page_hides_answer(self):
        out = os.path.join(self.tmp.name, "round")
        self.assertEqual(self.run_cli(self.args(out, "1:3", "4:3"))[0], 0)
        with open(os.path.join(out, "index.html")) as f:
            page = f.read()
        visible = re.sub(r"<script.*?</script>", "", page, flags=re.S)
        visible = re.sub(r"<[^>]+>", "", visible)
        self.assertNotIn("ours-", visible)
        self.assertNotIn("ref-", visible)
        self.assertIn("ours-0.wav", page)
        with open(os.path.join(out, "report.json")) as f:
            report = json.load(f)
        self.assertEqual(len(report["answer"]), 2)
        self.assertTrue(all(a in ("A", "B") for a in report["answer"]))
        for i in range(2):
            self.assertTrue(os.path.exists(os.path.join(out, f"ref-{i}.wav")))
            self.assertTrue(os.path.exists(os.path.join(out, f"ours-{i}.wav")))
        self.assertIn("delta", report["stretches"][0])
        # Each pair is level-matched to the reference so the blind test is fair.
        for st in report["stretches"]:
            self.assertLessEqual(abs(st["delta"]["I"]), 1.0)


if __name__ == "__main__":
    unittest.main()
