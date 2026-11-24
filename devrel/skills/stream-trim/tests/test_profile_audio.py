"""The audio path (prepare, final render, shorts audio) on profiles other
than ryan-obs. Ryan's own commands are pinned by test_golden."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "scripts")
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)

import audio_chain  # noqa: E402
import measure  # noqa: E402
import prepare  # noqa: E402
import profiles  # noqa: E402
import render  # noqa: E402
from test_measure import make_mp4  # noqa: E402
from test_profiles import two_track  # noqa: E402

PLAIN = os.path.abspath(os.path.join(HERE, "..", "profiles", "chain-plain.json"))


class ProfileAudioTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.config = os.path.join(self.tmp.name, "config")
        os.makedirs(os.path.join(self.config, "profiles"))
        env = mock.patch.dict(os.environ, {"STREAM_TRIM_CONFIG": self.config})
        env.start()
        self.addCleanup(env.stop)
        self.cache = os.path.join(self.tmp.name, "cache")
        patcher = mock.patch.object(prepare, "cache_dir", return_value=self.cache)
        patcher.start()
        self.addCleanup(patcher.stop)

    def add_profile(self, p):
        with open(os.path.join(self.config, "profiles", p["name"] + ".json"), "w") as f:
            json.dump(p, f)
        return profiles.load(p["name"])

    def test_prepare_rejects_track_mismatch(self):
        raw = os.path.join(self.tmp.name, "seven.mp4")
        make_mp4(raw, 7, 3)
        with self.assertRaises(profiles.ProfileError) as cm:
            prepare.prepare(raw, profiles.load("ryan-obs"))
        self.assertIn("has 7 audio tracks", str(cm.exception))
        self.assertFalse(os.path.exists(self.cache))

    def test_render_rejects_track_mismatch(self):
        raw = os.path.join(self.tmp.name, "two.mp4")
        make_mp4(raw, 2, 3)
        with self.assertRaises(profiles.ProfileError):
            render.render_final(raw, 0, 2, profiles.load("ryan-obs"))

    def test_cache_rebuilt_for_other_profile(self):
        raw = os.path.join(self.tmp.name, "six.mp4")
        make_mp4(raw, 6, 4)
        a = prepare.prepare(raw, profiles.load("ryan-obs"))
        self.assertEqual(a["profile"], "ryan-obs")
        other = self.add_profile(two_track(name="six-other", audio_tracks=6))
        with mock.patch.object(prepare.subprocess, "Popen", wraps=prepare.subprocess.Popen) as popen:
            b = prepare.prepare(raw, other)
        self.assertTrue(popen.called)
        self.assertEqual(b["profile"], "six-other")

    def test_legacy_cache_is_ryan(self):
        os.makedirs(self.cache)
        legacy = {"raw": "x", "duration": 4.0, "fps": 23.976, "silences": [], "in": 0, "out": 4}
        with open(os.path.join(self.cache, "analysis.json"), "w") as f:
            json.dump(legacy, f)
        with mock.patch.object(prepare.subprocess, "Popen") as popen:
            self.assertEqual(prepare.prepare("/nowhere.mp4", profiles.load("ryan-obs")), legacy)
        popen.assert_not_called()

    def test_two_track_profile_renders(self):
        raw = os.path.join(self.tmp.name, "two.mp4")
        make_mp4(raw, 2, 8)
        p = self.add_profile(two_track())
        a = prepare.prepare(raw, p)
        self.assertEqual(a["profile"], "test-two")
        out = render.render_final(raw, 1, 7, p)
        dur = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                              "stream=duration", "-of", "csv=p=0", out],
                             capture_output=True, text=True, check=True).stdout.strip()
        self.assertAlmostEqual(float(dur), 6.0, delta=0.03)
        self.assertAlmostEqual(measure.measure(out)["I"], -17, delta=1)

    def test_voice_filters_plain(self):
        with open(PLAIN) as f:
            chain = json.load(f)
        self.assertEqual(audio_chain.voice_filters(chain), "")
        g = audio_chain.build_filtergraph(chain, {"mic": "0:a:0", "theme": "0:a:1"}, 0, {"mic"}, "mic")
        self.assertNotIn(",,", g)
        self.assertIn("amix=inputs=2:normalize=0[mix]", g)

    def test_short_audio_uses_profile(self):
        raw = os.path.join(self.tmp.name, "two.mp4")
        make_mp4(raw, 2, 8)
        self.add_profile(two_track())
        wav = os.path.join(self.tmp.name, "short.wav")
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "short_audio.py"), raw, "1", "4", wav],
                           capture_output=True, text=True,
                           env={**os.environ, "STREAM_TRIM_PROFILE": "test-two"})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertAlmostEqual(measure.measure(wav)["I"], -14, delta=1)


if __name__ == "__main__":
    unittest.main()
