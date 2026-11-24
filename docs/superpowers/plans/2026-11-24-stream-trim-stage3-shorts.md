# stream-trim Stage 3: Shorts view Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** After the final render, the same local page shows Claude's shortlist of shorts from inside In/Out, lets Ryan nudge, pan, fix captions and pick, and renders the picks through `stream-shorts` with the same mix and voice chain as the long video.

**Architecture:** Claude (the skill session) finds and cleans the shortlist and writes `shorts/candidates.json`. The server reads it, runs `stream-shorts/scripts/shorts.py` for previews, captions and renders, and writes only Ryan's picks to `shorts/shorts.json`. `render-short.sh` gets an opt-in `--mix-audio SCRIPT` flag. stream-trim's `short_audio.py` renders the clip's audio (mix plus voice chain, two-pass loudness) to a WAV that replaces the mic-only track.

**Tech Stack:** Python 3 stdlib (http.server, subprocess, unittest), bash, ffmpeg with libass, plain HTML/JS.

**Spec:** `docs/superpowers/specs/2026-11-23-stream-trim-design.md` (section "Shorts", and "Stage 2 result").

## Global Constraints

- Python stdlib only, no new dependencies. The server binds 127.0.0.1 only.
- Run on its own, `/stream-shorts` behaves exactly as today. Without `--mix-audio`, `render-short.sh` prints the same ffmpeg command as before this plan.
- Output stays `shorts/` next to the recording. Previews and caption scratch files the page makes go in the cache (`<cache>/shorts-work/`), never in Google Drive.
- File ownership: Claude writes `shorts/candidates.json` and only that. The server writes `shorts/shorts.json` and never `candidates.json`.
- Clip `start`/`end` are on the transcript clock (the mic clock, 9 frames late), as in `stream-shorts`. The page shows times relative to the final edit: `t - shift - in`.
- The render pads a clip 0.2 s before `start` and 0.4 s after `end` (`render-short.sh`). A clip is "inside the edit" only if the padded span on the video clock is inside [In, Out].
- No em-dashes in page copy or SKILL.md prose.
- A new skill version is a bump in both `.claude-plugin/marketplace.json` and `devrel/.claude-plugin/plugin.json` (1.44.0 to 1.45.0).

## Review Focus

1. A candidate that starts less than 0.2 s after In or ends less than 0.4 s before Out. Its padded span crosses the edit, so it is shown as outside and can't be picked. Test: `test_inside_counts_padding` (Task 2).
2. A nudge that moves `start` past `end`, or a clip out of the edit. The server answers 400 with a reason and the page shows it. Test: `test_shorts_render_rejects_outside` (Task 3).
3. A `shorts/shorts.json` left from an earlier session. Its other clips are kept, and a clip with the same file name is replaced. Test: `test_merge_keeps_and_replaces` (Task 2).
4. `candidates.json` read mid-write, or with bad JSON. The page keeps waiting and the server answers 200 with `candidates: null` and an `error`, not a 500. Test: `test_shorts_bad_candidates` (Task 3).
5. The server restarts after the render. `edit.json` restores In/Out and the Shorts view. Test: `test_edit_survives_restart` (Task 3).

---

### Task 1: Opt-in mix audio for shorts

**Files:**
- Create: `devrel/skills/stream-trim/scripts/short_audio.py`
- Modify: `devrel/skills/stream-shorts/scripts/render-short.sh`, `devrel/skills/stream-shorts/scripts/shorts.py` (docstring + flag pass-through)
- Test: `devrel/skills/stream-trim/tests/test_short_audio.py`, `devrel/skills/stream-shorts/tests/test_mix_audio.py` (new folder)

