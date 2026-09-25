#!/usr/bin/env bash
# Draft a YouTube description for a local stream recording without an
# interactive session. Runs the youtube-stream-description skill through
# `claude -p` with the intake questions already answered.
#
# Usage:
#   describe-stream.sh <recording> [--title "Stream title"] [--stream-together]
#
# Output:
#   <recording-dir>/<recording-basename>.description.md
#   The description is in a fenced code block. Mentioned links are left out and
#   listed after the block as unverified, since nobody is there to confirm them.
#   Any transcript gaps are listed there too.

set -euo pipefail

FILE=""; TITLE=""; TOGETHER="no"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --title) TITLE="$2"; shift 2;;
    --stream-together) TOGETHER="yes"; shift;;
    -*) echo "unknown option: $1" >&2; exit 2;;
    *) FILE="$1"; shift;;
  esac
done

[[ -f "$FILE" ]] || { echo "Usage: describe-stream.sh <recording> [--title \"...\"] [--stream-together]" >&2; exit 2; }
FILE="$(cd "$(dirname "$FILE")" && pwd)/$(basename "$FILE")"
OUT="${FILE%.*}.description.md"

PROMPT="/youtube-stream-description Draft the description for this stream recording: $FILE

Answers to the intake questions, so do not ask me anything:
- Scenario: local recording, not yet uploaded
- Stream title: ${TITLE:-derive it from what the recording covers}
- Summary: take it from the recording
- Inline links to include: none. Leave every link mentioned in the recording out of the description. After the code block, list them as \"Unverified links, check before adding\".
- Stream Together / viewer call-in: $TOGETHER

Install nothing. If a dependency is missing, stop and say which one.
Output the final description as a single fenced code block. After it, list any transcript gaps the helper reported."

echo "Drafting description for $(basename "$FILE")..." >&2
RESULT="$(claude -p "$PROMPT" \
  --output-format json \
  --max-turns 40 \
  --allowedTools "Bash(bash:*)" "Bash(yt-dlp:*)" "Bash(ffmpeg:*)" "Bash(mlx_whisper:*)" "Read" "Skill" "Agent" "Glob" \
  --disallowedTools "AskUserQuestion" "Edit" "Write" \
  | python3 -c 'import json,sys; print(json.load(sys.stdin).get("result") or "")')"

if [[ -z "$RESULT" || "$RESULT" == ERROR:* ]]; then
  echo "${RESULT:-ERROR: claude returned no result}" >&2
  exit 1
fi

printf '%s\n' "$RESULT" > "$OUT"
echo "$OUT"
