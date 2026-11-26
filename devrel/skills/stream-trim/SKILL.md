---
name: stream-trim
description: "Trim a live-stream recording and export it without Premiere. Opens a local page on the raw OBS file with In and Out already set to the first and last words, applies the recording setup from a profile (Ryan's: drop Full Mix and Spotify, mic 9 frames earlier) and the Podcast Voice replacement, and renders <name>-final.mp4 in 4K to renders/ next to the recording, then shows a shortlist of shorts from inside the edit and renders the ones Ryan picks with the same audio. Use to trim, edit, export, or render a stream, to make shorts from the finished edit, or to skip Premiere for a stream."
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

   Then run the tool check from `stream-shorts` step 1 (ffmpeg with libass, `mlx_whisper`), and follow its install rules if something is missing. Shorts also need the Jost font, which `render-short.sh` checks for. If Ryan doesn't want shorts this time, skip this check and steps 6 to 8 (step 9 still runs).

2. **Check the profile** before anything slow runs:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/profiles.py check "<raw>"
   ```
   Add `--profile <name>` if one was named. If it also prints `CLOUD_ONLY`, the recording is only in Google Drive and hasn't been downloaded. Reading it from there made prepare take 84 minutes instead of about 6. Ask Ryan to right-click it in Finder and choose **Make available offline**, wait for him to say it's done, then run the check again. Go on only when `CLOUD_ONLY` is gone. `PROFILE <name>` means go on, and pass `--profile <name>` to `prepare.py` and `server.py` below. On `ERROR: NO_DEFAULT` there's no profile on this machine: ask whether to set one up (see **First-run setup**) or which existing one to use. On a track-count mismatch, report it as-is and ask which profile fits this recording, or offer first-run setup. On any other `ERROR:` line (a profile file that isn't valid JSON, a missing field, a default that names a deleted profile), report it as-is and stop. Don't guess a profile.

3. **Prepare** with `run_in_background`, quoting the path:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/prepare.py "<raw>" --profile <name>
   ```
   Tell Ryan it reads the whole recording once: a 720p preview, the mic waveform, and where his voice starts and stops. With the file downloaded this takes about 6 minutes. Reruns on the same file are instant. Wait for the exit notification. If it prints an `ERROR:` line, report it as-is and stop.

4. **Start the page** with `run_in_background`:
   ```bash
   python3 -u ${CLAUDE_SKILL_DIR}/scripts/server.py "<raw>" --profile <name>
   ```
   Read its output file for the `READY http://127.0.0.1:<port>/` line, then `open` that URL. If it prints an `ERROR:` line instead, report it as-is. When it says the cache was made with another profile, rerun step 3 with this profile, then this step.

5. **Tell Ryan** what prepare printed, as one short list:
   - In, Out and length, as h:mm:ss
   - the keys: Space, J/K/L, I/O, arrows (1 frame), Shift+arrows (1 s), Q/W to jump to In/Out, drag the markers
   - that Render writes `renders/<name>-final.mp4` next to the recording and never overwrites one, and that picking a title later renames it
   - that the Shorts tab works right away: it shows the transcription's progress until the shortlist is in, and he can pick and render shorts while the final renders (both run slower side by side)

6. **Find the shorts while he trims.** First delete any `shorts/candidates.json` left next to the recording from an earlier session, so the page doesn't show an old shortlist:
   ```bash
   rm -f "<recording dir>/shorts/candidates.json"
   ```
   Then, right after telling him about the page, invoke the `find-stream-shorts` skill with the raw path. Transcription doesn't depend on In/Out, so it runs while he trims and renders. If it returns an `ERROR:` line, tell him and skip the shorts. The page still works for the trim.

