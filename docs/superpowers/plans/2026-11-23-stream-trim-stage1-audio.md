# stream-trim Stage 1: Voice Chain and Mix (Go/No-Go) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the ffmpeg voice chain and mix that replace Premiere's Podcast Voice. Then tune them against Ryan's Nov 12 render until he signs off, or stop.

**Architecture:** One JSON file holds every audio setting. A pure Python module turns it into an ffmpeg `-filter_complex` string, so Stage 2's render and proxy and Stage 3's shorts can all reuse it. A compare tool cuts matching stretches out of the raw OBS file (processed through the chain) and out of Ryan's Premiere render, measures both, and writes a blind A/B page for listening.

**Tech Stack:** Python 3 stdlib only (no numpy, no pytest: use `unittest`), ffmpeg/ffprobe from the homebrew-ffmpeg tap.

**Spec:** `docs/superpowers/specs/2026-11-23-stream-trim-design.md`

Stages 2 (trim page and 4K render) and 3 (Shorts view) get their own plans after this gate passes. They depend on what tuning settles.

## Global Constraints

- Skill lives in `devrel/skills/stream-trim/`. Scripts go in `scripts/` and tests in `tests/`, run with `python3 -m unittest discover -s devrel/skills/stream-trim/tests`.
- OBS track layout: 1 Full Mix, 2 mic, 3 guest + StreamElements, 4 Spotify, 5 theme song, 6 Firebot. Final mix = 2, 3, 5, 6 into one stereo track. 1 and 4 are dropped.
- The mic lags the video by 9 frames. The frame rate is read from the file (24000/1001 gives 0.375375 s).
- Mic and guest go through the voice chain. Loudness normalization runs on the whole mix.
- Never modify or overwrite the source recording or the reference render. Outputs go to a folder the caller names.
- Prose shown to Ryan (A/B page text) follows his CLAUDE.md: no em-dashes.

## Reference facts (Nov 12 stream, read from the .prproj on 2026-11-23)

- Raw: `.../Streams/Nov 12/2026-11-12 10-24-27.mp4`. Reference: `.../Streams/Nov 12/renders/Contributor Toolkit -  Open in Any Editor and XDebug Step Debugging - Live Stream Nov 12, 2026.mp4` (two spaces after "Toolkit -").
- Premiere ticks: 254016000000 per second.
- The sequence starts at raw 344.555 s (InPoint 87521858424000). The mic clip starts at raw 344.930 s (InPoint 87617209680000), so the mic is 9 frames later. Render time `t` is raw time `t + 344.555` for video and tracks 3, 5, 6, and raw `t + 344.930` for the mic.
- Podcast Voice chain (Enhance Speech off), with normalized values from the project:
  - Reduce Rumble FFT points: 0.000907, 0.004167, 0.004688, 0.005208 of Nyquist. That is about 22, 100, 112 and 125 Hz, so a low cut near 100 to 125 Hz.
  - Dynamics: level detector attack 0.002 s, release 0.05 s. Curve points (loc, val) are (0.1563, 0.0888), (0.2500, 0.2267), (0.3225, 0.3225), (0.5575, 0.6688), (1.0, 0.9914).
  - DeEsser: threshold 0.7803, center 0.2089, bandwidth 0.3250.
  - Graphic EQ (10 bands, 0.5 = flat): band 4 = 0.5145, 5 = 0.5062, 7 = 0.5145, 8 = 0.5228, 9 = 0.5083.
  - Vocal Enhancer: mode 0.
  - Loudness auto-match: on.
  - Mic clip Volume Level 0.21645, which is +1.71 dB (Level = 10^((dB-15)/20)).

## Review Focus

1. A stretch that starts during the "Starting Soon" silence, or runs past the end of either file. Expect a clear `ERROR:` before any ffmpeg work, not a short or silent clip.
2. A raw file with fewer than 6 audio tracks (an old recording, or a stream-prep `-edit.mp4`). Expect `ERROR: expected 6 audio tracks, found N`, not a wrong track picked silently.
3. Paths with spaces, commas and two spaces in a row (the reference path has all three). Expect every subprocess call to use argv lists, never a shell string.
4. A chain JSON missing a key, or with a key misspelled. Expect `build_filtergraph` to raise `KeyError` naming the key, not to drop the stage silently.
5. Two compare runs into the same output folder. Expect the second run to refuse unless `--force` is given, so an earlier listening round isn't lost.

