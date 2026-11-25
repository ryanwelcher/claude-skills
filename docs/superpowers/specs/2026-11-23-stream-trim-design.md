# stream-trim: prep, trim, export and cut shorts from a live stream without Premiere

Date: 2026-11-23
Status: approved by Ryan 2026-11-23

## Intent and why

Ryan wants to stop using Adobe Premiere Pro. Live streams are the first
workflow to move. Today a stream goes through `stream-prep` (the Premiere
UXP plugin sets up the sequence, cuts the intro, fixes mic sync and gain),
and then Ryan does two things by hand in Premiere before exporting:

1. Trim the start and the end.
2. Apply Essential Sound > Podcast Voice to the mic.

`stream-trim` replaces both, and the Premiere step around them, with a
devrel skill and a small local browser UI. Ryan then wants the same UI
to carry on into shorts: take the finished edit and render vertical
shorts from it, so one page covers prep, trim, export and shorts for a
stream. Assembling other kinds of videos is a later, separate project.

## Goals

- From the raw OBS recording, produce a finished, upload-ready file with
  no Premiere involved.
- A browser page where Ryan checks and adjusts one In point and one Out
  point, then clicks Render.
- In and Out are pre-filled with good guesses, so most streams need only
  a glance and Render.
- Voice processing that replaces Podcast Voice closely enough that Ryan
  is happy shipping it.
- After the export, the same page shows a shortlist of shorts from the
  finished edit; Ryan picks, adjusts, and renders them there.

## Non-goals

- More than one segment per recording (no cutting out the middle).
- Overlays, graphics, titles, chapters, multi-file assembly.
- Rewriting how shorts are found, laid out or captioned. The UI drives
  the existing `stream-shorts` scripts; it doesn't replace them.
- Changing `stream-prep` or its Premiere plugin. They stay as they are
  for any stream Ryan still wants to edit in Premiere.

## Anti-goals

- Audio that sounds worse than Podcast Voice. If the ffmpeg chain can't
  get close, that is a failure even if trimming works.
- A UI that needs a build step, a framework, or a long-running service.
- Touching the original recording.

## Constraints and known facts

- Input is the raw OBS 4K mp4 (OBS "Rebrand" scene collection). Track
  layout as documented in `stream-prep/SKILL.md`: 1 Full Mix, 2 mic,
  3 guest + StreamElements, 4 Spotify, 5 theme song, 6 Firebot.
- The mic (track 2) lags video by 9 frames (0.375375 s at 23.976 fps);
  frame rate is read from the file.
- The mic is digital silence during "Starting Soon"; voice begins 4:19 to
  5:50 in. The existing Quick Action detects it with
  `silencedetect=noise=-45dB:d=2` on `0:a:1` and trusts it only if the
  silence runs at least 60 s from the start.
- ffmpeg on this Mac (homebrew-ffmpeg tap) has `arnndn`, `afftdn`,
  `deesser`, `acompressor`, `loudnorm`, `showwavespic`.
- Podcast Voice can't be inspected or scripted, so the replacement is
  an approximation tuned by ear.

## Approaches considered

- **A. Local browser trimmer + ffmpeg render (picked).** Proxy preview
  with processed audio, pre-filled In/Out, ffmpeg render with a voice
  chain. Fits the existing `stream-prep` / `stream-shorts` pattern (raw
  OBS file, ffmpeg, a skill). Cost: we build and tune it.
- B. LosslessCut for trimming plus a skill for audio. No UI to build, but
  two tools, and no pre-filled points.
- C. DaVinci Resolve Studio ($295): Voice Isolation and Dialogue Leveler
  are the closest match to Podcast Voice, and it's scriptable. But it
  swaps one heavy editor for another. Worth revisiting for the "assemble
  other videos" project, not this one.

Ryan picked A.

## Design

### Flow

