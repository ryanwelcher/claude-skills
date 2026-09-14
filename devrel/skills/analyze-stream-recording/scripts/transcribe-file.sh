#!/usr/bin/env bash
# Transcribe a local video/audio file into a condensed, timestamped transcript
# suitable for deriving a description hook and chapter markers.
#
# Usage:
#   transcribe-file.sh <path-to-file> [bucket_seconds] [model]
#
# Defaults:
#   bucket_seconds = 120   (one transcript line per 2 minutes of stream)
#   model          = mlx-community/whisper-small-mlx
#
# Output:
#   Prints ONLY a pointer, never the transcript itself:
#     CONDENSED: <path>   one "[HH:MM:SS] text" line per bucket
#     LINES: <n>
#     WORDS: <n>
#     SRT: <path>         full cue-level transcript
#   Read the CONDENSED file to work with the content. Keeping the payload out of
#   stdout means the tool result stays tiny even when the transcript is 20k words.
#
# Why condensed: a 2-hour stream produces thousands of SRT cues. Bucketing keeps
# the transcript small enough to reason over while preserving the timestamps
# needed for chapters.

set -euo pipefail

FILE="${1:-}"
BUCKET="${2:-120}"
MODEL="${3:-mlx-community/whisper-small-mlx}"

if [ -z "$FILE" ]; then
  echo "ERROR: no input file. Usage: transcribe-file.sh <path-to-file> [bucket_seconds] [model]" >&2
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "ERROR: file not found: $FILE" >&2
  exit 1
fi

MISSING=0
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ERROR: ffmpeg not found. Install with: brew install ffmpeg" >&2
  MISSING=1
fi
if ! command -v mlx_whisper >/dev/null 2>&1; then
  echo "ERROR: mlx_whisper not found. Install with: uv tool install mlx-whisper" >&2
  echo "       (Apple Silicon only. On Intel use: pipx install openai-whisper)" >&2
  MISSING=1
fi
[ "$MISSING" -eq 1 ] && exit 1

WORKDIR=$(mktemp -d)
trap 'rm -f "$WORKDIR/audio.wav"' EXIT

echo "Extracting audio from $(basename "$FILE")..." >&2
ffmpeg -nostdin -loglevel error -y -i "$FILE" \
  -vn -ac 1 -ar 16000 -c:a pcm_s16le "$WORKDIR/audio.wav"

# Bias the decoder toward names and jargon it otherwise mangles ("Ryan Welch",
# "Gutenburg"). Override with WHISPER_PROMPT for an off-topic stream.
PROMPT="${WHISPER_PROMPT:-Ryan Welcher, WordPress, Gutenberg, block editor, block theme, theme.json, Interactivity API, Block Bindings, WP-CLI, Playground, create-block, DataViews, Abilities API, PHP, JavaScript, React.}"

echo "Transcribing with $MODEL (this takes a few minutes for a long stream)..." >&2
mlx_whisper "$WORKDIR/audio.wav" \
  --model "$MODEL" \
  --initial-prompt "$PROMPT" \
  --output-format srt \
  --output-dir "$WORKDIR" >/dev/null

SRT="$WORKDIR/audio.srt"
if [ ! -f "$SRT" ]; then
  echo "ERROR: transcription produced no SRT at $SRT" >&2
  exit 1
fi

CONDENSED="$WORKDIR/condensed.txt"

python3 - "$SRT" "$BUCKET" > "$CONDENSED" <<'PY'
import re, sys

srt_path, bucket = sys.argv[1], int(sys.argv[2])

# SRT cue timestamps look like: 00:01:23,456 --> 00:01:27,890
TS = re.compile(r"^(\d\d):(\d\d):(\d\d),\d{3}\s+-->")

buckets = {}
current = None
with open(srt_path, encoding="utf-8") as fh:
    for line in fh:
        line = line.rstrip("\n")
        m = TS.match(line)
        if m:
            h, mnt, s = (int(x) for x in m.groups())
            current = ((h * 3600 + mnt * 60 + s) // bucket) * bucket
            continue
        if current is None or not line.strip() or line.strip().isdigit():
            continue
        buckets.setdefault(current, []).append(line.strip())

for start in sorted(buckets):
    stamp = "%02d:%02d:%02d" % (start // 3600, (start % 3600) // 60, start % 60)
    print("[%s] %s" % (stamp, " ".join(buckets[start])))
PY

if [ ! -s "$CONDENSED" ]; then
  echo "ERROR: condensed transcript is empty (SRT at $SRT)" >&2
  exit 1
fi

echo "CONDENSED: $CONDENSED"
echo "LINES: $(wc -l < "$CONDENSED" | tr -d ' ')"
echo "WORDS: $(wc -w < "$CONDENSED" | tr -d ' ')"
echo "SRT: $SRT"
