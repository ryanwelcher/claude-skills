#!/usr/bin/env python3
"""Turn a layout from layouts.json into an ffmpeg filter and a caption height.

Usage: layout.py <name> [pan_x]

Prints two lines:
  the filter chain, from [0:v] to an unlabelled 1080x1920 output
  the caption y, in 1080x1920 pixels

A layout is a stack of bands, top to bottom. Each band crops a box from the
source, given in 1920x1080 pixels and scaled to the recording's real size, and
scales it to 1080 wide by its height. Heights add up to 1920. One band may have
a "pan" range: pan_x replaces that band's crop x, so a clip can slide the crop
toward what's being talked about.

If SHORTS_LAYOUTS names a JSON file of the same shape, its layouts are added
to (and override) the built-in ones. shorts.py points it at a layouts.json
next to shorts.json, so a one-off scene doesn't need a plugin change.
"""
import json, os, sys

LAYOUTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "layouts.json")

def fail(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)

if len(sys.argv) not in (2, 3):
    fail("usage: layout.py <name> [pan_x]")

data = json.load(open(LAYOUTS))
extra = os.environ.get("SHORTS_LAYOUTS")
if extra and os.path.exists(extra):
    try:
        more = json.load(open(extra))
    except ValueError as err:
        fail("%s: %s" % (extra, err))
    data["layouts"].update(more.get("layouts", {}))
    data["default"] = more.get("default", data["default"])
name = sys.argv[1] or data["default"]
if name not in data["layouts"]:
    fail("unknown layout '%s'. Known: %s" % (name, ", ".join(sorted(data["layouts"]))))
layout = data["layouts"][name]
pan_x = int(float(sys.argv[2])) if len(sys.argv) == 3 and sys.argv[2] != "" else None

bands = layout["bands"]
if sum(b["height"] for b in bands) != 1920:
    fail("layout '%s': band heights add up to %d, not 1920" % (name, sum(b["height"] for b in bands)))

chains = []
for i, b in enumerate(bands):
    w, h, x, y = b["crop"]
    if "pan" in b and pan_x is not None:
        lo, hi = b["pan"]
        if not lo <= pan_x <= hi:
            fail("layout '%s': pan_x %d is outside %d-%d" % (name, pan_x, lo, hi))
        x = pan_x
    if x < 0 or y < 0 or x + w > 1920 or y + h > 1080:
        fail("layout '%s': band '%s' crop runs off the 1920x1080 frame" % (name, b["name"]))
    # A crop that isn't the band's shape gets stretched.
    if abs((w / h) / (1080 / b["height"]) - 1) > 0.02:
        fail("layout '%s': band '%s' crop %dx%d doesn't match its 1080x%d shape"
             % (name, b["name"], w, h, b["height"]))
    src = "[0:v]" if len(bands) == 1 else "[b%d]" % i
    dst = "" if len(bands) == 1 else "[o%d]" % i
    chains.append("%scrop=iw*%d/1920:ih*%d/1080:iw*%d/1920:ih*%d/1080,scale=1080:%d%s"
                  % (src, w, h, x, y, b["height"], dst))

if len(bands) == 1:
    print(chains[0])
else:
    split = "[0:v]split=%d%s" % (len(bands), "".join("[b%d]" % i for i in range(len(bands))))
    stack = "%svstack=inputs=%d" % ("".join("[o%d]" % i for i in range(len(bands))), len(bands))
    print(";".join([split] + chains + [stack]))
print(layout["caption_y"])