**Interfaces:**
- Consumes: `audio_chain.render_stretch(raw, start_s, seconds, chain, out_wav)` (video clock start), `audio_chain.load_chain`.
- Produces:
  - `short_audio.SHORTS_LOUDNESS = {"I": -14, "TP": -1.5}`
  - `short_audio.shorts_chain(chain: dict) -> dict`: a deep copy with `loudness.I` and `loudness.TP` replaced, `LRA` kept.
  - CLI `python3 short_audio.py <raw> <video_start_s> <seconds> <out.wav>`, which loads `chain.json` next to the script. Exit 0 and silent on success. On failure, prints `ERROR: <msg>` to stderr and exits 1.
  - `render-short.sh --mix-audio SCRIPT`, render mode only (ignored by `--preview` and `--captions`).
  - `shorts.json` top-level key `"mix_audio": "<abs path>"`. When it's set, `shorts.py` passes `--mix-audio <path>`.

- [ ] **Step 1: Write the failing tests**

`test_short_audio.py`, using `make_mp4` from `test_measure`:
- `test_shorts_chain`: the result has `I == -14`, `TP == -1.5` and `LRA == chain["loudness"]["LRA"]`, and the input dict is unchanged.
- `test_cli_renders_clip`: a 6-track 12 s tone file, CLI `2 4 out.wav`. The result is 48000 Hz, 2 channels, duration 4 ± 0.01 s, and `measure.measure(out)["I"]` is within 1 LU of -14.
- `test_cli_error`: start 11, length 4 on the 12 s file. Exit 1, and stderr starts with `ERROR:`.

`test_mix_audio.py` (adds `../../stream-trim/tests` to `sys.path` for `make_mp4`). It skips if `~/Library/Fonts/Jost-SemiBold.ttf` or `/Library/Fonts/Jost-SemiBold.ttf` is missing, or if ffmpeg lacks `ass`. A words file `[[1.0, 1.4, "hello"], [1.5, 2.0, "world"]]`. All runs use `--dry-run` on clip `1 3`.
- `test_default_unchanged`: no flag. The output contains `[1:a:1]loudnorm=I=-14:TP=-1.5:LRA=11` and doesn't contain `audio.wav`.
- `test_mix_audio_command`: `--mix-audio /x/short_audio.py`. The output has a line starting `python3 /x/short_audio.py`, followed by the raw path, VS and DUR (VS = 0.8 - 9*1001/24000, DUR = 2.6, to 3 decimals) and a path ending `audio.wav`. The ffmpeg line has `-i` on that wav, `-map 1:a`, and no `loudnorm`.
- `test_mix_audio_needs_raw`: a 4-track file with `--mix-audio`. Exit 1, and stderr contains `6 audio tracks`.
- `test_shorts_py_passes_mix_audio`: a manifest with `mix_audio` set, run with `shorts.py --dry-run`. The output contains `python3 /x/short_audio.py`.

- [ ] **Step 2: Run them and watch them fail**

Run: `python3 -m unittest discover -s devrel/skills/stream-trim/tests -p 'test_short_audio.py' && python3 -m unittest discover -s devrel/skills/stream-shorts/tests`
Expected: FAIL. `short_audio` is missing, and `--mix-audio` is an unknown argument (5-arg usage error).

- [ ] **Step 3: Implement**

`short_audio.py`: `shorts_chain` and a CLI around `render_stretch`.

`render-short.sh`:
- Parse `--mix-audio`.
- In render mode, after the track probe, fail with `ERROR: --mix-audio needs the raw OBS recording (6 audio tracks)` when there are fewer than 6 tracks.
- `run python3 "$MIX_AUDIO" "$IN" "$VS" "$DUR" "$TMP/audio.wav"`, then ffmpeg with inputs `-ss VS -t DUR -i IN` and `-i $TMP/audio.wav`, filter `${LAYOUT},ass=...[v]`, `-map "[v]" -map 1:a`.
- Same codecs. The no-flag path stays as it is.

`shorts.py`: pass the flag through, and document `mix_audio` in the docstring.

- [ ] **Step 4: Run both suites**

Run: `python3 -m unittest discover -s devrel/skills/stream-trim/tests && python3 -m unittest discover -s devrel/skills/stream-shorts/tests`
Expected: PASS (43 + 3 in stream-trim, 4 in stream-shorts).

