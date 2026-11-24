---
name: stream-trim
description: Trim a live-stream recording and export it without Premiere. Opens a local page on the raw OBS file with In and Out already set to the first and last words, applies the stream-prep fixes (drop Full Mix and Spotify, mic 9 frames earlier) and the Podcast Voice replacement, and renders <name>-final.mp4 in 4K next to the recording. Use to trim, edit, export, or render a stream, or to skip Premiere for a stream.
allowed-tools: Bash(python3 *) Bash(ffmpeg *) Bash(ffprobe *) Bash(open *) Bash(curl *)
---

# Stream Trim

Input: `$ARGUMENTS` is the path to a raw OBS stream recording (6 audio tracks, "Rebrand" layout, see `stream-prep`).

The audio settings (mix and voice chain) live in `scripts/chain.json`. They were tuned against Ryan's Premiere Podcast Voice render of the Nov 12 stream. Change them only if he asks.

## Steps

1. **Check ffmpeg** has the Mac hardware encoder (for the preview) and libx265 (for the final). Read the list into a variable first, because `grep -q` on a pipe fails under pipefail:
   ```bash
   enc=$(ffmpeg -hide_banner -encoders 2>/dev/null); case "$enc" in *h264_videotoolbox*libx265*) echo OK ;; *) echo MISSING ;; esac
   ```
   If it prints `MISSING`, stop and tell Ryan. This needs an ffmpeg built for macOS with VideoToolbox and libx265.

2. **Prepare** with `run_in_background`, quoting the path:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/prepare.py "<raw>"
   ```
   Tell Ryan it reads the whole recording once: a 720p preview, the mic waveform, and where his voice starts and stops. From Google Drive this takes 10 minutes or more. Reruns on the same file are instant. Wait for the exit notification. If it prints an `ERROR:` line, report it as-is and stop.

3. **Start the page** with `run_in_background`:
   ```bash
   python3 -u ${CLAUDE_SKILL_DIR}/scripts/server.py "<raw>"
   ```
   Read its output file for the `READY http://127.0.0.1:<port>/` line, then `open` that URL.

4. **Tell Ryan** what prepare printed, as one short list:
   - In, Out and length, as h:mm:ss
   - the keys: Space, J/K/L, I/O, arrows (1 frame), Shift+arrows (1 s), Q/W to jump to In/Out, drag the markers
   - that Render writes `<name>-final.mp4` next to the recording and never overwrites one

5. **When he says it's rendered, or asks,** check the render state:
   ```bash
   curl -s http://127.0.0.1:<port>/api/render
   ```
   On `done`, give him the `output` path. On `error`, report `error` as-is. Leave the server running while he's still using the page. When he's done, stop the background server task.

## Notes

- The cache (preview, waveform, analysis) is in `~/Library/Caches/stream-trim/`, never next to the recording. That keeps a 1 GB preview out of Google Drive. Deleting the folder is safe.
- Default In is 0.5 s before the first word, but only when the mic is silent for at least 60 s from the start (Starting Soon). Otherwise In is 0. Default Out is 1 s after the last word.
- `scripts/compare.py` is the blind A/B tool used to tune `chain.json` against a Premiere render. It isn't part of the normal flow.
