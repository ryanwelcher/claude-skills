---
name: write-article
description: |
  Write articles, tutorials, blog posts, or P2 updates in Ryan Welcher's voice, with
  Simplified Technical English for tutorial steps. Use to draft a tutorial, developer blog
  post, P2 update, or announcement that should sound like Ryan, or to refine an existing
  article against the same rules.
---

# write-article — Write in Ryan's Voice

Draft articles, blog posts, and P2 content in Ryan Welcher's established writing style.

Article structure, openings, closings, and formatting rules live in
`references/writing-style.md`. Read it before drafting or refining; this file is only the workflow.

## Voice source of truth

Ryan's voice lives in the shared voice card, the same one `sounds-like-me` uses. Read it live before drafting or refining, and never copy its rules here:

```
${CLAUDE_SKILL_DIR}/../youtube-script/references/style-card.md
```

Its line-level rules apply to every article: **Anti-AI tells**, **Hard bans**, **Verbal tics**, **Humor**, and **How he explains tech**. Skip its video-only sections (**Open**, **On-camera presence**, **Close**); article openings and closings come from `writing-style.md`. If the card and `writing-style.md` disagree on how a line sounds, the card wins.

## STE for action zones

Tutorials use a hybrid: Ryan's voice for intros, reasoning, and transitions; Simplified Technical English for the parts readers *act* on (numbered steps, prerequisites, warnings, UI paths, troubleshooting). The rules live in the shared card — read it live, never copy it here:

```
${CLAUDE_SKILL_DIR}/../ste-pass/references/ste-card.md
```

Pick the mode from the card's **Destination defaults** (hybrid for the Developer Blog, Block Developer Cookbook, and ryanwelcher.com tutorials; off for P2 and opinion posts). The user can override with "strict STE" or "no STE". Inside action zones, the STE card overrides `writing-style.md`. When STE is off, don't read the card.

## Workflow

The same four steps apply to a new article and to refining an existing one. It's a **refine** when the user points at an existing article (a file path or a pasted draft) and asks to refine, tighten, fix, restructure, or review it.

### Step 1 — Gather context

Ask for (or infer from the conversation):
- **Topic/title:** What is the article about?
- **Target audience:** WordPress developers (default), internal team (P2), general?
- **Format:** Tutorial, opinion piece, P2 update/announcement, snaps post?
- **Destination:** Where it will publish — this sets the STE mode (see "STE for action zones").
- **Key points:** What should the article cover? Any specific code examples, gotchas, or decisions to highlight?
- **Existing content:** Any draft, outline, notes, or prior posts to build from?

**New article:** if the user provides a topic but no outline, generate a brief outline first and confirm before drafting.

**Refine:** read the current file on disk first. Never work from an earlier version or memory; the user may have edited it by hand. Infer the context from the article and ask only for what it doesn't tell you.

### Step 2 — Draft or check

**New article:** pick the structure for the format from `writing-style.md` (tutorial by default) and write a complete draft that follows it.

**Refine:** check the article against every rule a new draft must meet: every line against the voice card's rules (see "Voice source of truth"), all of `writing-style.md` (voice and tone, sentence structure, opening, structure for its format, closing, formatting, code examples, technical level, and the P2 patterns for a P2), the Step 3 checklist, and the STE card in action zones when STE is on. Every miss is a finding, including small ones and ones that look obvious.

### Step 3 — Review checklist

**New article:** verify these before presenting the draft. **Refine:** every item the article fails is a finding.
- [ ] Opens without preamble — context and point established in first paragraph
- [ ] No "In this article..." or similar formulaic openers
- [ ] Code examples are complete and runnable (not pseudocode)
- [ ] Gotchas/edge cases are addressed
- [ ] Ends with a closing (see **Article Closings** in `writing-style.md`): a so-what plus one pointer, after the last code block — not a recap
- [ ] Headers make the article scannable
- [ ] Tone is first-person, active, peer-to-peer (not instructional/lecturing)
- [ ] Every line passes the voice card's **Anti-AI tells** and **Hard bans**
- [ ] Technical level matches audience (intermediate-to-advanced WP dev)
- [ ] If STE is on: every numbered step is one imperative action, 20 words max
- [ ] If STE is on: warnings/cautions come before their step; each procedure ends with a "make sure that…" check
- [ ] If STE is on: voice zones still sound like Ryan — STE did not leak into the intro or reasoning

### Step 4 — Present and iterate

**New article:** present the full draft.

**Refine:** present every finding as a numbered list. Each finding gives the location, what's there now (quoted), the rule it breaks (named, with its source: the voice card, `writing-style.md`, or the STE card), and the proposed fix. When something is missing or broken (a closing, a gotchas section, pseudocode), write the proposed text or code in full. A proposed closing follows **Article Closings** in `writing-style.md`. End by asking which to apply: "all", specific numbers, or skip. That question is the last thing in your reply, and your turn ends there, with the file untouched. After the user's reply names which findings to apply, edit only those, keep everything else as it is (wording, facts, links, code), and list what changed.

Either way, if the user wants more changes, apply them while preserving the style. Do not revert to generic AI writing patterns (avoid recap conclusions, hedging language, or motivational framing).

## Target Destinations

- **ryanwelcher.com** — personal developer blog, tutorial-heavy
- **Internal team P2** — work P2 posts for the team
- **WordPress.org developer blog** — broader WordPress developer audience
- **make.wordpress.org** — WordPress contributor community

Adjust formality and internal-reference density based on destination.

## Rules

- Always read `references/writing-style.md` and the voice card (`../youtube-script/references/style-card.md`) before drafting or refining.
- For tutorials with STE on, also read `../ste-pass/references/ste-card.md` before drafting or refining.
- Default to tutorial structure unless the user specifies otherwise.
- Generate an outline for confirmation before a full draft if the topic is complex or ambiguous.
- Do not publish content — always produce a draft for the user to review.
- When refining, the file stays untouched until the user picks which findings to apply.
