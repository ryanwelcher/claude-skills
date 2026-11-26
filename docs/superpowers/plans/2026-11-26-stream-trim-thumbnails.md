# stream-trim thumbnails Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thumbnails for the final and each short, built from real frames of Ryan, picked on the stream-trim page and saved next to each video.

**Architecture:**
- A Swift helper does the Apple Vision work: face boxes, face quality and person cutout.
- `thumbs.py` pulls frames with ffmpeg and composites them with Pillow.
- The page server keeps the options, picks and change requests in the cache's `thumbs.json`, mirroring `titles.json`.
- Claude does every vidIQ step from SKILL.md.

**Tech Stack:** Python 3 stdlib + Pillow, Swift (Vision, AppKit) via `swiftc`, ffmpeg, the existing page.html/server.py.

**Spec:** `docs/superpowers/specs/2026-11-26-stream-trim-thumbnails-design.md`

## Global Constraints

- macOS only. No new installs beyond Xcode command-line tools (`swiftc`) and Pillow (already present).
- Never read a cloud-only raw: check `profiles.cloud_only(raw)` before any ffmpeg read.
- Sizes: long-form 1280x720 JPEG; Shorts 1080x1920 JPEG; each under 2 MB.
- Picked file: `<video stem>.jpg` next to the video. Options: `thumbnails/<stem>-<k>-plain.jpg` and `-<k>-vidiq.jpg` in the video's folder.
- Font: the profile's `thumbnail_font` (`{"name", "file"}`); Ryan's is Inter Black (`Inter_18pt-Black.ttf`, in `~/Library/Fonts`). Missing key → `/System/Library/Fonts/Supplemental/Arial Black.ttf`.
- Text: upper case, first line yellow `#FFD400`, the rest white, dark outline, soft shadow.
- No em-dashes or AI-isms in user-facing copy. Push to trunk; no branches.
- Credits: final polished automatically (3 x 22); shorts plain only (2 each), with **Polish with vidIQ** on request.

## Review Focus

1. A frame with two people (guest on cam, a face on screen): the cutout must be the person under the chosen face box only. Test: Task 1 `test_cutout_two_people`.
2. A title pick after thumbnails exist: the picked `.jpg` and the `thumbnails/` options must follow the rename, or the page loses them. Test: Task 3 `test_title_pick_renames_thumbs`.
3. Long thumbnail text (one word of 14 letters, or 4 words): it must shrink to fit, not run off the image. Test: Task 2 `test_compose_long_text_fits`.
4. A raw that went cloud-only between renders: `thumbs.py frames` must refuse without reading it. Test: Task 2 `test_frames_refuses_cloud_only`.
5. A change request on an option that no longer exists (renamed or deleted): the server must refuse with 409, not queue a request Claude can't act on. Test: Task 3 `test_change_missing_file`.

---

### Task 1: Vision helper

