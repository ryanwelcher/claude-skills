---
name: ste-pass
description: Audit or rewrite existing tutorials, recipes, workshop steps, or docs with Simplified Technical English (STE) in action zones (steps, prerequisites, warnings, UI paths), keeping Ryan's voice elsewhere. Findings first. Use for an STE pass, clearer steps, or readers whose first language isn't English.
---

# STE Pass

Audit an **existing** file or passage so its action zones follow Simplified Technical English. This
does NOT write new content and does NOT change Ryan's voice outside action zones. **Findings first,
fixes on approval.**

Skills that *draft* content (e.g. `write-article`) do not invoke this skill — they read the card
directly while writing. This skill is for content that already exists.

The rules live in the card, `${CLAUDE_SKILL_DIR}/references/ste-card.md`. Never inline them here.

## Step 1 — Pick the mode and the path

- **Scope:** `hybrid` (default — action zones only) or `strict` (whole file). Use strict only
  when the user asks ("strict", "full STE", "the whole thing").
- **Destination:** if the user names one and the card's **Destination defaults** say **Off** (P2,
  social, scripts), say so and ask before continuing. You can check the defaults without reading
  the card: P2, opinion, social, and YouTube/WND scripts are off; tutorials, recipes, workshops, and
  Developer Blog posts are hybrid.
- **Path:**
  - **Quick** — a passage pasted in chat, or a file with **40 or fewer lines of prose** outside
    code blocks. Read the card and audit inline. Do not run the linter or the helper; on content
    this short they cost more than they save.
  - **Full** — anything longer. Use the `ste-audit` helper (Step 2). It runs in a fork on Sonnet,
    reads the card, maps the zones, runs `ste-lint.py`, and returns findings with full rewrites.
    Opus stays for talking to Ryan and applying the edits.

## Step 2 — Find (don't fix yet)

**Quick path:** read the card, map the zones, and check the action zones against the **Writing
rules** and **Word swaps**, skipping everything in **Never change**.

**Full path:** invoke the `ste-audit` skill with the arguments `<file path> <hybrid|strict>
[destination]`. It returns exactly three sections: **Zone map**, **Findings**, **Borderline**. If it
returns a single `ERROR:` line, report it and stop. Do not re-read the card or re-run the linter to
double-check it; drop a finding only if it clearly touches code, a UI label, or a voice zone.

If pointed at a URL, fetch it and save a local copy in the scratchpad first; never publish.

## Step 3 — Present findings for approval (DO NOT edit yet)

Show:
1. The **zone map**, so Ryan can correct a misclassified zone.
2. The numbered **findings**, grouped by section: the **offending text**, the **card rule** it
   breaks, and the **proposed rewrite**.
3. The **borderline** findings, listed separately.

Ask which to apply: "all", specific numbers, or skip. **Make no edits in this step.** If the user
already pre-approved every finding, say so and continue to Step 4.

## Step 4 — Apply approved fixes in place

Read the **current** file on disk (Ryan may have edited it since the audit), then apply only the
approved rewrites with `Edit`. Preserve manual edits, code blocks, links, and formatting. Do not
touch voice zones in hybrid mode. If a rewrite no longer matches the file, skip it and say so.

## Step 5 — Log new rules

When an approved fix reflects a **new** rule Ryan wants enforced next time, read the card, add the
rule to its rules or word swaps, and append a dated one-line entry to
`references/refinement-log.md`. Do not duplicate an existing rule. If the rule is mechanical (a
word, a length, a pattern), add it to `scripts/ste-lint.py` too.

If the resolved path is under `~/.claude/plugins/cache`, warn that these edits are lost on the next
`/plugin update` and must be ported to the source repo.

If Ryan rejects a finding because it is really a **voice** issue, do not add it here — that rule
belongs in the voice card, so point him to `sounds-like-me`.

## Step 6 — Report

Briefly recap: the mode and path used, the fixes applied (tied to card rules), any refinement-log
entries added, and any skipped or borderline findings still open.

## Non-negotiables

- **Findings first, fixes on approval** — never edit in the same step you surface findings.
- **Hybrid by default.** Voice zones belong to Ryan's voice cards, not to this skill.
- Never change code, commands, UI labels, or technical names.
- Quick path for short content; `ste-audit` for everything else. Never run the linter yourself.
- Apply edits against the on-disk file, not memory.
