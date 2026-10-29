# Content format and house style

## Contents

1. Files and ordering
2. The intro file
3. Item files
4. Tags
5. Working markers and notes
6. House style
7. Notes files

## 1. Files and ordering

`scripts/build.mjs` reads `content/post/` in filename order:

- **Top-level `.md` files** are rendered as they are. Use `00-intro.md` for everything before
  the first section and `99-outro.md` for the closing line.
- **Folders** are sections. Each one has a `_section.md` (frontmatter `title`, optional `tags`,
  optional body text) plus one file per item.
- Number folders in tens (`10-`, `20-`) and items in tens with three digits (`010-`, `020-`),
  so you can slot new ones in between without renaming.

Use the standard section order from past editions. Leave out a section if the release has
nothing for it:

| Folder | Section title |
|---|---|
| `10-priority-items` | Priority Items for WordPress X.Y |
| `20-new-blocks` | New Blocks |
| `30-improved-blocks` | Improved Blocks and Block handling |
| `40-editor-enhancements` | Editor enhancements |
| `50-admin-workflow` | Admin / Workflow updates |
| `60-developer-goodies` | Developer Goodies |

Priority Items holds the 4–6 headline features. Everything else goes in the section where a
reader would look for it.

## 2. The intro file

`00-intro.md` follows the published layout, in this order:

1. The welcome line ("Welcome to the Source of Truth for WordPress X.Y!"), the paragraph about
   how to use the post with the contact line, and the thank-you line naming the reviewers.
2. `## Changelog`, with the subtitle "Any changes are cataloged here as the release goes on."
   Entries go newest first. Each one is a bold date, then bullets:

   ```markdown
   **October 27, 2026**

   * Added the Secrets API to Developer Goodies.
   * Removed the Description List block (punted to 7.3).

   **October 21, 2026**: First edition.
   ```
3. `## Important note/guidelines` (the "Try not to just copy and paste" paragraph and the two
   bullets about tags and resources).
