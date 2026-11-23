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
        make_mp4(cls.ref, 1, 8)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def args(self, out, *extra):
        return ["--raw", self.raw, "--reference", self.ref, "--offset", "0",
                "--chain", CHAIN, "--out", out, *extra]

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
        self.assertEqual(compare.main(self.args(out, "1:3", "4:3")), 0)
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


if __name__ == "__main__":
    unittest.main()
