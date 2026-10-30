#!/usr/bin/env python3
"""Write word-by-word "pop" captions for one short as an ASS subtitle file.

Usage: make-captions.py <words.json> <start> <end> <out.ass>

<start> and <end> are seconds on the transcript's clock: the same times the
short is cut at. Caption times in the file are relative to <start>, so the
file lines up with the rendered clip.

Words are shown in groups of up to MAX_WORDS. A group also ends at
punctuation or a pause. While a word is being said it turns ACTIVE colour.
"""
import json, sys

MAX_WORDS = 3
PAUSE = 0.5          # seconds of silence that ends a group
HOLD = 0.3           # keep a group on screen this long after its last word
FONT = "Helvetica Neue"
SIZE = 84
WHITE = "&HFFFFFF&"
ACTIVE = "&H4F6BF2&"  # the orange of "Codes" in the stream wordmark (BGR)
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

events = []
for g, group in enumerate(groups):
    next_start = groups[g + 1][0][0] if g + 1 < len(groups) else end
    group_end = min(group[-1][1] + HOLD, next_start)
    for k, w in enumerate(group):
        # Each word's event runs until the next word starts, so the line never
        # blinks off between words.
        w_end = group[k + 1][0] if k + 1 < len(group) else group_end
        text = " ".join(
            ("{\\c%s}%s{\\c%s}" % (ACTIVE, esc(x[2]), WHITE)) if j == k else esc(x[2])
            for j, x in enumerate(group))
        events.append("Dialogue: 0,%s,%s,Pop,,0,0,0,,{\\pos(540,%d)}%s" % (ts(w[0]), ts(w_end), CAPTION_Y, text))

with open(out_path, "w", encoding="utf-8") as fh:
    fh.write("""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Pop,%s,%d,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,7,2,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" % (FONT, SIZE))
    fh.write("\n".join(events) + "\n")