---

### Task 1: Chain settings and filtergraph builder

**Files:**
- Create: `devrel/skills/stream-trim/scripts/chain.json`
- Create: `devrel/skills/stream-trim/scripts/audio_chain.py`
- Test: `devrel/skills/stream-trim/tests/test_audio_chain.py`

**Interfaces:**
- Produces: `load_chain(path: str) -> dict`.
- Produces: `voice_filters(chain: dict) -> str`, a comma-joined ffmpeg audio filter list for one voice track (no labels).
- Produces: `build_filtergraph(chain: dict, inputs: dict[str, str], mic_shift_s: float) -> str`. `inputs` maps role to an ffmpeg stream spec: `{"mic": "0:a:1", "guest": "0:a:2", "theme": "0:a:4", "firebot": "0:a:5"}`. It returns a `-filter_complex` string whose final label is `[mix]`, before loudness. Loudness is applied by the caller (Task 2), because it needs two passes.
- Produces: `TRACKS = {"mic": 2, "guest": 3, "theme": 5, "firebot": 6}` (OBS track numbers, 1-based).

`chain.json` starting values (translated from the reference facts, and the knobs tuning will turn):

```json
{
  "mic_gain_db": 1.71,
  "rumble_hz": 110,
  "compand": {"attacks": 0.002, "decays": 0.05,
              "points": [[-90, -90], [-84, -91], [-75, -77], [-68, -68], [-44, -33], [0, -1]]},
  "deesser": {"i": 0.4, "m": 0.5, "f": 0.5},
  "eq_db": {"250": 0.6, "500": 0.25, "2000": 0.6, "4000": 0.9, "8000": 0.3},
  "presence": {"hz": 180, "db": 0, "q": 1.0},
  "levels_db": {"guest": 0, "theme": 0, "firebot": 0},
  "loudness": {"I": -14, "TP": -1, "LRA": 11}
}
```

Compand points come from the Dynamics curve with `dB = (x - 1) * 100`. That mapping is an assumption and the first thing tuning checks. `presence` stands in for Vocal Enhancer "Low Tone" and starts off (0 dB). The loudness target starts at YouTube's -14. Task 3 measures the reference's real loudness, and that number replaces it.

- [ ] **Step 1: Write the failing tests** in `test_audio_chain.py` (unittest):
  - `test_voice_filters_order`: for the shipped `chain.json`, the filter names in `voice_filters()` appear in this order: `highpass`, `compand`, `deesser`, `equalizer` (one per `eq_db` key), and `bass` or `equalizer` for presence only when `presence.db != 0`.
  - `test_voice_filters_values`: the result contains `highpass=f=110`, `attacks=0.002`, `decays=0.05`, `points=-90/-90|-84/-91|-75/-77|-68/-68|-44/-33|0/-1`, and `equalizer=f=4000:t=q:w=1.41:g=0.9`.
  - `test_build_filtergraph_shift_and_mix`: with `mic_shift_s=0.375375`, the graph contains `atrim=start=0.375375,asetpts=PTS-STARTPTS` on the mic branch only, `volume=1.71dB` on the mic, the voice filters on the mic and guest branches only, `amix=inputs=4:normalize=0`, and ends with `[mix]`.
  - `test_missing_key_raises`: deleting `"compand"` raises `KeyError` with `'compand'` in the message.
  - `test_zero_level_omits_volume`: `levels_db.theme == 0` gives no `volume=` filter on the theme branch, and `-3` gives `volume=-3dB`.

- [ ] **Step 2: Run the tests to make sure they fail.**
  Run: `python3 -m unittest discover -s devrel/skills/stream-trim/tests -v`
  Expected: FAIL with `ModuleNotFoundError: No module named 'audio_chain'`. The test adds `../scripts` to `sys.path`.

