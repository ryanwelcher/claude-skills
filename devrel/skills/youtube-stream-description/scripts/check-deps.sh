#!/usr/bin/env bash
# Report which external tools a given scenario needs and are missing, with the
# exact install command for each. Exit 0 when nothing is missing.
#
# Usage:
#   check-deps.sh <scenario>
#   scenario = upcoming | post-stream | improve-existing | local-recording
#
# The skill runs this before doing any work so that the *parent* conversation
# can ask the user whether to install. Subagents cannot ask questions, so this
# must never be pushed into a fork.

set -uo pipefail

SCENARIO="${1:-upcoming}"

need() {
  local tool="$1" install="$2" note="${3:-}"
  if command -v "$tool" >/dev/null 2>&1; then
    return 0
  fi
  echo "MISSING: $tool -> $install${note:+  ($note)}"
  return 1
}

MISSING=0

# Every scenario pulls recent descriptions for voice reference.
need yt-dlp "brew install yt-dlp" || MISSING=1

case "$SCENARIO" in
  local-recording)
    need ffmpeg "brew install ffmpeg" || MISSING=1
    need mlx_whisper "uv tool install mlx-whisper" "Apple Silicon only; on Intel use: pipx install openai-whisper, which this skill does not yet support" || MISSING=1
    ;;
  upcoming|post-stream|improve-existing)
    ;;
  *)
    echo "ERROR: unknown scenario '$SCENARIO' (expected upcoming | post-stream | improve-existing | local-recording)"
    exit 2
    ;;
esac

if [ "$MISSING" -eq 0 ]; then
  echo "OK: all dependencies present for '$SCENARIO'"
fi
exit "$MISSING"
