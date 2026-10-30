#!/usr/bin/env python3
"""Write the captions for one short as an ASS subtitle file.

Usage: make-captions.py <words.json> <start> <end> <out.ass>

<start> and <end> are seconds on the transcript's clock: the same times the
short is cut at. Caption times in the file are relative to <start>, so the
file lines up with the rendered clip.

The look matches the Firecut shorts on the channel: words in groups of up to
MAX_WORDS, all caps, white with a soft navy glow, and each group whips in and
out with a horizontal blur. A group also ends at punctuation or a pause.
"""
import json, sys

MAX_WORDS = 3
PAUSE = 0.5          # seconds of silence that ends a group
HOLD = 0.3           # keep a group on screen this long after its last word
WHIP_IN = 120        # ms for a group to sharpen in
WHIP_OUT = 80        # ms for a group to blur out
# Brand type from the stream overlays (BRB, "Stream ended"). It must be the
# static Jost-SemiBold.ttf: libass ignores the weight axis of the variable
# Jost font and draws its default weight. The white stroke on the Face layer
# thickens it to the ExtraBold look of the Firecut captions.
FONT = "Jost SemiBold"
SIZE = 128
CAPTION_Y = 900      # the seam between the cam band and the screen band

words_path, start, end, out_path = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
words = [w for w in json.load(open(words_path)) if w[0] >= start and w[1] <= end]

def ts(t):
    t = max(0.0, t - start)
    cs = int(round(t * 100))
    return "%d:%02d:%02d.%02d" % (cs // 360000, cs // 6000 % 60, cs // 100 % 60, cs % 100)

def esc(s):
    return s.replace("\\", "").replace("{", "(").replace("}", ")")

groups, group = [], []
for i, w in enumerate(words):
    group.append(w)
    nxt = words[i + 1] if i + 1 < len(words) else None
    if (len(group) == MAX_WORDS or w[2][-1:] in ".,?!" or nxt is None
            or nxt[0] - w[1] >= PAUSE):
        groups.append(group)
        group = []

# libass only blurs evenly, so the whip is faked: the group starts stretched
# wide and blurred, snaps to normal, and stretches and fades on the way out.
def whip(duration_ms, blur):
    out_at = max(WHIP_IN, duration_ms - WHIP_OUT)
    return ("\\fscx135\\blur16\\alpha&H60&"
            "\\t(0,%d,\\fscx100\\blur%d\\alpha&H00&)"
            "\\t(%d,%d,\\fscx135\\blur16\\alpha&HFF&)" % (WHIP_IN, blur, out_at, duration_ms))

events = []
for g, group in enumerate(groups):
    next_start = groups[g + 1][0][0] if g + 1 < len(groups) else end
    g_start, g_end = group[0][0], min(group[-1][1] + HOLD, next_start)
    ms = int(round((g_end - g_start) * 1000))
    text = " ".join(esc(w[2]) for w in group).upper()
    span = "%s,%s" % (ts(g_start), ts(g_end))
    events.append("Dialogue: 0,%s,Glow,,0,0,0,,{\\pos(540,%d)%s}%s" % (span, CAPTION_Y, whip(ms, 10), text))
    events.append("Dialogue: 1,%s,Face,,0,0,0,,{\\pos(540,%d)%s}%s" % (span, CAPTION_Y, whip(ms, 0), text))

with open(out_path, "w", encoding="utf-8") as fh:
    fh.write("""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Glow,{font},{size},&H00552B2D,&H00552B2D,&H40552B2D,&H00000000,0,0,0,0,100,100,0,0,1,12,0,5,40,40,0,1
Style: Face,{font},{size},&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,1,2.5,0,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""".format(font=FONT, size=SIZE))
    fh.write("\n".join(events) + "\n")