**Files:**
- Create: `devrel/skills/stream-trim/scripts/vision.swift`, `devrel/skills/stream-trim/scripts/vision.py`
- Create: `devrel/skills/stream-trim/tests/fixtures/face.jpg` (a copy of Ryan's public thumbnail `BBI7WONLdOc` at 640x360, already saved locally this session from vidIQ)
- Test: `devrel/skills/stream-trim/tests/test_vision.py`

**Interfaces:**
- Produces:
  - `vision.binary() -> str`: compiles `vision.swift` with `swiftc -O` into `~/Library/Caches/stream-trim/vision-<sha1 of source>` if missing, and returns the path. Raises `vision.VisionError("thumbnails need the Xcode command-line tools: run xcode-select --install")` when `swiftc` isn't found.
  - `vision.faces(paths: list[str]) -> list[dict]`: one dict per input, in order: `{"path", "faces": [{"box": [x, y, w, h], "quality": float}]}`. The box is in pixels with a top-left origin.
  - `vision.cutout(image: str, face_box: list, out_png: str) -> list`: writes an RGBA PNG of only the person instance whose mask covers the centre of `face_box`, cropped to that person's bounding box. Returns the crop box `[x, y, w, h]` in source pixels. Raises `VisionError` if no person covers the face.
- The Swift CLI is `vision faces <img>...`, printing JSON lines, and `vision cutout <img> <x> <y> <w> <h> <out.png>`, printing the JSON crop box. It uses `VNDetectFaceRectanglesRequest`, `VNDetectFaceCaptureQualityRequest` and `VNGenerateForegroundInstanceMaskRequest`.

- [ ] **Step 1: Write the failing tests** in `test_vision.py`. Skip all of them if `shutil.which("swiftc")` is None.
  - `test_faces_finds_one`: `faces([fixture])` gives exactly one face, `quality > 0`, and a box centre within the right half (x > 320).
  - `test_faces_none`: a 640x360 flat grey JPEG gives `faces == []`.
  - `test_cutout_alpha`: the cutout PNG is mode RGBA, has transparent pixels (alpha 0) and opaque pixels (alpha 255), and the crop box contains the face box.
  - `test_cutout_two_people`: the fixture side by side with its mirror (1280x360). Cutting out with the right face's box gives a crop box whose x is >= 640.
  - `test_binary_cached`: two calls to `binary()` return the same path, and the second doesn't run `swiftc` (patch `subprocess.run` after the first call and assert it isn't called).
- [ ] **Step 2: Run, expect failures.** Run `cd devrel/skills/stream-trim && python3 -m unittest tests.test_vision -v`. Expected: ImportError, no module `vision`.
- [ ] **Step 3: Write `vision.swift` and `vision.py`.**
- [ ] **Step 4: Run, expect passes.** Same command. Expected: 5 tests OK.
- [ ] **Step 5: Commit.** `stream-trim: Vision helper for face boxes and cutouts`

### Task 2: thumbs.py frames and compose

**Files:**
- Create: `devrel/skills/stream-trim/scripts/thumbs.py`
- Test: `devrel/skills/stream-trim/tests/test_thumbs.py`

**Interfaces:**
- Consumes: `vision.faces`, `vision.cutout` and `profiles.cloud_only` from Task 1.
- Produces:
  - `thumbs.frame_times(start: float, end: float, count: int = 30) -> list[float]`: evenly spaced and strictly inside the range (the first at `start + step/2`).
  - `thumbs.frames(raw, start, end, outdir, count=30, keep=8) -> list[dict]`: grabs a frame at each time with `ffmpeg -ss t -i raw -frames:v 1`, runs `vision.faces`, drops frames with no face, and keeps the `keep` with the best top-face quality. Each is written as `<outdir>/frame-<t:.2f>.jpg`. Returns `[{"path", "t", "box", "quality"}]`, best first. Raises `ValueError("<raw> is only in the cloud ...")` when `cloud_only(raw)`.
  - `thumbs.compose(frame, face_box, lines, orientation, out, font=None, side=None, background=None) -> str`.
    - `orientation` is `"landscape"` (1280x720) or `"portrait"` (1080x1920).
    - `lines` is 1 to 3 strings, drawn upper case.
    - `side` is `"right"` or `"left"`, the side for the person in landscape. With None, it's left when the longest line is over 10 characters, else right.
    - `background` is an optional other frame path.
    - Writes a JPEG under 2 MB and returns `out`.
  - The CLI, for Claude:
    - `thumbs.py frames <raw> <start> <end> <outdir>` prints JSON.
    - `thumbs.py compose <frame> <x> <y> <w> <h> <orientation> <out> --line "..." [--line ...] [--side left|right] [--background <frame>] [--profile <name>]` prints the output path. The font comes from the profile.
