# stream-trim profiles Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move every setup value stream-trim hardcodes (tracks, mic delay, voice chain, loudness, caption font, layouts, voice pass) into named profiles, with Ryan's output byte-for-byte unchanged.

**Architecture:** A new `profiles.py` loads a profile (built-in `ryan-obs` in the repo, others in `~/.config/stream-trim/profiles/`). The stream-trim scripts ask it instead of using constants. stream-shorts never reads profiles: it gets optional flags, fed from new `shorts.json` fields that the server writes. A golden test records every ffmpeg command for Ryan's Nov 12 setup before any change and guards it after.

**Tech Stack:** Python 3 stdlib, bash, ffmpeg/ffprobe, unittest.

**Spec:** `docs/superpowers/specs/2026-11-24-stream-trim-profiles-design.md`

## Global Constraints

- Ryan's ffmpeg commands must be identical before and after (golden test from Task 1, never regenerated after Task 1).
- `stream-prep` is not touched. `stream-shorts` without the new flags keeps today's behaviour.
- `scripts/chain.json` stays where it is and unchanged.
- Built-in profiles: `devrel/skills/stream-trim/profiles/`. Personal: `~/.config/stream-trim/profiles/<name>.json`; `~/.config/stream-trim/default` names the default. A personal profile with a built-in's name wins. No `default` file means no default (never a fallback to `ryan-obs`).
- A profile that fails to load or doesn't match the recording stops with one plain `ERROR:` line before anything slow runs.
- Apple Silicon Macs only; no encoder, transcriber or path changes.
- No em-dashes in prose the skill writes. Push to trunk; no branch or worktree.
- Tests: `python3 -m unittest discover -s devrel/skills/stream-trim/tests && python3 -m unittest discover -s devrel/skills/stream-shorts/tests` from the repo root (both must pass at every task end).

## Review Focus

1. A personal profile with a JSON typo or a missing field: one `ERROR:` line naming the file and the field, no traceback. (Task 2: `test_bad_json`, `test_missing_field`.)
2. A profile whose track numbers exceed `audio_tracks`, or whose role names don't match the chain's levels: rejected at load. (Task 2: `test_track_out_of_range`, `test_role_not_in_chain`.)
3. A recording with more or fewer tracks than the profile (a 7-track file on `ryan-obs`): stops before prepare. (Task 3: `test_prepare_rejects_track_mismatch`.)
4. Re-running a cached recording under a different profile: the proxy is rebuilt, not reused with the old mix; a cache from before profiles counts as `ryan-obs` and is reused. (Task 3: `test_cache_rebuilt_for_other_profile`, `test_legacy_cache_is_ryan`.)
5. A teammate layouts file and a per-recording `shorts/layouts.json` both defining a layout: the per-recording one wins. (Task 4: `test_layouts_files_in_order`.)

---

### Task 1: Golden commands for ryan-obs

**Files:**
- Create: `devrel/skills/stream-trim/tests/test_golden.py`
- Create: `devrel/skills/stream-trim/tests/golden/ryan-obs-commands.json` (generated)

**Interfaces:**
- Produces: `test_golden.capture() -> dict[str, list|str]`, the commands keyed by name. Later tasks only change the call sites inside `capture()` when a signature changes; the JSON file is never regenerated after this task.

- [ ] **Step 1: Record Nov 12's probe values**

Run: `python3 -c "import sys; sys.path.insert(0,'devrel/skills/stream-trim/scripts'); import audio_chain; print(audio_chain.probe('$HOME/Library/CloudStorage/GoogleDrive-ryan.welcher@a8c.com/My Drive/Videos/Streams/Nov 12/2026-11-12 10-24-27.mp4'))"`
Expected: `(6, <duration>, 23.976...)`. Put these three values in `test_golden.py` as `NOV12 = (tracks, duration, fps)`.

- [ ] **Step 2: Write `capture()` and the test**

