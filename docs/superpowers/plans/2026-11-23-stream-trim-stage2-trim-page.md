# stream-trim Stage 2: Trim Page and 4K Render Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ryan runs `/stream-trim <raw OBS file>`, checks the pre-filled In and Out on a local page, clicks Render, and gets `<name>-final.mp4` next to the recording, with no Premiere involved.

**Architecture:**
- **Prepare.** One ffmpeg pass over the raw file writes three things into a cache folder: a 720p preview with the final mix, the mic waveform peaks, and the mic silences. That cache gives the default In and Out.
- **Serve.** A stdlib Python HTTP server serves one static page, the proxy (with Range support so the video can seek), and a small JSON API.
- **Render.** The render runs in a background thread. It takes two passes, like `render_stretch`: a loudness measure on the audio, then the 4K encode.

**Tech Stack:** Python 3 stdlib only (`http.server`, `threading`, `array`, `unittest`), ffmpeg with VideoToolbox, plain HTML/JS/canvas with no framework or build step.

**Spec:** `docs/superpowers/specs/2026-11-23-stream-trim-design.md` (Stage 1 result at the bottom)

## Global Constraints

- Everything lives in `devrel/skills/stream-trim/`. Tests run with `python3 -m unittest discover -s devrel/skills/stream-trim/tests` and must stay green, including Stage 1's 19 tests.
- Track layout, mix and voice chain come from `audio_chain.py` and `scripts/chain.json`. Don't copy filter strings anywhere else.
- The mic lags the video by `MIC_LAG_FRAMES` (9) frames. All times shown or stored are on the video clock.
- Default In = voice start - 0.5 s (`LEAD_IN`). The voice start only counts if the mic is silent (-45 dB, 2 s) from 0 for at least 60 s, otherwise In = 0. This matches the Quick Action rule.
- Default Out = voice end + 1.0 s (`TAIL`), capped at the duration.
- Final video: 4K like the source, `h264_videotoolbox` at `-b:v 5M` (Ryan's current Premiere export is H.264 at about 4.9 Mbps). Audio: AAC 320k, stereo, 48 kHz, whole-mix two-pass loudnorm with `chain.json` loudness (`I -17`, `TP -1`, `LRA 20`), `linear=true`.
- Output `<recording dir>/<name>-final.mp4`. Never overwrite it, and write to `<name>-final.partial.mp4` first. Never modify the recording.
- The cache goes in `~/Library/Caches/stream-trim/<key>/`, never next to the recording. Recordings live in Google Drive, and a 1 GB proxy there would sync to the cloud. `<key>` = the first 16 hex characters of sha1(`realpath|size|mtime`).
- The server binds `127.0.0.1` only.
- Page text follows Ryan's CLAUDE.md: no em-dashes.
- New skill: register it in `devrel/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, bump devrel to the same version in both, and add a README row.

## Review Focus

1. **A recording with no Starting Soon silence** (voice from 0) or no closing silence. Expect In = 0 or Out = duration, with no crash and no negative times.
2. **Scrubbing the preview.** Expect the browser's Range requests to get `206 Partial Content` with the right `Content-Range`. A `200` with the whole file breaks seeking in Chrome on a 1 GB file.
3. **Render clicked twice, or while one is running.** Expect a single render and `409` for the second.
4. **A render that fails or is stopped part way.** Expect no `-final.mp4`, the `.partial.mp4` removed, and the error text on the page.
5. **In/Out from the page that are out of range, reversed, or not numbers.** Expect `400` with a message, and no render started.

---

### Task 1: Prepare pass (proxy, peaks, silences, defaults)

**Files:**
- Create: `devrel/skills/stream-trim/scripts/prepare.py`
- Modify: `devrel/skills/stream-trim/scripts/audio_chain.py`
- Test: `devrel/skills/stream-trim/tests/test_prepare.py`

**Interfaces:**
- Consumes: `audio_chain.build_filtergraph`, `probe`, `TRACKS`, `ROLES`, `MIC_LAG_FRAMES`, `load_chain`.
- Produces in `audio_chain.py`: `mix_graph(chain: dict, fps: float) -> tuple[str, float]`, which returns (the graph ending in `[mix]`, the shift). Refactor `render_stretch` to use it, so Task 3 shares it.
- Produces in `prepare.py`:
  - `cache_dir(raw: str) -> str`
  - `parse_silences(stderr: str, duration: float) -> list[tuple[float, float]]`. A trailing `silence_start` with no end closes at `duration`.
  - `defaults(silences, duration) -> dict` with `voice_start`, `voice_end`, `in`, `out`.
  - `peaks_from_pcm(pcm: bytes, rate: int, per_s: int) -> list[float]`, with peak abs values from 0 to 1 at `per_s` buckets per second.
  - `prepare(raw: str, chain: dict, progress=None) -> dict`. It writes `proxy.mp4`, `peaks.json` (`{"per_s": 20, "peaks": [...]}`) and `analysis.json` (`{"raw", "duration", "fps", "silences", "voice_start", "voice_end", "in", "out"}`) to `cache_dir(raw)`, and returns the analysis. If `analysis.json` already exists, it returns it without running ffmpeg.
  - The CLI `python3 prepare.py <raw>` prints `CACHE <dir>`.

One ffmpeg pass reads the raw file once. That matters because Drive reads are slow.
- `-filter_complex`: `mix_graph(...)` plus a mic branch, `[0:a:1]atrim=start=<shift>,asetpts=PTS-STARTPTS,asplit[m1][m2]`.
  - `[m1]silencedetect=noise=-45dB:d=2,anullsink`
  - `[m2]aresample=1000,aformat=sample_fmts=s16:channel_layouts=mono[pk]`
  - `[mix]loudnorm=I=<I>:TP=<TP>:LRA=<LRA>[pa]` (single pass is fine for a preview), and `[0:v]scale=-2:720[pv]`
- Outputs:
  - `-map [pv] -map [pa] -c:v h264_videotoolbox -b:v 2M -c:a aac -b:a 160k -movflags +faststart proxy.partial.mp4`, then rename
  - `-map [pk] -f s16le pipe:1`, read by Python into `peaks_from_pcm`

- [ ] **Step 1: Write the failing tests:**
  - `test_parse_silences`: a canned stderr with `silence_start: 0` / `silence_end: 300.5`, `silence_start: 1000` / `silence_end: 1003`, and a trailing `silence_start: 5300` with no end, at duration 5400, gives `[(0, 300.5), (1000, 1003), (5300, 5400)]`.
  - `test_defaults_normal`: those silences give `voice_start 300.5`, `in 300.0`, `voice_end 5300`, `out 5301.0`.
  - `test_defaults_no_intro`: the first silence is shorter than 60 s, or there is none, so `in == 0` and `voice_start == 0`.
  - `test_defaults_no_outro`: no silence touches the end, so `voice_end == out == duration`. A tail past the end is capped: voice end at duration - 0.4 gives `out == duration`.
  - `test_peaks_from_pcm`: 2 s of s16 mono at 1000 Hz, with `per_s=20`, gives 40 values. A full-scale sample in bucket 3 gives `peaks[3] == 1.0`, and silence gives `0.0`.
  - `test_cache_dir_stable`: the same file gives the same dir, the dir is under `~/Library/Caches/stream-trim/`, and touching the file (a new mtime) changes it.
  - `test_prepare_end_to_end` (generated media): 70 s of mic silence then a tone to 90 s, then silence to 100 s, from `make_mp4` extended with a `tone_from`/`tone_to` option. It gives `proxy.mp4` with 1 video and 1 audio stream at height 720, `analysis.json` `in ≈ 69.5` (±0.1) and `out ≈ 91` (±0.1), and a second call returns quickly without re-running. Use the 6-track shape. `cache_dir` is patched to a temp dir in tests.
- [ ] **Step 2: Run the tests, expect FAIL** (no `prepare` module).
- [ ] **Step 3: Implement** `mix_graph` (and switch `render_stretch` to it), then `prepare.py`.
- [ ] **Step 4: Run the whole suite, expect `OK`** (Stage 1's tests prove the refactor kept `render_stretch` the same).
- [ ] **Step 5: Commit** `stream-trim: prepare pass (proxy, peaks, default In/Out)`.

### Task 2: Final render

**Files:**
- Create: `devrel/skills/stream-trim/scripts/render.py`
- Test: `devrel/skills/stream-trim/tests/test_render.py`

**Interfaces:**
- Consumes: `audio_chain.mix_graph`, `probe`, `measure.parse_loudnorm`, `measure.run_ffmpeg`.
- Produces: `final_path(raw: str) -> str` (`<dir>/<stem>-final.mp4`).
- Produces: `parse_progress(line: str, total_s: float) -> float | None`. It reads `out_time_us=` lines from `-progress pipe:1` and returns a 0 to 100 percent.
- Produces: `render_final(raw, in_s, out_s, chain, progress=None, stop=None) -> str`. `progress(percent: float, phase: str)` takes `phase` of `"measuring"` or `"encoding"`. `stop` is a `threading.Event`. It returns the output path, and raises `FileExistsError` if that path exists and `ValueError` for a bad range. On any failure or stop it removes `.partial.mp4` and raises `RuntimeError("stopped")` or the ffmpeg error.
  - Pass 1: `-ss in -t (out-in+shift) -i raw`, `mix_graph` + `atrim=duration`, then `loudnorm print_format=json`, output to `-f null`. Audio only, with `-vn`.
  - Pass 2: the same input. `[0:v]trim=duration=<out-in>,setpts=PTS-STARTPTS[v]`, and the audio with measured loudnorm `linear=true,aresample=48000`.
  - Settings: `-c:v h264_videotoolbox -b:v 5M -tag:v avc1 -c:a aac -b:a 320k -ar 48000 -movflags +faststart`.
  - Both passes run under `subprocess.Popen` with `-progress pipe:1`, and are killed when `stop` is set.

- [ ] **Step 1: Write the failing tests** (generated 6-track media, 12 s):
  - `test_final_path`: `/x/Nov 12/2026-11-12 10-24-27.mp4` gives `/x/Nov 12/2026-11-12 10-24-27-final.mp4`.
  - `test_parse_progress`: `out_time_us=5000000` at total 10 gives `50.0`, and `progress=end` and junk lines give `None`.
  - `test_render_final_trims_exactly`: `render_final(raw, 2, 8, ...)` writes the final file. Its duration is 6 s ±1 frame, it has 1 video and 1 audio stream (AAC, 2 ch, 48000), and no `.partial.mp4` is left.
  - `test_render_final_refuses_existing`: a second call raises `FileExistsError`, and the first file is untouched (same mtime).
  - `test_render_final_bad_range`: `(8, 2)`, `(-1, 3)` and `(2, 99)` each raise `ValueError`.
  - `test_render_final_stop_cleans_up`: a `stop` event set from the progress callback on the first encoding update raises `RuntimeError("stopped")`, and leaves neither the final file nor the partial.
- [ ] **Step 2: Run, expect FAIL.**
- [ ] **Step 3: Implement** `render.py`.
- [ ] **Step 4: Run the whole suite, expect `OK`.**
- [ ] **Step 5: Commit** `stream-trim: frame-accurate 4K final render with two-pass loudness`.

### Task 3: Local server and API

**Files:**
- Create: `devrel/skills/stream-trim/scripts/server.py`
- Test: `devrel/skills/stream-trim/tests/test_server.py`

**Interfaces:**
- Consumes: `prepare.cache_dir`, the files from Task 1, and `render.render_final` / `final_path`.
- Produces: `make_server(raw: str, chain: dict, port: int = 0) -> ThreadingHTTPServer`, which needs the cache to exist. The CLI `python3 server.py <raw>` prints `READY http://127.0.0.1:<port>/` and then serves until killed.
- Routes:
  - `GET /` serves `page.html` (Task 4). Until that exists, serve a placeholder file.
  - `GET /proxy.mp4` handles single-range `Range: bytes=a-b` and `a-` with `206`, `Accept-Ranges: bytes`, `Content-Range`. With no Range header it returns `200`. It streams in 1 MiB chunks.
  - `GET /api/state` returns `analysis.json` plus `peaks` and `per_s` plus `"render": <status>` plus `"output": final_path(raw)` plus `"exists": bool`.
  - `POST /api/render` takes the JSON `{"in": float, "out": float}`. Floats with 0 ≤ in < out ≤ duration get `202` and start the thread. Otherwise it returns `400 {"error": "..."}`. It returns `409` while a render is running, and `409` if the output exists.
  - `GET /api/render` returns `{"state": "idle"|"running"|"done"|"error", "phase", "percent", "output", "error"}`.
  - `POST /api/stop` sets the stop event, and returns `200` when a render is running and `409` otherwise.
- Render state lives on the server object, guarded by a `threading.Lock`.

- [ ] **Step 1: Write the failing tests.** Start a server on port 0 in a thread, against a temp cache with a small generated `proxy.mp4` and `analysis.json`, then use `urllib`:
  - `test_state`: returns 200 with the analysis' `in`/`out`, the `peaks` list, and `render.state == "idle"`.
  - `test_proxy_range`: `Range: bytes=10-19` gives `206`, `Content-Range: bytes 10-19/<size>`, and exactly those 10 bytes. `bytes=10-` gives the rest. No header gives `200` and the full size.
  - `test_render_validation`: `{"in": 5, "out": 2}`, `{"in": "a", "out": 2}`, `{"in": -1, "out": 2}` and `{"in": 0, "out": 1e9}` each give `400`, and the state stays idle.
  - `test_render_conflict`: with `render_final` patched to block on an event, the first POST gives `202` and the second gives `409`. After the event is released, state is `done` and `output` is set.
  - `test_render_error_reported`: with `render_final` patched to raise `RuntimeError("boom")`, state becomes `error` with `error == "boom"`.
  - `test_binds_localhost`: `server.server_address[0] == "127.0.0.1"`.
- [ ] **Step 2: Run, expect FAIL.**
- [ ] **Step 3: Implement** `server.py`.
- [ ] **Step 4: Run the whole suite, expect `OK`.**
- [ ] **Step 5: Commit** `stream-trim: local server with ranged proxy and render API`.

### Task 4: Trim page

**Files:**
- Create: `devrel/skills/stream-trim/scripts/page.html`
- Test: `devrel/skills/stream-trim/tests/test_page.py`

**Interfaces:**
- Consumes: the Task 3 routes.
- The layout follows the spec sketch:
  - the video (`/proxy.mp4`) on top, full width
  - a waveform canvas under it, drawn from `peaks`, with the In and Out markers (draggable), a playhead, and the area outside In/Out dimmed
  - a line reading `In h:mm:ss.ff   Out h:mm:ss.ff   Length h:mm:ss.ff`, using the fps from state (`.ff` = frames)
  - a key legend, and the **Render** button
  - during a render, a progress bar showing phase and percent, and a **Stop** button
  - when done, the output path and a note that shorts come next (Stage 3)
- Keys:
  - Space: play/pause
  - J/K/L: back / pause / forward. L pressed again doubles the playback rate, up to 8x. J seeks back 5 s.
  - I / O: set In / Out to the playhead
  - Left / Right: one frame; Shift+Left / Shift+Right: 1 s
  - Q / W: jump to In / Out
  - Clicking the waveform seeks.
- Render is disabled while a render runs or the output exists. In that case the page shows "<name>-final.mp4 already exists".

- [ ] **Step 1: Write the failing test** `test_page_static`. `page.html` exists, contains no em-dash (U+2014), loads no external URLs (no `http` in `src=`/`href=`), and references `/api/state`, `/api/render`, `/api/stop` and `/proxy.mp4`.
- [ ] **Step 2: Run, expect FAIL.**
- [ ] **Step 3: Implement** `page.html` (inline CSS and JS).
- [ ] **Step 4: Run the whole suite, expect `OK`.**
- [ ] **Step 5: Check in the browser.** Run prepare and the server on a generated 2-minute 6-track test file (in the scratchpad), open the URL with Claude in Chrome, and check each of these:
  - the waveform shows the silences
  - I and O move the markers, and the readout updates
  - the arrow keys step one frame (the readout's frame count changes by 1)
  - dragging the In marker works
  - Render shows progress, then the path
  - a second Render is disabled

  Record a GIF named `stream-trim-page-check.gif`.
- [ ] **Step 6: Commit** `stream-trim: trim page`.

### Task 5: Skill, registration, and the real run

**Files:**
- Create: `devrel/skills/stream-trim/SKILL.md`
- Modify: `devrel/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `README.md`

**SKILL.md** (front matter `name: stream-trim`, a description of what it does and when to use it in Ryan's words: trim a stream, Podcast Voice, export without Premiere; `allowed-tools: Bash(python3 *) Bash(ffmpeg *) Bash(ffprobe *) Bash(open *)`). Steps:
1. Check `ffmpeg` has `h264_videotoolbox` (`ffmpeg -hide_banner -encoders`, read into a variable first, which is the pipefail gotcha from stream-shorts).
2. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/prepare.py "<raw>"` with `run_in_background`. Say it reads the whole recording once (about 10+ min from Google Drive) and that reruns are instant.
3. Start `server.py "<raw>"` with `run_in_background`, read its `READY` line, and `open` the URL.
4. Tell Ryan the defaults (In, Out, length) and the keys in one short list.
5. When he says he rendered, or asks, check `GET /api/render`. Report the output path, or the error as-is. Stop the server when he's done.

- [ ] **Step 1: Write SKILL.md**, register the skill in both manifests, bump devrel from `1.43.0` to `1.44.0` in both, and add the README row (devrel table and skills table).
- [ ] **Step 2: Check the manifests:** `python3 -c "import json;[json.load(open(p)) for p in ['devrel/.claude-plugin/plugin.json','.claude-plugin/marketplace.json']]"` exits 0, and `grep -c stream-trim` returns ≥1 in each.
- [ ] **Step 3: Real run on Nov 12 with Ryan.** Run the skill steps on `.../Streams/Nov 12/2026-11-12 10-24-27.mp4`. The checks:
  - `analysis.json` `in` lands within 1 s of 344.555 - 0.5 = 344.06 (Ryan's own Premiere In was 344.555 s on the video clock).
  - Ryan renders from the page.
  - The final file is 4K, H.264 and AAC 48k stereo, and its whole-file integrated loudness is within 1 LU of -17. Check with `measure.measure` on its audio, extracted with `-vn`.
  - Ryan watches the start and end, and spot-checks a guest or alert moment if he names one.
- [ ] **Step 4: Commit and push** `stream-trim: SKILL.md, register skill (devrel 1.44.0)`. Then remind Ryan to run `bin/link-skills`, per the memory on the skills plugin setup.