- Background: the source frame (or `background`) covers the canvas, gets a Gaussian blur of radius 18, is darkened to 45% brightness, then gets a 35% overlay of `#0B1E3F`.
- Person: the cutout is scaled to 95% of canvas height (landscape) or 55% (portrait, bottom-aligned), and placed against its side.
- Text area: the other ~55% of width (landscape), or the top 40% (portrait). The font size starts at 150 px (landscape) or 170 px (portrait) and drops in 6 px steps until every line fits. The outline is `#111` with a 10 px stroke. The shadow is offset 6 px, blurred and 60% black.

- [ ] **Step 1: Write the failing tests:**
  - `test_frame_times`: `frame_times(10, 40, 3) == [15.0, 25.0, 35.0]`.
  - `test_frames_refuses_cloud_only`: patch `profiles.cloud_only` to return True, and patch `subprocess.run`. `frames(...)` raises ValueError mentioning "cloud", and `subprocess.run` isn't called.
  - `test_frames_ranks` (skip without swiftc): a 4 s mp4 made with ffmpeg that alternates the fixture image and grey (2 s each). `frames(mp4, 0, 4, tmp, count=4, keep=8)` returns only frames from the fixture half, best first.
  - `test_compose_landscape` (skip without swiftc): the output is 1280x720 JPEG, under 2 MB, and the top-left text area holds yellow pixels (R>200, G>180, B<80).
  - `test_compose_portrait` (skip without swiftc): the output is 1080x1920, and the bottom 30% holds pixels from the cutout (not the tinted background colour).
  - `test_compose_long_text_fits` (skip without swiftc): with `lines=["CONTRIBUTORTOOLKIT", "IS", "HERE"]`, no yellow pixel is in the outer 8 px border.
- [ ] **Step 2: Run, expect failures.** Run `python3 -m unittest tests.test_thumbs -v`. Expected: ImportError.
- [ ] **Step 3: Implement `thumbs.py`.**
- [ ] **Step 4: Run, expect passes.** Same command, expect OK. Then open one landscape and one portrait output with Read and check them by eye against the reference thumbnails.
- [ ] **Step 5: Commit.** `stream-trim: thumbs.py pulls frames of Ryan and composites thumbnails`

### Task 3: Server thumbnails API

**Files:**
- Modify: `devrel/skills/stream-trim/scripts/server.py` (a new `# -- thumbnails --` section after titles; routes in `do_GET`/`do_POST`; `pick_title` renames thumbnails)
- Test: `devrel/skills/stream-trim/tests/test_server.py`

**Interfaces:**
- State lives in `<cache>/thumbs.json`: `{"options": {"final"|"<n>": [{"file": abs path, "kind": "plain"|"vidiq"}]}, "picked": {target: abs path of the picked .jpg}, "requests": [{"id": int, "target", "file", "change": str|null, "polish": bool}], "next_id": int}`.
- `GET /api/thumbs` returns `{"options", "picked", "requests"}`. `/api/shorts` also carries it as `"thumbs"`, the way it carries `"titles"`.
- `POST /api/thumbs` (Claude): `{"final": [...], "shorts": {"<n>": [...]}}`. Each file must exist and end in `.jpg`, and `kind` must be plain or vidiq. Options are appended; a duplicate file is ignored.
- `POST /api/thumb` (page):
  - `{"target", "file"}` picks: copies the file to `<video dir>/<video stem>.jpg` and returns `{"path"}`. The video is the final (`edit.output`) or short n's file in `shorts.json`.
  - `{"target", "file", "change": "text"}` queues a change (text 1 to 500 chars).
  - `{"target", "file", "polish": true}` queues a polish (plain options only).
  - Each queue call returns `{"id"}`.
  - 409 when the file isn't a current option or doesn't exist, or when the video isn't rendered yet.
- `POST /api/thumbs/done` (Claude): `{"id"}` removes the request. 404 if unknown.
- `pick_title` renames the thumbnails with the video: when a video is renamed from `A.mp4` to `B.mp4`, it moves `A.jpg` to `B.jpg` if present, and each option file whose basename starts with `A-` is moved to the same name starting with `B-`. The paths in `thumbs.json` are updated to match.