- [ ] **Step 5: Commit** `stream-shorts: opt-in --mix-audio; stream-trim: short_audio.py`

### Task 2: Edit points and shorts logic

**Files:**
- Create: `devrel/skills/stream-trim/scripts/shorts_view.py`
- Modify: `devrel/skills/stream-trim/scripts/render.py` (extract snapping)
- Test: `devrel/skills/stream-trim/tests/test_shorts_view.py`, `tests/test_render.py`

**Interfaces:**
- Produces:
  - `render.snap_range(in_s, out_s, fps, duration) -> (float, float)`, the same rounding `render_final` does today, which `render_final` now calls.
  - `shorts_view.PAD_BEFORE = 0.2`, `PAD_AFTER = 0.4`
  - `to_secs(t) -> float` (a number, `"MM:SS(.ss)"` or `"HH:MM:SS(.ss)"`); `fmt(t) -> "HH:MM:SS.ss"`
  - `video_span(clip, shift) -> (float, float)` = (start - PAD_BEFORE - shift, end + PAD_AFTER - shift)
  - `inside(clip, edit, shift) -> bool` (`edit` is `{"in", "out"}`)
  - `number(clip) -> int | None` (the `NN-` prefix, as in shorts.py)
  - `load_candidates(path, edit, shift) -> list[dict]`. It reads the shorts.json shape, and each clip gains `n`, `inside`, `edit_start` and `edit_end` (start/end minus shift minus In). It raises `ValueError` on bad JSON, a missing `clips`, or a clip without `file`/`start`/`end`/a number.
  - `merge_picks(existing, recording, words, mix_audio, picks) -> dict`. `existing` is a dict, a bare list (old format) or None. It keeps the clips whose `file` isn't in `picks`, replaces the ones that are, sorts by number, and sets `recording`, `words` and `mix_audio`.

- [ ] **Step 1: Write the failing tests**
- `test_snap_range`: `snap_range(343.83, 5699.66, 24000/1001, 5706.45)` gives frame-grid values (k/fps) within half a frame, and Out is capped at duration.
- `test_to_secs_and_fmt`: `"00:41:12.40"` gives 2472.4, `"5:30"` gives 330.0, `fmt(2472.4) == "00:41:12.40"`.
- `test_inside_counts_padding`: with edit `{"in": 100, "out": 200}` and shift 0.375, start 100.5 (0.375 + 0.2 = 0.575 > 0.5) is outside, start 100.6 is inside. End 199.9 is outside, end 199.5 is inside.
- `test_load_candidates`: 2 clips, one outside. `n`, `inside` and `edit_start` are correct. Bad JSON, a missing `clips` and a clip without a number each raise `ValueError`.
- `test_merge_keeps_and_replaces`: the existing file has 01 and 02, and the picks are a new 02 and a 03. The result has 01 (kept), the new 02 and 03, in order, with `mix_audio` set. A bare-list `existing` is wrapped.

- [ ] **Step 2: Run and watch them fail.** Run `python3 -m unittest discover -s devrel/skills/stream-trim/tests -p 'test_shorts_view.py'`. Expected: ImportError.
- [ ] **Step 3: Implement** `shorts_view.py` and `snap_range`.
- [ ] **Step 4: Run the whole stream-trim suite.** Expected: PASS.
- [ ] **Step 5: Commit** `stream-trim: shorts_view logic, snap_range`

### Task 3: Shorts API on the server

**Files:**
- Modify: `devrel/skills/stream-trim/scripts/server.py`
- Test: `devrel/skills/stream-trim/tests/test_server.py`

