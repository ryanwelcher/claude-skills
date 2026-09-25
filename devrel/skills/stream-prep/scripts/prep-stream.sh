#!/usr/bin/env bash
# Prep an OBS stream recording for Premiere: drop unwanted audio tracks and
# pull the mic track earlier by N frames. Writes <name>-edit.mp4 next to the
# original. Video and untouched audio tracks are stream-copied; only the
# shifted track is re-encoded (AAC 320k) so the trim is sample-accurate.
set -euo pipefail

DROP="1,4"  # OBS track numbers to remove (1 = Full Mix, 4 = Spotify)
SHIFT=2     # OBS track number to pull earlier (2 = mic)
FRAMES=9    # how many video frames earlier

usage() {
  echo "Usage: prep-stream.sh [--drop 1,4] [--shift 2] [--frames 9] <file> [more files...]" >&2
  exit 1
}

files=()
while [ $# -gt 0 ]; do
  case "$1" in
    --drop) DROP="$2"; shift 2 ;;
    --shift) SHIFT="$2"; shift 2 ;;
    --frames) FRAMES="$2"; shift 2 ;;
    -h|--help) usage ;;
    -*) echo "ERROR: unknown option $1" >&2; usage ;;
    *) files+=("$1"); shift ;;
  esac
done
[ ${#files[@]} -gt 0 ] || usage

for bin in ffmpeg ffprobe; do
  command -v "$bin" >/dev/null || { echo "ERROR: $bin not found (brew install ffmpeg)" >&2; exit 1; }
done

case ",$DROP," in *",$SHIFT,"*)
  echo "ERROR: track $SHIFT is both dropped and shifted" >&2; exit 1 ;;
esac

for in in "${files[@]}"; do
  [ -f "$in" ] || { echo "ERROR: file not found: $in" >&2; exit 1; }

  out="${in%.*}-edit.mp4"
  [ -e "$out" ] && { echo "ERROR: output already exists: $out" >&2; exit 1; }

  fps=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$in")
  count=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$in" | wc -l | tr -d ' ')
  offset=$(awk -v f="$FRAMES" -v r="$fps" 'BEGIN { split(r, p, "/"); if (p[2] == "") p[2] = 1; printf "%.6f", f * p[2] / p[1] }')

  for t in $(echo "$DROP" | tr ',' ' ') "$SHIFT"; do
    if [ "$t" -lt 1 ] || [ "$t" -gt "$count" ]; then
      echo "ERROR: $in has $count audio tracks, can't use track $t" >&2; exit 1
    fi
  done

  maps=(-map 0:v:0)
  codecs=()
  kept=()
  n=0
  for t in $(seq 1 "$count"); do
    case ",$DROP," in *",$t,"*) continue ;; esac
    if [ "$t" -eq "$SHIFT" ]; then
      maps+=(-map "[shifted]")
      codecs+=("-c:a:$n" aac "-b:a:$n" 320k)
    else
      maps+=(-map "0:a:$((t - 1))")
      codecs+=("-c:a:$n" copy)
    fi
    kept+=("$t")
    n=$((n + 1))
  done

  echo "==> $in"
  echo "    ${fps} fps, ${FRAMES} frames = ${offset}s; keeping tracks ${kept[*]}, shifting track $SHIFT"

  # Write to a temp name so a failed or cancelled run never leaves a half-written -edit file.
  tmp="${out%.mp4}.partial.mp4"
  trap 'rm -f "$tmp"' EXIT
  ffmpeg -nostdin -hide_banner -loglevel error -stats -i "$in" \
    -filter_complex "[0:a:$((SHIFT - 1))]atrim=start=${offset},asetpts=PTS-STARTPTS[shifted]" \
    "${maps[@]}" -c:v copy "${codecs[@]}" "$tmp"
  mv "$tmp" "$out"
  trap - EXIT

  echo "    wrote $out"
done
