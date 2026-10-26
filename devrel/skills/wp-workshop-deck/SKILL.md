---
name: wp-workshop-deck
description: |
  Use when a WordPress workshop repo needs its presentation slides built, rebuilt, or extended
  from slides-outline.md, including adding a deck for a new workshop length
  (slideshows/<length>/index.html), or when a deck needs publishing to Spacefast as its own
  auto-deploying site. Pairs with wp-workshop-scaffold, which writes the outline.
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

## Publishing to Spacefast

Only when Ryan asks. Each deck folder is its own Space, connected to the GitHub repo, so a push
to `trunk` that changes `slideshows/<length>/` redeploys that deck and other pushes are skipped.
Use the `spacefast:spacefast` skill for sign-in and team lookup. Use the `sf` CLI. If it is not
installed, ask before running it through `npx -y spacefast`.

1. **Name it.** The title is the workshop title from the README's first heading. The slug is
   that title in kebab-case. If another length of this workshop already has a Space, propose a
   title and slug that include the length. Confirm the title, slug, team, and access with Ryan.
2. **Publish once** from the deck folder. Do a dry run first. It must list only `index.html`
   and any files the deck loads. `<team>` is the team ID from the team lookup.
   ```
   sf publish . --team <team> -n "<title>" --slug <slug> --access public --dry-run
   sf publish . --team <team> -n "<title>" --slug <slug> --access public --json -y
   ```
3. **Fix the link file.** The CLI writes `.spacefast/space.json` with `"space"` set to the
   slug. Change it to the Space ID (`spc_…`, in the publish JSON or from `getSpace`). The ID
   stays the same if the Space is renamed later, but the slug doesn't. Commit `space.json` but
   don't push it yet. If
   `slideshows/.gitignore` doesn't exist, create it so it covers every deck folder:
   ```
   **/.spacefast/state.json
   **/.spacefast-*
   **/.spacefast/.space-link-*.tmp
   ```
   Delete any `.gitignore` the CLI wrote inside the deck folder.
4. **Connect the repo.** Ask Ryan to connect the GitHub repo to the Space in the Spacefast
   dashboard. The plugin's sign-in can't read GitHub app installations. When Ryan confirms, run
   this immediately. Spacefast builds the repo root as soon as the repo connects, which deploys
   the plugin's build output instead of the deck.
   ```
   sf git update --space <spc_id> --root-directory slideshows/<length> \
     --auto-deploy-production --no-auto-deploy-previews \
     --ignored-build-command 'git diff --quiet HEAD^ HEAD -- "$(git rev-parse --show-toplevel)/slideshows/<length>"' \
     --json -y
   ```
   Then push. The `space.json` commit changes the deck folder, so it builds the deck and
   replaces the repo-root build.
5. **Record it.** Add the folder and its live URL to the Publishing table in
   `slideshows/README.md` (create the table if it's missing), and push.

Check: the live URL returns 200 with the deck's `<title>`, and `show_space_deployments` shows
the live version built from the latest deck commit, not from the repo-root build.

## Common mistakes

| Mistake | Instead |
|---|---|
| Writing a new deck engine or theme | Copy `templates/deck.html` unchanged |
| Making clicks advance slides | Keyboard and clicker only; the template already does this |
| `…` in code with no label | First comment line says `trimmed` |
| Code typed from memory or from the outline | Copy from `code-reference/section-N/` |
| Lab paths as plain text | Link them to GitHub, opening in a new tab |
| Publishing without `-n` and `--slug` | The Space is named after the folder (`90-minutes`); set both on the first publish |
| Trusting the first build after connecting the repo | It built the repo root; set the root directory, then push a deck change |
| Fixing overflow by lowering font sizes in the theme | Widen the code column (`grid-template-columns` or `flex` on that slide), cut words, split the slide, or use `pre.code.tight` |
