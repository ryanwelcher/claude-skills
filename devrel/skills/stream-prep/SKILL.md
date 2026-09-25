---
name: stream-prep
description: Prep an OBS stream recording for Premiere so it imports clean and in sync. Drops the Full Mix and Spotify audio tracks, pulls the mic track 9 frames earlier, keeps the other tracks separate, and writes <name>-edit.mp4 next to the original. Use to prep, clean up, or fix audio sync on a stream recording before editing.
allowed-tools: Bash(bash *)
---

# Stream Prep

Input: `$ARGUMENTS` is one or more paths to OBS recordings (mp4/mov/mkv).

## Default track layout (OBS "Rebrand" scene collection)

| Track | Source | Default |
|---|---|---|
| 1 | Full Mix | dropped |
| 2 | Mic (Rode Shotgun / Yeti) | kept, pulled 9 frames earlier |
| 3 | Guest + StreamElements overlay | kept |
| 4 | Spotify | dropped |
| 5 | Theme song | kept |
| 6 | Firebot | kept |

## Steps

1. Run the script in the **foreground** with the Bash tool's `timeout` set to `600000`. Quote each path:
   ```bash
   bash ${CLAUDE_SKILL_DIR}/scripts/prep-stream.sh "<file>" ["<file>" ...]
   ```
   Add flags only when the user asks for something other than the defaults:
   - `--drop 1,4`: OBS track numbers to remove
   - `--shift 2`: OBS track number to pull earlier
   - `--frames 9`: how many frames earlier. The frame rate is read from the file.

2. If it prints an `ERROR:` line, report it as-is. Do not delete or overwrite an existing `-edit.mp4` unless the user asks.

3. On success, tell the user the output path(s) and which tracks were kept. In Premiere the kept tracks show up as A1–A4 in the order 2, 3, 5, 6, with the mic on A1.

The original recording is never modified. Video and the untouched audio tracks are copied as-is. Only the mic track is re-encoded (AAC 320k), which is what makes the shift exact to the sample.

## Premiere plugin (in-Premiere alternative)

`premiere-plugin/` holds a headless UXP plugin that does the same prep inside Premiere 2026 (26.3+) on the **original** recording, with no new media file. It creates `<name>.prproj` next to the video, imports it, builds a sequence, removes the A1/A4 clips, pulls A2 9 frames earlier, and names the tracks (Mic, Guest, Theme Song, Firebot).

- Trigger it from Finder: right-click the recording, then **Quick Actions > Open in Premiere (stream)**. The Quick Action writes a job to `~/Library/Application Support/stream-prep/jobs/` and opens Premiere. The plugin picks the job up and a notification reports the result.
- Install or update: `premiere-plugin/build.sh --install`, then restart Premiere. The plugin only loads at launch.
- Log: `~/Library/Logs/stream-prep-ppro.log`.
- Intro cut: the Quick Action runs ffmpeg `silencedetect` on OBS track 2 (the mic) and passes the first-sound time as `voiceStart`. If the mic is silent for at least 60 s from the start, the plugin trims every clip so your first word lands 1 s into the timeline (`LEAD_IN`). Otherwise nothing is trimmed. The source media is untouched, so the intro can be dragged back.
- The track layout and offset are constants at the top of `premiere-plugin/index.js`.
- Premiere checks every action in a transaction against the timeline as it was before the transaction, so a clip at 0 can't be moved left. The plugin pushes everything out 1 s, resyncs the mic, and pulls everything back, which takes four undo steps.