7. **Write the shortlist to the page** as soon as `find-stream-shorts` returns. Don't wait for the final: shorts are cut from the raw, so they don't need it. Keep every clip, even ones outside Ryan's trim; the page flags those and he decides. If he asks about the render meanwhile, check `/api/render` as in step 10. Then:
   - Fix dangling-word starts and ends with the rules in `stream-shorts` step 5, using the `Words` file.
   - Write the clips to `shorts/candidates.draft.json` next to the recording, in the `shorts.json` shape from `stream-shorts` step 3, with `"recording"` (the raw path) and `"words"`. If the profile has a `layouts` file, add `"layouts"` with its absolute path (it's relative to the profile file), so the previews use the profile's layouts. Number the files in timestamp order, starting after the highest number already in `shorts/shorts.json` if that file exists. `shorts.py` picks clips by number, so a repeated number would re-render the older clip, and the page refuses it.
   - Pick each clip's layout: `coding-rebrand` (Code + me) when the screen matters to the moment, `me` (Just me) when Ryan is just talking. He can switch it on the card, between every layout that has a label. Then preview the layouts and look at each jpg with Read, as in `stream-shorts` step 4. Set `layout`, `pan_x` or `skip` (with the reason) on each clip:
     ```bash
     python3 ${CLAUDE_SKILL_DIR}/../stream-shorts/scripts/shorts.py --preview "<recording dir>/shorts/candidates.draft.json" all
     ```
   - Run the same command with `--captions` instead of `--preview`. Put mishearings on the clip as `"suggested_fixes": {"heard": "meant"}`. The page shows them as checkboxes that start ticked, so they go into the render unless Ryan unticks them. Only suggest a fix you're sure of; mention a doubtful one to Ryan instead.
   - Delete the preview jpgs, then rename the draft so the page never reads a half-written file:
     ```bash
     mv "<recording dir>/shorts/candidates.draft.json" "<recording dir>/shorts/candidates.json"
     ```
   - Tell Ryan the shortlist is in the Shorts tab, how many clips, and any you skipped with the reasons. The left side lists every short as one row, grouped by state: To render, Shortlist, Rendered and a collapsed Dismissed list. He ticks a row to render it and clicks a row to open it in the editor on the right. There he can nudge start and end by 0.5 s, switch between Code + me and Just me, slide the crop, untick a wrong suggested fix or type more, press Play to watch a quick 540x960 draft (mic audio only, a few seconds to make), and add or remove it from To render. A rendered short also has Show in Finder, its title picks, and Re-render once he changes it. "Not this one" dismisses a short and Restore brings it back. Shortlist entries that copy a short already rendered are hidden behind one line. The Render button writes the ticked ones to `shorts/`.

8. **When the shorts are rendered**, put title options on the page, then write the descriptions. Wait with Monitor and an until-loop (check every 30 s) on `/api/shorts` until `render.state` is `done` or `error`. Then:
   - Read the picks from `shorts/shorts.json` and get each one's caption text with `shorts.py --captions` on that file. Report each failed clip's error from `/api/shorts` as-is.
   - For each rendered short, draft 3 or 4 titles under 100 characters from what's said in the clip, and run the em-dash and AI-ism scan on them. Score each once with `mcp__vidiq__vidiq_score_title`, `type: "short"` (5 viDIQ credits a title). If that tool isn't available, leave the scores out and tell Ryan why.
   - Post them to the page. Write the JSON to a file in the scratchpad first, so no title needs shell quoting:
     ```bash
     curl -s -X POST http://127.0.0.1:<port>/api/titles -H 'Content-Type: application/json' --data @<file>
     ```
     with `{"shorts": {"<n>": [{"title": "...", "score": 74}, ...]}}` (`score` is `null` without viDIQ). Tell Ryan the options are on each card, with a box for his own, and that **Use this title** renames the short to `NN - <Title>.mp4`.
   - Wait with Monitor and an until-loop (check every 30 s) on `curl -s http://127.0.0.1:<port>/api/titles` until `picked` has every short you posted.
   - Then follow `stream-shorts` steps 7, 8 and 9 for those clips (descriptions file, voice pass, em-dash and AI-ism scan, report). The file line is the clip's `file` in `shorts/shorts.json`, and the title is Ryan's pick from `/api/titles`, word for word. The voice pass covers the descriptions only: never change a picked title, because the file is named after it.
   - Run the `sounds-like-me` voice pass only when the profile's `voice_pass` is `sounds-like-me`. Read it from the profile file: `~/.config/stream-trim/profiles/<name>.json` if it exists, otherwise `${CLAUDE_SKILL_DIR}/profiles/<name>.json`. With `null`, write the titles and descriptions plain, in the person's own words from the clip. The separate em-dash and AI-ism scan always runs.
   - Then make each short's thumbnails, as in **Thumbnails** steps 1 to 4 below: portrait, 2 per short, plain only. Post them and don't wait for picks; go on to step 9. He can press **Polish with vidIQ** on a card for the ones he wants polished, and step 6 answers that after the final.

9. **Write the full video's title and description** once the final is rendered: after step 8, or without shorts, once `/api/render` says `done`. Get `edit.in`, `edit.out` and `shift` from `/api/shorts`. The transcript runs `shift` seconds behind the video, so the final's 00:00 is `edit.in + shift` on the transcript clock:
   - With the `ryan-obs` profile, invoke the `youtube-stream-description` skill with:
     ```
     <raw path> --window <edit.in + shift> <edit.out + shift> --out <recording dir>/renders --titles-url http://127.0.0.1:<port>
     ```
     (seconds, 3 decimals). Its scored title options go on the page under the finished render, and Ryan's pick renames the final to `renders/<Title>.mp4`. It writes `renders/youtube-description.txt` next to the final, with chapters that match the final, his picked title, and the voice pass.
   - With any other profile, that skill's template and voice cards are Ryan's, so don't use it. Offer the chapter list instead: invoke `analyze-stream-recording` with `<raw path> --window <start> <end>` and give them its Chapters section.
   - Then make the final's thumbnails, as in **Thumbnails** steps 1 to 5 below: landscape, 3 options, each polished once with vidIQ. Then run **Thumbnails** step 6 for every video, the final and the shorts.

10. **When he asks about the final render,** check it:
   ```bash
   curl -s http://127.0.0.1:<port>/api/render
   ```
   On `done`, give him the `output` path. On `error`, report `error` as-is. Leave the server running while he's still using the page. When he's done with the page and the shorts, stop the background server task.

## Thumbnails

For the final and each rendered short, after its title is picked. They're built from real frames of the person, so the face is always theirs; vidIQ only polishes a finished composite. Without `swiftc` (`thumbs.py` says so), skip thumbnails and tell them to run `xcode-select --install`. Without the vidIQ tools, make the plain ones only and say why.

1. **Frames.** Get `shift`, `edit.in` and `edit.out` from `/api/shorts`. For the final, pass `edit.in` and `edit.out` as they are (they're on the video clock already):
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/thumbs.py frames "<raw path>" <edit.in> <edit.out> <scratchpad>/frames-final
   ```
   For a short, pass the clip's `start` and `end` from `shorts/shorts.json` as they are (`HH:MM:SS.xx` is fine), plus `--shift <shift>`, since they're on the transcript clock:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/thumbs.py frames "<raw path>" <start> <end> <scratchpad>/frames-<n> --shift <shift>
   ```
   It prints the 8 frames with the clearest face, best first, each with its face `box`. It refuses a cloud-only raw; tell them to download it. Look at the frames with Read and pick the ones with the strongest expression that fits the title (surprised, thinking, excited): 3 for the final, 2 per short.
2. **Text.** Write 2 or 3 words for each thumbnail in the style of their thumbnails ("FINDING CORE BUGS!", "NO DOCKER!"), not the title itself, and run the em-dash and AI-ism scan on them. Use different words on each option.
3. **Compose** each one into the `thumbnails/` folder next to the video, named after the video's current file name without `.mp4` (`<stem>`), numbered from 1:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/thumbs.py compose "<frame>" <x> <y> <w> <h> landscape "<video dir>/thumbnails/<stem>-<k>-plain.jpg" --line "Core bugs!" --profile <name>
   ```
   Use `portrait` for a short. A second `--line` adds a line (3 at most; the first is yellow). `--side left|right` puts the person on that side; by default they go left when a line is long. `--background <frame>` uses another frame behind them. Look at each result with Read before posting it.
4. **Post** them, from a JSON file in the scratchpad:
   ```bash
   curl -s -X POST http://127.0.0.1:<port>/api/thumbs -H 'Content-Type: application/json' --data @<file>
   ```
   with `{"final": [{"file": "<abs path>", "kind": "plain"}]}` or `{"shorts": {"<n>": [...]}}`. Tell them the options are under the final's title and in each short's editor, and that **Use this thumbnail** saves it as `<video name>.jpg` next to the video.
5. **Polish the final's options** (with vidIQ). Check `mcp__vidiq__vidiq_balance` and say what it will spend: "Polishing 3 thumbnails, 66 credits." Don't wait for an OK. For each plain option:
   - Upload it: call `mcp__vidiq__vidiq_upload_image` with no `image` to get an `uploadUrl` and `transferId`, run `curl -sS -X PUT --data-binary @"<file>" "<uploadUrl>"`, then call it again with the `transferId` for the `imageId`.
   - Call `mcp__vidiq__vidiq_refine_thumbnail` with `sourceThumbnail` set to the `imageId`, `orientation: "landscape"`, `title` set to the picked title, `referenceImages` set to the profile's `thumbnail_refs` as `https://i.ytimg.com/vi/<id>/maxresdefault.jpg` (leave it out if the profile has none), and these instructions: "Keep the person's face, expression and the text exactly as they are. Make the background richer and the lighting punchier, in the style of the reference thumbnails."
   - Poll `mcp__vidiq__vidiq_job_poll` until it's `completed`, download its `imageUrl` with curl to `<stem>-<k>-vidiq.jpg` in the same folder, and post it with `"kind": "vidiq"`.
6. **Answer requests**, once the final's options are up. Wait with Monitor and an until-loop (check every 30 s) on `curl -s http://127.0.0.1:<port>/api/thumbs`, stopping when `requests` isn't empty or every target you posted is in `picked`. Answer each request as below, then wait again. When every target is picked and `requests` is empty, check `/api/thumbs` once more, then stop and tell him to ask you if he wants another change, since the page keeps taking requests but nothing is watching. If he says he's done with thumbnails, stop even if some aren't picked. For each request:
   - `"polish": true`: polish that option as in 5 (`portrait` for a short), 22 credits.
   - A `change` on a vidIQ option: `mcp__vidiq__vidiq_refine_thumbnail` on that file (upload it first) with their words as the instructions, plus "Keep the person's face exactly as it is."
   - A `change` on a plain option: if it's about the words, the side or the frame, rebuild it with `thumbs.py compose` (free). If it asks for a look only vidIQ gives ("add a glow"), polish it with their words added to the instructions.
   - Save the result as the next number (`<stem>-<k>-plain.jpg` or `-vidiq.jpg`), post it, then mark the request done: `curl -s -X POST http://127.0.0.1:<port>/api/thumbs/done -H 'Content-Type: application/json' -d '{"id": <id>}'`.
   - A title picked later renames the video, its `.jpg` and its options; read the paths from `/api/thumbs`, not from memory.

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

- The "Claude needs you" banner: Claude Code hooks run `scripts/attention.py` whenever Claude waits on Ryan in the terminal (a permission prompt, a question box, or a turn that ends by asking him something) and again when he answers. The hooks live in the devrel plugin's `hooks/hooks.json` for a plugin install, and in `~/.claude/settings.json` on Ryan's Mac (his skills load from the repo, not the plugin). They are not in this file's frontmatter: hooks there never registered. Each page server registers itself, with the Claude session that started it, in `~/Library/Caches/stream-trim/servers/`, and a hook only reaches pages from its own session. Every call is logged to `~/Library/Caches/stream-trim/servers/hooks.log` (time, event, session, pages reached), so a missing banner can be traced.
- `SETUP.md` is the overview for anyone setting this up: what's required, what's optional (viDIQ), what only runs for Ryan, and what first-run setup asks. Point a new user to it.
- Titles picked on the page: `:` becomes ` -` and `/` becomes `-` in the file name, since Finder won't take them. Picking again renames from the current name, and a name that's already taken is refused. The cache's `edit.json` and `shorts/shorts.json` follow each rename, so the page, the Streams tab and re-renders all find the renamed files.
- The page's Streams tab lists every recording with a cache, newest first: whether the raw is local, the final, shorts and description, and the cache size, with Show in Finder buttons and a Copy command button for `/stream-trim` on that recording. It's built from the caches, so deleting a cache folder takes its stream off the list. Show in Finder is also next to Render once the final exists, and in the Shorts tab.
- The cache (preview, waveform, analysis) is in `~/Library/Caches/stream-trim/`, never next to the recording. That keeps a 1 GB preview out of Google Drive. Deleting the folder is safe.
- Default In is 0.5 s before the first word, but only when the mic is silent for at least 60 s from the start (Starting Soon). Otherwise In is 0. Default Out is 1 s after the last word.
- File ownership for shorts: Claude writes `shorts/candidates.json`, and only that. The page writes `shorts/shorts.json` with Ryan's picks, which keeps `shorts.py ... all` meaning "what Ryan picked". To change a clip after a render, edit `shorts.json` and re-render as in `stream-shorts`.
- Shorts use the same mix and voice chain as the final, through `scripts/short_audio.py` (`"mix_audio"` in `shorts.json`), at the profile's `shorts_loudness` (Ryan's: -14 LUFS, the level Shorts, Reels and TikTok play at). The page also writes the profile's mic track, lags, caption font and layouts file into `shorts.json`. `/stream-shorts` on its own still uses the mic alone.
- The prepared cache remembers its profile. Running the same recording with another profile prepares it again.
- The page's layout previews go in the cache, not in `shorts/`.
- `scripts/compare.py` is the blind A/B tool used to tune `chain.json` against a Premiere render. It isn't part of the normal flow.
