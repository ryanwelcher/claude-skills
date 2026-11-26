import os
import re
import unittest

SKILL = os.path.join(os.path.dirname(__file__), "..", "SKILL.md")


class SkillDocTest(unittest.TestCase):
    def setUp(self):
        with open(SKILL, encoding="utf-8") as f:
            self.doc = f.read()

    def step(self, n):
        return re.search(rf"^{n}\. \*\*.*?(?=^\d+\. \*\*|^## )", self.doc, re.S | re.M).group(0)

    def test_shorts_thumbnails_dont_wait(self):
        # Step 8 makes and posts the shorts' thumbnails only; waiting there would hold up step 9.
        s8 = self.step(8)
        self.assertIn("steps 1 to 4", s8)
        self.assertIn("don't wait", s8)

    def test_requests_loop_after_final(self):
        s9 = self.step(9)
        self.assertIn("step 6", s9)
        self.assertIn("once more", self.doc)


    def test_thumbnails_only_entry(self):
        self.assertIn("Thumbnails only", self.doc)
        self.assertIn("/api/titles", self.doc[self.doc.index("Thumbnails only"):])

    def test_vidiq_results_go_through_fit(self):
        self.assertIn("thumbs.py fit", self.doc)
        self.assertNotIn("download its `imageUrl` with curl to `<stem>-<k>-vidiq.jpg`", self.doc)

    def test_other_brands_flagged(self):
        self.assertIn("no other company's characters or packaging", self.doc)
