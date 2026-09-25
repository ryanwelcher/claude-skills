---
name: youtube-stream-description
description: Draft YouTube descriptions for Ryan Welcher's @ryanwelchercodes live streams in his template. Use to write or improve a stream description from an upcoming topic, a published video URL/ID, or a local recording file (mp4/mov/mkv) not yet uploaded.
---

# YouTube Stream Description

Draft YouTube descriptions for the @ryanwelchercodes channel that match Ryan's existing format and voice.

## Scenarios

- **Upcoming stream** — promotional framing for a stream that hasn't happened yet (future tense, "Join me as...")
- **Post-stream** — recap framing for a stream that just ended (past tense or evergreen)
- **Improve existing** — user provides a video URL and wants the description rewritten
- **Local recording** — user provides a path to a video file that hasn't been uploaded yet; the `analyze-stream-recording` helper transcribes it and returns the hook material and chapters

## Workflow

1. **Confirm what's needed.** Ask only the questions the user hasn't already answered:
   - Scenario (upcoming / post-stream / improve-existing / local-recording)
   - Stream title
   - 1-3 sentence summary of what the stream covers — skip this when a local recording was provided, since the transcript supplies it
   - Any specific links to include inline (PRs, repos, docs, blueprint URLs)
   - Stream Together / viewer call-in feature in use? (default: no)

2. **Check dependencies for the chosen scenario.** Run:
   ```bash
   bash ${CLAUDE_SKILL_DIR}/scripts/check-deps.sh <scenario>
   ```
   - `OK` → continue.
   - One or more `MISSING:` lines → use AskUserQuestion to offer the exact install commands printed. On yes, run them and re-run the check. On no, stop and say which scenarios still work without them. **Never install without asking, and never push this step into a helper skill**: subagents cannot ask the user anything.

3. **Fetch reference descriptions** to ground voice/format. Always run this before drafting:
   ```bash
   bash ${CLAUDE_SKILL_DIR}/scripts/fetch-recent.sh 5
   ```
   Output is titles plus hook paragraphs only; the boilerplate is intentionally stripped because TEMPLATE.md already holds it.

4. **For an existing video**, fetch its current title + hook (boilerplate stripped the same way):
   ```bash
   yt-dlp --quiet --no-warnings --skip-download --print "%(title)s" --print "%(description)s" "<URL_OR_ID>" | awk '/^Connect:/{exit} {print}'
   ```

5. **For a local recording file**, invoke the `analyze-stream-recording` skill with the file path. It runs in a fork, so the transcript never enters this conversation. It returns four sections:
   - **Recap** → raw material for the hook. Write the hook from what was actually built, broke, and got solved; do not restate the filename or title.
   - **Chapters** → already validated against YouTube's rules. Use verbatim.
   - **Mentioned links** → all unverified. Show them to the user and include only the ones they confirm.
   - **Transcript gaps** → if not "none", tell the user each range outside the code block, so they know which chapters to check by scrubbing the video. Do not fill a gap with guessed content.
   Draft from these sections only. If the recap or chapters look thin or wrong, tell the user what's missing and ask them; do not go looking for the transcript files.
   If it returns an `ERROR:` line instead, go back to step 2.

6. **Read the template** at `${CLAUDE_SKILL_DIR}/TEMPLATE.md` for the constant boilerplate (Connect / Projects / hashtags).

7. **Draft the description.** Compose:
   - Hook paragraph (1-3 sentences, casual, first-person, energetic — match recent descriptions)
   - Chapter list, if working from a local recording
   - Inline links the user provided or confirmed (e.g., `Pull Request: https://...`)
   - Stream Together blurb if applicable (see TEMPLATE.md)
   - Boilerplate sections from TEMPLATE.md verbatim
   - Hashtag line per the rules in TEMPLATE.md

8. **Output the full description in a single fenced code block** so the user can copy-paste it directly into YouTube Studio. Do not add commentary inside the code block.

## Defaults & guardrails

- **Timestamps depend on the source:**
  - Working from a topic/title or a published URL → no timestamps unless the user provides them. If provided, place after the hook paragraph and before any inline links.
  - Working from a local recording → use the helper's chapter list, placed after the hook paragraph and before any inline links.
- **Don't invent links.** Only include URLs the user gave you, confirmed from the helper's "Mentioned links", or that already exist in TEMPLATE.md.
- **Match voice from recent descriptions** — Ryan's tone is casual, first-person, energetic, often self-deprecating. Avoid corporate phrasing.
- **Keep boilerplate verbatim** from TEMPLATE.md — do not rewrite the Connect/Projects sections per stream.

## Headless

To draft from a recording without a session, run this from a terminal (not from inside the skill):
```bash
bash scripts/describe-stream.sh <recording> [--title "..."] [--stream-together]
bash scripts/describe-stream.sh <folder> [--stream-together]
```
It writes `<recording>.description.md` next to each file. With a folder, it skips recordings that already have one. Mentioned links and transcript gaps are listed after the code block for you to check.
