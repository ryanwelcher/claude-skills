---
name: wp-workshop-scaffold
description: |
  Scaffold a new WordPress workshop repo, reformat an existing repo to the canonical workshop
  shape (README, facilitator notes, slides outline, section files, code-reference snapshots,
  blueprint.json), or audit one read-only. Use when starting, retrofitting, or checking a
  workshop repo.
metadata:
  type: skill
---

# wp-workshop-scaffold

A skill for materializing the WordPress workshop repo shape used by the WordCamp
Portugal 2026 AI Workshop. Three modes: `create`, `reformat`, `audit`.

## Canonical shape

Top-level files:
- `plugin.php` (plugin) / `style.css` (theme) / `block.json` (block)
- `package.json`, `.editorconfig`, `.eslintrc`, `.gitignore`
- `blueprint.json` — Studio/Playground bootstrap
- `README.md` — pre-workshop setup, welcome, "what we're building", section map
- `facilitator-notes.md` — timing table, before-the-workshop checklist, section-by-section talking points + sticking points
- `slides-outline.md` — slide-by-slide outline
- `workshop-outline/section-N.md` — one file per section
- `code-reference/section-N/` — snapshot of the code state at the **end** of each coding section. This is also the **starting state** of section N+1 — no hidden setup between sections. (only for coding sections)
- `assets/` — images referenced by docs
- `includes/`, `src/` — scaffold dirs (start mostly empty, fill in as sections progress)

Section types: `tour`, `coding`, `demo`, `hackathon`. Only `coding` sections get a `code-reference/section-N/` snapshot.

## Authoring principles

Workshops scaffolded by this skill follow a **build-up** structure, in the spirit of a cookbook recipe that progresses from empty plate to plated dish:

- The workshop has one **north-star artifact** — a finished, demoable thing attendees walk away with. The README leads with it ("By the end you'll have built X") and the input questionnaire collects it up front.
- Each coding section adds **exactly one capability** to that artifact. The end state of section N is a more capable version of the end state of section N-1 — never a parallel detour, never a reset.
- `code-reference/section-N/` is both the end state of section N and the starting state of section N+1. There must be no hidden setup between sections — an attendee who falls behind can copy section N's snapshot and pick up at the start of section N+1 with zero gap.
- `tour`, `demo`, and `hackathon` sections punctuate the arc but don't break the chain — the code state carries through them unchanged.

### Code in section files

Coding sections must be **copy-paste runnable** — an attendee following along should never have to invent or guess code. Each step that introduces or changes code includes a fenced code block, using a **hybrid** style:

- **New file** → show the **full file** content. The block is preceded by the relative path on its own line (e.g., `src/view.js`), and the attendee creates the file and pastes the block verbatim.
- **Edit to an existing file** → show **only the inserted or replaced code**, preceded by a one-line anchor that tells the attendee where it goes. Anchors must be unambiguous: a function name, an existing line of code to insert after/before, or an explicit line-range to replace. Examples:
  - `In src/view.js, add inside the store() callback:`
  - `In render.php, replace the placeholder \`return '';\` with:`
  - `In block.json, add to the \`attributes\` object:`
- **Deletion** → quote the exact lines to remove, prefixed with `Remove from <file>:`.

### Step wording in section files

Attendees follow steps live, often in a second language. Write the **Steps** list of every section in Simplified Technical English, per the shared card (read it live when filling in sections — never copy its rules here):

```
${CLAUDE_SKILL_DIR}/../ste-pass/references/ste-card.md
```

The concept intro and **End state** paragraphs stay in Ryan's voice. `facilitator-notes.md` and `slides-outline.md` are not attendee-facing steps, so STE does not apply to them. To check existing sections, run `ste-pass`.

The end state of each coding section must match the corresponding `code-reference/section-N/` snapshot exactly — the snapshot is the ground truth, the section file is the path that gets there.

## Mode dispatch

When invoked, ask the user which mode (if not clear from the args):

1. **`create`** — scaffold a new workshop repo from scratch
2. **`reformat`** — reshape an existing repo (local path or git URL) to match
3. **`audit`** — read-only conformance report

---

## Mode: `create`

### Step 1 — Collect inputs interactively

Use `AskUserQuestion` (one question at a time when answers branch, batch when independent). Required:

