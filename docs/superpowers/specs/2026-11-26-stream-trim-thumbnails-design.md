# stream-trim: thumbnails

Status: approved by Ryan, 2026-11-26.

## Intent

Today Ryan uploads the final to YouTube, then uses the vidIQ extension to generate thumbnails there. He usually has to ask for many changes because the face in them doesn't look like him. He wants stream-trim to make thumbnails for the main video and for each short, as seamlessly as the title picks work now, and save them next to the videos: the main video's in `renders/`, each short's in `shorts/`.

## Goals

- A thumbnail for the final and for every rendered short, with no extra commands: it happens after the titles are picked.
- The face is always Ryan's real face, taken from the stream.
- The look matches his channel: his face on one side with a strong expression, 2 or 3 huge words in heavy yellow and white type with a dark outline, a dimmed screen grab or dark blue tech background behind.
- He picks on the page, and can type a change and get a new version without leaving the page.
- The picked file sits next to its video with the same name, and follows the video when a title pick renames it.

## Non-goals

- Uploading the thumbnail to YouTube. He uploads by hand. (vidIQ's `update_video_thumbnail` could do it later; not in this change.)
- Scoring with `vidiq_score_thumbnail`: it needs a live video ID, so it can't run before upload.
- Thumbnails for other platforms, A/B sets, or a general image editor on the page.

## Anti-goals

- A thumbnail whose face is redrawn by AI and doesn't look like him. That's the problem being solved; a polished option that drifts must never replace the plain one.
- Downloading a cloud-only raw. Frames come from the final and the rendered shorts, which are local.
- Spending vidIQ credits Ryan didn't expect.

## Constraints

- macOS only, like the rest of stream-trim. No new installs: background removal uses Apple's Vision framework (`VNGenerateForegroundInstanceMaskRequest`, macOS 14+) through a small Swift script, compiled once with the Swift that ships with the Xcode tools and cached in `~/Library/Caches/stream-trim/`. Compositing uses Pillow, already installed.
- The page server can't call vidIQ. Only Claude in the session can, so every vidIQ step is Claude's, using the same post-and-wait loop as titles (`/api/titles` + Monitor).
- YouTube sizes: long-form 1280x720 JPEG; Shorts 1080x1920 (9:16) JPEG; both under 2 MB. Custom Shorts thumbnails exist since July 2026 for Partner Program channels, desktop Studio only.
- Ryan's face, as stills, is sent to vidIQ. He chose that by choosing approach C.
- Cost: `refine_thumbnail` is 22 credits per call; `upload_image` is free.

## Approaches

- **A. vidIQ generates from scratch with face references.** Closest to the extension's look, but the face is still redrawn, which is the current problem.
- **B. Local composite from real frames, no AI.** Always his face, free and instant, but plainer: no glow, no invented UI cards, only expressions he actually made.
- **C. B, then vidIQ edits the composite (picked).** The composite is the source image for `vidiq_refine_thumbnail`, so vidIQ edits a real photo instead of drawing one. The plain composite is always kept as an option. Ryan picked C because it goes after "doesn't look like me" and still gets the polished look.

## Design

### When it runs

- `youtube-stream-description` already waits for `picked.final` before it returns (its step 8 with `--titles-url`), so the final's thumbnails start after that skill returns in step 9.

- **Final:** in step 9, once `picked.final` is set on `/api/titles`. The thumbnail text and frame choice need the title.
- **Shorts:** in step 8, once each short's title is picked.
- Without vidIQ, only the plain composites are made, and Claude says why.
- Without Swift (no Xcode command-line tools), thumbnails are skipped and Claude says to run `xcode-select --install`. `SETUP.md` lists it as optional. *(My call.)*
- A short re-rendered after a change keeps its thumbnail options and pick. Ryan can ask for new ones in the editor. *(My call.)*

### Making one thumbnail

1. **Frames.** A new script, `scripts/thumbs.py`, pulls about 30 evenly spaced frames from the raw over the video's range: the edit's In to Out for the final, the short's start to end for a short. The raw is already local by this point, since the final and the shorts were rendered from it, but the script checks the cloud-only flag first and stops with a message if it's set. It doesn't trust a fixed cam box, because scenes change during a stream: Vision finds the face anywhere in the full 1920x1080 frame (`VNDetectFaceRectanglesRequest`), ranks frames by face-capture quality (`VNDetectFaceCaptureQualityRequest`), and drops frames with no face. It writes the top 8 full frames to a temp folder, with the face box for each. *(Builder check; my call: the raw, not the final or the rendered short, so short thumbnails aren't limited to what the short's layout shows, and a `me` short still has a screen to use as background.)*
2. **Claude picks.** Claude looks at those 8 with Read and picks the 3 with the clearest, strongest expressions that fit the title (surprised, thinking, excited). For a short, 2.
3. **Cutout.** The Swift helper runs Vision person segmentation on the picked full frame and keeps only the instance under the face box, so a guest or a face on screen isn't included. It writes a PNG with transparency, cropped to Ryan.
4. **Text.** Claude writes 2 or 3 words per thumbnail, in his thumbnail style ("FINDING CORE BUGS!", "NO DOCKER!"), not the title itself. The em-dash and AI-ism scan runs on them.
5. **Composite.** `thumbs.py compose` builds it with Pillow:
   - Background: the same frame with Ryan removed, blurred, dimmed and tinted dark blue, or another frame from the range if Claude picks one with more on screen.
   - Ryan's cutout on one side, filling most of the height. Long-form: right side by default, left if the text is long. Shorts: bottom half.
   - Text on the other side (long-form) or top (shorts) in Inter Black, upper case, first line yellow and the rest white, with a dark outline and soft shadow. The font comes from the profile (`thumbnail_font`); Ryan's is Inter Black.
   - Saved as `thumbnails/<stem>-<k>-plain.jpg` in the video's folder.
6. **Polish.** Claude uploads each composite to vidIQ (`upload_image`, PUT to its upload URL), then calls `vidiq_refine_thumbnail` with the composite as `sourceThumbnail`, the title, `orientation` (landscape or portrait), 3 of Ryan's recent thumbnails as `referenceImages`, and instructions that keep the face and text and punch up the background and lighting. When the job finishes, the result is downloaded to `thumbnails/<stem>-<k>-vidiq.jpg`.

### On the page

- **Final:** a Thumbnails row under the final's title picks. **Shorts:** the same row in the editor for a rendered short.
- Each option is a card with the image, a "Plain" or "vidIQ" tag, **Use this thumbnail**, and a box: "Ask for a change". Sending a change queues a request; the card shows "Waiting for Claude".
- **Use this thumbnail** copies that option to `<video name>.jpg` next to the video and marks it picked. Picking again replaces it.
- When a title pick renames a video, its `.jpg` and its `thumbnails/` options are renamed with it.
- Show in Finder on the thumbnail.

### Server API

Modelled on `/api/titles`:

- `POST /api/thumbs` (Claude): `{"final": [{"file": "<abs path>", "kind": "plain"|"vidiq"}], "shorts": {"<n>": [...]}}`. Adds options; doesn't remove old ones.
- `GET /api/thumbs`: options, `picked` per target, and `requests`: `[{"id", "target", "file", "text"}]` not yet answered.
- `POST /api/thumb` (page): `{"target": "final"|n, "file": ...}` to pick, `{"target", "file", "change": "text"}` to queue a change, or `{"target", "file", "polish": true}` to queue a vidIQ polish of a plain option.
- `POST /api/thumbs/done` (Claude): `{"id": ...}` once a change has its new option posted.

### Changes loop

After posting options, Claude waits with Monitor (every 30 s) on `/api/thumbs` until every target has `picked` or a request appears. For a request on a vidIQ option, it calls `refine_thumbnail` on that option with Ryan's words. On a plain option, it treats the words as layout or text changes and rebuilds with `thumbs.py compose` (free) unless the change needs vidIQ ("add a glow"). It posts the new option and marks the request done. It stops waiting when every target is picked.

### Credits

Ryan's call: polish the final automatically, polish shorts only on request.

- Final: 3 composites, each polished once automatically: 66 credits.
- Each short: 2 plain composites, no automatic polish. Each plain card has a **Polish with vidIQ** button (22 credits per press), queued as a request like a change.
- Each change through vidIQ: 22 credits. Changes to a plain option that only need a rebuild are free.
- Claude checks `vidiq_balance` (free) before the final's polish and says what it will spend, without waiting for an OK.

### Profiles

New optional keys:

- `thumbnail_font`: `{"name", "file"}`. Ryan's: Inter Black from `~/Library/Fonts`.
- `thumbnail_refs`: YouTube video IDs whose thumbnails are the style references. Ryan's: `BBI7WONLdOc`, `ISTvqYVvi4Y`, `M6SnB2m3-DM`.
- Missing keys: a bundled default font, no style references.

### Tests

- `thumbs.py`: frame times for a range; refuses a cloud-only raw; compose output size, mode and file size for both orientations; text wrapping into 2 or 3 lines.
- Swift helper: a fixture frame with a face gives a face box and a mask that isn't empty; a frame with no face gives nothing back; with two people, the mask covers only the one under the given face box.
- Server: `/api/thumbs` validation, pick copies the file, change requests queue and clear, renames carry the `.jpg` and options.
- `test_page.py`: the Thumbnails row, Use this thumbnail and Ask for a change exist.

## Left to the builder

- The exact Vision calls and the Swift helper's command-line shape.
- Text sizing and the outline and shadow values, tuned by eye against the reference thumbnails.
- Card styling within the page's existing look.

## Follow-up (2026-11-26, after the first real run)

Ryan found the plain composite boring: a small cutout and one block of text. The composite now has three styles (`label`, `card`, `stack`) with the person drawn big (face about 40% of the height) on a warm glow, a vignetted background, tilted yellow and red label boxes, and in `card` a sharp tilted card of the screen from that frame. The final gets one of each. The vidIQ polish brief now asks for dynamic 3D text (same words) and one icon or logo Claude picks from the topic, such as a crossed-out Premiere icon; vidIQ draws it. A folder of exact logo PNGs is the fallback if a drawn one comes out wrong.
