"""Every ffmpeg command stream-trim builds for Ryan's setup, recorded before
profiles existed (GOLDEN_WRITE=1 wrote golden/ryan-obs-commands.json once).
Profiles must not change a single character of them."""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "scripts")
SHORTS_SCRIPTS = os.path.join(HERE, "..", "..", "stream-shorts", "scripts")
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)

import audio_chain  # noqa: E402
import measure  # noqa: E402
import prepare  # noqa: E402
import render  # noqa: E402
import short_audio  # noqa: E402
import shorts_view  # noqa: E402
from test_measure import make_mp4  # noqa: E402

GOLDEN = os.path.join(HERE, "golden", "ryan-obs-commands.json")
NOV12 = (6, 5706.45075, 23.976023976023978)  # audio_chain.probe() of the Nov 12 raw
RAW = "/rec/Nov 12/2026-11-12 10-24-27.mp4"
LOUDNORM = """[Parsed_loudnorm_0 @ 0x0]
{
	"input_i" : "-20.10",
	"input_tp" : "-3.20",
	"input_lra" : "9.80",
	"input_thresh" : "-30.50",
	"output_i" : "-17.00",
	"output_tp" : "-1.00",
	"output_lra" : "8.00",
	"output_thresh" : "-27.40",
	"normalization_type" : "dynamic",
	"target_offset" : "0.40"
}
"""


class Stop(Exception):
    pass


def chain():
    return audio_chain.load_chain(os.path.join(SCRIPTS, "chain.json"))


def python_commands(tmp):
    got = {}

    def popen(cmd, *a, **k):
        got["prepare"] = cmd
        raise Stop()

    with mock.patch.object(audio_chain, "probe", return_value=NOV12), \
            mock.patch.object(prepare, "cache_dir", return_value=os.path.join(tmp, "cache")), \
            mock.patch.object(prepare.subprocess, "Popen", side_effect=popen):
        try:
            prepare.prepare(RAW, chain())
        except Stop:
            pass

    runs = []

    def run(args, *a, **k):
        runs.append(args)
        return LOUDNORM

    with mock.patch.object(audio_chain, "probe", return_value=NOV12), \
            mock.patch.object(render, "_run", side_effect=run):
        try:
            render.render_final(RAW, 344.59425, 5699.527166666666, chain())
        except FileNotFoundError:
            pass  # os.replace of the partial file that was never written
    got["final_pass1"], got["final_pass2"] = runs

    runs.clear()
    with mock.patch.object(audio_chain, "probe", return_value=NOV12), \
            mock.patch.object(measure, "run_ffmpeg", side_effect=run):
        audio_chain.render_stretch(RAW, 463.0, 50.72, short_audio.shorts_chain(chain()), "/out/a.wav")
    got["stretch_pass1"], got["stretch_pass2"] = runs
    return {k: [s.replace(os.path.join(tmp, "cache"), "<CACHE>") for s in v] for k, v in got.items()}


def shell_commands(tmp):
    raw = os.path.join(tmp, "raw.mp4")
    make_mp4(raw, 6, 6)
    words = os.path.join(tmp, "words.json")
    with open(words, "w") as f:
        json.dump([[1.0, 1.4, "hello"], [1.5, 2.0, "world"]], f)
    out = os.path.join(tmp, "01-x.mp4")
    render_short = os.path.join(SHORTS_SCRIPTS, "render-short.sh")
    got = {}
    for name, flags in (("short_default", []), ("short_mix", ["--mix-audio", "/x/short_audio.py"]),
                        ("short_draft", ["--draft"]), ("short_preview", ["--preview"])):
        r = subprocess.run(["bash", render_short, "--dry-run", *flags, raw, words, "1", "3", out],
                           capture_output=True, text=True, check=True)
        got[name] = r.stdout
    manifest = os.path.join(tmp, "shorts.json")
    with open(manifest, "w") as f:
        json.dump(shorts_view.merge_picks(None, raw, words, "/x/short_audio.py",
                                          [{"file": "01-x.mp4", "start": "00:00:01.00", "end": "00:00:03.00"}]), f)
    r = subprocess.run([sys.executable, os.path.join(SHORTS_SCRIPTS, "shorts.py"), "--dry-run", manifest, "1"],
                       capture_output=True, text=True, check=True)
    got["shorts_py"] = r.stdout
    return {k: normalize(v, raw, words, tmp) for k, v in got.items()}


def normalize(text, raw, words, tmp):
    text = text.replace("\\", "")  # printf %q escaping in dry runs
    for real, label in ((raw, "<RAW>"), (words, "<WORDS>"), (tmp, "<DIR>")):
        text = text.replace(real, label).replace(os.path.realpath(real), label)
    return re.sub(r"(?:/[\w.-]+)+?/tmp\.\w+", "<TMP>", text)


def capture():
    with tempfile.TemporaryDirectory() as tmp:
        got = python_commands(tmp)
    with tempfile.TemporaryDirectory() as tmp:
        got.update(shell_commands(tmp))
    return got


class GoldenTest(unittest.TestCase):
    def test_ryan_obs_commands_unchanged(self):
        got = capture()
        if os.environ.get("GOLDEN_WRITE"):
            os.makedirs(os.path.dirname(GOLDEN), exist_ok=True)
            with open(GOLDEN, "w") as f:
                json.dump(got, f, indent=1, sort_keys=True)
        with open(GOLDEN) as f:
            want = json.load(f)
        self.assertEqual(sorted(got), sorted(want))
        for k in want:
            self.assertEqual(got[k], want[k], k)


if __name__ == "__main__":
    unittest.main()