- [ ] **Step 3: Implement** `load_chain`, `voice_filters` and `build_filtergraph` in `audio_chain.py`, and write `chain.json` exactly as above. Access keys with `chain["..."]` (never `.get`) so missing keys raise. Keep `amix` at `normalize=0` so each track keeps its level.

- [ ] **Step 4: Run the tests to make sure they pass.** Same command. Expected: `OK`.

- [ ] **Step 5: Commit.**
  ```bash
  git add devrel/skills/stream-trim
  git commit -m "stream-trim: chain settings and ffmpeg filtergraph builder"
  ```

### Task 2: Measuring and rendering a stretch

**Files:**
- Create: `devrel/skills/stream-trim/scripts/measure.py`
- Modify: `devrel/skills/stream-trim/scripts/audio_chain.py` (add the render function)
- Test: `devrel/skills/stream-trim/tests/test_measure.py`

**Interfaces:**
- Consumes: `build_filtergraph`, `TRACKS` (Task 1).
- Produces: `parse_ebur128(stderr: str) -> dict` with keys `I`, `LRA`, `TP` (floats, from the ffmpeg `ebur128=peak=true` summary block).
- Produces: `parse_loudnorm(stderr: str) -> dict` (the JSON block from `loudnorm=print_format=json`).
- Produces: `measure(path: str) -> dict`: `I`, `LRA`, `TP`, plus `bands`, a dict of octave centre Hz (63, 125, 250, 500, 1000, 2000, 4000, 8000) to RMS dB. Each band comes from a `bandpass=f=<hz>:width_type=o:w=1,astats=measure_overall=RMS_level:measure_perchannel=none` run, so no numpy is needed.
- Produces: `render_stretch(raw: str, start_s: float, seconds: float, chain: dict, out_wav: str) -> None`. It checks that the raw file has 6 audio tracks, reads the fps, and seeks with `-ss start_s` so the mic is trimmed by the 9-frame shift. It runs loudnorm pass 1 (measure, through `[mix]`), then pass 2 with `measured_*` and `linear=true`, and writes 48 kHz 24-bit stereo WAV.

- [ ] **Step 1: Write the failing tests** in `test_measure.py`:
  - `test_parse_ebur128`: a canned summary block (copy a real one from `ffmpeg -i <any wav> -af ebur128=peak=true -f null -` into the test as a string) parses to the printed I, LRA and TP values.
  - `test_parse_loudnorm`: a canned loudnorm JSON block parses, and `input_i` is a string, as ffmpeg prints it.
  - `test_render_stretch_rejects_wrong_track_count`: an mp4 generated in `setUpClass` with ffmpeg `sine` sources and 2 audio tracks raises `ValueError("expected 6 audio tracks, found 2")`.
  - `test_render_stretch_rejects_out_of_range`: on a 6-track, 10 s generated file, `start_s=8, seconds=5` raises `ValueError` mentioning `past the end`.
  - `test_render_stretch_sine_roundtrip`: on the 6-track file (1 kHz sine on track 2, silence elsewhere), `render_stretch(..., 2, 5, chain, out)` writes a WAV about 5 s long (±0.05), and `measure(out)["I"]` is within 1.5 LU of `chain["loudness"]["I"]`.
  - `test_measure_bands_peak_at_1k`: for that output, `bands[1000]` is the largest band.

- [ ] **Step 2: Run the tests to make sure they fail.** Same command. Expected: FAIL on import of `measure`.

- [ ] **Step 3: Implement** `measure.py` and `render_stretch`. All subprocess calls use argv lists. ffmpeg errors are raised as `RuntimeError` carrying the last 20 lines of stderr.

- [ ] **Step 4: Run the tests to make sure they pass.** Expected: `OK`. The generated media lives in a `tempfile.TemporaryDirectory`.

- [ ] **Step 5: Commit.** `git commit -m "stream-trim: two-pass loudness render of a stretch, and measurements"`

### Task 3: Compare tool and blind A/B page

**Files:**
- Create: `devrel/skills/stream-trim/scripts/compare.py`
- Create: `devrel/skills/stream-trim/scripts/ab.html` (template)
- Test: `devrel/skills/stream-trim/tests/test_compare.py`

