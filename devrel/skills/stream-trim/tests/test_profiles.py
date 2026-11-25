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
import profiles  # noqa: E402
from test_measure import make_mp4  # noqa: E402

CHAIN_JSON = os.path.join(SCRIPTS, "chain.json")
PLAIN = os.path.abspath(os.path.join(HERE, "..", "profiles", "chain-plain.json"))
CLI = os.path.join(SCRIPTS, "profiles.py")


def two_track(name="test-two", **over):
    p = {"name": name, "audio_tracks": 2,
         "tracks": {"1": {"role": "mic", "voice": True}, "2": {"role": "theme"}},
         "mic": "1", "mic_lag_frames": 0, "transcript_lag_frames": 0, "chain": PLAIN,
         "shorts_loudness": {"I": -14, "TP": -1.5},
         "caption_font": {"name": "Jost SemiBold", "file": "Jost-SemiBold.ttf"},
         "layouts": None, "voice_pass": None}
    p.update(over)
    return p


class ProfilesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.config = os.path.join(self.tmp.name, "config")
        env = mock.patch.dict(os.environ, {"STREAM_TRIM_CONFIG": self.config})
        env.start()
        self.addCleanup(env.stop)

    def write(self, profile, text=None):
        d = os.path.join(self.config, "profiles")
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, profile["name"] + ".json") if profile else os.path.join(d, "broken.json")
        with open(path, "w") as f:
            f.write(text if text is not None else json.dumps(profile))
        return path

    def set_default(self, name):
        os.makedirs(self.config, exist_ok=True)
        with open(os.path.join(self.config, "default"), "w") as f:
            f.write(name + "\n")

    def test_ryan_obs_values(self):
        p = profiles.load("ryan-obs")
        self.assertEqual(profiles.roles(p), [("mic", 2), ("guest", 3), ("theme", 5), ("firebot", 6)])
        self.assertEqual(profiles.voice_roles(p), {"mic", "guest"})
        self.assertEqual(profiles.mic_index(p), 1)
        self.assertEqual(profiles.mic_shift(p, 24000 / 1001), 0.375375)
        self.assertEqual(profiles.transcript_shift(p, 24000 / 1001), 0.375375)
        self.assertEqual(p["chain"], audio_chain.load_chain(CHAIN_JSON))
        self.assertEqual(os.path.realpath(p["chain_path"]), os.path.realpath(CHAIN_JSON))
        self.assertIsNone(p["layouts_path"])

    def test_no_default(self):
        with self.assertRaises(profiles.NoDefault):
            profiles.load()
        self.assertIsNone(profiles.default_name())

    def test_default_file(self):
        self.set_default("ryan-obs")
        self.assertEqual(profiles.default_name(), "ryan-obs")
        self.assertEqual(profiles.load()["name"], "ryan-obs")

    def test_personal_wins(self):
        self.write(two_track(name="ryan-obs"))
        self.assertEqual(profiles.load("ryan-obs")["audio_tracks"], 2)

    def test_unknown_name(self):
        with self.assertRaises(profiles.ProfileError) as cm:
            profiles.load("nope")
        self.assertIn("nope", str(cm.exception))

    def test_bad_json(self):
        self.write({"name": "broken"}, text='{"name": "broken",')
        with self.assertRaises(profiles.ProfileError) as cm:
            profiles.load("broken")
        self.assertIn("broken.json", str(cm.exception))

    def test_missing_field(self):
        p = two_track()
        del p["mic"]
        self.write(p)
        with self.assertRaises(profiles.ProfileError) as cm:
            profiles.load("test-two")
        self.assertIn('"mic"', str(cm.exception))

    def test_track_out_of_range(self):
        self.write(two_track(tracks={"1": {"role": "mic", "voice": True}, "7": {"role": "theme"}}))
        with self.assertRaises(profiles.ProfileError) as cm:
            profiles.load("test-two")
        self.assertIn("7", str(cm.exception))

    def test_mic_must_be_voice(self):
        self.write(two_track(tracks={"1": {"role": "mic"}, "2": {"role": "theme"}}))
        with self.assertRaises(profiles.ProfileError):
            profiles.load("test-two")

    def test_chain_level_without_role(self):
        chain = os.path.join(self.tmp.name, "chain-typo.json")
        with open(PLAIN) as f:
            c = json.load(f)
        c["levels_db"] = {"cohost": -3}
        with open(chain, "w") as f:
            json.dump(c, f)
        self.write(two_track(chain=chain))
        with self.assertRaises(profiles.ProfileError) as cm:
            profiles.load("test-two")
        self.assertIn("cohost", str(cm.exception))

    def test_relative_paths(self):
        d = os.path.join(self.config, "profiles")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "test-two-layouts.json"), "w") as f:
            f.write("{}")
        self.write(two_track(layouts="test-two-layouts.json"))
        self.assertEqual(profiles.load("test-two")["layouts_path"], os.path.join(d, "test-two-layouts.json"))

    def test_name_matches_file(self):
        p = two_track()
        p["name"] = "ryan-obs"
        os.makedirs(os.path.join(self.config, "profiles"), exist_ok=True)
        with open(os.path.join(self.config, "profiles", "laptop.json"), "w") as f:
            json.dump(p, f)
        with self.assertRaises(profiles.ProfileError) as cm:
            profiles.load("laptop")
        self.assertIn("laptop.json", str(cm.exception))
        self.assertIn('"name"', str(cm.exception))

    def test_wrong_types(self):
        for field, value in (("mic_lag_frames", "9"), ("transcript_lag_frames", None),
                             ("shorts_loudness", -14), ("shorts_loudness", {"I": -14}),
                             ("caption_font", "Jost SemiBold"), ("caption_font", {"name": "Jost"}),
                             ("voice_pass", 3)):
            self.write(two_track(**{field: value}))
            with self.assertRaises(profiles.ProfileError, msg=field) as cm:
                profiles.load("test-two")
            self.assertIn(field, str(cm.exception))

    def test_chain_missing_key(self):
        chain = os.path.join(self.tmp.name, "chain-short.json")
        with open(PLAIN) as f:
            c = json.load(f)
        del c["presence"]
        with open(chain, "w") as f:
            json.dump(c, f)
        self.write(two_track(chain=chain))
        with self.assertRaises(profiles.ProfileError) as cm:
            profiles.load("test-two")
        self.assertIn("presence", str(cm.exception))

    def test_chain_falls_back_to_builtin(self):
        self.write(two_track(chain="chain-plain.json"))
        p = profiles.load("test-two")
        self.assertEqual(p["chain_path"], PLAIN)

    def test_cache_key_follows_content(self):
        a = profiles.load("ryan-obs")
        self.write(two_track(name="ryan-obs", audio_tracks=6))
        b = profiles.load("ryan-obs")
        self.assertNotEqual(profiles.cache_key(a), profiles.cache_key(b))
        os.remove(os.path.join(self.config, "profiles", "ryan-obs.json"))
        self.assertEqual(profiles.cache_key(a), profiles.cache_key(profiles.load("ryan-obs")))

    def test_check_recording(self):
        p = profiles.load("ryan-obs")
        profiles.check_recording(p, 6)
        with self.assertRaises(profiles.ProfileError) as cm:
            profiles.check_recording(p, 7)
        self.assertEqual(str(cm.exception), "this recording has 7 audio tracks; profile ryan-obs expects 6")

    def test_cli_check(self):
        raw = os.path.join(self.tmp.name, "six.mp4")
        make_mp4(raw, 6, 2)
        r = subprocess.run([sys.executable, CLI, "check", raw], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("NO_DEFAULT", r.stderr)
        self.set_default("ryan-obs")
        r = subprocess.run([sys.executable, CLI, "check", raw], capture_output=True, text=True)
        self.assertEqual((r.returncode, r.stdout.strip()), (0, "PROFILE ryan-obs"))
        self.write(two_track())
        r = subprocess.run([sys.executable, CLI, "check", raw, "--profile", "test-two"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("has 6 audio tracks; profile test-two expects 2", r.stderr)

    def test_cli_set_default(self):
        r = subprocess.run([sys.executable, CLI, "set-default", "ryan-obs"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(profiles.default_name(), "ryan-obs")
        r = subprocess.run([sys.executable, CLI, "set-default", "nope"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)

    def test_cli_bad_args(self):
        raw = os.path.join(self.tmp.name, "two.mp4")
        make_mp4(raw, 2, 2)
        for args in (["check", raw, "--profile"], ["samples", raw, self.tmp.name, "--at"],
                     ["samples", raw, self.tmp.name, "--at", "abc"]):
            r = subprocess.run([sys.executable, CLI, *args], capture_output=True, text=True)
            self.assertEqual(r.returncode, 1, args)
            self.assertNotIn("Traceback", r.stderr, args)
            self.assertIn("ERROR:", r.stderr, args)

    def test_cli_samples(self):
        raw = os.path.join(self.tmp.name, "two.mp4")
        make_mp4(raw, 2, 12)
        out = os.path.join(self.tmp.name, "samples")
        r = subprocess.run([sys.executable, CLI, "samples", raw, out, "--at", "2"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        for n in (1, 2):
            wav = os.path.join(out, f"track-{n}.wav")
            self.assertIn(wav, r.stdout)
            self.assertAlmostEqual(audio_chain.probe(wav, video=False)[1], 5.0, delta=0.05)


if __name__ == "__main__":
    unittest.main()
