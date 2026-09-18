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
#   Or, if the transcription is still running after TRANSCRIBE_WAIT seconds:
#     PENDING: <status>   run this script again with the same arguments
#
# Why condensed: a 2-hour stream produces thousands of SRT cues. Bucketing keeps
# the transcript small enough to reason over while preserving the timestamps
# needed for chapters.
#
# Why cached and detached: a long recording on a cloud drive can take longer
# than one Bash tool call (10 min max). The work runs in transcribe-worker.sh,
# detached, writing into a cache directory keyed on the file's path, size,
# mtime, model and prompt. Each call to this script waits up to TRANSCRIBE_WAIT
# seconds (default 540) for that job, and a repeat call resumes waiting on the
# same job instead of starting over. Once done, repeat calls return instantly.
#
# Environment:
#   WHISPER_PROMPT             decoder bias terms (see below)
#   TRANSCRIBE_WAIT            seconds to wait per call (default 540)
#   STREAM_TRANSCRIPT_CACHE    cache root (default ~/.cache/stream-transcripts)

set -euo pipefail

FILE="${1:-}"
BUCKET="${2:-120}"
MODEL="${3:-mlx-community/whisper-small-mlx}"
WAIT="${TRANSCRIBE_WAIT:-540}"
CACHE_ROOT="${STREAM_TRANSCRIPT_CACHE:-$HOME/.cache/stream-transcripts}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

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

# Bias the decoder toward names and jargon it otherwise mangles ("Ryan Welch",
# "Gutenburg"). Override with WHISPER_PROMPT for an off-topic stream.
PROMPT="${WHISPER_PROMPT:-Ryan Welcher, WordPress, Gutenberg, block editor, block theme, theme.json, Interactivity API, Block Bindings, WP-CLI, Playground, create-block, DataViews, Abilities API, PHP, JavaScript, React.}"

# Cache key: same file (path + size + mtime) with the same model and prompt
# gives the same transcript. The bucket size only affects condensing, which is
# cheap, so it is not part of the key.
ABS_FILE="$(cd "$(dirname "$FILE")" && pwd)/$(basename "$FILE")"
FILE_STAT="$(stat -f '%z %m' "$ABS_FILE" 2>/dev/null || stat -c '%s %Y' "$ABS_FILE")"
KEY="$(printf '%s\n%s\n%s\n%s\n' "$ABS_FILE" "$FILE_STAT" "$MODEL" "$PROMPT" | shasum -a 256 | cut -c1-16)"
DIR="$CACHE_ROOT/$KEY"
mkdir -p "$DIR"

SRT="$DIR/audio.srt"
CONDENSED="$DIR/condensed-${BUCKET}.txt"

job_running() {
  [ -f "$DIR/pid" ] && kill -0 "$(cat "$DIR/pid")" 2>/dev/null
}

start_job() {
  rm -f "$DIR/failed" "$DIR/pid" "$DIR/audio.wav" "$DIR/audio.srt"
  echo $(( $(cat "$DIR/attempts" 2>/dev/null || echo 0) + 1 )) > "$DIR/attempts"
  : > "$DIR/log"
  nohup bash "$SCRIPT_DIR/transcribe-worker.sh" "$ABS_FILE" "$DIR" "$MODEL" "$PROMPT" \
    </dev/null >>"$DIR/log" 2>&1 &
  disown
  # Give the worker a moment to write its pid file.
  for _ in 1 2 3 4 5 6 7 8 9 10; do
    [ -f "$DIR/pid" ] && break
    sleep 0.5
  done
}

if [ ! -f "$DIR/done" ]; then
  if [ -f "$DIR/failed" ]; then
    # Report the failure once, then clear it so the next call retries.
    REASON="$(cat "$DIR/failed")"
    rm -f "$DIR/failed" "$DIR/attempts"
    echo "ERROR: $REASON" >&2
    exit 1
  fi

  if ! job_running; then
    # No job, or a worker that died without writing a marker (killed, reboot).
    # Restart it, but give up after two attempts so we never loop forever.
    if [ "$(cat "$DIR/attempts" 2>/dev/null || echo 0)" -ge 2 ]; then
      rm -f "$DIR/attempts"
      echo "ERROR: transcription worker stopped twice without finishing (see $DIR/log)" >&2
      exit 1
    fi
    echo "Starting transcription of $(basename "$FILE") (cache: $DIR)..." >&2
    start_job
  else
    echo "Resuming wait on the transcription already running (cache: $DIR)..." >&2
  fi

  WAITED=0
  while [ ! -f "$DIR/done" ] && [ ! -f "$DIR/failed" ] && [ "$WAITED" -lt "$WAIT" ]; do
    job_running || break
    sleep 5
    WAITED=$((WAITED + 5))
  done

  if [ -f "$DIR/failed" ]; then
    REASON="$(cat "$DIR/failed")"
    rm -f "$DIR/failed" "$DIR/attempts"
    echo "ERROR: $REASON" >&2
    exit 1
  fi

  if [ ! -f "$DIR/done" ]; then
    # Progress bars redraw with \r, so keep only the latest redraw.
    STATUS="$(tail -n 1 "$DIR/log" 2>/dev/null | tr '\r' '\n' | grep -v '^[[:space:]]*$' | tail -n 1 | cut -c1-120 || true)"
    echo "PENDING: ${STATUS:-transcription still running}. Run this script again with the same arguments."
    exit 0
  fi
fi

rm -f "$DIR/attempts"

if [ ! -s "$CONDENSED" ]; then
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
fi

if [ ! -s "$CONDENSED" ]; then
  rm -f "$CONDENSED"
  echo "ERROR: condensed transcript is empty (SRT at $SRT)" >&2
  exit 1
fi

echo "CONDENSED: $CONDENSED"
echo "LINES: $(wc -l < "$CONDENSED" | tr -d ' ')"
echo "WORDS: $(wc -w < "$CONDENSED" | tr -d ' ')"
echo "SRT: $SRT"