- [ ] **Step 1: Write the failing tests** in `test_server.py`, reusing `ServerTest`'s setup, with a rendered final faked the way the existing title tests do:
  - `test_post_thumbs_validates`: a missing file gives 400; kind `"x"` gives 400; a good post gives 200, and `GET /api/thumbs` lists it.
  - `test_pick_thumb_copies`: the pick returns `<final dir>/<final stem>.jpg`, the file exists, and its bytes match the option.
  - `test_change_and_polish_queue`: a change gives an id, and polish on a plain option gives an id. Polish on a vidiq option gives 400. `/api/thumbs/done` empties `requests`.
  - `test_change_missing_file`: a change on a file that isn't an option gives 409.
  - `test_title_pick_renames_thumbs`: with `final.jpg` and `thumbnails/final-1-plain.jpg` in place, picking the title "New Name" moves them to `New Name.jpg` and `thumbnails/New Name-1-plain.jpg`. `GET /api/thumbs` shows the new paths.
- [ ] **Step 2: Run, expect failures.** Run `python3 -m unittest tests.test_server -v 2>&1 | tail -20`. Expected: the 5 new tests fail with 404s.
- [ ] **Step 3: Implement it** in server.py.
- [ ] **Step 4: Run, expect passes.** Run the whole stream-trim suite: `python3 -m unittest discover -s tests`. Expected: OK.
- [ ] **Step 5: Commit.** `stream-trim: thumbnails API on the page server`

### Task 4: Thumbnails on the page

**Files:**
- Modify: `devrel/skills/stream-trim/scripts/page.html`. Add a `#final-thumbs` box after `#final-title`, and a `.thumb-box` in each card after `.title-box`.
- Modify: `devrel/skills/stream-trim/scripts/server.py`. Add `GET /thumb?path=<abs>`, which serves a `.jpg` only if it's a current option or a pick, else 404.
- Test: `devrel/skills/stream-trim/tests/test_page.py`, `tests/test_server.py`

**Interfaces:**
- Consumes: Task 3's API.
- Produces: `thumbBox(box, target, options, picked, requests)` in page.html, which draws one card per option:
  - The image (`/thumb?path=`), with portrait ones drawn smaller.
  - A tag: "Plain" or "vidIQ".
  - **Use this thumbnail**. The picked card gets the selected outline and a "Picked" label.
  - **Show in Finder**, through the existing `/api/reveal`.
  - **Polish with vidIQ** on plain cards.
  - An "Ask for a change" text box with Send.
  - An option with a pending request shows "Waiting for Claude".
- Empty states:
  - Final: "Thumbnails: Claude makes these after you pick the title."
  - Short: "Thumbnails for this short come from Claude after you pick its title."
- Redraws are keyed on JSON, the same as `titleBox`, so typing isn't wiped by the 4 s poll.

- [ ] **Step 1: Write the failing tests:**
  - `test_page.py`: page.html contains `id="final-thumbs"`, `thumb-box`, "Use this thumbnail", "Polish with vidIQ", "Ask for a change", "Waiting for Claude" and `/api/thumb`.
  - `test_server.py` `test_thumb_route_only_serves_options`: an option path gives 200 with `image/jpeg`; another jpg on disk gives 404.
