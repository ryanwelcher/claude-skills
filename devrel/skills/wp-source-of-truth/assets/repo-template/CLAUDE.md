# WordPress Source of Truth repo

This repo is the Source of Truth post for one WordPress release. `content/post/` is what readers
see. `npm run build` turns it into `dist/index.html` (the clean post) and `dist/draft/index.html`
(a review copy with notes, flags and hidden items). Spacefast rebuilds the site on every push to
`trunk`. `notes/` and `proposals/` never reach the clean post.

If the `wp-source-of-truth` skill is available, use it for any work here. Its references hold
the full content format and sweep procedure. If it isn't, follow the rules below.

## Content rules

- One item per file: frontmatter `title`, `tags` (from: end user, theme builder, plugin author,
  developer, site admin, enterprise, all), optional `flags` (edit, blessed, check, visuals,
  punted) and `published: false`. Then the body: short paragraphs with inline
  `([#123](url))` links, then `Tracking:` / `Read more:` / `Background:` lines, then
  `<!-- -->` working notes.
- Every claim needs a PR, ticket, commit or Make post behind it. Unsourced claims go in `notes/`.
  When a PR description and the merged code disagree, go with the code.
- Punted items move to `notes/punted.md` and never appear in the post.
- Once `sot.json` has a `published` date, reader-visible changes get a dated bullet in the
  Changelog in `content/post/00-intro.md` (newest date first).
- Run `npm run build` before every commit. Commit messages describe the change. No AI
  co-author or "generated with" lines.

## Sweep (scheduled or on request)

1. `git pull`. If `notes/status-report.md` was written today by the Status workflow, use it.
   Otherwise run `npm run status`.
2. For each changed ref, 🔍 note, or open question: if the fact settles it, apply the change on
   `trunk`. That covers:
   - clearing or adding markers and notes;
   - hiding an item that missed Beta (`published: false`);
   - moving a confirmed punt to `notes/punted.md`;
   - adding a dev-note `Read more:` link;
   - resolving the question;
   - factual corrections: swapping a now-wrong fact (version, date, "proposed" → committed)
     inside an existing sentence, with the source cited in the sweep log.
3. New items, rewritten sentences or paragraphs, and priority or Overview changes go on a
   `proposal/<date>-<slug>` branch as a PR. Never commit those straight to `trunk`. Check
   `gh pr list` first so you don't open a duplicate.
4. Add a dated entry at the top of `notes/sweep-log.md` (what was checked, what changed, what
   was proposed, which questions were resolved), build, commit, and push.
5. The wordpress-develop commit that pins Gutenberg for each Beta or RC lists every PR it
   includes. That's the most direct proof a PR is in. Otherwise, a merged PR's milestone (`Gutenberg NN.N`) is the plugin version it ships in. If that version
   is after the release's range (see `sot.json`), the PR needs a backport or a Beta/RC post that
   confirms it.
