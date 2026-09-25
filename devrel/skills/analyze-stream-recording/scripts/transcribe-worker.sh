#!/usr/bin/env bash
# Detached worker for transcribe-file.sh. Do not call directly.
#
# Usage:
#   transcribe-worker.sh <input-file> <cache-dir> <model> <prompt>
#
# Writes into <cache-dir>:
#   pid        this worker's PID while it runs
#   log        ffmpeg / mlx_whisper stderr
#   audio.srt  the full transcript (only once whisper finishes)
#   done       marker: transcript is complete
#   failed     marker: the job failed; contents are the reason
#
# Runs detached so a transcription longer than one Bash tool call (10 min max)
# survives. transcribe-file.sh starts it once and then waits on the markers.

set -uo pipefail

FILE="$1"
DIR="$2"
MODEL="$3"
PROMPT="$4"

echo $$ > "$DIR/pid"

fail() {
  echo "$1" > "$DIR/failed"
  rm -f "$DIR/audio.wav" "$DIR/pid"
  exit 1
}

echo "Extracting audio from $(basename "$FILE")..." >> "$DIR/log"
ffmpeg -nostdin -loglevel error -y -i "$FILE" \
  -vn -ac 1 -ar 16000 -c:a pcm_s16le "$DIR/audio.wav" >> "$DIR/log" 2>&1 \
  || fail "ffmpeg could not extract audio (see $DIR/log)"

echo "Transcribing with $MODEL..." >> "$DIR/log"
# Without --condition-on-previous-text False, one misheard window feeds the
# next and Whisper can repeat a single phrase for half an hour. The silence
# threshold skips quiet stretches where it would otherwise invent text.
mlx_whisper "$DIR/audio.wav" \
  --model "$MODEL" \
  --initial-prompt "$PROMPT" \
  --condition-on-previous-text False \
  --word-timestamps True \
  --hallucination-silence-threshold 2 \
  --output-format srt \
  --output-dir "$DIR" >> "$DIR/log" 2>&1 \
  || fail "mlx_whisper failed (see $DIR/log)"

[ -s "$DIR/audio.srt" ] || fail "transcription produced no SRT in $DIR"

# If a range still looped, re-transcribe it once with different settings.
bash "$(dirname "${BASH_SOURCE[0]}")/repair-transcript.sh" "$FILE" "$DIR" "$MODEL"

# The WAV is roughly 115 MB per hour of stream. The SRT is all we need to keep.
rm -f "$DIR/audio.wav" "$DIR/pid"
touch "$DIR/done"
