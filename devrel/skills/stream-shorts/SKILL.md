---
name: stream-shorts
description: Cut vertical shorts (9:16, facecam on top, screen below, word-by-word captions) from a local live-stream recording. Proposes a shortlist of standalone moments, then renders the ones Ryan picks into a shorts/ folder next to the recording. Use to make shorts, clips, reels, or highlights from a stream, instead of Firecut, Opus Clip, or Descript.
allowed-tools: Bash(bash *) Bash(python3 *) Bash(ffmpeg *) Bash(ffprobe *) Read Write
---

# Stream Shorts

Input: `$ARGUMENTS` is the path to a stream recording. The raw OBS mp4 and stream-prep's `<name>-edit.mp4` both work; the render script detects which one it has and lines the mic up either way.

Layout and captions are fixed for the OBS **"Coding - Rebrand"** scene. See the header of `scripts/render-short.sh` for the crop boxes.

## Steps

1. **Check ffmpeg.** Run `ffmpeg -hide_banner -filters | grep -w ass`. If nothing prints, stop and give Ryan this install command to run (do not run it yourself):
   ```
   brew uninstall ffmpeg && brew tap homebrew-ffmpeg/ffmpeg && brew install homebrew-ffmpeg/ffmpeg/ffmpeg
   ```

2. **Get the shortlist.** Invoke the `find-stream-shorts` skill with the recording path. It runs in a fork and returns a `Shortlist` table, a `Words` path and `Transcript gaps`. If it returns an `ERROR:` line, report it and stop. Show Ryan the table as-is, plus any gaps, and ask which to render. Ryan can answer with numbers ("1, 4, 7") and nudges ("start 4 two seconds later").

3. **Save the picks** to `shorts/shorts.json` next to the recording (create the folder). Keep anything already in the file. One entry per pick:
   ```json
   {"file": "01-why-the-block-never-rerenders.mp4", "start": "00:41:12.40", "end": "00:41:55.10", "hook": "...", "screen_x": 200}
   ```
   Number files in pick order, with a short slug from the hook.

4. **Preview each pick.** Render the layout frame and look at it with Read:
   ```bash
   bash ${CLAUDE_SKILL_DIR}/scripts/render-short.sh --preview "<recording>" "<words>" <start> <end> "<recording dir>/shorts/<NN>-<slug>.jpg"
   ```
   - If the top band doesn't show Ryan's face (another scene was live, such as BRB, a guest, or full-screen cam), do not render the clip. Tell Ryan which one and why.
   - If the bottom band cuts off the thing being talked about, preview again with `--screen-x` (0 = left edge of the screen, 882 = right edge, default 200) and save the value that works in `shorts.json`.
   - Delete the preview jpg once the clip is rendered.

5. **Render** each pick that passed, in the **foreground** with the Bash `timeout` at `600000`:
   ```bash
   bash ${CLAUDE_SKILL_DIR}/scripts/render-short.sh [--screen-x N] "<recording>" "<words>" <start> <end> "<recording dir>/shorts/<NN>-<slug>.mp4"
   ```
   It prints `SHORT: <path>` on success. Report an `ERROR:` line as-is.

6. **Report** the output paths and anything skipped. Remind Ryan that captions are Whisper's words as-is, so names and jargon need a look before posting.

## Re-rendering

To nudge a clip later, edit its entry in `shorts/shorts.json` and run step 5 for that entry. The transcript is cached, so nothing needs to be transcribed again.

## Not covered

- Other OBS scenes (guest, Watch Party, full-screen cam) have no layout preset.
- No titles, descriptions or posting. Post copy goes through `write-social-post`.
