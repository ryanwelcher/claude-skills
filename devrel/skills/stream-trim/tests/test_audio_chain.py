import copy
import os
import re
import sys
import unittest

SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, SCRIPTS)

import audio_chain  # noqa: E402

CHAIN_PATH = os.path.join(SCRIPTS, "chain.json")
# Fixed values for the string tests, so tuning chain.json doesn't break them.
FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixture_chain.json")
INPUTS = {"mic": "0:a:1", "guest": "0:a:2", "theme": "0:a:4", "firebot": "0:a:5"}


def branch(graph, role_input):
    """The filter text of the branch that starts at [role_input]."""
    m = re.search(r"\[" + re.escape(role_input) + r"\]([^;]*)", graph)
    return m.group(1) if m else ""


class VoiceFiltersTest(unittest.TestCase):
    def setUp(self):
        self.chain = audio_chain.load_chain(CHAIN_PATH)

    def test_voice_filters_order(self):
        names = [f.split("=")[0] for f in audio_chain.voice_filters(self.chain).split(",")
                 if "=" in f and not f.startswith(("t=", "w=", "g="))]
        expected = ["highpass", "compand", "deesser"] + ["equalizer"] * len(self.chain["eq_db"])
        self.assertEqual(names, expected)

        chain = copy.deepcopy(self.chain)
        chain["presence"]["db"] = 2
        names = [f.split("=")[0] for f in audio_chain.voice_filters(chain).split(",")]
        self.assertEqual(names[-1], "equalizer")
        self.assertEqual(len([n for n in names if n == "equalizer"]), len(chain["eq_db"]) + 1)

    def test_voice_filters_values(self):
        f = audio_chain.voice_filters(audio_chain.load_chain(FIXTURE_PATH))
        self.assertIn("highpass=f=110", f)
        self.assertIn("attacks=0.002", f)
        self.assertIn("decays=0.05", f)
        self.assertIn("points=-90/-90|-84/-91|-75/-77|-68/-68|-44/-33|0/-1", f)
        self.assertIn("equalizer=f=4000:t=q:w=1.41:g=0.9", f)


class BuildFiltergraphTest(unittest.TestCase):
    def setUp(self):
        self.chain = audio_chain.load_chain(FIXTURE_PATH)

    def test_build_filtergraph_shift_and_mix(self):
        g = audio_chain.build_filtergraph(self.chain, INPUTS, 0.375375)
        voice = audio_chain.voice_filters(self.chain)
        mic, guest = branch(g, "0:a:1"), branch(g, "0:a:2")
        theme, firebot = branch(g, "0:a:4"), branch(g, "0:a:5")
        self.assertIn("atrim=start=0.375375,asetpts=PTS-STARTPTS", mic)
        for other in (guest, theme, firebot):
            self.assertNotIn("atrim", other)
        self.assertIn("volume=1.71dB", mic)
        self.assertIn(voice, mic)
        self.assertIn(voice, guest)
        self.assertNotIn("compand", theme)
        self.assertNotIn("compand", firebot)
        self.assertIn("amix=inputs=4:normalize=0", g)
        self.assertTrue(g.endswith("[mix]"))

    def test_missing_key_raises(self):
        chain = copy.deepcopy(self.chain)
        del chain["compand"]
        with self.assertRaises(KeyError) as cm:
            audio_chain.build_filtergraph(chain, INPUTS, 0.375375)
        self.assertIn("compand", str(cm.exception))

    def test_zero_level_omits_volume(self):
        g = audio_chain.build_filtergraph(self.chain, INPUTS, 0.375375)
        self.assertNotIn("volume=", branch(g, "0:a:4"))
        chain = copy.deepcopy(self.chain)
        chain["levels_db"]["theme"] = -3
        g = audio_chain.build_filtergraph(chain, INPUTS, 0.375375)
        self.assertIn("volume=-3dB", branch(g, "0:a:4"))


if __name__ == "__main__":
    unittest.main()