1. Ryan runs the skill on a recording (`/stream-trim <file>`). The
   skill does everything `stream-prep` does today (drop Full Mix and
   Spotify, shift the mic 9 frames, find the voice start, mic gain), but
   in ffmpeg as part of the render, not by writing a Premiere project.
2. The skill runs an analysis pass and makes a preview proxy, then starts
   a local server and opens the page in the browser.
3. Ryan checks In and Out, adjusts if needed, clicks Render.
4. The server renders the final file next to the recording and the page
   shows progress, then the output path.
5. The page moves on to Shorts (below).

### Analysis

- Voice start: same silencedetect rule as the Quick Action. Default In =
  voice start minus 0.5 s lead-in. If the 60 s rule fails, In = 0.
- Voice end: last non-silent stretch on the mic. Default Out = voice end
  plus a short tail (builder's call, around 1 s).
- Waveform: a mic waveform image (or peak data) for the page.

### Preview proxy

- Low-res H.264 (about 720p) via VideoToolbox, cached next to the
  recording or in a cache dir (builder's call), reused on rerun.
- Its single audio track is the same mix and processing as the final
  render, so what Ryan hears is what ships.

### The page

- One static HTML file served by the local server. No framework, no
  build step.
- Video player on the proxy, mic waveform under it with In and Out
  markers, a playhead, and draggable markers.
- Keys like Premiere: Space play/pause, J/K/L, I and O set points,
  Left/Right nudge one frame, Shift+arrow nudge 1 s, a key to jump to
  In and to Out.
- Shows In, Out and resulting duration. A Render button.
- Sketch:

  ```
  +--------------------------------------------------+
  |                 [ video preview ]                |
  +--------------------------------------------------+
  | ▁▂▅▇▅▂▁ |[In]▅▇▆▅▇▆▅▇▆▅▇▆▅▇▆▅▇▆▅▇▆[Out]| ▁▂▁      |
  +--------------------------------------------------+
  In 0:05:12.40   Out 1:42:08.10   Length 1:36:55.70
  [I] set in  [O] set out  [←/→] 1 frame     [Render]
  ```

### Render

- Input: the original 4K recording, trimmed to In/Out (frame-accurate,
  so re-encoded, not stream-copied).
- Video: 4K (same as the recording, which is what Ryan uploads), HEVC
  through software x265 (`-preset fast -crf 24`, tag hvc1). Ryan asked for
  the smallest file at the highest quality. On a 20 s clip of the Nov 12
  stream it measured SSIM 0.997 at 1.9 Mbps, against 0.995 at 5.5 Mbps for
  h264_videotoolbox and 0.993 at 4.1 Mbps for hevc_videotoolbox, at about
  2.5x realtime.
- Audio (Ryan confirmed): one stereo mix of mic (2), guest +
  StreamElements (3), theme song (5) and Firebot (6). Full Mix (1) and
  Spotify (4) are dropped. The mic goes through the voice chain.
  Claude's call: the guest track goes through the same chain, and the
  levels of 3, 5 and 6 against the mic are set during the tuning step by
  matching Ryan's Premiere reference. Loudness normalization runs on the
  whole mix, not the mic alone.
- A 4K render of a 90+ minute stream can outlast a foreground command,
  so the server runs ffmpeg in the background and the page polls for
  progress.
- Voice chain (starting point, tuned by ear against a Premiere Podcast
  Voice export): high-pass ~80 Hz, `arnndn` noise reduction, compressor,
  light presence EQ, `deesser`, `loudnorm` to -14 LUFS / -1 dBTP
  (two-pass).
- Output: `<name>-final.mp4` next to the recording. Never overwrite; write
  to a temp name and rename on success, like `prep-stream.sh`.

### Tuning the voice chain

Part of the build, before the UI: Ryan exports a 2 to 3 minute stretch
of one stream from Premiere with Podcast Voice, his usual mic gain and
his usual mix (talking, typing, ideally a laugh). Claude renders the
same stretch through the chain and mix. Ryan listens and picks. Repeat
until he's happy. Lock the chain and levels in a script.

Reference (found 2026-11-23): the Nov 12 stream has the raw OBS file,
its `.prproj`, and Ryan's final Premiere render
(`renders/Contributor Toolkit - ... Nov 12, 2026.mp4`: 4K H.264 at
about 4.9 Mbps, AAC stereo 320k, 1:29:15). The full render is the
reference, so no separate export is needed. The `.prproj` stores the
Podcast Voice settings as plain parameters. It is a chain of standard
effects with Enhance Speech (the AI part) off: Reduce Rumble (FFT
filter), Dynamics (expander/compressor curve), DeEsser, a 10-band
graphic EQ with small boosts, Vocal Enhancer, and Loudness on. Each
has an ffmpeg counterpart, so tuning starts from these values rather
than from guesses. The mic clip level is about +1.7 dB.

This is a go/no-go gate: no UI work starts until Ryan signs off on the
audio. If several rounds can't get close, stop and decide with Ryan
(Resolve, trim-only, or something else).

### Shorts (stage 2 of the same page)

Builds on `stream-shorts` as it is (`find-stream-shorts` helper,
`shorts/shorts.json`, `scripts/shorts.py`, `render-short.sh`).

- After Render finishes, the page switches to a Shorts view.
- Finding the moments needs Claude (`find-stream-shorts` is an LLM
  skill), so the skill session, not the server, runs it and writes the
  shortlist into `shorts/candidates.json`. The page polls for that file and
  shows the candidates. The skill kicks this off automatically (Claude's call)
  once the final render is done.
- Only moments inside In/Out are offered: "from the final edit".
- How "from the edit" is built (Claude's call): shorts are still cut from
  the raw recording (so the existing mic-offset logic, transcript and
  crop presets keep working unchanged), at times inside In/Out, with
  the same mix and voice chain as the long video (Ryan confirmed shorts
  use the same audio as the long video), loudness-normalized per clip. The page shows times relative to the final edit.
- Per candidate the page shows the hook, start/end (nudgeable), the
  layout preview jpg (`shorts.py --preview`) with a `pan_x` slider, the
  caption text (`shorts.py --captions`) with a place to add fixes, and
  a checkbox. "Render selected" runs `shorts.py` on the ticked clips and
  shows progress per clip.
- Output stays `shorts/` next to the recording.

Builder-check calls (Claude's, for Ryan to check):

- The steps of `stream-shorts` that need judgment stay with Claude, in
  the skill session, which stays alive while the page is open. Before
  the shortlist reaches the page, Claude fixes dangling-word starts and
  ends, previews layouts and picks a layout or `skip` for each, and
  flags likely mishearings (shown on the page as suggested fixes).
  After "Render selected", Claude writes `shorts-descriptions.txt` and
  runs the voice pass and the em-dash/AI-ism scan on it, as today.
- File ownership: Claude writes the candidates to
  `shorts/candidates.json`. The page writes only the picked clips to
  `shorts/shorts.json`, so `shorts.py ... all` keeps meaning "what Ryan
  picked". Neither writes the other's file.
- `render-short.sh` gets an opt-in flag for the stream-trim audio. Run
  on its own, `/stream-shorts` behaves exactly as it does today unless
  Ryan asks otherwise. This is a version bump on a shipped skill.

### Where it lives

`~/repositories/claude-skills/devrel/skills/stream-trim/` with `SKILL.md`
and `scripts/`. Deployed the same way as the other devrel skills.

## Left to the builder

- Server language (Python stdlib or Node, no dependencies), port choice.
- Proxy cache location and naming.
- Waveform as an image or as peak data drawn on a canvas.
- Exact tail length after voice end.
- Progress reporting from ffmpeg to the page.

## Build order

1. Voice chain and mix tuning against Ryan's reference (go/no-go).
2. Analysis, proxy, trim page, 4K render.
3. Shorts view and the `render-short.sh` audio flag.

## Open questions

None left for Ryan, other than the reference export for step 1.

## Stage 1 result (2026-11-23)

Passed. Ryan listened to the round 1 blind A/B on the Nov 12 stream
(stretches at 5:00, 40:00 and 1:15:00 into the render, each 150 s,
level-matched) and said: "the audio is good".

Final `scripts/chain.json`:

```json
{
  "mic_gain_db": 1.71,
  "rumble_hz": 80,
  "compand": {"attacks": 0.002, "decays": 0.05,
              "points": [[-90, -90], [-84, -91], [-75, -77], [-68, -68], [-44, -33], [0, -1]]},
  "deesser": {"i": 0.4, "m": 0.5, "f": 0.5},
  "eq_db": {"250": 0.6, "500": 0.25, "2000": 0.6, "4000": 0.9, "8000": 0.3},
  "presence": {"hz": 180, "db": 0, "q": 1.0},
  "levels_db": {"guest": 0, "theme": 0, "firebot": 0},
  "loudness": {"I": -17, "TP": -1, "LRA": 20}
}
```

Round 1 numbers (ours minus reference): LRA +0.5 / +1.4 / +0.8 LU.
Octave bands 63 Hz to 8 kHz within ±1.1 dB, except 125 Hz at -1.5 dB
on stretch 1. Ours peaks at -1 dBTP; Premiere's render reaches +0.1.

Not yet checked: the guest + StreamElements track (3) through the voice
chain. Stage 2 should include one stretch with a guest or an alert.

## Stage 2 result (2026-11-24)

Real run on the Nov 12 stream (95 min raw):

- Default In 343.83 s, within 1 s of the Premiere render's 344.06. Ryan
  moved it to 344.594 s (0:05:44:14), about a frame from Premiere's start.
- Final: 4K HEVC (x265 fast, crf 24, hvc1), AAC 48 kHz stereo, 1:29:14.93
  for both streams (exactly Out minus In), 1.56 GB at 2.3 Mbps.
- Loudness on the whole file: I -17.1 LUFS, LRA 12.8 LU, TP -0.9 dBTP.
- Ryan listened and approved the audio: "The audio sounds fantastic."
- Prepare took 84 min of wall clock at 35% CPU, likely reading the raw from
  Google Drive. That needs fixing before this is a weekly tool.
- The final is written next to the raw, not in `renders/`.

## Stage 3 result (2026-11-24)

Real run on the Nov 12 stream, from the 4K final above:

- The first shortlist was empty: Whisper guessed the language from the
  opening music and transcribed the stream as Welsh. The transcriber now
  forces English (`--language en`, cache settings `v5-words-en`). The
  re-transcribed stream gave 8 candidates, all inside the edit.
- Ryan picked 3 (contributor day setup, Xdebug on one site, Pantera
  confession). All three are 1080x1920 H.264 with AAC 48 kHz stereo. Audio
  lengths are exactly end minus start plus 0.6 s (50.72, 21.14, 22.28 s), and
  loudness is I -13.9, -14.7 and -14.7 LUFS against the -14 target.
- The first render went out without the suggested caption fixes ticked, so
  "Goonberg", "XDBUG" and "Trenkill" were burned in. They were re-rendered
  with the fixes. Unticked suggestions are easy to miss.
- Added after the plan, at Ryan's request:
  - A Play button on each card. It plays a 540x960 draft with mic audio only
    and the real cut, crop and captions. A 31 s clip takes 3.6 s to make.
  - Progress for the shorts render: a moving bar while the audio is made,
    then the encoding percent from ffmpeg's `-stats`, on the card and for
    the whole batch. A 51 s short renders in about 8 s.
- Titles and descriptions went through `sounds-like-me`; Ryan approved both
  fixes.
- Next: profiles (track roles, mic delay, voice chain, loudness, caption
  font) so the skill can be shared. Today those are hardcoded in about six
  places.

## Stage 4 result (2026-11-24)

Profiles, from `2026-11-24-stream-trim-profiles-design.md`:

- A profile file now holds what was hardcoded: track roles, which track
  is the mic, mic and transcript delays in frames, the voice chain,
  shorts loudness, caption font, short layouts, and whether the
  `sounds-like-me` pass runs. Ryan's is the built-in `profiles/ryan-obs.json`.
  Teammates' profiles live in `~/.config/stream-trim/profiles/`, and
  `~/.config/stream-trim/default` names the machine's default. With no
  default the skill asks; it never falls back to Ryan's.
- Ryan's output is unchanged. `tests/test_golden.py` pins every ffmpeg
  command built for the Nov 12 setup, recorded before profiles existed,
  and still matches character for character.
- On Nov 12 with `ryan-obs`: the profile check passed, prepare reused the
  existing cache, all 8 short cards loaded, and a draft rendered.
- Simulated teammate, a 3-minute 2-track cut of Nov 12 taken through
  first-run setup: the final's audio was exactly Out minus In at -17.2
  LUFS. The short was 1080x1920 with exact audio length and the
  teammate's own layout, at -15 LUFS instead of -14, because the plain
  chain has no compressor and true peak caps the level.
- The final review found five important problems, all fixed with tests:
  a profile whose name didn't match its file, re-renders using the
  machine default instead of the stream's profile, wrong value types
  passing the check, edited profiles reusing the old cache, and a chain
  path that broke on plugin updates. The five minors it left were fixed
  in 1.46.1, including the server refusing a cache made with another
  profile.
- Not tested on a real teammate machine yet.

Follow-ups (2026-11-25, Ryan's picks):

- The final goes to `renders/<name>-final.mp4` next to the recording,
  matching his older stream folders. Shorts stay in `shorts/`, where
  stream-shorts expects them. Nov 12's final, made before this change,
  was moved into `renders/` by hand.
- `profiles.py check` prints `CLOUD_ONLY` when the raw isn't downloaded
  (the macOS dataless flag) and skips reading it, since a read can start
  the download. The skill asks Ryan to make it available offline and
  checks again. While a file is cloud-only Drive reports a wrong size
  (1.2 GB for the 8.5 GB Nov 12 raw), and the cache key uses the size, so
  prepare must only run on the downloaded file.
- New step 9: after the final (and the shorts text), stream-trim runs
  `youtube-stream-description` on the raw with a transcript window from
  In to Out on the transcript clock (`edit.in + shift`, `edit.out +
  shift`). `transcribe-file.sh` takes `TRANSCRIPT_WINDOW` and condenses
  and checks just that part of the cached transcript, counting from In, so
  nothing is transcribed twice and the chapters match the final. The
  result goes to `renders/youtube-description.txt`. The title is scored
  with viDIQ (at most 3 rounds of 4 or 5 titles, 5 credits a call, stop
  at 80). Other profiles get only the chapter list, since the template
  and voice cards are Ryan's.
- Streams tab and Show in Finder (Ryan asked whether to keep a record of
  past streams, and whether that meant an app; he kept it a skill). The
  list is built from the caches (`streams.py`), so there is no separate
  record to keep in step. `/api/reveal` takes a stream id and an item
  (raw, final, shorts, description) and resolves the path itself, so the
  page never hands the server a path. Opening another stream still goes
  through Claude, since it may need prepare and a transcript.
- Shorts before the final (Ryan: shorts are standalone, and waiting for
  the render wastes time). The Shorts tab opens right away; "inside" and
  edit times follow the page's current In/Out (prepare's defaults on the
  server before an edit exists). Shorts outside the trim are shown at the
  bottom, flagged, and still pickable. Shorts can render while the final
  encodes; both run slower.
- Finding-shorts progress: the server finds the transcriber's cache folder
  (`TRANSCRIBE_PRINT_DIR=1 transcribe-file.sh`) and reads its log: audio,
  transcribing (last cue time / stream length), checking (repair), Claude
  picking (time since `done`), ready. The Shorts tab label shows the
  percent. Rule from Ryan: nothing greyed out without a reason.
- Title picker: Claude posts options (`POST /api/titles`; final: up to 3
  viDIQ rounds; shorts: one round of 3 or 4, `type: short`). Ryan picks or
  types his own; `POST /api/title` renames the final to
  `renders/<Title>.mp4` or a short to `shorts/NN - <Title>.mp4`, with `:`
  as ` -` and `/` as `-`. `edit.json`, `shorts.json` and the cache's
  `titles.json` follow the rename, so re-renders and the Streams tab find
  the files. Descriptions are written after, with the picked titles word
  for word.
- "Claude needs you" banner (Ryan kept watching a page that looked stalled
  while Claude waited on an approval in the terminal). Hooks in the
  skill's frontmatter, live for the session once the skill starts, run
  `scripts/attention.py`: PermissionRequest and PreToolUse on
  AskUserQuestion set it, the Notification types permission_prompt,
  idle_prompt and elicitation_dialog set it, PostToolUse and
  UserPromptSubmit clear it. Page servers register in
  `~/Library/Caches/stream-trim/servers/` so the hooks find them. The page
  polls `/api/attention` and shows a sticky banner plus a "●" in the tab
  title. A denied permission isn't a hook event, so the banner then stays
  until Claude's next step or Ryan's next message. Ryan's user settings
  also got allow rules for the skill's own scripts and its local curl
  calls, so most prompts don't happen at all.
- Two looks per short (Ryan: code moments want the screen, talking moments
  want just him). Layouts gained `label`; the card shows a switch between
  the labelled ones: Code + me (`coding-rebrand`), Just me (`me`, a 9:16
  slice of the camera cutout, about 2.3x upscaled from 4K) and Just me
  square (`me-square`, a square of the camera over a blurred, dimmed copy;
  `layout.py` learned `background` plus per-band `top`). Claude picks the
  starting layout per clip. The camera is a background-removed cutout over
  the screen, so "just me" shows some editor UI behind Ryan; a separate
  camera recording in OBS would fix that (not done: Ryan isn't changing
  his OBS setup now).
- The frontmatter hooks never registered (Ryan's first real run showed no
  banner; the session ran only settings hooks). The docs don't list which
  events skill frontmatter accepts, so the hooks moved to where the docs
  confirm they work: the devrel plugin's `hooks/hooks.json`, and Ryan's
  `~/.claude/settings.json` (his skills load from the repo, not the
  plugin). Those run in every session, so each page server now records
  `CLAUDE_CODE_SESSION_ID` from the session that started it, and
  `attention.py` only posts to pages whose session matches the hook's
  `session_id`.
- A turn that ends with a question in plain text (the voice-pass "which
  fixes?") set no banner: the idle notification never fires while a
  background task (the page server) runs. A Stop hook now runs
  `attention.py stop`, which sets "Claude asked you something" when
  Claude's last message ends with a question mark (from
  `last_assistant_message`, else the transcript's tail). A turn that ends
  without a question, like waiting on a render, sets nothing.
- Shorts tab overhaul (Ryan: a rendered short stayed ticked and asked to
  render again; unclear what was rendered or queued; no way to drop one).
  Cards sit in sections by state: To render, Shortlist, Rendered, and a
  collapsed Dismissed list. Each card has a state chip. Rendered shorts
  lose the checkbox, play the real file, and get Show in Finder; editing
  one marks it "Changed since render" with its own Re-render. "Not this
  one" dismisses, Restore brings it back. Rendered state comes from
  `shorts/shorts.json` plus the files, and dismissals from the cache's
  `dismissed.json`, so both survive a reload. A rendered card reopens with
  the values it was rendered with.
