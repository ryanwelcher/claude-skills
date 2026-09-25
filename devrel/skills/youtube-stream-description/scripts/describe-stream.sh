#!/usr/bin/env bash
# Draft a YouTube description for a local stream recording without an
# interactive session. Runs the youtube-stream-description skill through
# `claude -p` with the intake questions already answered.
#
# Usage:
#   describe-stream.sh <recording> [--title "Stream title"] [--stream-together]
#   describe-stream.sh <folder> [--stream-together]
#
# With a folder, drafts every mp4/mov/mkv in it that has no .description.md
# yet, one at a time (transcription shares the GPU). A failure on one
# recording is reported and the rest still run.
#
# Output:
#   <recording-dir>/<recording-basename>.description.md
#   The description is in a fenced code block. Mentioned links are left out and
#   listed after the block as unverified, since nobody is there to confirm them.
#   Any transcript gaps are listed there too.

set -euo pipefail

TARGET=""; TITLE=""; TOGETHER="no"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --title) TITLE="$2"; shift 2;;
    --stream-together) TOGETHER="yes"; shift;;
    -*) echo "unknown option: $1" >&2; exit 2;;
    *) TARGET="$1"; shift;;
  esac
done

USAGE='Usage: describe-stream.sh <recording|folder> [--title "..."] [--stream-together]'
[[ -e "$TARGET" ]] || { echo "$USAGE" >&2; exit 2; }
if [[ -d "$TARGET" && -n "$TITLE" ]]; then
  echo "--title only works with a single recording, not a folder" >&2
  exit 2
fi

describe() {
  local file out prompt result
  file="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
  out="${file%.*}.description.md"

  prompt="/youtube-stream-description Draft the description for this stream recording: $file

Answers to the intake questions, so do not ask me anything:
- Scenario: local recording, not yet uploaded
- Stream title: ${TITLE:-derive it from what the recording covers}
- Summary: take it from the recording
- Inline links to include: none. Leave every link mentioned in the recording out of the description. After the code block, list them as \"Unverified links, check before adding\".
- Stream Together / viewer call-in: $TOGETHER

Install nothing. If a dependency is missing, stop and say which one.
Output the final description as a single fenced code block. After it, list any transcript gaps the helper reported."

  echo "Drafting description for $(basename "$file")..." >&2
  result="$(claude -p "$prompt" \
    --output-format json \
    --max-turns 40 \
    --allowedTools "Bash(bash:*)" "Bash(yt-dlp:*)" "Bash(ffmpeg:*)" "Bash(mlx_whisper:*)" "Read" "Skill" "Agent" "Glob" \
    --disallowedTools "AskUserQuestion" "Edit" "Write" \
    | python3 -c 'import json,sys; print(json.load(sys.stdin).get("result") or "")')" || true

  if [[ -z "$result" || "$result" == ERROR:* ]]; then
    echo "${result:-ERROR: claude returned no result} ($(basename "$file"))" >&2
    return 1
  fi

  printf '%s\n' "$result" > "$out"
  echo "$out"
}

if [[ -f "$TARGET" ]]; then
  describe "$TARGET"
  exit
fi

FAILED=0
shopt -s nullglob nocaseglob
for f in "$TARGET"/*.mp4 "$TARGET"/*.mov "$TARGET"/*.mkv; do
  [[ -f "${f%.*}.description.md" ]] && continue
  describe "$f" || FAILED=$((FAILED + 1))
done
[[ "$FAILED" -eq 0 ]] || { echo "$FAILED recording(s) failed" >&2; exit 1; }