1. **Workshop title** (e.g. "Stop Doing It Yourself")
2. **Event / subtitle** (e.g. "WordCamp Portugal 2026")
3. **Finished artifact (north-star)** — one short paragraph describing what attendees will have built and be able to demo at the end. Rendered as the README's "What we're building" hero and used to anchor the build-up arc (see Authoring principles).
4. **Date** (absolute, e.g. "2026-05-15")
5. **Presenter(s)** — name + affiliation each. Loop: "add another presenter?" until done.
6. **Documentation links** — list of URLs that should appear in README/section pages (Studio docs, AI plugin repo, Abilities API docs, etc.). Loop until done.
7. **Plugin slug** (e.g. `wcpt-2026-ai-workshop`) — used for directory name, package.json `name`, blueprint.json plugin path
8. **WP target**: `plugin` / `theme` / `block`
9. **WP version target** (e.g. `7.0-RC4`, `beta`, `latest`) — for blueprint.json `preferredVersions.wp`
10. **Plugins to preinstall via blueprint** — list of slugs (loop until done; empty allowed)
11. **Target directory** — absolute path where the repo should be created. Refuse if it already exists.

### Step 2 — Materialize

Read each file in `templates/` (sibling of this SKILL.md), substitute `{{placeholders}}`, write to target directory.

Placeholders used across templates:
- `{{TITLE}}`, `{{EVENT}}`, `{{DATE}}`
- `{{NORTH_STAR}}` — one-paragraph description of the finished artifact; rendered in README as the "What we're building" hero
- `{{PRESENTERS_BLOCK}}` — multi-line, one bullet per presenter
- `{{DOC_LINKS_BLOCK}}` — multi-line, one bullet per link
- `{{PLUGIN_SLUG}}`, `{{WP_TARGET}}` (plugin/theme/block), `{{WP_VERSION}}`
- `{{BLUEPRINT_PLUGINS}}` — either an empty string (no extra plugins) or a comma-prefixed list of additional `installPlugin` step objects to append to `blueprint.json`'s `steps` array. Format: `,\n    { "step": "installPlugin", ... },\n    { "step": "installPlugin", ... }` (leading comma; no trailing comma).
- `{{REPO_URL}}` — optional; leave as placeholder string `https://github.com/REPLACE-ME/{{PLUGIN_SLUG}}` if user didn't provide

Files to generate:
- `plugin.php` (only if WP target is `plugin`) — from `templates/plugin.php.tmpl`
- `style.css` (only if `theme`) — from `templates/style.css.tmpl`
- `block.json` (only if `block`) — from `templates/block.json.tmpl`
- `package.json` — from `templates/package.json.tmpl`
- `.editorconfig`, `.eslintrc`, `.gitignore` — copied verbatim
- `blueprint.json` — from `templates/blueprint.json.tmpl`
- `README.md` — from `templates/README.md.tmpl`
- `facilitator-notes.md` — from `templates/facilitator-notes.md.tmpl`
- `slides-outline.md` — from `templates/slides-outline.md.tmpl`
- `workshop-outline/section-1.md` — single TODO stub from `templates/workshop-outline/section.md.tmpl` (sections left as TODOs per design)
- `src/index.js` — empty/minimal scaffold
- `includes/.gitkeep`, `assets/.gitkeep` — keep dirs present

**Do NOT** create `code-reference/` directories at create time. Document in README that they will be added per coding section.

**Do NOT** run `git init`. **Do NOT** run `studio` commands. Files only.

### Step 3 — Report

Print: target path, file count, and three next-step suggestions: declare sections, `git init`, create Studio site from `blueprint.json`.

---

## Modes: `reformat` and `audit`

These modes live in separate files so `create` does not load them. Read the one you need before you start:

- **`reformat`** → `${CLAUDE_SKILL_DIR}/references/mode-reformat.md` (it also reads `mode-audit.md` for the checks)
- **`audit`** → `${CLAUDE_SKILL_DIR}/references/mode-audit.md`

---

## Notes for Claude when running this skill

- **Use absolute paths in every tool call.** Don't `cd`. The target directory may not be the cwd.
- **Don't invent placeholder values.** If the user skips a question, leave the placeholder as a literal `{{TODO: ...}}` marker in the output so they can grep for it later.
- **One question at a time when answers branch.** Batch independent questions in a single `AskUserQuestion` call.
- **Templates live in `templates/` next to this SKILL.md.** Read them with the `Read` tool; substitute placeholders in memory; write with `Write`.
- **`code-reference/` snapshots are created later, not at scaffold time.** When the user fills in a coding section, they can re-invoke this skill with a separate flow (not implemented in v1 — document as a TODO).
- **Never push.** Never run `git push`, `git push --force`, `git reset --hard`, or destructive operations. The user reviews diffs themselves.
