#!/usr/bin/env bash
# Render one vertical short (1080x1920) from a stream recording: facecam band
# on top, screen crop below, word-by-word captions burned in, mic audio only.
#
# Usage:
#   render-short.sh [--screen-x PX] [--preview] <recording> <words.json> <start> <end> <out>
#
#   <start> <end>  seconds or HH:MM:SS(.ss) on the transcript clock (the times
#                  sentences.py prints). Padding is added here.
#   <out>          the .mp4 to write, or with --preview a .jpg of the layout at
#                  the middle of the clip (no captions, no audio, fast).
#   --screen-x PX  left edge of the screen crop, in 1920-wide pixels
#                  (default 200; 0 = far left, 882 = far right).
#
# Works on either file:
#   - the raw OBS recording (6 audio tracks). The mic is OBS track 2, which
#     runs 9 frames late; so does the Full Mix the transcript was made from.
#     The video is cut that much earlier so voice, captions and picture line up.
#   - stream-prep's <name>-edit.mp4 (4 tracks). The mic is the first track and
#     already in sync.
#
# Crop boxes are for the "Coding - Rebrand" OBS scene, in 1920x1080 pixels and
# scaled to the recording's real size (the recordings are 4K):
#   cam:    600x500 at (1320, 520)  -> 1080x900 on top
#   screen: 1038x980 at (X, 20)     -> 1080x1020 below (stops above the bottom bar)

set -euo pipefail

SCREEN_X=200
PREVIEW=0
while [ $# -gt 0 ]; do
  case "$1" in
    --screen-x) SCREEN_X="$2"; shift 2 ;;
    --preview) PREVIEW=1; shift ;;
    *) break ;;
  esac
done

if [ $# -ne 5 ]; then
  echo "ERROR: usage: render-short.sh [--screen-x PX] [--preview] <recording> <words.json> <start> <end> <out>" >&2
  exit 1
fi
IN="$1"; WORDS="$2"; OUT="$5"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

[ -f "$IN" ] || { echo "ERROR: recording not found: $IN" >&2; exit 1; }
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

LAYOUT="[0:v]split=2[c][s];\
[c]crop=iw*600/1920:ih*500/1080:iw*1320/1920:ih*520/1080,scale=1080:900[cam];\
[s]crop=iw*1038/1920:ih*980/1080:iw*${SCREEN_X}/1920:ih*20/1080,scale=1080:1020[scr];\
[cam][scr]vstack"

if [ "$PREVIEW" -eq 1 ]; then
  MID="$(awk -v v="$VS" -v d="$DUR" 'BEGIN { print v + d / 2 }')"
  ffmpeg -nostdin -loglevel error -y -ss "$MID" -i "$IN" -frames:v 1 \
    -filter_complex "${LAYOUT}[v]" -map "[v]" -q:v 3 "$OUT"
  echo "PREVIEW: $OUT"
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

# ffmpeg's filter syntax chokes on spaces, quotes and colons in a path, and
# recordings live under "My Drive", so the captions go in a plain temp path.
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
python3 "$SCRIPT_DIR/make-captions.py" "$WORDS" "$S" "$E" "$TMP/captions.ass"

mkdir -p "$(dirname "$OUT")"
ffmpeg -nostdin -loglevel error -stats -y \
  -ss "$VS" -t "$DUR" -i "$IN" \
  -ss "$S" -t "$DUR" -i "$IN" \
  -filter_complex "${LAYOUT},ass=$TMP/captions.ass[v];[1:a:${MIC}]loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
  -map "[v]" -map "[a]" \
  -c:v h264_videotoolbox -b:v 12M -profile:v high \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart "$OUT"

echo "SHORT: $OUT"
