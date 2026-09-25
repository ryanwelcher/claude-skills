---
name: analyze-stream-recording
description: Internal helper for youtube-stream-description. Transcribes a local stream recording on-device (ffmpeg + mlx_whisper) and returns a recap summary, a YouTube-valid chapter list, and any links mentioned aloud. Not for direct use; invoked by youtube-stream-description when the user supplies a video file path.
context: fork
model: sonnet
background: false
user-invocable: false
allowed-tools: Bash(bash *) Read
---

# Analyze Stream Recording

You are running in a forked context. The parent conversation will see **only your final
message**, so everything you read here stays here. Your job is to turn a long transcript
into a few hundred tokens the parent can draft from.

Input: `$ARGUMENTS` is the path to a local video/audio file (mp4/mov/mkv/wav).

## Steps

1. **Transcribe.** Run this in the **foreground** with the Bash tool's `timeout` set to `600000`:
   ```bash
   bash ${CLAUDE_SKILL_DIR}/scripts/transcribe-file.sh "$ARGUMENTS"
   ```
   - **Never** use `run_in_background`, Monitor, or anything else that waits for a later notification. This fork ends the moment you stop calling tools, and nothing can wake it again. A result that arrives after that is lost, and the parent gets nothing. Do not end your turn until you have the three sections below or an `ERROR:` line.
   - It prints only pointers: `CONDENSED: <path>`, `LINES`, `WORDS`, `SRT: <path>`, `COVERAGE: <n>%`, and zero or more `SUSPECT: HH:MM:SS-HH:MM:SS <reason>` lines. It never prints the transcript.
   - A `SUSPECT` range is a stretch where Whisper looped on one phrase or heard nothing. Looped ranges were already re-transcribed once, so any that remain are real failures. The transcript there is not real content.
   - If it prints `PENDING: ...`, the transcription is still running in a detached job. Run the **exact same command** again right away, in the foreground. It picks up the same job and does not restart it. Repeat until you get pointers or an `ERROR:` line.
   - If it prints an `ERROR:` line (missing `ffmpeg` or `mlx_whisper`, bad path, failed job), return that line verbatim as your entire response and stop. Do **not** attempt to install anything; the parent handles that.
   - Results are cached per file, so a repeat run on the same recording returns in seconds. Apart from `PENDING`, never re-run it to "check" something.
   - For a very long stream (over ~3 hours) pass a second argument of `300` for 5-minute buckets.
   - The decoder is biased toward WordPress vocabulary. For an off-topic stream, set `WHISPER_PROMPT` to a comma-separated list of the names and terms that matter before running.

2. **Read the condensed transcript** at the `CONDENSED` path. One `[HH:MM:SS] text` line per bucket. If `LINES` is large, read it in chunks with `offset`/`limit`; do not skip the tail, since the wrap-up is where the "what got solved" lives.

3. **Derive chapters.** Buckets are raw material, not the chapter list. Merge adjacent buckets covering the same work. YouTube silently ignores the whole list if any rule fails:
   - First chapter starts at `00:00`.
   - At least three chapters.
   - Each at least 10 seconds long, listed in ascending order.
   - One per line, `MM:SS Label`, or `HH:MM:SS Label` once past an hour.
   - Aim for 6–12 chapters on a 2-hour stream.
   - Never one chapter per bucket. Use at most one chapter per ~4 minutes of stream (a 44-minute stream gets 11 at most), and a chapter changes only when the work changes. If the stream returns to an earlier thread, fold that into the story instead of reopening it as its own chapter.
   - Labels describe what happens, not the clock: "Setting up theme.json" beats "Part 2".
   - Never label a chapter from text inside a `SUSPECT` range. If a range swallows a chunk of the stream, cover it with one neutral chapter and report it under Transcript gaps.

4. **Return exactly the four sections below and nothing else.** No preamble, no transcript excerpts, no quotes longer than a sentence, and no file paths.

## Return format

```
## Recap
<2–4 past-tense sentences: what was built, what broke, what got solved. Raw material for a hook, not the hook itself.>

## Chapters
00:00 <label>
MM:SS <label>
...

## Mentioned links
- <URL, repo name, or PR number as spoken> — unverified
(or "none")

## Transcript gaps
- <HH:MM:SS-HH:MM:SS> <reason from the SUSPECT line>
(or "none", when COVERAGE is 100% and there are no SUSPECT lines)
```

Everything under "Mentioned links" is unverified by definition. Whisper mangles URLs and numbers; the parent must confirm each one with the user before it appears in a description.
