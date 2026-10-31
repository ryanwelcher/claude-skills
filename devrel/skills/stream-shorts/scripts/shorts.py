#!/usr/bin/env python3
"""Render, preview, or print captions for clips listed in a shorts.json.

Usage: shorts.py [--preview | --captions] [--dry-run] <shorts.json> [CLIP ...]

CLIP is a clip's number (the NN- prefix of its file) or "all" (the default).
Outputs go next to shorts.json: <file> for a render, <file>.jpg for a preview.

shorts.json:
  {
    "recording": "/path/to/stream.mp4",
    "words": "/path/to/words.json",
    "clips": [
      {"file": "01-why-the-block-never-rerenders.mp4",
       "start": "00:41:12.40", "end": "00:41:55.10", "hook": "...",
       "layout": "coding-rebrand", "pan_x": 200,
       "fixes": {"use block props": "useBlockProps"},
       "skip": "BRB scene was live"}
    ]
  }

Only file, start and end are required. A clip with "skip" set is left out
unless it's asked for by number. "screen_x" is the old name for "pan_x".
A layouts.json next to shorts.json adds layouts for this recording only.
"""
import json, os, subprocess, sys

RENDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render-short.sh")

def fail(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)

args = sys.argv[1:]
mode = None
dry = False
while args and args[0].startswith("--"):
    flag = args.pop(0)
    if flag in ("--preview", "--captions"):
        mode = flag
    elif flag == "--dry-run":
        dry = True
    else:
        fail("unknown option " + flag)
if not args:
    fail("usage: shorts.py [--preview | --captions] [--dry-run] <shorts.json> [CLIP ...]")

manifest_path = os.path.abspath(args.pop(0))
picks = args or ["all"]
try:
    manifest = json.load(open(manifest_path))
except (OSError, ValueError) as err:
    fail("can't read %s: %s" % (manifest_path, err))
if not isinstance(manifest, dict) or "clips" not in manifest:
    fail("%s needs {\"recording\", \"words\", \"clips\"} at the top level" % manifest_path)
for key in ("recording", "words"):
    if not manifest.get(key):
        fail("%s has no \"%s\"" % (manifest_path, key))
out_dir = os.path.dirname(manifest_path)
os.environ["SHORTS_LAYOUTS"] = os.path.join(out_dir, "layouts.json")

def number(clip):
    head = clip["file"].split("-", 1)[0]
    return int(head) if head.isdigit() else None

clips = manifest["clips"]
if picks == ["all"]:
    chosen = [c for c in clips if not c.get("skip")]
else:
    chosen = []
    for p in picks:
        match = [c for c in clips if p.isdigit() and number(c) == int(p)]
        if not match:
            fail("no clip numbered %s in %s" % (p, manifest_path))
        chosen += match

failed = []
for clip in chosen:
    for key in ("file", "start", "end"):
        if key not in clip:
            fail("a clip has no \"%s\": %s" % (key, json.dumps(clip)))
    out = os.path.join(out_dir, clip["file"])
    if mode == "--preview":
        out = os.path.splitext(out)[0] + ".jpg"
    cmd = ["bash", RENDER]
    if mode:
        cmd.append(mode)
    if dry:
        cmd.append("--dry-run")
    if clip.get("layout"):
        cmd += ["--layout", clip["layout"]]
    pan = clip.get("pan_x", clip.get("screen_x"))
    if pan is not None:
        cmd += ["--pan-x", str(pan)]
    if clip.get("fixes"):
        cmd += ["--fixes", json.dumps(clip["fixes"])]
    cmd += [manifest["recording"], manifest["words"], str(clip["start"]), str(clip["end"]), out]

    if mode == "--captions":
        print("== %s" % clip["file"])
    sys.stdout.flush()
    if subprocess.call(cmd) != 0:
        failed.append(clip["file"])

if failed:
    fail("failed: " + ", ".join(failed))
