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
