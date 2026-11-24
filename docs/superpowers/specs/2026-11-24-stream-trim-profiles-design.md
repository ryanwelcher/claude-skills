# stream-trim profiles (Stage 4)

## Intent

stream-trim replaces Premiere for Ryan's streams, but it assumes his exact
OBS setup: 6 audio tracks in fixed roles, a mic that runs 9 frames late, his
Podcast Voice settings, his caption font and his voice cards. A profile
describes a setup in one file, so a teammate with their own OBS setup can use
the same skill without editing code.

It is mostly for Ryan. The whole thing is an experiment in leaving Premiere,
and his current setup must not change.

## Goals

- Ryan's run is unchanged: `/stream-trim <file>` uses his profile
  automatically, he never picks one, and every ffmpeg command is identical
  to today's.
- A teammate can run stream-trim on their own OBS recording. On their first
  run Claude helps them build a profile, and every later run uses it.
- One place describes a setup. No script hardcodes track numbers, the mic
  delay, loudness targets or the caption font.

## Non-goals

- `stream-prep` is not touched. It stays as Ryan's fallback if the
  experiment fails.
- `stream-shorts` used on its own (including on a `-edit.mp4`) keeps today's
  behaviour. It gets optional flags; its defaults stay Ryan's values.
- No shared repository of teammates' profiles.
- No automatic measurement of a teammate's mic delay.
- No caption styles beyond the font.
- No Windows or Linux support. Apple Silicon Macs only (Ryan's decision):
  the encoder, transcriber and paths stay as they are, and SKILL.md states
  the requirement.

## Anti-goals

- Any change to Ryan's output. A profile system that renders his streams
  even slightly differently has failed, however tidy it is.
- A wrong profile that renders quietly. A mismatch must stop the run before
  anything slow starts.

## Approaches

1. **One profile file the scripts read (picked).** A loader returns the
   default profile, or a named one. Every hardcoded value becomes a lookup.
   First-run setup writes the same file. Small change, easy to test, one
   source of truth.
2. A settings file in each recording's folder. It suits one-off setups, but
   a teammate would set it up again for every stream.
3. No file; Claude passes every value as options. Fragile: a missed option
   silently falls back to Ryan's values, the quiet wrong render this design
   must avoid.

## Decisions

### Where profiles live (Ryan's decision)

- Ryan's profile `ryan-obs` ships in the repo at
  `devrel/skills/stream-trim/profiles/ryan-obs.json`. It is the built-in
  default and the example teammates copy.
- Everyone else's profiles live on their own machine in
  `~/.config/stream-trim/profiles/<name>.json`. A plugin update never
  touches them, and nothing goes through Ryan's repo.
- `~/.config/stream-trim/default` holds the name of that person's default
  profile. A profile in `~/.config` with the same name as a built-in one
  wins.
- With no `default` file there is no default (Claude's call, from the
  builder check): the skill asks once which profile this machine uses, or
  runs first-run setup, and writes the file. Falling back to `ryan-obs`
  would let a teammate whose OBS also writes 6 tracks render with Ryan's
  roles, delay and voice chain without any error. Ryan's machine gets its
  `default` file (`ryan-obs`) as part of this change, so he is never asked.

### What a profile holds

Field names are a proposal; the builder may refine them.

```json
{
  "name": "ryan-obs",
  "audio_tracks": 6,
  "tracks": {
    "2": {"role": "mic", "voice": true},
    "3": {"role": "guest", "voice": true},
    "5": {"role": "theme"},
    "6": {"role": "firebot"}
  },
  "mic": "2",
  "mic_lag_frames": 9,
  "transcript_lag_frames": 9,
  "chain": "chain.json",
  "shorts_loudness": {"I": -14, "TP": -1.5},
  "caption_font": {"name": "Jost SemiBold", "file": "Jost-SemiBold.ttf"},
  "layout": "coding-rebrand",
  "layouts": null,
  "voice_pass": "sounds-like-me"
}
```

- **tracks**: the kept tracks, by OBS track number (1-based), with a role
  name. Unlisted tracks are dropped (Ryan: 1 Full Mix, 4 Spotify).
  `voice: true` means the voice chain applies to that track.
- **mic**: the voice track used for the 9:16 drafts and as the anchor for
  the lag trim.
- **mic_lag_frames**: how many frames late the mic is against the video.
  0 for a setup without the problem.
- **transcript_lag_frames**: how late track 1 is. The shared transcriber
  (`analyze-stream-recording`, not changed here) decodes the file's first
  audio track, so the transcript's clock follows track 1. For Ryan, track 1
  is the Full Mix, which lags with the mic: 9. The current code assumes the
  transcript clock equals the mic clock; this field makes it explicit.
- **chain**: the chain file for the final mix: voice processing, per-role
  levels and the final loudness, in today's `chain.json` shape, resolved next
  to the profile. Ryan's points at today's `scripts/chain.json`, which stays
  where it is and unchanged (it is what his blind A/B approved). A shipped
  `chain-plain.json` has the voice processing off and levels at 0 dB; new
  profiles use it unless the teammate tunes their own. Its role levels are
  keyed by role name, so role names in `tracks` and `chain` must match; the
  loader checks this.
- **shorts_loudness**: replaces the `-14 / -1.5` constant in
  `short_audio.py`.
- **caption_font**: replaces the Jost name in `make-captions.py` and the
  font-file check in `render-short.sh`.
- **layout** and **layouts** (Ryan's decision): the default short layout for
  this setup, and an optional layouts file next to the profile in
  stream-shorts' `layouts.json` shape. Ryan's profile names
  `coding-rebrand` and has no file, so today's built-in layouts apply. A
  teammate's profile names the layout first-run setup built and points at
  their file. stream-trim passes the file to stream-shorts the way a
  per-recording `shorts/layouts.json` is passed today (a per-recording file
  still overrides both), and uses `layout` as each candidate's default.
- **voice_pass**: `sounds-like-me` for Ryan. `null` for a teammate: shorts
  titles and descriptions are written plain and the voice-card pass is
  skipped. The separate em-dash and AI-ism scan always runs.

### Choosing a profile

- The skill uses the person's default profile.
- Before prepare starts, it checks the recording against the profile: the
  audio track count must equal `audio_tracks`. On a mismatch it stops and
  asks which profile to use, or offers first-run setup. Nothing slow runs on
  a mismatched profile.
- Ryan can name a profile in the request ("trim this with the laptop
  profile"). The server takes `--profile NAME`.
- The page shows the profile name next to the recording name.

### First-run setup (teammates)

Run by Claude when there is no profile in `~/.config` and the recording
doesn't match `ryan-obs`, or when asked:

1. List the recording's audio tracks, and cut a 5-second sample of each from
   a stretch where the person is talking, into a temp folder, so they can
   hear which is which.
2. Ask what each track is and which to drop. Voice tracks get `voice: true`.
3. Ask about mic delay. If they don't know it, use 0 and say how to check:
   open the Shorts tab, press Play on a draft and watch the lips. Same for
   `transcript_lag_frames`, which follows track 1.
4. Warn if track 1 carries no voice, since the transcript (and the
   shortlist) come from track 1.
5. Build their short layout, following stream-shorts' "Adding a layout"
   steps: grab a full frame from a stretch of their usual scene, work out
   the facecam and screen boxes with them, preview it, and save it in
   `~/.config/stream-trim/profiles/<name>-layouts.json`.
6. Use `chain-plain.json`, Ryan's shorts loudness and font, and
   `voice_pass: null`.
7. Write `~/.config/stream-trim/profiles/<name>.json` and, if there is no
   default yet, `~/.config/stream-trim/default`.

### What changes in the code

Every place that hardcodes a setup value reads the profile instead:

- `audio_chain.py`: `TRACKS`, `ROLES`, `VOICE_ROLES`, `MIC_LAG_FRAMES`.
- `prepare.py`, `render.py`, `compare.py`: the "6 audio tracks" checks and
  the mic track index.
- `server.py`: the shift, the default layout and layouts file, and passing
  the profile to everything it runs.
- `short_audio.py`: the shorts loudness.
- `render-short.sh`, `make-captions.py`, `shorts.py` (stream-shorts): new
  optional flags for the mic track, lag frames and caption font, passed
  through from a `shorts.json` field the same way `mix_audio` is. Without
  them, today's behaviour. stream-shorts never reads profiles itself.
- `SKILL.md`: profile check before prepare, first-run setup, and
  `voice_pass` deciding whether `sounds-like-me` runs.

## Constraints

- Ryan's ffmpeg commands must be identical before and after. Proof: record
  every command each script builds for the Nov 12 recording (final render,
  prepare, short audio, shorts render, draft, still) before the change, and
  a test compares them character for character after. The Nov 12 raw is on
  this machine (available offline in Drive), so the baseline comes from real
  dry runs, captured before any code changes.
- All existing stream-trim and stream-shorts tests keep passing.
- A profile that fails to load or doesn't match the recording stops the run
  with one plain error line naming the problem.
- No em-dashes in any prose the skill writes.

## Left to the builder

- The loader's exact API, and how the shell script gets values (flags from
  Python callers, as proposed above).
- Exact field names and validation messages.
- How the command recording for the identical-output test is captured
  (dry-run flags exist on the shorts side; the Python side may need a hook).
- Contents of `chain-plain.json` beyond "voice processing off, levels 0 dB,
  loudness the same as Ryan's final".