**Interfaces:**
- Consumes: everything in Task 2; `short_audio.py` (its path).
- Produces:
  - `make_server(raw, chain, port=0, shorts_py=SHORTS_PY)`, where `SHORTS_PY = <scripts>/../../stream-shorts/scripts/shorts.py`. The server refuses to start, with a clear error, if that file is missing.
  - After a successful final render, the server writes `<cache>/edit.json` = `{"in", "out", "output"}` with the snapped values. `/api/state` gains `"edit": {...} | null`.
  - `GET /api/shorts` returns `{"edit", "shift", "candidates": list | null, "error": str | null, "layouts": {name: [lo, hi] | null}, "render": {"state": "idle|running|done|error", "clips": {"<n>": {"state": "queued|rendering|done|error", "output", "error"}}}}`. Layout pan ranges come from stream-shorts `layouts.json`, overlaid with `shorts/layouts.json` if present.
  - `POST /api/shorts/preview {n, start, end, pan_x}` returns 200 `{"url": "/shorts/preview/<NN>.jpg?v=<mtime>"}`. It writes a one-clip manifest in `<cache>/shorts-work/` (copying `shorts/layouts.json` there if present) and runs `shorts.py --preview <manifest> NN`.
  - `POST /api/shorts/captions {n, start, end, fixes}` returns 200 `{"text": "..."}` (stdout of `shorts.py --captions`).
  - `GET /shorts/preview/<NN>.jpg` serves the file from the work dir.
  - `POST /api/shorts/render {"picks": [{n, start, end, pan_x, fixes}]}` returns 202, then runs `shorts.py <shorts/shorts.json> NN` for each pick in turn and tracks each clip's state by its `SHORT:`/`ERROR:` output.
    - 409 while the final render or a shorts render is running, or if there's no `edit.json`.
    - 400 for an unknown `n`, start >= end, or a clip outside the edit.
    - The clip written to `shorts.json` is the candidate (`file`, `hook`, `layout`) plus the pick's overrides. `mix_audio` is set to `short_audio.py`.
  - Preview/captions errors return 400 with the `ERROR:` line.

- [ ] **Step 1: Write the failing tests.** They use a stub `shorts_py`: a Python script that appends its argv to a log file. For `--preview` it writes the jpg path. For `--captions` it prints `HELLO WORLD`. For a render it prints `SHORT: <path>`.
  - `test_edit_survives_restart`: write `edit.json`, start a new server, and `/api/state` and `/api/shorts` report `edit`.
  - `test_shorts_no_candidates`: `candidates` is null and `error` is null.
  - `test_shorts_bad_candidates`: a half-written JSON gives 200, `candidates` null, and `error` set.
  - `test_shorts_preview_and_captions`: preview returns a url that serves the jpg, the stub log shows `--preview` on a manifest inside the cache, and captions returns `HELLO WORLD`.
  - `test_shorts_render`: two picks give 202. Polling reaches `done` for both, `shorts/shorts.json` has both clips and `mix_audio`, and `candidates.json` is unchanged (bytes equal).
  - `test_shorts_render_rejects_outside`: start >= end gives 400, an outside clip gives 400, no `edit.json` gives 409, and a second render while one is running gives 409.
- [ ] **Step 2: Run and watch them fail.** Run `python3 -m unittest discover -s devrel/skills/stream-trim/tests -p 'test_server.py'`. Expected: the new tests FAIL with 404s.
- [ ] **Step 3: Implement** the routes and state on `TrimServer`, reusing its lock and thread pattern.
- [ ] **Step 4: Run the whole suite.** Expected: PASS.
- [ ] **Step 5: Commit** `stream-trim: shorts API`

### Task 4: Shorts view on the page

**Files:**
- Modify: `devrel/skills/stream-trim/scripts/page.html`
- Test: `devrel/skills/stream-trim/tests/test_page.py`

**Interfaces:**
- Consumes: the Task 3 routes; `/api/state` `edit`.

Behaviour:
- Two tabs, **Trim** and **Shorts**. Shorts is enabled once an edit exists, and the page switches to it when the render reaches `done`. The page's initial In/Out come from `edit` when present.
- With no candidates yet: "Claude is finding shorts in this edit. They'll show up here." The page polls `/api/shorts` every 3 s.
- Each card shows:
  - a checkbox (disabled with the reason for `skip` or outside clips)
  - the hook
  - start and end in edit timecode (the existing `tc()`), each with -0.5 s and +0.5 s buttons
  - the preview image (requested one card at a time on first view, and again after a nudge or a pan change)
  - a `pan_x` slider when the layout has a range, which re-previews on `change`
  - the caption text (refreshed after nudges and fix changes)
  - suggested fixes as unticked checkboxes, `heard → meant`
  - a textarea for more fixes, one `heard = meant` per line
