---
name: done
description: |
  Save a structured log of the current conversation (summary, decisions, changes, follow-ups)
  to the DevRel Obsidian vault. Use to save or log this conversation, save a recap, dump the
  chat to Obsidian, or wrap up a session.
---

# /done — Session Log Dumper

When this skill is invoked, write a structured session log to the DevRel Obsidian vault.

## Steps

### 1. Gather context via Bash

Run these two commands in parallel:

```bash
git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "no-branch"
```

```bash
date +%Y%m%d
```

Also generate a short session ID:
```bash
date +%s%N | md5 | head -c 8
```
(on macOS `md5` works; on Linux use `md5sum | head -c 8`)

### 2. Derive the filename

Format:
```
YYYYMMDD Conversation - <Topic> [<branch>].md
```

- `YYYYMMDD` — today's date from the bash command above
- `<Topic>` — 3–6 word summary of the main thing discussed, title-cased, spaces only (no slashes or colons)
- `<branch>` — git branch name, or `no-branch` if not in a git repo

Example:
```
20260217 Conversation - Done Skill Creation [main].md
```

### 3. Build the file content

Use this exact structure:

```markdown
---
created: YYYY-MM-DD
type: conversation
source: claude-code
status: unvalidated
session_id: <8-char hex id>
branch: <branch>
cwd: <working directory if relevant>
tags: []
---

# <Topic>

## Summary

<2–4 sentence plain-English summary of what was worked on and what was accomplished.>

## Key Decisions

- <Decision 1>
- <Decision 2>
...

## What Was Done

- <Concrete action or change 1>
- <Concrete action or change 2>
...

## Files Changed

- `<path>` — <one-line reason>
...

(Omit this section if no files were modified.)

## Open Questions

- <Unresolved question or uncertainty 1>
- <Unresolved question or uncertainty 2>
...

(Omit this section if nothing is unresolved.)

## Follow-ups

- [ ] <Action item 1>
- [ ] <Action item 2>
...

(Omit this section if there are no explicit follow-ups.)

## Notes

<Any extra context, links, or references worth preserving. Omit if empty.>
```

### 4. Write the file

Save to:
```
/Users/ryanwelcher/Documents/DevRel/Claude Conversations/<filename>
```

Use the Write tool. Do NOT open or preview the file afterward — just confirm the path.

### 5. Confirm

Reply with a single short message:
```
Saved → Claude Conversations/<filename>
```

Nothing else. No summary, no list of what you extracted. Just the path.

---

## Rules

- Be ruthlessly specific. "Decided to use X because Y" beats "discussed options".
- If no files were changed, omit the "Files Changed" section entirely.
- If there are no open questions, omit that section.
- Keep the Summary under 4 sentences.
- Do not add sections that aren't in the template.
- Do not ask for confirmation before writing. Just write it.
- **Always inline links for any referenced issues, tickets, or PRs:**
  - WordPress Trac tickets (`#12345` or `Trac #12345`) → `[Trac #12345](https://core.trac.wordpress.org/ticket/12345)`
  - GitHub PRs/issues on `wordpress-develop` → `[PR #12345](https://github.com/WordPress/wordpress-develop/pull/12345)`
  - GitHub PRs/issues on `gutenberg` → `[PR #12345](https://github.com/WordPress/gutenberg/pull/12345)`
  - For other GitHub repos, use the full URL from context if available
  - Never leave a bare `#number` reference — always wrap it in a markdown link
