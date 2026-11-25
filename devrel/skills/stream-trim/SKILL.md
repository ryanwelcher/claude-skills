---
name: stream-trim
description: Trim a live-stream recording and export it without Premiere. Opens a local page on the raw OBS file with In and Out already set to the first and last words, applies the recording setup from a profile (Ryan's: drop Full Mix and Spotify, mic 9 frames earlier) and the Podcast Voice replacement, and renders <name>-final.mp4 in 4K next to the recording, then shows a shortlist of shorts from inside the edit and renders the ones Ryan picks with the same audio. Use to trim, edit, export, or render a stream, to make shorts from the finished edit, or to skip Premiere for a stream.
allowed-tools: Bash(python3 *) Bash(bash *) Bash(ffmpeg *) Bash(ffprobe *) Bash(open *) Bash(curl *) Bash(mv *) Bash(rm *) Read Write Edit Skill
---

# Stream Trim

Input: `$ARGUMENTS` is the path to a raw OBS stream recording, and optionally a profile name ("trim this with the laptop profile").

Needs an Apple Silicon Mac (the hardware encoder, `mlx_whisper` and the Mac cache and font folders).

A **profile** describes a recording setup: which OBS tracks to keep and what each one is, how many frames late the mic runs, the voice chain, loudness, caption font, short layouts, and whether the `sounds-like-me` voice pass runs. Ryan's is `profiles/ryan-obs.json` (6 tracks, "Rebrand" layout, see `stream-prep`); its voice chain is `scripts/chain.json`, tuned against his Premiere Podcast Voice render of the Nov 12 stream. Change it only if he asks. Everyone else's profiles live in `~/.config/stream-trim/profiles/`, and `~/.config/stream-trim/default` names the machine's default.

## Steps

1. **Check ffmpeg** has the Mac hardware encoder (for the preview) and libx265 (for the final). Read the list into a variable first, because `grep -q` on a pipe fails under pipefail:
   ```bash
   enc=$(ffmpeg -hide_banner -encoders 2>/dev/null); case "$enc" in *h264_videotoolbox*libx265*) echo OK ;; *) echo MISSING ;; esac
   ```
   If it prints `MISSING`, stop and tell Ryan. This needs an ffmpeg built for macOS with VideoToolbox and libx265.

   Then run the tool check from `stream-shorts` step 1 (ffmpeg with libass, `mlx_whisper`), and follow its install rules if something is missing. Shorts also need the Jost font, which `render-short.sh` checks for. If Ryan doesn't want shorts this time, skip this check and steps 6 to 8.

2. **Check the profile** before anything slow runs:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/profiles.py check "<raw>"
   ```
   Add `--profile <name>` if one was named. `PROFILE <name>` means go on, and pass `--profile <name>` to `prepare.py` and `server.py` below. On `ERROR: NO_DEFAULT` there's no profile on this machine: ask whether to set one up (see **First-run setup**) or which existing one to use. On a track-count mismatch, report it as-is and ask which profile fits this recording, or offer first-run setup. On any other `ERROR:` line (a profile file that isn't valid JSON, a missing field, a default that names a deleted profile), report it as-is and stop. Don't guess a profile.

3. **Prepare** with `run_in_background`, quoting the path:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/prepare.py "<raw>" --profile <name>
   ```
   Tell Ryan it reads the whole recording once: a 720p preview, the mic waveform, and where his voice starts and stops. From Google Drive this takes 10 minutes or more. Reruns on the same file are instant. Wait for the exit notification. If it prints an `ERROR:` line, report it as-is and stop.

4. **Start the page** with `run_in_background`:
   ```bash
   python3 -u ${CLAUDE_SKILL_DIR}/scripts/server.py "<raw>" --profile <name>
   ```
   Read its output file for the `READY http://127.0.0.1:<port>/` line, then `open` that URL. If it prints an `ERROR:` line instead, report it as-is. When it says the cache was made with another profile, rerun step 3 with this profile, then this step.

5. **Tell Ryan** what prepare printed, as one short list:
   - In, Out and length, as h:mm:ss
   - the keys: Space, J/K/L, I/O, arrows (1 frame), Shift+arrows (1 s), Q/W to jump to In/Out, drag the markers
   - that Render writes `<name>-final.mp4` next to the recording and never overwrites one

6. **Find the shorts while he trims.** First delete any `shorts/candidates.json` left next to the recording from an earlier session, so the page doesn't show an old shortlist:
   ```bash
   rm -f "<recording dir>/shorts/candidates.json"
   ```
   Then, right after telling him about the page, invoke the `find-stream-shorts` skill with the raw path. Transcription doesn't depend on In/Out, so it runs while he trims and renders. If it returns an `ERROR:` line, tell him and skip the shorts. The page still works for the trim.

7. **Wait for the edit**, then write the shortlist to the page. Wait with Monitor and an until-loop (check every 30 s) on:
   ```bash
   curl -s http://127.0.0.1:<port>/api/shorts
   ```
   until `edit` isn't `null`. If he asks about the render meanwhile, check `/api/render` as in step 9. Then:
   - Keep only the clips that sit inside the edit, with the render's padding. On the transcript clock (the shortlist's times), a clip is inside when `start - 0.2 - shift >= in` and `end + 0.4 - shift <= out`, using `edit.in`, `edit.out` and `shift` from `/api/shorts`.
   - Fix dangling-word starts and ends with the rules in `stream-shorts` step 5, using the `Words` file.
   - Write the clips to `shorts/candidates.draft.json` next to the recording, in the `shorts.json` shape from `stream-shorts` step 3, with `"recording"` (the raw path) and `"words"`. If the profile has a `layouts` file, add `"layouts"` with its absolute path (it's relative to the profile file), so the previews use the profile's layouts. Number the files in timestamp order, starting after the highest number already in `shorts/shorts.json` if that file exists. `shorts.py` picks clips by number, so a repeated number would re-render the older clip, and the page refuses it.
   - Preview the layouts and look at each jpg with Read, as in `stream-shorts` step 4. Set `layout`, `pan_x` or `skip` (with the reason) on each clip:
     ```bash
     python3 ${CLAUDE_SKILL_DIR}/../stream-shorts/scripts/shorts.py --preview "<recording dir>/shorts/candidates.draft.json" all
     ```
   - Run the same command with `--captions` instead of `--preview`. Put mishearings on the clip as `"suggested_fixes": {"heard": "meant"}`. The page shows them as checkboxes that start ticked, so they go into the render unless Ryan unticks them. Only suggest a fix you're sure of; mention a doubtful one to Ryan instead.
   - Delete the preview jpgs, then rename the draft so the page never reads a half-written file:
     ```bash
     mv "<recording dir>/shorts/candidates.draft.json" "<recording dir>/shorts/candidates.json"
     ```
   - Tell Ryan the shortlist is in the Shorts tab, how many clips, and any you skipped with the reasons. On each card he can nudge start and end by 0.5 s, move the screen crop, untick a wrong suggested fix or type more, press Play to watch a quick 540x960 draft (mic audio only, a few seconds to make), and pick. Render selected writes the picks to `shorts/`.

8. **When the shorts are rendered**, write the titles and descriptions. Wait with Monitor and an until-loop (check every 30 s) on `/api/shorts` until `render.state` is `done` or `error`. Then:
   - Read the picks from `shorts/shorts.json` and get each one's caption text with `shorts.py --captions` on that file.
   - Follow `stream-shorts` steps 7, 8 and 9 for the clips that rendered (descriptions file, voice pass, em-dash and AI-ism scan, report). Report each failed clip's error from `/api/shorts` as-is.
   - Run the `sounds-like-me` voice pass only when the profile's `voice_pass` is `sounds-like-me`. Read it from the profile file: `~/.config/stream-trim/profiles/<name>.json` if it exists, otherwise `${CLAUDE_SKILL_DIR}/profiles/<name>.json`. With `null`, write the titles and descriptions plain, in the person's own words from the clip. The separate em-dash and AI-ism scan always runs.

9. **When he asks about the final render,** check it:
   ```bash
   curl -s http://127.0.0.1:<port>/api/render
   ```
   On `done`, give him the `output` path. On `error`, report `error` as-is. Leave the server running while he's still using the page. When he's done with the page and the shorts, stop the background server task.

## First-run setup

For someone with their own OBS setup, when `profiles.py check` says `NO_DEFAULT`, a track count doesn't match, or they ask. Pick a short name with them (`<name>`), then:

1. Cut a 5-second sample of each audio track from a stretch where they're talking (pass `--at <seconds>` to move it), into the scratchpad:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/profiles.py samples "<raw>" "<scratchpad>/samples" --at <seconds>
   ```
   Tell them the paths so they can listen (`open` a file plays it).
2. Ask what each track is (mic, guest, music, alerts...) and which to drop. Voice tracks (a mic, a guest) get `"voice": true`. One voice track is `"mic"`.
3. Ask how many frames late their mic runs against the video. If they don't know, use 0 and tell them how to check: in the Shorts tab, press Play on a draft and watch the lips. Ask the same for track 1 (`transcript_lag_frames`), since the transcript and shortlist come from track 1. If it's their mic, it's the same number.
4. If track 1 has no voice on it, warn them: the shortlist will be poor, because the transcript comes from track 1.
5. Build their short layout with the "Adding a layout" steps in `stream-shorts`: grab a frame from their usual scene, work out the facecam and screen boxes with them, and preview it. Save it to `~/.config/stream-trim/profiles/<name>-layouts.json` with `"default"` set to that layout.
6. Write `~/.config/stream-trim/profiles/<name>.json`. Copy the shape of `profiles/ryan-obs.json`, with their tracks, `"mic"`, the two lag values, `"chain": "chain-plain.json"` (the built-in plain chain, voice processing off, unless they tune their own), `"name"` equal to `<name>` (it must match the file name), Ryan's `shorts_loudness` and `caption_font`, `"layouts": "<name>-layouts.json"` and `"voice_pass": null`.
7. Check it, and make it the default if the machine has none:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/profiles.py check "<raw>" --profile <name>
   python3 ${CLAUDE_SKILL_DIR}/scripts/profiles.py set-default <name>
   ```
   Then carry on from step 3 with `--profile <name>`.

## Notes

- The cache (preview, waveform, analysis) is in `~/Library/Caches/stream-trim/`, never next to the recording. That keeps a 1 GB preview out of Google Drive. Deleting the folder is safe.
- Default In is 0.5 s before the first word, but only when the mic is silent for at least 60 s from the start (Starting Soon). Otherwise In is 0. Default Out is 1 s after the last word.
- File ownership for shorts: Claude writes `shorts/candidates.json`, and only that. The page writes `shorts/shorts.json` with Ryan's picks, which keeps `shorts.py ... all` meaning "what Ryan picked". To change a clip after a render, edit `shorts.json` and re-render as in `stream-shorts`.
- Shorts use the same mix and voice chain as the final, through `scripts/short_audio.py` (`"mix_audio"` in `shorts.json`), at the profile's `shorts_loudness` (Ryan's: -14 LUFS, the level Shorts, Reels and TikTok play at). The page also writes the profile's mic track, lags, caption font and layouts file into `shorts.json`. `/stream-shorts` on its own still uses the mic alone.
- The prepared cache remembers its profile. Running the same recording with another profile prepares it again.
- The page's layout previews go in the cache, not in `shorts/`.
- `scripts/compare.py` is the blind A/B tool used to tune `chain.json` against a Premiere render. It isn't part of the normal flow.
