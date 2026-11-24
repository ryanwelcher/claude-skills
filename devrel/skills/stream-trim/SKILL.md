---
name: stream-trim
description: Trim a live-stream recording and export it without Premiere. Opens a local page on the raw OBS file with In and Out already set to the first and last words, applies the stream-prep fixes (drop Full Mix and Spotify, mic 9 frames earlier) and the Podcast Voice replacement, and renders <name>-final.mp4 in 4K next to the recording, then shows a shortlist of shorts from inside the edit and renders the ones Ryan picks with the same audio. Use to trim, edit, export, or render a stream, to make shorts from the finished edit, or to skip Premiere for a stream.
allowed-tools: Bash(python3 *) Bash(bash *) Bash(ffmpeg *) Bash(ffprobe *) Bash(open *) Bash(curl *) Bash(mv *) Bash(rm *) Read Write Edit Skill
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

   Then run the tool check from `stream-shorts` step 1 (ffmpeg with libass, `mlx_whisper`), and follow its install rules if something is missing. Shorts also need the Jost font, which `render-short.sh` checks for. If Ryan doesn't want shorts this time, skip this check and steps 5 to 7.

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

5. **Find the shorts while he trims.** First delete any `shorts/candidates.json` left next to the recording from an earlier session, so the page doesn't show an old shortlist:
   ```bash
   rm -f "<recording dir>/shorts/candidates.json"
   ```
   Then, right after telling him about the page, invoke the `find-stream-shorts` skill with the raw path. Transcription doesn't depend on In/Out, so it runs while he trims and renders. If it returns an `ERROR:` line, tell him and skip the shorts. The page still works for the trim.

6. **Wait for the edit**, then write the shortlist to the page. Wait with Monitor and an until-loop (check every 30 s) on:
   ```bash
   curl -s http://127.0.0.1:<port>/api/shorts
   ```
   until `edit` isn't `null`. If he asks about the render meanwhile, check `/api/render` as in step 8. Then:
   - Keep only the clips that sit inside the edit, with the render's padding. On the transcript clock (the shortlist's times), a clip is inside when `start - 0.2 - shift >= in` and `end + 0.4 - shift <= out`, using `edit.in`, `edit.out` and `shift` from `/api/shorts`.
   - Fix dangling-word starts and ends with the rules in `stream-shorts` step 5, using the `Words` file.
   - Write the clips to `shorts/candidates.draft.json` next to the recording, in the `shorts.json` shape from `stream-shorts` step 3, with `"recording"` (the raw path) and `"words"`. Number the files in timestamp order, starting after the highest number already in `shorts/shorts.json` if that file exists. `shorts.py` picks clips by number, so a repeated number would re-render the older clip, and the page refuses it.
   - Preview the layouts and look at each jpg with Read, as in `stream-shorts` step 4. Set `layout`, `pan_x` or `skip` (with the reason) on each clip:
     ```bash
     python3 ${CLAUDE_SKILL_DIR}/../stream-shorts/scripts/shorts.py --preview "<recording dir>/shorts/candidates.draft.json" all
     ```
   - Run the same command with `--captions` instead of `--preview`. Put likely mishearings on the clip as `"suggested_fixes": {"heard": "meant"}`. The page shows them as checkboxes.
   - Delete the preview jpgs, then rename the draft so the page never reads a half-written file:
     ```bash
     mv "<recording dir>/shorts/candidates.draft.json" "<recording dir>/shorts/candidates.json"
     ```
   - Tell Ryan the shortlist is in the Shorts tab, how many clips, and any you skipped with the reasons. On each card he can nudge start and end by 0.5 s, move the screen crop, tick suggested fixes or type more, press Play to watch a quick 540x960 draft (mic audio only, a few seconds to make), and pick. Render selected writes the picks to `shorts/`.

7. **When the shorts are rendered**, write the titles and descriptions. Wait with Monitor and an until-loop (check every 30 s) on `/api/shorts` until `render.state` is `done` or `error`. Then:
   - Read the picks from `shorts/shorts.json` and get each one's caption text with `shorts.py --captions` on that file.
   - Follow `stream-shorts` steps 7, 8 and 9 for the clips that rendered (descriptions file, voice pass, em-dash and AI-ism scan, report). Report each failed clip's error from `/api/shorts` as-is.

8. **When he asks about the final render,** check it:
   ```bash
   curl -s http://127.0.0.1:<port>/api/render
   ```
   On `done`, give him the `output` path. On `error`, report `error` as-is. Leave the server running while he's still using the page. When he's done with the page and the shorts, stop the background server task.

## Notes

- The cache (preview, waveform, analysis) is in `~/Library/Caches/stream-trim/`, never next to the recording. That keeps a 1 GB preview out of Google Drive. Deleting the folder is safe.
- Default In is 0.5 s before the first word, but only when the mic is silent for at least 60 s from the start (Starting Soon). Otherwise In is 0. Default Out is 1 s after the last word.
- File ownership for shorts: Claude writes `shorts/candidates.json`, and only that. The page writes `shorts/shorts.json` with Ryan's picks, which keeps `shorts.py ... all` meaning "what Ryan picked". To change a clip after a render, edit `shorts.json` and re-render as in `stream-shorts`.
- Shorts use the same mix and voice chain as the final, through `scripts/short_audio.py` (`"mix_audio"` in `shorts.json`), at -14 LUFS, the level Shorts, Reels and TikTok play at. `/stream-shorts` on its own still uses the mic alone.
- The page's layout previews go in the cache, not in `shorts/`.
- `scripts/compare.py` is the blind A/B tool used to tune `chain.json` against a Premiere render. It isn't part of the normal flow.
