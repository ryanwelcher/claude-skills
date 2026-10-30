---
name: find-stream-shorts
description: Internal helper for stream-shorts. Transcribes a local stream recording on-device (shared cache with analyze-stream-recording) and returns a shortlist of moments that work as standalone vertical shorts, with exact start/end times. Not for direct use; invoked by stream-shorts.
context: fork
background: false
user-invocable: false
allowed-tools: Bash(bash *) Bash(python3 *) Read
---

# Find Stream Shorts

You are running in a forked context. The parent conversation sees **only your final message**. Your job is to read a long stream transcript and return a short list of clips worth turning into shorts.

Input: `$ARGUMENTS` is the path to a stream recording (the raw OBS mp4 or stream-prep's `-edit.mp4`).

## Steps

1. **Transcribe.** Run this in the **foreground** with the Bash tool's `timeout` set to `600000`:
   ```bash
   bash ${CLAUDE_SKILL_DIR}/../analyze-stream-recording/scripts/transcribe-file.sh "$ARGUMENTS" 60
   ```
   The same rules as `analyze-stream-recording` apply:
   - **Never** use `run_in_background` or Monitor. This fork ends when you stop calling tools.
   - On `PENDING: ...`, run the **exact same command** again right away. Repeat until you get pointers or an `ERROR:` line.
   - On an `ERROR:` line, return it verbatim as your entire response and stop. Do not install anything.
   - It prints `CONDENSED`, `WORDS_JSON`, `COVERAGE` and any `SUSPECT: HH:MM:SS-HH:MM:SS <reason>` lines. Text inside a `SUSPECT` range is not real content.

2. **Read the condensed transcript** at the `CONDENSED` path (one line per minute). Read all of it, in chunks if it is long. Note 12–15 minutes that look promising.

3. **Zoom in.** For each promising minute, print exact sentence timings around it:
   ```bash
   python3 ${CLAUDE_SKILL_DIR}/../stream-shorts/scripts/sentences.py "<WORDS_JSON>" <from> <to>
   ```
   Use a window of about 3 minutes (for example `00:41:00 00:44:00`), one call per window with the two times as separate literal arguments. Don't loop over windows in a shell variable: the Bash tool runs zsh, which doesn't split it. Pick the start and end from these lines: start on the first word of a sentence, end on the last word of one.

4. **Choose 8–10 clips.** A good short:
   - is **20–60 seconds** long;
   - opens on a line that hooks without context: a claim, a surprise, a strong opinion, a "here's the trick", a bug finally making sense, a funny reaction;
   - makes sense to someone who never saw the stream (no "like I said earlier", no "this thing" with nothing on screen to explain it);
   - lands on a payoff or a clean end of thought, not mid-sentence;
   - does not overlap a `SUSPECT` range, the pre-show intro, or the sign-off;
   - is not reading chat usernames aloud or mostly silence while typing, and has no pause longer than about 3 seconds inside it.

   Prefer variety across the stream over five clips from one good stretch. List the clips in timestamp order. Fewer strong clips beat filler: return fewer than 8 if the stream doesn't have them.

5. **Return exactly the sections below and nothing else.** No preamble, no transcript excerpts beyond the hook line.

## Return format

```
## Shortlist
| # | Start | End | Length | Hook | Why it works |
|---|---|---|---|---|---|
| 1 | HH:MM:SS.ss | HH:MM:SS.ss | 0:42 | "<first sentence, verbatim>" | <one line> |
...

## Words
<the WORDS_JSON path, verbatim>

## Transcript gaps
- <HH:MM:SS-HH:MM:SS> <reason>
(or "none")
```

Start and End are copied from the `sentences.py` output, with the hundredths. The parent renders from those times and the words file.