4. `## Overview`: the italic "what's shared here is being actively pursued" note, the highlight
   grid image with an italic caption once it exists, 2–4 paragraphs of narrative, and the release
   date sentence.
   - `### Resources`: Help Test, Dev Notes tag, Field Guide (from RC 1), Roadmap, Development
     Cycle page, and the What's new for developers posts.
   - The Gutenberg range sentence ("This release consists of features from the Gutenberg plugin
     versions A – B"), with pipe-separated links to each release post, then "Later Gutenberg
     releases contain bug fixes, backported to the WordPress X.Y release branch."
   - `### Assets`: the line linking the asset folder.
   - `### Tags`: the tag legend (section 4).

The byline, reading time, "Updated" date and table of contents are generated from `sot.json`
and the content. Don't write them in the intro.

## 3. Item files

```markdown
---
title: Notes in the canvas margin
tags: [end user, site admin, enterprise]
flags: [check, visuals]
---

Notes appear in a margin next to the canvas, so a thread stays open while you edit block
settings ([#83786](https://github.com/WordPress/gutenberg/pull/83786)). Use the **Notes** submenu
in the **Options** menu to show or hide them ([#83768](https://github.com/WordPress/gutenberg/pull/83768)).

![Two note threads in the margin beside a paragraph block](assets/notes-margin.png)
*Note threads in the margin on a narrow screen.*

Tracking: [Notes iteration for WordPress 7.2](https://github.com/WordPress/gutenberg/issues/80015) (#80015)

<!-- 🔍 Merged after the last plugin release before Beta 1; confirm it's in Beta 1. -->
```

Frontmatter keys:

| Key | Meaning |
|---|---|
| `title` | The H3 heading. No emoji and no tags in it, because they break the table of contents. |
| `tags` | Audience tags from section 4. Leave the list empty to inherit the section's tags. |
| `flags` | Working markers as words: `edit`, `blessed`, `check`, `visuals`, `punted`. Never published. |
| `slug` | Optional anchor override, so an existing link survives a title change. |
| `published` | `false` keeps the item out of the page but in the repo, e.g. an at-risk item waiting for Beta 1. |

Body anatomy, in this order:

1. **1–3 short paragraphs.** Say what changed and what the reader can do now. Put the PR or
   ticket link in parentheses right after the claim it supports: `([#12345](url))`. Several PRs
   go in one set of parentheses: `([#1](url), [#2](url))`.
2. **Visuals**, if any: an image with real alt text, and an italic caption line below it when
   the image needs context. Store files in `content/assets/` and reference them as
   `assets/<name>`.
3. **Link lines**, each on its own line:
   - `Tracking: [Issue title](url) (#N)` for the iteration or tracking issue.
   - `Read more: [Dev note or Make post title](url)` once a dev note or proposal exists. Add a
     Trac link in parentheses if there is one.
   - `Background: [Post title](url)` for context posts that aren't dev notes.
4. **Working notes** in `<!-- -->` at the end.

A group item, such as "Global Styles and theme.json" under Developer Goodies, uses `####`
subheadings inside one file. Each H4 gets its own entry in the table of contents. A "General
quality of life improvements" item is a bullet list that starts each bullet with the bold block
name: `* **Columns:** …`.

## 4. Tags

Use exactly these seven, singular and lowercase, because the page's filter buttons and readers'
browser searches both match on the exact string:

`end user` · `theme builder` · `plugin author` · `developer` · `site admin` · `enterprise` · `all`

Put the most affected audience first. The page's audience buttons are strict: with **developer** on, readers see only items tagged `developer` (or whose section is tagged `developer`), and the intro is hidden. So tag every audience an item really affects. `all` is a button of its own, not a wildcard. In
the old Google Doc format, tags were a `==[end user] [site admin]==` line under the heading; the
importer converts that line to frontmatter.

## 5. Working markers and notes

| Emoji | Flag word | Meaning |
|---|---|---|
| ✏️ | `edit` | Copy needs editing |
| 🙏 | `blessed` | Blessed feature, developed during the Beta cycle |
| 🔍 | `check` | To-do or double-check |
| 🎨 | `visuals` | Visuals being made |
| 🏈 | `punted` | Confirmed punted to the next release |

Markers go in `flags`, or inline inside a `<!-- -->` note. The build strips both from the page,
and it also strips any emoji marker left in visible text, with a warning, so a missed marker
never reaches readers. Clear a flag once nothing in the item's working notes still needs it.

A working note says what to check and what to do with the answer: "🔍 Merged Oct 18, after
Gutenberg 24.2; confirm it's in Beta 1. Remove the sentence if not." Notes that say only "check
this" can't be resolved by a sweep.

## 6. House style

Match the published 7.1 post:

- Write for the reader who uses the feature. Say what they can now do ("You can now set a block's
  position per viewport"), not what the PR did ("Adds viewport support to position").
- Keep it plain and specific. No hype words ("exciting", "powerful", "game-changing").
- Use **bold** for UI labels and menu paths (**Options** > **Notes**), `code` for identifiers,
  functions, filters, settings and files, and `<kbd>` for keys (`<kbd>Shift</kbd>+<kbd>Tab</kbd>`).
- Use present tense, as if it ships. The Overview note already covers the caveat that it may
  not.
- Developer items name the API and the migration step: what's deprecated, what replaces it, and
  what to test.
- Check every link's format: the number in the text matches the URL, the brackets are balanced,
  and it points at `/pull/` for PRs and `/issues/` for issues. The 7.1 post shipped with links
  like `([79104)](…)`, and the build can't catch those.
- Don't copy PR titles or descriptions as they are. Readers see the post, not GitHub.

## 7. Notes files

| File | Holds |
|---|---|
| `notes/research.md` | Release basics (milestone table, squad, Gutenberg range), official planning sources, and a research entry for every candidate, including ones that never reach the post |
| `notes/sweep-log.md` | One dated entry per sweep, newest first (format in `sweep.md`) |
| `notes/open-questions.md` | A numbered list of questions that block a decision. Remove an answered question and note the answer in the sweep log. |
| `notes/punted.md` | Items confirmed out of the release, with the reason and a source link |
| `notes/backlog.md` | Items carried over from the previous release, to re-check |
| `notes/status.json` | Written by `npm run status`. Don't edit it by hand. |
| `notes/doc-updates.md` | Doc changes waiting to be pasted in while the Doc write path isn't set up (`google-doc.md`, section 4) |
