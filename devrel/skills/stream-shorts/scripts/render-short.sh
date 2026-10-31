#!/usr/bin/env bash
# Render one vertical short (1080x1920) from a stream recording: facecam band
# on top, screen crop below, word-by-word captions burned in, mic audio only.
#
# Usage:
#   render-short.sh [options] <recording> <words.json> <start> <end> <out>
#
#   <start> <end>  seconds or HH:MM:SS(.ss) on the transcript clock (the times
#                  sentences.py prints). Padding is added here.
#   <out>          the .mp4 to write, or with --preview a .jpg of the layout at
#                  the middle of the clip (no captions, no audio, fast).
#
#   --layout NAME  a layout from layouts.json (default: its "default").
#   --pan-x PX     left edge of the layout's panning band, in 1920-wide pixels
#                  (range per layout; coding-rebrand: 0-882, default 200).
#                  --screen-x is the old name and still works.
#   --fixes JSON   per-clip caption fixes, {"heard": "meant"}, on top of
#                  glossary.json.
#   --preview      write the layout frame instead of the clip.
#   --captions     print the caption text instead of rendering (no ffmpeg).
#   --dry-run      print the ffmpeg command instead of running it.
#
# Works on either file:
#   - the raw OBS recording (6 audio tracks). The mic is OBS track 2, which
#     runs 9 frames late; so does the Full Mix the transcript was made from.
#     The video is cut that much earlier so voice, captions and picture line up.
#   - stream-prep's <name>-edit.mp4 (4 tracks). The mic is the first track and
#     already in sync.
#
# Crop boxes and caption height come from layouts.json (see layout.py).

set -euo pipefail

LAYOUT_NAME=""
PAN_X=""
FIXES="{}"
MODE=render
DRY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --layout) LAYOUT_NAME="$2"; shift 2 ;;
    --pan-x|--screen-x) PAN_X="$2"; shift 2 ;;
    --fixes) FIXES="$2"; shift 2 ;;
    --preview) MODE=preview; shift ;;
    --captions) MODE=captions; shift ;;
    --dry-run) DRY=1; shift ;;
    *) break ;;
  esac
done

if [ $# -ne 5 ]; then
  echo "ERROR: usage: render-short.sh [--layout NAME] [--pan-x PX] [--fixes JSON] [--preview|--captions] [--dry-run] <recording> <words.json> <start> <end> <out>" >&2
  exit 1
fi
IN="$1"; WORDS="$2"; OUT="$5"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

[ -f "$IN" ] || [ "$MODE" = captions ] || { echo "ERROR: recording not found: $IN" >&2; exit 1; }
[ -f "$WORDS" ] || { echo "ERROR: words.json not found: $WORDS" >&2; exit 1; }

to_secs() {
  echo "$1" | awk -F: '{ s = 0; for (i = 1; i <= NF; i++) s = s * 60 + $i; print s }'
}
START="$(to_secs "$3")"
END="$(to_secs "$4")"

# A little air before the first word and after the last.
S="$(awk -v s="$START" 'BEGIN { s -= 0.2; print (s < 0 ? 0 : s) }')"
E="$(awk -v e="$END" 'BEGIN { print e + 0.4 }')"
DUR="$(awk -v s="$S" -v e="$E" 'BEGIN { print e - s }')"

# Layout first: a bad name or pan value should fail before any slow work.
LAYOUT_OUT="$(python3 "$SCRIPT_DIR/layout.py" "$LAYOUT_NAME" "$PAN_X")"
LAYOUT="$(sed -n 1p <<< "$LAYOUT_OUT")"
CAPTION_Y="$(sed -n 2p <<< "$LAYOUT_OUT")"

if [ "$MODE" = captions ]; then
  python3 "$SCRIPT_DIR/make-captions.py" --text --caption-y "$CAPTION_Y" --fixes "$FIXES" "$WORDS" "$S" "$E" -
  exit 0
fi

# Print a command, or run it.
run() {
  if [ "$DRY" -eq 1 ]; then printf '%q ' "$@"; echo; else "$@"; fi
}

AUDIO_TRACKS="$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$IN" | wc -l | tr -d ' ')"
FPS="$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$IN")"
if [ "$AUDIO_TRACKS" -ge 6 ]; then
  MIC=1
  OFFSET="$(awk -v r="$FPS" 'BEGIN { split(r, f, "/"); print 9 * f[2] / f[1] }')"
else
  MIC=0
  OFFSET=0
fi
VS="$(awk -v s="$S" -v o="$OFFSET" 'BEGIN { v = s - o; print (v < 0 ? 0 : v) }')"

if [ "$MODE" = preview ]; then
  MID="$(awk -v v="$VS" -v d="$DUR" 'BEGIN { print v + d / 2 }')"
  run ffmpeg -nostdin -loglevel error -y -ss "$MID" -i "$IN" -frames:v 1 \
    -filter_complex "${LAYOUT}[v]" -map "[v]" -q:v 3 "$OUT"
  [ "$DRY" -eq 1 ] || echo "PREVIEW: $OUT"
  exit 0
fi

# Read the whole list first: under pipefail, grep -q exiting early would kill
# ffmpeg with SIGPIPE and fail the check even when the filter is there.
FILTERS="$(ffmpeg -hide_banner -filters 2>/dev/null)"
if ! grep -qw ass <<< "$FILTERS"; then
  echo "ERROR: this ffmpeg can't burn in captions (no libass). Install the homebrew-ffmpeg build:" >&2
  echo "  brew uninstall ffmpeg && brew tap homebrew-ffmpeg/ffmpeg && brew install homebrew-ffmpeg/ffmpeg/ffmpeg" >&2
  exit 1
fi

# Without the brand font libass silently swaps in another one.
if [ ! -f "$HOME/Library/Fonts/Jost-SemiBold.ttf" ] && [ ! -f "/Library/Fonts/Jost-SemiBold.ttf" ]; then
  echo "ERROR: caption font missing. Install the static Jost-SemiBold.ttf (Google Fonts, Jost) into ~/Library/Fonts." >&2
  exit 1
fi

# ffmpeg's filter syntax chokes on spaces, quotes and colons in a path, and
# recordings live under "My Drive", so the captions go in a plain temp path.
TMP="$(mktemp -d)"
# A dry run keeps the captions file so the printed command can be checked.
[ "$DRY" -eq 1 ] || trap 'rm -rf "$TMP"' EXIT
python3 "$SCRIPT_DIR/make-captions.py" --caption-y "$CAPTION_Y" --fixes "$FIXES" "$WORDS" "$S" "$E" "$TMP/captions.ass"

mkdir -p "$(dirname "$OUT")"
run ffmpeg -nostdin -loglevel error -stats -y \
  -ss "$VS" -t "$DUR" -i "$IN" \
  -ss "$S" -t "$DUR" -i "$IN" \
  -filter_complex "${LAYOUT},ass=$TMP/captions.ass[v];[1:a:${MIC}]loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
  -map "[v]" -map "[a]" \
  -c:v h264_videotoolbox -b:v 12M -profile:v high \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart "$OUT"

[ "$DRY" -eq 1 ] || echo "SHORT: $OUT"