**Interfaces:**
- Consumes: `render_stretch`, `measure`, `load_chain`.
- Produces the CLI: `python3 compare.py --raw <raw> --reference <render> --offset 344.555 --chain <chain.json> --out <dir> [--force] <render_start_s>:<seconds> [...]`
- For each stretch `i`, it writes into `<dir>`:
  - `ref-<i>.wav`, cut from the reference at `render_start_s`
  - `ours-<i>.wav`, from `render_stretch(raw, render_start_s + offset, ...)`
  - `report.json`, with both measurements per stretch, their differences (`I`, `LRA`, `TP`, each band), and the chain used
  - `index.html`, where each stretch shows two players labelled **A** and **B**, in random order per stretch. Which is ours stays in `report.json` under `"answer"` and is shown by a **Reveal** button.
- `--out` that already exists without `--force` exits 1 with `ERROR: <dir> exists, pass --force to overwrite`.

- [ ] **Step 1: Write the failing tests:**
  - `test_parse_stretch`: `"300:150"` gives `(300.0, 150.0)`, and `"5:00"` raises.
  - `test_refuses_existing_out`: a CLI run into an existing directory exits 1 with that message.
  - `test_ab_page_hides_answer`: the generated `index.html` contains no `ours-` file name inside visible text, only in the `src` attributes, and `report.json["answer"]` has one `"A"` or `"B"` per stretch.

- [ ] **Step 2: Run the tests to make sure they fail.** Expected: FAIL on import of `compare`.

- [ ] **Step 3: Implement** `compare.py` and `ab.html`. The page is static, with no network requests. It is opened with `open <dir>/index.html`.

- [ ] **Step 4: Run the tests to make sure they pass.** Expected: `OK`.

- [ ] **Step 5: Alignment check on the real files.** Run on stretch `300:150`. Then run `silencedetect=noise=-40dB:d=0.3` on `ref-0.wav` and `ours-0.wav`. The first five silence ends must agree within 0.03 s. If they're off by a constant, the offset facts are wrong: stop and report the shift.

- [ ] **Step 6: Commit.** `git commit -m "stream-trim: blind A/B compare tool"`

### Task 4: Tuning rounds with Ryan, then go/no-go

**Files:**
- Modify: `devrel/skills/stream-trim/scripts/chain.json`
- Modify: `docs/superpowers/specs/2026-11-23-stream-trim-design.md` (record the result)

- [ ] **Step 1: Round 0.** Run compare on three stretches: `300:150` (talking), `2400:150` and `4500:150`. Before the run, find a guest or alert moment by running silencedetect on track 3 and swap it into one of the last two. Output goes to `~/Movies/stream-trim-tuning/round-0/`. Change `chain.json` `loudness.I` to the reference's measured `I` (the mean across stretches, rounded to 0.5) before running.

- [ ] **Step 2: Objective pass.** Adjust `chain.json` until, for every stretch, `|ΔI| ≤ 0.5 LU`, `|ΔLRA| ≤ 1.5 LU`, and every band from 125 to 8000 Hz is within 1.5 dB. Make one change per run, and log each change and its effect in `round-N/notes.md`. If the compand mapping can't get LRA within range, try `dB = (x - 1) * 60` before anything else.

- [ ] **Step 3: Ryan listens.** Give him the `index.html` path. Ask which of A or B he prefers per stretch, and what's off. He presses Reveal afterwards. Apply his notes and run the next round (`round-1`, ...).

- [ ] **Step 4: Gate.** Pass means Ryan says he'd ship ours. If he can't tell them apart, or prefers ours, that is a pass too. After 4 rounds without a pass, stop and ask Ryan: Resolve, trim-only, or keep going.

- [ ] **Step 5: Record and commit.** Add a "Stage 1 result" section to the spec with the final `chain.json` values, the last round's numbers, and Ryan's verdict.
  ```bash
  git add devrel/skills/stream-trim/scripts/chain.json docs/superpowers/specs/2026-11-23-stream-trim-design.md
  git commit -m "stream-trim: tuned voice chain, Stage 1 gate result"
  git push origin trunk
  ```
