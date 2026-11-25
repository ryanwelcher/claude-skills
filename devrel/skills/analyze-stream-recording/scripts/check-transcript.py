#!/usr/bin/env python3
"""Flag the parts of a Whisper SRT that are not real transcript.

Usage: check-transcript.py <audio.srt> <duration_seconds> [--window <start> <end>]

With --window, only [start, end) seconds of the recording are checked, and
the times printed count from start (see condense.py).

Prints:
  COVERAGE: <n>%                          share of the recording outside any SUSPECT range
  SUSPECT: HH:MM:SS-HH:MM:SS <reason>     a repeated-phrase loop or a long silence

Whisper can loop one phrase for half an hour, which leaves a transcript that
looks complete but isn't. transcribe-worker.sh uses the "repeated" ranges to
decide what to re-transcribe; transcribe-file.sh reports whatever is left.
"""
import re, sys

args = sys.argv[1:]
window = None
if "--window" in args:
    i = args.index("--window")
    window = (float(args[i + 1]), float(args[i + 2]))
    del args[i:i + 3]
srt_path, duration = args[0], float(args[1] or 0)
LOOP_MIN, GAP_MIN = 60, 90

TS = re.compile(r"^(\d\d):(\d\d):(\d\d),(\d{3})\s+-->\s+(\d\d):(\d\d):(\d\d),(\d{3})")

def secs(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

def stamp(t):
    t = int(t)
    return "%02d:%02d:%02d" % (t // 3600, (t % 3600) // 60, t % 60)

cues = []
with open(srt_path, encoding="utf-8") as fh:
    for line in fh:
        line = line.strip()
        m = TS.match(line)
        if m:
            g = m.groups()
            cues.append([secs(*g[:4]), secs(*g[4:]), ""])
        elif cues and line and not line.isdigit():
            cues[-1][2] += " " + line

if window:
    # Clip the cues to the window and count from its start.
    w0, w1 = window
    cues = [[max(a, w0) - w0, min(b, w1) - w0, x] for a, b, x in cues if b > w0 and a < w1]
    duration = w1 - w0

norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
suspects = []

# Runs of consecutive identical cues.
i = 0
while i < len(cues):
    j = i
    while j + 1 < len(cues) and norm(cues[j + 1][2]) == norm(cues[i][2]):
        j += 1
    if cues[j][1] - cues[i][0] > LOOP_MIN:
        phrase = cues[i][2].strip()[:60]
        suspects.append((cues[i][0], cues[j][1], 'repeated "%s"' % phrase))
    i = j + 1

# Long stretches with no cues, including before the first and after the last.
edges = [0.0] + [t for c in cues for t in (c[0], c[1])] + [max(duration, cues[-1][1] if cues else 0)]
for k in range(0, len(edges) - 1, 2):
    if edges[k + 1] - edges[k] > GAP_MIN:
        suspects.append((edges[k], edges[k + 1], "no speech"))

suspects.sort()
lost = sum(e - s for s, e, _ in suspects)
total = duration or (cues[-1][1] if cues else 0)
pct = 0 if not total else max(0, round(100 * (total - lost) / total))
print("COVERAGE: %d%%" % pct)
for s, e, why in suspects:
    print("SUSPECT: %s-%s %s" % (stamp(s), stamp(e), why))