`capture()` builds, with today's code, the commands for Ryan's setup on the raw path `RAW = "/rec/Nov 12/2026-11-12 10-24-27.mp4"`:
- `prepare`: patch `audio_chain.probe` to return `NOV12`, `prepare.cache_dir` to a temp dir, and `subprocess.Popen` to record argv and raise a sentinel exception.
- `final_pass1`, `final_pass2`: `render.render_final(RAW, 344.59425, 5699.527166666666, chain)` with `render._run` patched to record args and return a canned loudnorm JSON block (`input_i -20.1`, `input_tp -3.2`, `input_lra 9.8`, `input_thresh -30.5`, `target_offset 0.4`); `os.path.exists` for the output path returns False.
- `stretch_pass1`, `stretch_pass2`: `audio_chain.render_stretch(RAW, 463.0, 50.72, short_audio.shorts_chain(chain), "/out/a.wav")` with `measure.run_ffmpeg` patched the same way.
- `short_default`, `short_mix`, `short_draft`, `short_preview`: `render-short.sh --dry-run` (plus `--mix-audio /x/short_audio.py`, `--draft`, `--preview`) on a generated 6-track 24000/1001 file (`test_measure.make_mp4`), words `[[1.0,1.4,"hello"],[1.5,2.0,"world"]]`, start `1` end `3`.
- `shorts_py`: `shorts.py --dry-run` on a manifest made by `shorts_view.merge_picks` for one clip `{"file":"01-x.mp4","start":"00:00:01.00","end":"00:00:03.00"}` with `mix_audio` set.

Normalize before comparing: the generated file path to `<RAW>`, temp dirs to `<TMP>`, the words path to `<WORDS>`; strip the `printf %q` backslashes. `GOLDEN_WRITE=1` writes the JSON; otherwise `test_ryan_obs_commands_unchanged` asserts `capture() == json.load(golden)` key by key with `self.assertEqual(got[k], want[k], k)`.

- [ ] **Step 3: Check the generated file matches the real one**

Run `render-short.sh --dry-run` on the real Nov 12 raw and on the generated file with the same words, start and end; normalize both paths.
Expected: identical output. Commands depend only on track count, fps and paths, so the stubbed baseline equals a real dry run. Ledger this as a Ruling (spec asked for real dry runs).

- [ ] **Step 4: Write the golden file and run the test**

Run: `GOLDEN_WRITE=1 python3 -m unittest test_golden` (in `stream-trim/tests`), then without `GOLDEN_WRITE`.
Expected: OK both times; the JSON has all 10 keys.

- [ ] **Step 5: Prove the test bites**

Temporarily change `MIC_LAG_FRAMES = 9` to `8` and run the test.
Expected: FAIL naming `prepare` (and others). Revert.

- [ ] **Step 6: Commit**

```bash
git add devrel/skills/stream-trim/tests/test_golden.py devrel/skills/stream-trim/tests/golden
git commit -m "stream-trim: golden ffmpeg commands for Ryan's setup"
```

---

### Task 2: profiles.py, ryan-obs and chain-plain

**Files:**
- Create: `devrel/skills/stream-trim/scripts/profiles.py`
- Create: `devrel/skills/stream-trim/profiles/ryan-obs.json`
- Create: `devrel/skills/stream-trim/profiles/chain-plain.json`
- Test: `devrel/skills/stream-trim/tests/test_profiles.py`