- **Render selected (N)** posts the picks, then shows each clip's state, and the output path when it's done. Errors show the server's message.

- [ ] **Step 1: Write the failing test.** In `test_page_static`, add `/api/shorts`, `/api/shorts/preview`, `/api/shorts/captions` and `/api/shorts/render` to the refs. The em-dash and external-URL checks stay.
- [ ] **Step 2: Run it and watch it fail.**
- [ ] **Step 3: Implement.**
- [ ] **Step 4: Run the suite (PASS), then check in Chrome.** Use a generated 2-minute 6-track file, run prepare and the server, render a short edit, and write a `candidates.json` by hand with 3 clips (one outside, one `skip`). Check that:
  - the tab switches
  - outside and skipped clips are disabled
  - nudges move the timecode and refresh the captions
  - the slider re-previews
  - Render selected walks to done

  This uses the real `shorts.py`, so a real 1080x1920 file comes out. Record a GIF.
- [ ] **Step 5: Commit** `stream-trim: Shorts view`

### Task 5: Skill flow, versions, real run

**Files:**
- Modify: `devrel/skills/stream-trim/SKILL.md`, `.claude-plugin/marketplace.json`, `devrel/.claude-plugin/plugin.json`, `README.md` (the stream-trim row now mentions shorts), the spec (a Stage 3 result section)

SKILL.md additions, in order:
1. Step 1 also runs the `stream-shorts` tool check (ffmpeg with libass, mlx_whisper, Jost font) and follows that skill's install rules.
2. Once the page is open, invoke `find-stream-shorts` with the raw path while Ryan trims. Transcription doesn't depend on In/Out.
3. Wait for the edit. Use Monitor with an until-loop on `curl -s <url>/api/shorts` until `edit` is non-null.
4. From the shortlist:
   - Keep only the clips inside the edit (the padding rule in Global Constraints).
   - Fix dangling-word starts and ends with the `stream-shorts` step 5 rules.
   - Write `shorts/candidates.draft.json` in the shorts.json shape.
   - Run `shorts.py --preview` on the draft and look at each jpg. Set `layout`, `pan_x` or `skip`.
   - Run `--captions` and put likely mishearings in `suggested_fixes`.
   - Delete the jpgs, then `mv` the draft to `shorts/candidates.json`. The rename means the page never reads a half-written file.
   - Tell Ryan the shortlist is on the page.
5. Wait for the shorts render, using Monitor on `/api/shorts` until `render.state` is `done` or `error`. Then do `stream-shorts` steps 7 to 9 (descriptions, voice pass, em-dash/AI-ism scan, report).
6. Notes: `candidates.json` is Claude's and `shorts.json` is the page's. Shorts are mixed at -14 LUFS (platform norm) with the long video's chain.

- [ ] **Step 1:** Edit SKILL.md, the README row, and the version 1.44.0 to 1.45.0 in both manifests. Run the full suites of both skills. Expected: PASS.
- [ ] **Step 2: Commit and push** `stream-trim 1.45.0: shorts from the edit`
- [ ] **Step 3: Real run with Ryan** on the Nov 12 stream. The final and `edit.json` already exist. Write `edit.json` from the Stage 2 values (in 344.59425, out 5699.527166666666) if it's missing.
  - Claude runs steps 2 to 4.
  - Ryan picks and renders at least two shorts, with one nudge and one caption fix.
  - Check each output: 1080x1920, AAC 48 kHz stereo, length = end - start + 0.6 ± 0.05 s, `I` within 1 LU of -14, and the captions in sync with the voice (Ryan watches).
  - Record the result in the spec.
