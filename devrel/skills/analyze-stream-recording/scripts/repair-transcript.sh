#!/usr/bin/env bash
# Re-transcribe the ranges where Whisper looped on one phrase, and splice the
# new cues into <cache-dir>/audio.srt. Called by transcribe-worker.sh once the
# first pass finishes. One attempt per range; whatever still loops afterwards
# is reported by transcribe-file.sh as a SUSPECT range.
#
# Usage:
#   repair-transcript.sh <input-file> <cache-dir> <model>
#
# The retry drops the initial prompt (it can seed a loop) and samples at a
# non-zero temperature, so it does not decode the same way twice. The first-pass
# SRT is kept as audio.first-pass.srt for comparison.

set -uo pipefail

FILE="$1"
DIR="$2"
MODEL="$3"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRT="$DIR/audio.srt"

DURATION="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FILE" 2>/dev/null || echo 0)"
RANGES="$(python3 "$SCRIPT_DIR/check-transcript.py" "$SRT" "$DURATION" \
  | sed -n 's/^SUSPECT: \([0-9:]*\)-\([0-9:]*\) repeated .*/\1 \2/p')"

[ -z "$RANGES" ] && exit 0

cp "$SRT" "$DIR/audio.first-pass.srt"
WORK="$DIR/repair"
mkdir -p "$WORK"

while read -r START END; do
  echo "Re-transcribing looped range $START-$END..." >> "$DIR/log"
  rm -f "$WORK/range.wav" "$WORK/range.srt"
  ffmpeg -nostdin -loglevel error -y -ss "$START" -to "$END" -i "$FILE" \
    -vn -ac 1 -ar 16000 -c:a pcm_s16le "$WORK/range.wav" >> "$DIR/log" 2>&1 || continue
  mlx_whisper "$WORK/range.wav" \
    --model "$MODEL" \
    --condition-on-previous-text False \
    --temperature 0.2 \
    --word-timestamps True \
    --hallucination-silence-threshold 2 \
    --output-format srt \
    --output-dir "$WORK" >> "$DIR/log" 2>&1 || continue
  [ -s "$WORK/range.srt" ] || continue

  # Drop the first-pass cues that start inside the range, then add the new
  # cues shifted by the range start.
  python3 - "$SRT" "$WORK/range.srt" "$START" "$END" <<'PY' || continue
import re, sys

main_path, part_path, start, end = sys.argv[1:5]
TS = re.compile(r"(\d\d):(\d\d):(\d\d),(\d{3})\s+-->\s+(\d\d):(\d\d):(\d\d),(\d{3})")

def hms(s):
    h, m, sec = (int(x) for x in s.split(":"))
    return h * 3600 + m * 60 + sec

def secs(g):
    return int(g[0]) * 3600 + int(g[1]) * 60 + int(g[2]) + int(g[3]) / 1000

def fmt(t):
    ms = int(round(t * 1000))
    return "%02d:%02d:%02d,%03d" % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, ms % 1000)

def read(path, offset=0.0):
    cues = []
    for block in open(path, encoding="utf-8").read().strip().split("\n\n"):
        lines = block.strip().splitlines()
        for i, line in enumerate(lines):
            m = TS.search(line)
            if m:
                g = m.groups()
                cues.append((secs(g[:4]) + offset, secs(g[4:]) + offset, "\n".join(lines[i + 1:])))
                break
    return cues

lo, hi = hms(start), hms(end)
kept = [c for c in read(main_path) if not (lo <= c[0] < hi)]
merged = sorted(kept + read(part_path, lo))
with open(main_path, "w", encoding="utf-8") as fh:
    for n, (s, e, text) in enumerate(merged, 1):
        fh.write("%d\n%s --> %s\n%s\n\n" % (n, fmt(s), fmt(e), text))
PY
done <<< "$RANGES"

rm -rf "$WORK"
exit 0