**Interfaces:**
- Produces:
  - `profiles.ProfileError(ValueError)`; `profiles.NoDefault(ProfileError)`.
  - `profiles.config_dir() -> str`: `$STREAM_TRIM_CONFIG` or `~/.config/stream-trim`.
  - `profiles.default_name() -> str | None`.
  - `profiles.load(name: str | None = None) -> dict`: the profile JSON plus `"path"`, `"chain_path"` (absolute), `"chain"` (loaded dict), `"layouts_path"` (absolute or None). `name=None` uses the default; raises `NoDefault` if none.
  - `profiles.roles(p) -> list[tuple[str, int]]`: `(role, track)` sorted by track number.
  - `profiles.voice_roles(p) -> set[str]`.
  - `profiles.mic_index(p) -> int` (0-based audio stream index).
  - `profiles.mic_shift(p, fps) -> float` = `round(mic_lag_frames / fps, 6)`.
  - `profiles.transcript_shift(p, fps) -> float` = `round(transcript_lag_frames / fps, 6)`.
  - `profiles.check_recording(p, tracks: int) -> None`; raises `ProfileError("this recording has 7 audio tracks; profile ryan-obs expects 6")`.
  - CLI: `profiles.py check <raw> [--profile NAME]` prints `PROFILE <name>`, or `ERROR: NO_DEFAULT ...` / `ERROR: <mismatch>` and exits 1. `profiles.py samples <raw> <outdir> [--at SECONDS]` writes `track-N.wav` (5 s each, default `--at` 10% into the file) and prints the paths. `profiles.py set-default <name>` writes `default`.

- [ ] **Step 1: Write the profile files**

`ryan-obs.json`: the spec's example verbatim except `"chain": "../scripts/chain.json"` and no `layout` field: `"layouts": null`. Ruling for the ledger: the layouts file's existing `"default"` key (layout.py already honours it) names a teammate's default layout, so a separate `layout` field would be a second source for the same thing.
`chain-plain.json`: today's `chain.json` shape with `mic_gain_db 0`, `levels_db` all 0, `loudness` equal to `chain.json`'s, and the voice filters neutral: `rumble_hz 0`, `compand` null, `deesser` null, `eq_db {}`, `presence` null. `audio_chain.voice_filters` must skip null/empty/0 entries (covered in Task 3).

- [ ] **Step 2: Write the failing tests**

```python
class ProfilesTest(unittest.TestCase):  # setUp: STREAM_TRIM_CONFIG -> temp dir
    def test_ryan_obs_values(self):
        p = profiles.load("ryan-obs")
        self.assertEqual(profiles.roles(p), [("mic", 2), ("guest", 3), ("theme", 5), ("firebot", 6)])
        self.assertEqual(profiles.voice_roles(p), {"mic", "guest"})
        self.assertEqual(profiles.mic_index(p), 1)
        self.assertEqual(profiles.mic_shift(p, 24000 / 1001), 0.375375)
        self.assertEqual(p["chain"], audio_chain.load_chain(CHAIN_JSON))
        self.assertIsNone(p["layouts_path"])
    def test_no_default(self):          # no default file -> NoDefault, even though ryan-obs exists
    def test_default_file(self):        # default "ryan-obs" -> load() returns it
    def test_personal_wins(self):       # ~/.config/.../ryan-obs.json with audio_tracks 2 shadows the built-in
    def test_bad_json(self):            # ProfileError message contains the file name
    def test_missing_field(self):       # no "mic" -> message contains "mic"
    def test_track_out_of_range(self):  # track "7" with audio_tracks 6
    def test_role_not_in_chain(self):   # role "cohost" not in chain levels_db
    def test_check_recording(self):     # 7 vs 6 -> exact message above
    def test_cli_check(self):           # on a generated 6-track file with default ryan-obs -> "PROFILE ryan-obs"; with no default -> exit 1, "NO_DEFAULT"
    def test_cli_samples(self):         # 2-track 12 s file, --at 2 -> track-1.wav and track-2.wav, each 5.0 s
```

- [ ] **Step 3: Run them**

Run: `python3 -m unittest test_profiles` (in `stream-trim/tests`). Expected: FAIL, `No module named 'profiles'`.

- [ ] **Step 4: Implement `profiles.py`**

Validation on load: required fields `name, audio_tracks, tracks, mic, mic_lag_frames, transcript_lag_frames, chain, shorts_loudness, caption_font, voice_pass`; track keys are integers 1..audio_tracks; role names unique; `mic` is a key of `tracks` with `voice: true`; every role except the mic role is in `chain["levels_db"]`. Resolve `chain` and `layouts` relative to the profile file's folder.

- [ ] **Step 5: Run the tests, then both suites**