- [ ] **Step 2: Run, expect failures.** Run `python3 -m unittest tests.test_page tests.test_server -v 2>&1 | tail -15`.
- [ ] **Step 3: Implement it.**
- [ ] **Step 4: Run, expect passes,** then check it in Chrome on the fake server (`scratchpad/fake/run.py`, with options posted to `/api/thumbs` from Task 2's outputs). Pick one, queue a change, and check that Show in Finder works.
- [ ] **Step 5: Commit.** `stream-trim: thumbnail picker on the page`

### Task 5: SKILL.md, profile, setup, versions

**Files:**
- Modify: `devrel/skills/stream-trim/SKILL.md`. In step 8, after the short titles are picked: plain thumbnails for each short. In step 9, after `youtube-stream-description` returns: the final's thumbnails and polish. Add a new "Thumbnail requests" loop.
- Modify: `devrel/skills/stream-trim/profiles/ryan-obs.json`. Add `"thumbnail_font": {"name": "Inter Black", "file": "Inter_18pt-Black.ttf"}` and `"thumbnail_refs": ["BBI7WONLdOc", "ISTvqYVvi4Y", "M6SnB2m3-DM"]`.
- Modify: `devrel/skills/stream-trim/scripts/profiles.py`. Both keys are optional, and validation rejects wrong types.
- Modify: `devrel/skills/stream-trim/SETUP.md`. Xcode command-line tools are optional, for thumbnails.
- Modify: `docs/superpowers/specs/2026-11-26-stream-trim-thumbnails-design.md` (only if something changed during the build), plus `README.md`, `devrel/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, which go to 1.55.0.
- Test: `tests/test_profiles.py`

The SKILL.md steps pin these values:
- **Frames:** `python3 ${CLAUDE_SKILL_DIR}/scripts/thumbs.py frames "<raw>" <start> <end> <scratch>`. For the final, the range is the edit's In/Out on the raw clock. For a short, it's the clip's start/end. Read the top 8 and pick 3 for the final, 2 per short.
- **Text:** 2 or 3 words per thumbnail in his thumbnail style, not the title. Run the em-dash and AI-ism scan on them.
- **Compose:** into `<video dir>/thumbnails/<stem>-<k>-plain.jpg`, then post them.
- **Final polish:**
  - Check `vidiq_balance` and say "Polishing 3 thumbnails, 66 credits".
  - For each composite, call `vidiq_upload_image` with no image, PUT the file to `uploadUrl` with curl, and call it again with `transferId`.
  - Call `vidiq_refine_thumbnail` with `sourceThumbnail` set to the imageId and `orientation: "landscape"`. Pass `title` (the picked title) and `referenceImages` (the profile's `thumbnail_refs` as `https://i.ytimg.com/vi/<id>/maxresdefault.jpg`). The instructions: "Keep the person's face, expression and the text exactly as they are. Make the background richer and the lighting punchier, in the style of the reference thumbnails."
  - Poll `vidiq_job_poll`, download `imageUrl` to `<stem>-<k>-vidiq.jpg`, and post it.
- **Requests loop:** Monitor every 30 s on `/api/thumbs` until every target has a pick and `requests` is empty.
  - A polish request runs the refine above. A change on a vidiq option is a refine with Ryan's words as the instructions.
  - A change on a plain option is rebuilt with `thumbs.py compose` when it's about text, side or frame. If it asks for a look only vidIQ can give, it's polished with his words added to the instructions.
  - Post the new option, then post `/api/thumbs/done`.
- **Fallbacks:** without vidIQ, plain only, and say why. Without swiftc, skip thumbnails and say to run `xcode-select --install`.

- [ ] **Step 1: Write the failing tests:** `test_profiles.py` `test_thumbnail_keys`. `ryan-obs` loads with `thumbnail_font.file == "Inter_18pt-Black.ttf"` and three refs; a profile with `"thumbnail_refs": "x"` raises ProfileError.
- [ ] **Step 2: Run, expect failures.**
- [ ] **Step 3: Implement it and write the docs.** Run the em-dash scan on the SKILL.md and SETUP.md changes.
- [ ] **Step 4: Run every suite** (stream-trim, stream-shorts, analyze-stream-recording). Expected: OK.
- [ ] **Step 5: Commit and push.** `stream-trim: thumbnails for the final and shorts, devrel 1.55.0`
