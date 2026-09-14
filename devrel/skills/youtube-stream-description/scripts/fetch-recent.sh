#!/usr/bin/env bash
# Fetch the hook paragraphs of recent @ryanwelchercodes videos for use as a
# voice/format reference.
#
# Usage:
#   fetch-recent.sh [count] [channel_url]
#
# Defaults:
#   count       = 5
#   channel_url = https://www.youtube.com/@ryanwelchercodes/videos
#
# Output is deliberately minimal: title + description text cut at the first
# "Connect:" line. Everything after that is boilerplate the skill already has in
# TEMPLATE.md, so re-fetching it would only cost context.

set -euo pipefail

COUNT="${1:-5}"
CHANNEL="${2:-https://www.youtube.com/@ryanwelchercodes/videos}"

if ! command -v yt-dlp >/dev/null 2>&1; then
  echo "ERROR: yt-dlp not found. Install with: brew install yt-dlp"
  exit 1
fi

IDS=$(yt-dlp --quiet --no-warnings --flat-playlist --playlist-end "$COUNT" \
  --print "%(id)s" "$CHANNEL" 2>/dev/null || true)

if [ -z "$IDS" ]; then
  echo "ERROR: no videos found at $CHANNEL (network, rate limit, or bad URL)"
  exit 1
fi

N=0
for id in $IDS; do
  OUT=$(yt-dlp --quiet --no-warnings --skip-download \
    --print "Title: %(title)s" \
    --print "%(description)s" \
    "https://www.youtube.com/watch?v=$id" 2>/dev/null || true)
  [ -z "$OUT" ] && continue
  N=$((N + 1))
  echo "=== $id ==="
  # Keep only the hook / body; drop from the first "Connect:" line onward.
  printf '%s\n' "$OUT" | awk '
    /^Connect:/ { exit }
    { lines[++n] = $0 }
    END {
      while (n > 0 && lines[n] ~ /^[[:space:]]*$/) n--
      for (i = 1; i <= n; i++) print lines[i]
    }'
  echo ""
done

if [ "$N" -eq 0 ]; then
  echo "ERROR: fetched $COUNT ids but no metadata came back"
  exit 1
fi

echo "# $N descriptions, boilerplate stripped at 'Connect:'"
