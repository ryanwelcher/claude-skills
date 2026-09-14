---
name: write-article
description: |
  Write articles, tutorials, blog posts, or P2 updates in Ryan Welcher's voice, with
  Simplified Technical English for tutorial steps. Use to draft a tutorial, developer blog
  post, P2 update, or announcement that should sound like Ryan.
---

# write-article — Write in Ryan's Voice

Draft articles, blog posts, and P2 content in Ryan Welcher's established writing style.

The voice, structures, openings, closings, and formatting rules all live in
`references/writing-style.md`. Read it before drafting; this file is only the workflow.

## STE for action zones

Tutorials use a hybrid: Ryan's voice for intros, reasoning, and transitions; Simplified Technical English for the parts readers *act* on (numbered steps, prerequisites, warnings, UI paths, troubleshooting). The rules live in the shared card — read it live, never copy it here:

```
${CLAUDE_SKILL_DIR}/../ste-pass/references/ste-card.md
```

Pick the mode from the card's **Destination defaults** (hybrid for the Developer Blog, Block Developer Cookbook, and ryanwelcher.com tutorials; off for P2 and opinion posts). The user can override with "strict STE" or "no STE". Inside action zones, the STE card overrides `writing-style.md`. When STE is off, don't read the card.

## Workflow

### Step 1 — Gather context

Ask for (or infer from the conversation):
- **Topic/title:** What is the article about?
- **Target audience:** WordPress developers (default), internal team (P2), general?
- **Format:** Tutorial, opinion piece, P2 update/announcement, snaps post?
- **Destination:** Where it will publish — this sets the STE mode (see "STE for action zones").
- **Key points:** What should the article cover? Any specific code examples, gotchas, or decisions to highlight?
- **Existing content:** Any draft, outline, notes, or prior posts to build from?

If the user provides a topic but no outline, generate a brief outline first and confirm before drafting.

### Step 2 — Draft

Pick the structure for the format from `writing-style.md` (tutorial by default) and write a complete draft that follows it.

### Step 3 — Review checklist

Before presenting the draft, verify:
- [ ] Opens without preamble — context and point established in first paragraph
- [ ] No "In this article..." or similar formulaic openers
- [ ] Code examples are complete and runnable (not pseudocode)
- [ ] Gotchas/edge cases are addressed
- [ ] Closes without a summary paragraph — ends at the content
- [ ] Headers make the article scannable
- [ ] Tone is first-person, active, peer-to-peer (not instructional/lecturing)
- [ ] Technical level matches audience (intermediate-to-advanced WP dev)
- [ ] If STE is on: every numbered step is one imperative action, 20 words max
- [ ] If STE is on: warnings/cautions come before their step; each procedure ends with a "make sure that…" check
- [ ] If STE is on: voice zones still sound like Ryan — STE did not leak into the intro or reasoning

### Step 4 — Present and iterate

Present the full draft. If the user wants changes, apply them while preserving the style. Do not revert to generic AI writing patterns (avoid adding conclusions, hedging language, or motivational framing).

## Target Destinations

- **ryanwelcher.com** — personal developer blog, tutorial-heavy
- **Internal team P2** — work P2 posts for the team
- **WordPress.org developer blog** — broader WordPress developer audience
- **make.wordpress.org** — WordPress contributor community

Adjust formality and internal-reference density based on destination.

## Rules

- Always read `references/writing-style.md` before drafting.
- For tutorials with STE on, also read `../ste-pass/references/ste-card.md` before drafting.
- Default to tutorial structure unless the user specifies otherwise.
- Generate an outline for confirmation before a full draft if the topic is complex or ambiguous.
- Do not publish content — always produce a draft for the user to review.
