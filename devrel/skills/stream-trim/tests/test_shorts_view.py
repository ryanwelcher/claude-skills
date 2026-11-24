import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import profiles  # noqa: E402
import shorts_view as sv  # noqa: E402

EDIT = {"in": 100, "out": 200}
SHIFT = 0.375


def clip(n, start, end, **extra):
    return {"file": f"{n:02d}-c{n}.mp4", "start": start, "end": end, **extra}


RYAN = profiles.load("ryan-obs")


class ShortsViewTest(unittest.TestCase):
    def test_to_secs_and_fmt(self):
        self.assertAlmostEqual(sv.to_secs("00:41:12.40"), 2472.4)
        self.assertAlmostEqual(sv.to_secs("5:30"), 330.0)
        self.assertEqual(sv.to_secs(12.5), 12.5)
        self.assertEqual(sv.fmt(2472.4), "00:41:12.40")

    def test_inside_counts_padding(self):
        self.assertFalse(sv.inside(clip(1, 100.5, 150), EDIT, SHIFT))
        self.assertTrue(sv.inside(clip(1, 100.6, 150), EDIT, SHIFT))
        self.assertFalse(sv.inside(clip(1, 150, 199.99), EDIT, SHIFT))
        self.assertTrue(sv.inside(clip(1, 150, 199.95), EDIT, SHIFT))
        self.assertEqual(sv.video_span(clip(1, 110, 120), SHIFT), (110 - 0.2 - SHIFT, 120 + 0.4 - SHIFT))

    def test_load_candidates(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "candidates.json")
            with open(p, "w") as f:
                json.dump({"recording": "r", "words": "w",
                           "clips": [clip(1, "00:02:00.00", "00:02:30.00", hook="h"), clip(2, 50, 60)]}, f)
            got = sv.load_candidates(p, EDIT, SHIFT)
            self.assertEqual([c["n"] for c in got], [1, 2])
            self.assertEqual([c["inside"] for c in got], [True, False])
            self.assertAlmostEqual(got[0]["edit_start"], 120 - SHIFT - 100)
            self.assertAlmostEqual(got[0]["edit_end"], 150 - SHIFT - 100)
            for bad in ('{"clips": [', '{"recording": "r"}',
                        json.dumps({"clips": [{"file": "x.mp4", "start": 1, "end": 2}]}),
                        json.dumps({"clips": [{"file": "01-x.mp4", "start": 1}]})):
                with open(p, "w") as f:
                    f.write(bad)
                with self.assertRaises(ValueError):
                    sv.load_candidates(p, EDIT, SHIFT)

    def test_merge_keeps_and_replaces(self):
        existing = {"recording": "old", "words": "w", "clips": [clip(1, 1, 2), clip(2, 3, 4)]}
        new2 = clip(2, 30, 40, hook="new")
        got = sv.merge_picks(existing, "/raw.mp4", "/words.json", "/sa.py", [clip(3, 5, 6), new2], RYAN)
        self.assertEqual([c["file"] for c in got["clips"]], ["01-c1.mp4", "02-c2.mp4", "03-c3.mp4"])
        self.assertEqual(got["clips"][1], new2)
        self.assertEqual((got["recording"], got["words"], got["mix_audio"]), ("/raw.mp4", "/words.json", "/sa.py"))
        bare = sv.merge_picks([clip(1, 1, 2)], "/raw.mp4", "/w", "/sa.py", [clip(2, 3, 4)], RYAN)
        self.assertEqual([c["file"] for c in bare["clips"]], ["01-c1.mp4", "02-c2.mp4"])
        self.assertEqual(sv.merge_picks(None, "/r", "/w", "/s", [clip(1, 1, 2)], RYAN)["clips"], [clip(1, 1, 2)])


if __name__ == "__main__":
    unittest.main()
