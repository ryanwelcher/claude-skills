#!/usr/bin/env python3
"""Write the captions for one short as an ASS subtitle file.

Usage: make-captions.py [--caption-y Y] [--fixes JSON] [--text] <words.json> <start> <end> <out.ass>

<start> and <end> are seconds on the transcript's clock: the same times the
short is cut at. Caption times in the file are relative to <start>, so the
file lines up with the rendered clip.

--caption-y Y   height of the captions in the 1080x1920 frame (the layout's
                caption_y; default 900).
--fixes JSON    a JSON object of {"heard": "meant"} phrase fixes for this clip,
                on top of glossary.json. Matching ignores case and punctuation.
--text          print the caption groups as text, one per line, instead of
                writing the .ass file (pass - as <out.ass>).

The look matches the Firecut shorts on the channel: words in groups of up to
MAX_WORDS, all caps, white with a soft navy glow, and each group whips in and
out with a horizontal blur. A group also ends at punctuation or a pause.
"""
import argparse, json, os, re, sys

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
GLOSSARY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "glossary.json")

ap = argparse.ArgumentParser()
ap.add_argument("--caption-y", type=int, default=900)
ap.add_argument("--fixes", default="{}")
ap.add_argument("--text", action="store_true")
ap.add_argument("words_path")
ap.add_argument("start", type=float)
ap.add_argument("end", type=float)
ap.add_argument("out_path")
args = ap.parse_args()
words_path, start, end, out_path = args.words_path, args.start, args.end, args.out_path
CAPTION_Y = args.caption_y
words = [w for w in json.load(open(words_path)) if w[0] >= start and w[1] <= end]

def ts(t):
    t = max(0.0, t - start)
    cs = int(round(t * 100))
    return "%d:%02d:%02d.%02d" % (cs // 360000, cs // 6000 % 60, cs // 100 % 60, cs % 100)

def esc(s):
    return s.replace("\\", "").replace("{", "(").replace("}", ")")

# Whisper always hears "Automattic" as "automatic", and the vocabulary prompt
# can't help: with --condition-on-previous-text False it only applies to the
# first 30 s. The company follows "my employer" / "hosted with" / "owned by" /
# "inside of" and is followed by punctuation or a small word, while the
# adjective ("automatic updates", "I have it automatic") is not.
AFTER = {"employer", "with", "by", "of", "at", "for", "from", "join", "joined"}
BEFORE = {"or", "and", "all", "so", "for", "i", "we", "is", "the", "to", "which", "who"}

def fix_names(words):
    bare = lambda s: s.lower().strip(".,?!")
    for i, w in enumerate(words):
        if bare(w[2]) != "automatic" or i == 0 or bare(words[i - 1][2]) not in AFTER:
            continue
        nxt = bare(words[i + 1][2]) if i + 1 < len(words) else ""
        if w[2][-1] in ".,?!" or nxt in BEFORE or not nxt:
            w[2] = "Automattic" + w[2][len("automatic"):]

fix_names(words)

# Phrase fixes: glossary.json for terms Whisper gets wrong on every stream,
# then the clip's own fixes. A fix can change the number of words ("theme
# JSON" -> "theme.json"); the new words share the old ones' time evenly and
# the last one keeps the trailing punctuation.
def norm(s):
    return s.lower().strip(".,?!;:\"'")

def apply_fixes(words, fixes):
    rules = sorted(([norm(t) for t in k.split()], v.split()) for k, v in fixes.items() if k.split())
    rules.sort(key=lambda r: -len(r[0]))
    out, i = [], 0
    while i < len(words):
        for pat, rep in rules:
            n = len(pat)
            if [norm(w[2]) for w in words[i:i + n]] == pat:
                tail = re.search(r"[.,?!;:]*$", words[i + n - 1][2]).group(0)
                s, e = words[i][0], words[i + n - 1][1]
                step = (e - s) / max(len(rep), 1)
                for j, t in enumerate(rep):
                    out.append([s + j * step, s + (j + 1) * step, t + (tail if j == len(rep) - 1 else "")])
                i += n
                break
        else:
            out.append(words[i])
            i += 1
    return out

fixes = json.load(open(GLOSSARY)) if os.path.exists(GLOSSARY) else {}
try:
    fixes.update(json.loads(args.fixes))
except ValueError as err:
    sys.exit("ERROR: --fixes is not a JSON object: %s" % err)
words = apply_fixes(words, fixes)

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

if args.text:
    for group in groups:
        t = max(0.0, group[0][0] - start)
        print("[%d:%05.2f] %s" % (t // 60, t % 60, " ".join(w[2] for w in group).upper()))
    sys.exit(0)

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