Expected: all OK, golden still OK.

- [ ] **Step 6: Commit**

```bash
git add devrel/skills/stream-trim/scripts/profiles.py devrel/skills/stream-trim/profiles devrel/skills/stream-trim/tests/test_profiles.py
git commit -m "stream-trim: profiles loader, ryan-obs and chain-plain"
```

---

### Task 3: stream-trim audio and prepare read the profile

**Files:**
- Modify: `scripts/audio_chain.py` (drop `TRACKS`, `ROLES`, `VOICE_ROLES`, `MIC_LAG_FRAMES`; `voice_filters` skips null/empty/0 entries)
- Modify: `scripts/prepare.py`, `scripts/render.py`, `scripts/short_audio.py`, `scripts/compare.py`
- Test: `tests/test_audio_chain.py`, `tests/test_prepare.py`, `tests/test_render.py`, `tests/test_short_audio.py`, `tests/test_golden.py` (call sites only)

**Interfaces:**
- Consumes: Task 2's `profiles.*`.
- Produces:
  - `audio_chain.mix_graph(profile, fps) -> (graph, mic_shift)`; `audio_chain.build_filtergraph(chain, inputs, mic_shift_s, roles, voice_roles)`.
  - `audio_chain.render_stretch(raw, start_s, seconds, profile, out_wav, loudness=None)`: `loudness` overrides the chain's for shorts.
  - `prepare.prepare(raw, profile, progress=None)`; `analysis.json` gains `"profile": name`.
  - `render.render_final(raw, in_s, out_s, profile, progress=None, stop=None)`.
  - `short_audio.py` loads `profiles.load(os.environ.get("STREAM_TRIM_PROFILE"))` and uses its `shorts_loudness`.
  - CLIs `prepare.py <raw> [--profile NAME]`.

- [ ] **Step 1: Write the failing tests**

```python
def test_prepare_rejects_track_mismatch(self):    # 7-track file, ryan-obs -> ProfileError "has 7 audio tracks", no cache dir written
def test_cache_rebuilt_for_other_profile(self):   # prepare under ryan-obs, then under a 6-track test profile -> proxy rebuilt, analysis["profile"] updated
def test_legacy_cache_is_ryan(self):              # analysis.json without "profile" + ryan-obs -> returned as is, no ffmpeg run
def test_two_track_profile_renders(self):         # 2-track file, profile tracks {"1": mic voice, "2": theme}, lags 0, chain-plain -> render_final output has audio 6.0 s and I within 1 LU of the chain target
def test_voice_filters_plain(self):               # voice_filters(chain-plain) == "" and build_filtergraph still valid
def test_short_audio_uses_profile(self):          # STREAM_TRIM_PROFILE=<2-track test profile> -> WAV made from track 1
```

- [ ] **Step 2: Run them**

Expected: FAIL (wrong signatures / missing behaviour).

- [ ] **Step 3: Implement**

Replace each hardcoded value with the profile lookup: the "6 audio tracks" checks become `profiles.check_recording`; `TRACKS["mic"]` becomes `mic_index`; `MIC_LAG_FRAMES / fps` becomes `mic_shift`; inputs come from `roles(p)` in track order (Ryan's order equals today's `ROLES`). In `prepare`, check the profile before creating the cache dir; reuse a cached analysis only when its `profile` (missing means `ryan-obs`) equals the profile's name. Update `test_golden.capture()` call sites to pass `profiles.load("ryan-obs")`.

- [ ] **Step 4: Run both suites**

Expected: all OK, including `test_ryan_obs_commands_unchanged`.

- [ ] **Step 5: Commit**

```bash
git add devrel/skills/stream-trim/scripts devrel/skills/stream-trim/tests
git commit -m "stream-trim: audio, prepare and render read the profile"
```

---

### Task 4: stream-shorts flags

**Files:**
- Modify: `devrel/skills/stream-shorts/scripts/render-short.sh`, `make-captions.py`, `layout.py`, `shorts.py`, `SKILL.md` (document the new `shorts.json` fields and `mix_audio`)
- Test: `devrel/skills/stream-shorts/tests/test_profile_flags.py`

