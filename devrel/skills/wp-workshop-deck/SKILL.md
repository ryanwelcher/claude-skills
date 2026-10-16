---
name: wp-workshop-deck
description: |
  Use when a WordPress workshop repo needs its presentation slides built, rebuilt, or extended
  from slides-outline.md, including adding a deck for a new workshop length
  (slideshows/<length>/index.html). Pairs with wp-workshop-scaffold, which writes the outline.
metadata:
  type: skill
---

# wp-workshop-deck

A workshop deck is `templates/deck.html` plus slides. The template already has the deck's
navigation, build steps, slide outline, controls panel, presenter view, timer, 16:9 scaling,
brand theme, and code styling, all checked on projectors. A new deck reuses it unchanged, so
every deck looks and works the same.

## Inputs

From the workshop repo: `slides-outline.md` (one entry per slide), `facilitator-notes.md`
(run sheet and timings), `workshop-outline/section-N.md`, `code-reference/section-N/`, the
starter `src/`, and the GitHub repo URL.

## Build

1. Copy `templates/deck.html` to `slideshows/<length>/index.html` (for example
   `slideshows/90-minutes/`). Fill `{{DECK_TITLE}}` and `{{DEMO_BLUEPRINT_URL}}`.
2. Replace the `{{SLIDES}}` comment line with one `<section class="slide">` per outline
   entry, in outline order. Take each slide's markup from the closest example in
   `references/slide-patterns.html`. The examples come from one real workshop, so rewrite
   every word, code line, link, and note from this workshop's files.
3. Give every slide:
   - `data-type`: `t` talk, `p` lab, `c` checkpoint.
   - An eyebrow. A section's first slide reads `Section N · Name` plus its clock range. Later
     talk slides can shorten the name. Lab slides read `Section N · Lab` plus the timebox, and
     checkpoint slides `Section N · Checkpoint`. The arc slides use the first-slide names.
   - `data-notes` written from the outline entry and the run sheet's notes for that section.
4. Code on a slide is copied from the file it shows: the starter `src/` for the tour,
   `code-reference/section-N/` for each section. When a block is shortened, its first comment
   line says `trimmed` and `…` marks each gap. Code that isn't from the plugin says so in
   its first comment (for example `// plain JS, for comparison`). Slide-only explanation
   comments are fine, and so is indenting with spaces where the source uses tabs.
5. Bullets step one per press on their own. Put `<ul data-no-steps>` on lists that should show
   at once (intro, who-am-I). When a bullet explains a line of code, wrap that code in
   `<mark data-step-mark="N">` with N = the bullet's position.
6. On lab slides, link the **Where** and **Rescue** paths to GitHub
   (`blob/trunk/…` for files, `tree/trunk/…` for folders) with `target="_blank" rel="noopener"`.
7. If the repo has `scripts/checkpoint.js` (`npm run checkpoint`), add the reminders to the
   speaker notes: on each lab slide, run checkpoint N while the room works; on each checkpoint
   slide, Ctrl+Tab to the site and reload.

## Check before calling it done

- **Layout:** serve the deck folder (`python3 -m http.server`), open it in Chrome, and run
  `references/layout-check.js` once in the top page (DevTools console or a browser tool's
  JavaScript runner). It loads the deck in sized frames itself, and it must report no
  problem slides at every size.
- **Code:** compare every code block with its source file. Fix anything that differs and isn't
  labeled `trimmed`.
- **Voice:** run the `sounds-like-me` skill on the on-slide text. Speaker notes are presenter
  shorthand: scan them for em-dashes only. A subagent reports findings for Ryan to approve.
- **Numbering:** after adding or cutting slides, update the slide numbers and section ranges in
  `slides-outline.md` and the run sheet in `facilitator-notes.md`.

## Publishing

Not part of this skill. When asked, each deck folder can be its own Spacefast Space connected
to the repo. Set the Space's root directory to the deck folder before its first build.

## Common mistakes

| Mistake | Instead |
|---|---|
| Writing a new deck engine or theme | Copy `templates/deck.html` unchanged |
| Making clicks advance slides | Keyboard and clicker only; the template already does this |
| `…` in code with no label | First comment line says `trimmed` |
| Code typed from memory or from the outline | Copy from `code-reference/section-N/` |
| Lab paths as plain text | Link them to GitHub, opening in a new tab |
| Fixing overflow by lowering font sizes in the theme | Widen the code column (`grid-template-columns` or `flex` on that slide), cut words, split the slide, or use `pre.code.tight` |
