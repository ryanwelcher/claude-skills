#!/usr/bin/env python3
"""Flatten mlx_whisper's JSON output into a word list.

Usage: whisper-words.py <audio.json> [offset_seconds]

Prints a JSON array of [start, end, word] with times rounded to the
millisecond and shifted by the offset. stream-shorts reads this as words.json
to cut on word boundaries and time the captions.
"""
import json, sys

path = sys.argv[1]
offset = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0

words = []
for seg in json.load(open(path, encoding="utf-8")).get("segments", []):
    for w in seg.get("words", []):
        text = w.get("word", "").strip()
        if text:
            words.append([round(w["start"] + offset, 3), round(w["end"] + offset, 3), text])

json.dump(words, sys.stdout, separators=(",", ":"))
