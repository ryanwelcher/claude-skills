---
name: sounds-like-me
description: Voice pass on an existing script, teleprompter, or written draft so it sounds like Ryan Welcher. Checks lines against his voice cards, shows findings for approval, fixes approved ones in place, and logs new rules. Use for a voice pass or voice check, "make this sound like me," or reworking an existing draft.
user-invocable: false
---

# Sounds Like Me

Audit an **existing** file (script, teleprompter, blog draft, social post) so every line sounds like Ryan. This does NOT write new content — it finds off-voice lines, shows them to Ryan, and fixes the ones he approves. **Findings first, fixes on approval.**

## Step 0 — Load the voice cards (REQUIRED, every time)

The cards are the single source of truth. **Read them live** — never rely on a copy in this skill, and never hardcode the rules here (they'd drift). They ship in sibling skills of this plugin, so read them relative to this skill's directory:

```
${CLAUDE_SKILL_DIR}/../youtube-script/references/style-card.md    # core voice — ALWAYS read
${CLAUDE_SKILL_DIR}/../wnd-script/references/wnd-series-card.md   # WND delta — read for WND files
```

When the plugin is loaded in place (symlinked from the source repo), these resolve into git and refinement-log updates persist. If the resolved path is under `~/.claude/plugins/cache`, still read it, but warn in Step 7 that any refinement-log entries written there are lost on the next `/plugin update` and must be ported to the source repo.

For **written** content (blog posts, tutorials, recipes, workshop sections, docs), also read the STE card — it defines the action zones this skill must leave alone:

```
${CLAUDE_SKILL_DIR}/../ste-pass/references/ste-card.md            # zones — read for written tutorials/docs
```

1. Always read **`style-card.md`** in full — the core voice, including **Anti-AI tells** and **Hard bans**. Its refinement log lives in a separate `refinement-log.md`; don't read it, every entry is already distilled into the card.
2. If the target is a **What's New for Developers (WND)** file, also read **`wnd-series-card.md`** in full (open/close/identity deltas). Detect WND from the filename (`WND`, `What's New for Developers`) or content (branded greeting open, "have a good one" close). Other series may have their own card — read it if one exists.
3. If unsure which series a file belongs to, ask before passing.

## Step 1 — Read the target(s)

Read the **current** file(s) — the user may have edited them by hand since they were written. Never work from memory or an earlier version; the file on disk is the source. If pointed at a folder (e.g. a WND month folder), find every script/teleprompter in it and treat them as a set.

## Step 2 — Find (don't fix yet)

Go line by line through the **spoken/written content only** (skip `[SCREEN]` directions, `>` notes, headers).

**Skip STE action zones in written content.** Numbered steps, prerequisites, `**WARNING:**` / `**CAUTION:**` / `**NOTE:**` blocks, UI click paths, and troubleshooting tables follow `ste-card.md`, not the voice card. Plain, imperative, joke-free wording there is intentional — never flag it as off-voice or rewrite it into chattier prose. If an action zone has a clarity problem, suggest running `ste-pass` instead. Scripts and teleprompters have no action zones.

Flag anything that trips a card rule:

- **Anti-AI tells** and **Hard bans** from `style-card.md` (dive in / delve / supercharge, label-colon openers, "real talk," relentless parallelism, press-release rhythm, etc.).
- **Off-voice phrasing** the cards flag — corporate/PM framing ("the action item changed from X to Y"), announce-the-feeling ("here's the part I love"), meme/internet slang, cost/price framing for effort, and **over-use of a single emphasis word** (e.g. "whole" more than ~2–3 times across a file).
- **Series conventions** (WND): branded greeting open (NOT a cold open), "…have a good one" close (NOT "friends"), identity = **developer advocate at Automattic**.
- The gut check: **if a line wouldn't survive Ryan reading it out loud, it's a finding.**

## Step 3 — Present findings for approval (DO NOT edit yet)

Show Ryan a numbered list. For each finding give: the file + rough location, the **offending line**, the **card rule** it breaks (name it), and a **proposed rewrite** in his voice. Group by file. Keep it skimmable. Then ask which to apply — "all," specific numbers, or skip. Note any **borderline** ones separately (you're unsure it's really off-voice) so he can rule on them. **Make no edits in this step.**

## Step 4 — Fix the approved findings in place

Apply only the approved rewrites with `Edit`. Preserve the user's manual edits and the file's format (read-copy teleprompter vs. `**VO:**` script). Don't touch facts, URLs, or `> ✅ / ⚠️` notes.

## Step 5 — Keep versions in sync

If a script **and** a teleprompter exist for the same piece, apply each approved fix to **both** so they don't drift. Sync only the spoken wording — respect each format's conventions (teleprompter spells out URLs, softens code identifiers; script keeps `[SCREEN]` lanes and `>` notes).

## Step 6 — Log new corrections

When an approved fix reflects a **new** rule Ryan would want enforced next time, append a dated bullet to the correct refinement log (don't duplicate an existing rule):

- **Core-voice** correction (true on any channel/series) → the relevant section of `style-card.md`, plus a dated bullet in `../youtube-script/references/refinement-log.md`.
- **Series-specific** correction → the relevant section of that series' card (e.g. `wnd-series-card.md`), plus a dated bullet in that card's `refinement-log.md`.
  Routing to the shared card is what keeps the voices from drifting — when unsure whether it's core or series-specific, prefer the shared `style-card.md`.

## Step 7 — Report

Briefly recap: what you changed (tie each to a card rule), which files you synced, any **refinement-log entries** added, and any findings Ryan **skipped** or borderline lines still open.

## Non-negotiables

- **Findings first, fixes on approval** — never edit in the same step you surface findings.
- Read the cards **live** every run; never inline their rules here.
- Never voice-edit STE action zones in written content — they belong to `ste-card.md`.
- Audit the on-disk file, not memory — honor manual edits.
- Keep script + teleprompter in sync on approved fixes.
- Route new rules to the right refinement log (core → shared style card).
