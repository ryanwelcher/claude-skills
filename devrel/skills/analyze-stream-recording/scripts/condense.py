#!/usr/bin/env python3
"""Condense a Whisper SRT into one "[HH:MM:SS] text" line per bucket.

Usage: condense.py <audio.srt> <bucket_seconds> [--window <start> <end>]

With --window, only cues that start inside [start, end) seconds are kept,
and their times count from start, so start reads as 00:00:00. stream-trim
uses it for chapters that match its trimmed final.
"""
import re
import sys

args = sys.argv[1:]
window = None
if "--window" in args:
    i = args.index("--window")
    window = (float(args[i + 1]), float(args[i + 2]))
    del args[i:i + 3]
srt_path, bucket = args[0], int(args[1])

# SRT cue timestamps look like: 00:01:23,456 --> 00:01:27,890
TS = re.compile(r"^(\d\d):(\d\d):(\d\d),(\d{3})\s+-->")

buckets = {}
current = None
with open(srt_path, encoding="utf-8") as fh:
    for line in fh:
        line = line.rstrip("\n")
        m = TS.match(line)
        if m:
            h, mnt, s, ms = (int(x) for x in m.groups())
            t = h * 3600 + mnt * 60 + s
            if window:
                t += ms / 1000
                current = None if not window[0] <= t < window[1] else int((t - window[0]) // bucket) * bucket
            else:
                current = (t // bucket) * bucket
            continue
        if current is None or not line.strip() or line.strip().isdigit():
            continue
        buckets.setdefault(current, []).append(line.strip())

for start in sorted(buckets):
    stamp = "%02d:%02d:%02d" % (start // 3600, (start % 3600) // 60, start % 60)
    print("[%s] %s" % (stamp, " ".join(buckets[start])))