**Interfaces:**
- Produces:
  - `render-short.sh --mic-track N --mic-lag-frames F --transcript-lag-frames F --font-name NAME --font-file FILE`. When given: mic stream `N-1`; `OFFSET = F_transcript * den / num` with the same awk expression as today; mic audio input `-ss` at `VS + F_mic * den / num` (literally `$S` when the two lags are equal, so Ryan's command is unchanged); font check looks for `FILE` in `~/Library/Fonts` and `/Library/Fonts`. Absent: today's code path.
  - `make-captions.py --font NAME` (default `Jost SemiBold`).
  - `layout.py`: `SHORTS_LAYOUTS` may hold several files joined by `os.pathsep`, applied in order; later files win, `default` included.
  - `shorts.json` top-level fields `mic_track`, `mic_lag_frames`, `transcript_lag_frames`, `caption_font` (`{"name","file"}`), `layouts` (path). `shorts.py` turns them into the flags above (render, draft and preview modes) and sets `SHORTS_LAYOUTS` to `<layouts>` then `<shorts dir>/layouts.json`.

- [ ] **Step 1: Write the failing tests**

```python
def test_two_track_dry_run(self):        # 2-track file, --mic-track 1 --mic-lag-frames 0 --transcript-lag-frames 0 -> "[1:a:0]loudnorm", VS == 0.8
def test_mic_lag_differs(self):          # 6-track, mic lag 9, transcript lag 0 -> video -ss 0.8, audio -ss 0.8 + 9*1001/24000
def test_font_flags(self):               # --font-name "Inter Bold" --font-file Inter-Bold.ttf, font missing -> exit 1 naming Inter-Bold.ttf
def test_make_captions_font(self):       # --font "Inter Bold" -> ASS Style line uses Inter Bold
def test_layouts_files_in_order(self):   # two files both define "cam" and "default"; second wins for both
def test_shorts_py_passes_profile(self): # manifest with all five fields -> dry run shows the flags' effect and SHORTS_LAYOUTS order
def test_no_flags_unchanged(self):       # existing test_mix_audio cases still pass (run in the suite)
```

- [ ] **Step 2: Run them**

Expected: FAIL (unknown option / no font flag).

- [ ] **Step 3: Implement the flags**

- [ ] **Step 4: Run both suites**

Expected: all OK, golden unchanged.

- [ ] **Step 5: Commit**

```bash
git add devrel/skills/stream-shorts
git commit -m "stream-shorts: optional mic, lag, font and layouts settings"
```

---

### Task 5: Server and page use the profile

**Files:**
- Modify: `scripts/server.py`, `scripts/shorts_view.py`, `scripts/page.html`
- Test: `tests/test_server.py`, `tests/test_shorts_view.py`, `tests/test_page.py`

**Interfaces:**
- Consumes: Tasks 2-4.
- Produces:
  - `server.make_server(raw, profile, port=0, shorts_py=SHORTS_PY)`; CLI `server.py <raw> [--profile NAME]`; on a load error or mismatch it exits with `ERROR: ...` before printing `READY`.
  - `self.shift = profiles.transcript_shift(profile, fps)` (Ryan: unchanged 0.375375).
  - `/api/state` and `/api/shorts` gain `"profile": name`; `/api/shorts` layouts overlay order: stream-shorts built-ins, profile `layouts_path`, `shorts/layouts.json`.
  - `shorts_view.merge_picks(existing, recording, words, mix_audio, picks, profile)` writes the five Task 4 fields: `mic_track` (1-based), the two lags, `caption_font`, `layouts` (omitted when None).
  - Every `shorts.py` run (preview, draft, captions, render) gets `STREAM_TRIM_PROFILE=<name>` in its environment; the work manifest carries the same five fields.
  - Page: the profile name after the recording name in the header (`<span id="profile">`).

- [ ] **Step 1: Write the failing tests**

```python
def test_state_has_profile(self):             # /api/state["profile"] == "ryan-obs"
def test_shorts_json_has_profile_fields(self):# after a render: mic_track 2, lags 9/9, caption_font Jost, no "layouts"
def test_profile_layouts_overlay(self):       # test profile with a layouts file defining "cam" -> /api/shorts layouts has "cam"; shorts/layouts.json redefining it wins
def test_shorts_env_profile(self):            # stub logs os.environ["STREAM_TRIM_PROFILE"] == profile name
def test_server_cli_mismatch(self):           # server.py on a 2-track file with default ryan-obs -> exit 1, "ERROR:", no READY
```
Plus `test_page.py`: `'id="profile"'` and `S.profile` in the page.

- [ ] **Step 2: Run them**

Expected: FAIL.

- [ ] **Step 3: Implement**

- [ ] **Step 4: Run both suites**

Expected: all OK, golden unchanged.

- [ ] **Step 5: Commit**

```bash
git add devrel/skills/stream-trim
git commit -m "stream-trim: server and page run on the chosen profile"
```

---

### Task 6: SKILL.md, Ryan's default, real runs

**Files:**
- Modify: `devrel/skills/stream-trim/SKILL.md`, `.claude-plugin/marketplace.json`, `devrel/.claude-plugin/plugin.json` (1.46.0), README stream-trim row (mention profiles)
- Create (Ryan's machine, outside the repo): `~/.config/stream-trim/default` containing `ryan-obs`

**Interfaces:**
- Consumes: the CLIs from Tasks 2, 3 and 5.

- [ ] **Step 1: SKILL.md**

- Requirements line: Apple Silicon Mac.
- New step before prepare: run `profiles.py check <raw> [--profile NAME]`. `PROFILE <name>`: go on with `--profile <name>` on every script. `NO_DEFAULT` or a mismatch: stop and ask which profile, or offer first-run setup. Nothing slow runs first.
- First-run setup section: the spec's seven steps, using `profiles.py samples`, stream-shorts' "Adding a layout" steps (saving to `~/.config/stream-trim/profiles/<name>-layouts.json` with `"default"` set to the new layout), `chain-plain.json` (path relative to the profile: write the absolute path of the built-in), `voice_pass: null`, then `profiles.py check` to validate and `profiles.py set-default` if there is no default.
- Descriptions step: run `sounds-like-me` only when the profile's `voice_pass` is `sounds-like-me`; the em-dash and AI-ism scan always runs.
- Ryan can name a profile in the request.

- [ ] **Step 2: Ryan's default and his real run**

Write `~/.config/stream-trim/default` = `ryan-obs`. Run `profiles.py check` on the Nov 12 raw, then start the server on it.
Expected: `PROFILE ryan-obs`; the server reuses the existing Nov 12 cache (no prepare run) and the page header shows `ryan-obs`. Press Play on one card; the draft plays.

- [ ] **Step 3: Teammate simulation**

Cut a 3-minute 2-track file from Nov 12 into the scratchpad (`-map 0:v -map 0:a:1 -map 0:a:4`, so mic on track 1, theme on track 2). With `STREAM_TRIM_CONFIG` set to a scratch folder, follow the SKILL first-run setup: `check` gives `NO_DEFAULT`, `samples` gives two 5 s WAVs, write a profile (mic track 1 voice, theme track 2, mic lag 9, transcript lag 9, chain-plain, a layouts file copying `coding-rebrand` as `test-cam`, default `test-cam`). Prepare, render a final with In 10 / Out 170, write a one-clip `candidates.json`, render it from the page.
Expected: final has audio = Out minus In and I within 1 LU of the chain target; the short is 1080x1920 and uses `test-cam`; nothing under the real `~/.config/stream-trim` changed except Step 2's `default`.

- [ ] **Step 4: Run both suites, commit, push**

```bash
git add devrel .claude-plugin README.md
git commit -m "stream-trim: profiles (Stage 4), devrel 1.46.0"
git push origin HEAD
```
