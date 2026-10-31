---
name: stream-shorts
description: Cut vertical shorts (9:16, facecam on top, screen below, all-caps captions that whip in a few words at a time) from a local live-stream recording. Proposes a shortlist of standalone moments, then renders the ones Ryan picks into a shorts/ folder next to the recording. Use to make shorts, clips, reels, or highlights from a stream, instead of Firecut, Opus Clip, or Descript.
allowed-tools: Bash(bash *) Bash(python3 *) Bash(ffmpeg *) Bash(ffprobe *) Read Write Edit
---

# Stream Shorts

Input: `$ARGUMENTS` is the path to a stream recording. The raw OBS mp4 and stream-prep's `<name>-edit.mp4` both work; the render script detects which one it has and lines the mic up either way.

Everything about a clip lives in `shorts/shorts.json` next to the recording, and `scripts/shorts.py` previews, captions, and renders from it. Don't pass clip times to `render-short.sh` by hand.

## Steps

1. **Check the tools.** Transcribing needs `mlx_whisper` (Apple Silicon only), and transcribing and rendering both need an ffmpeg with libass (for burning in captions):
   ```bash
   if ! command -v ffmpeg >/dev/null; then echo "ffmpeg: MISSING"; elif ffmpeg -hide_banner -filters 2>/dev/null | grep -qw ass; then echo "ffmpeg: OK"; else echo "ffmpeg: NO_LIBASS"; fi; command -v mlx_whisper >/dev/null && echo "mlx_whisper: OK" || echo "mlx_whisper: MISSING ($(uname -m))"
   ```
   If both print `OK`, go to step 2. Otherwise ask Ryan with one AskUserQuestion whether to install what's missing now. Say which tools and why each is needed, and that it can take several minutes. The commands:
   - `ffmpeg: MISSING`: `brew tap homebrew-ffmpeg/ffmpeg && brew install homebrew-ffmpeg/ffmpeg/ffmpeg`
   - `ffmpeg: NO_LIBASS`: the same, with `brew uninstall ffmpeg && ` in front (the stock Homebrew ffmpeg has no libass).
   - `mlx_whisper: MISSING (arm64)`: `uv tool install mlx-whisper`. If `command -v uv` finds nothing, put `brew install uv && ` in front.
   - `mlx_whisper: MISSING` on anything other than `arm64`: it can't be installed; this Mac isn't Apple Silicon. Stop and tell Ryan.

   If he says yes, check `command -v brew` first when a command uses it. Without Homebrew, stop and tell him to install it from https://brew.sh. Run each install with `run_in_background` (the ffmpeg build can outlast the foreground timeout), wait for its exit notification, then run the check again. If `mlx_whisper` is installed but still not found, run `uv tool update-shell` and check again. On two `OK`s, continue to step 2. If an install fails, report the last lines of its output and stop.

   If he says no, stop and give him the commands to run himself with `!`.

2. **Get the shortlist.** Invoke the `find-stream-shorts` skill with the recording path. It runs in a fork and returns a `Shortlist` table, a `Words` path and `Transcript gaps`. If it returns an `ERROR:` line, report it and stop. Show Ryan the table as-is, plus any gaps, and ask which to render. Ryan can answer with numbers ("1, 4, 7") and nudges ("start 4 two seconds later").

3. **Save the picks** to `shorts/shorts.json` next to the recording (create the folder). Keep any clips already in the file. If the file is an old bare list of clips, wrap it in the shape below.
   ```json
   {
     "recording": "<absolute recording path>",
     "words": "<the Words path>",
     "clips": [
       {"file": "01-why-the-block-never-rerenders.mp4", "start": "00:41:12.40", "end": "00:41:55.10", "hook": "..."}
     ]
   }
   ```
   Number files in pick order, with a short slug from the hook. Optional clip keys:
   - `layout`: a name from `scripts/layouts.json`. Leave it out for the default, `coding-rebrand`.
   - `pan_x`: slides the layout's panning band left or right. The range depends on the layout; for `coding-rebrand` it's the screen crop, 0 = left edge, 882 = right edge, default 200. `screen_x` is the old name and still works.
   - `fixes`: caption fixes for this clip, `{"heard": "meant"}`.
   - `skip`: the reason a clip isn't rendered. Clips with `skip` set are left out of `all`.

4. **Preview the layout** for each pick, then look at each jpg with Read:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/shorts.py --preview "<recording dir>/shorts/shorts.json" all
   ```
   This writes `<NN>-<slug>.jpg` next to each clip.
   - If the bottom band cuts off the thing being talked about, set `pan_x` on that clip and preview it again (`... shorts.json 4`).
   - If the frame shows a different scene from the layout's, set `layout` to one that fits. For example, use `center` for full-screen cam. If no layout fits, see **Adding a layout**. If the scene isn't worth a short (BRB, a starting-soon screen), set `skip` with the reason and tell Ryan.
   - Delete the preview jpgs once the clips are rendered.

5. **Check the captions** before rendering. This step needs no ffmpeg and takes seconds:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/shorts.py --captions "<recording dir>/shorts/shorts.json" all
   ```
   Show Ryan the output with likely mishearings marked: names, WordPress APIs, product names, anything that reads wrong. Put each fix he approves in that clip's `fixes`. If a mishearing will come back on other streams (a term Whisper always gets wrong), suggest adding it to `scripts/glossary.json` in the claude-skills repo instead. Fixes match whole words and ignore case and punctuation, and the captions are uppercased, so casing fixes do nothing.

6. **Render** one clip per Bash call, in the **foreground** with the Bash `timeout` at `600000`:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/scripts/shorts.py "<recording dir>/shorts/shorts.json" <NN>
   ```
   It prints `SHORT: <path>` on success. Report an `ERROR:` line as-is.

7. **Report** the output paths and anything skipped, with the reasons.

## Re-rendering

To nudge a clip later, edit its entry in `shorts/shorts.json` and run step 6 for that clip number. The transcript is cached, so nothing needs to be transcribed again. `--dry-run` prints the ffmpeg command without running it.

## Adding a layout

A layout is a stack of bands, top to bottom. Each band crops a box from the source, in 1920x1080 pixels, and scales it to 1080 wide. The band heights add up to 1920, and each crop must have its band's shape (`layout.py` rejects a layout that would stretch). One band can have a `pan` range for `pan_x`. `caption_y` is where the captions sit, usually on a seam between bands.

1. Grab a full frame at the clip's midpoint, scaled to the 1920x1080 coordinate space, and look at it with Read:
   ```bash
   ffmpeg -nostdin -loglevel error -y -ss <seconds> -i "<recording>" -frames:v 1 -vf scale=1920:1080 "<recording dir>/shorts/frame.jpg"
   ```
2. Work out the boxes, then write them to `layouts.json` next to `shorts.json`. Layouts there are only for this recording and can override the built-in ones:
   ```json
   {"layouts": {"guest": {"description": "...", "bands": [{"name": "cam", "crop": [w, h, x, y], "height": 900}, ...], "caption_y": 900}}}
   ```
3. Preview, adjust, and delete `frame.jpg` when done. If Ryan will use the scene again, offer to move the layout into `scripts/layouts.json` in the claude-skills repo (and bump the plugin version).

## Not covered

- No titles, descriptions or posting. Post copy goes through `write-social-post`.
