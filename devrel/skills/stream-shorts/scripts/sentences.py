#!/usr/bin/env python3
"""Print one transcript sentence per line, with exact start and end times.

Usage: sentences.py <words.json> <from> <to>

<from> and <to> are HH:MM:SS or seconds. Output lines look like:
  [00:31:02.48-00:31:06.90] So the problem is the block never re-renders.

The condensed transcript is bucketed by minutes, which is too coarse to cut a
short. This gives the clip picker sentence boundaries to cut on.
"""
import json, sys

def secs(t):
    if ":" not in t:
        return float(t)
    parts = [float(p) for p in t.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0.0)
    return parts[0] * 3600 + parts[1] * 60 + parts[2]

def stamp(t):
    return "%02d:%02d:%05.2f" % (t // 3600, (t % 3600) // 60, t % 60)

words_path, lo, hi = sys.argv[1], secs(sys.argv[2]), secs(sys.argv[3])
words = [w for w in json.load(open(words_path)) if lo <= w[0] < hi]

# A sentence ends on terminal punctuation or a pause of a second or more.
sentence = []
for i, w in enumerate(words):
    sentence.append(w)
    nxt = words[i + 1] if i + 1 < len(words) else None
    if w[2][-1:] in ".?!" or nxt is None or nxt[0] - w[1] >= 1.0:
        print("[%s-%s] %s" % (stamp(sentence[0][0]), stamp(sentence[-1][1]), " ".join(x[2] for x in sentence)))
        sentence = []
