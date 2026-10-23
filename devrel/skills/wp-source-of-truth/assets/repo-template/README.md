# WordPress X.Y Source of Truth

The source for the WordPress X.Y Source of Truth. Every push to `trunk` rebuilds the site on
Spacefast.

- Live post: `sot.json` → `spacefast.liveUrl` (reader link: `spacefast.shareLink`)
- Draft review copy, with working notes and hidden items: `/draft/` (reviewer link: `spacefast.draftLink`)

## Working on it

Ask Claude, which uses the `wp-source-of-truth` skill or, without it, this repo's `CLAUDE.md`:

- "Sweep the X.Y SoT": re-checks every PR, Trac ticket and dev note, fixes statuses and facts,
  and opens proposal PRs for anything editorial.
- "Add <feature> to the SoT": researches it and writes it in house style.
- "SoT help" / "What's set up?": explains the workflow and checks the setup steps below.

To edit by hand, change the files in `content/post/`, run `npm run build`, and push.

## Layout

- `content/post/`: the post, one Markdown file per item, in filename order
- `notes/`: research, sweep log, open questions, punted items, status data (never published)
- Open PRs named `proposal/…`: new items and rewrites waiting for review. Each one gets a
  Spacefast preview.

```bash
npm ci
npm run build          # dist/index.html (clean post) and dist/draft/index.html (review copy)
npm run build:strict   # also fails on markers or placeholders left in published text
npm run status         # re-check every linked PR and Trac ticket
```

## Setup status

Tick these off as you go. The full steps are in the skill's README, section 5.

- [ ] GitHub repo created and pushed
- [ ] Spacefast site created (`sot.json` → `spacefast.space`)
- [ ] Autodeploy connected (`sf git connect`, production branch `trunk`)
- [ ] Reader and reviewer share links created, and the reader link checked against `/draft/`
- [ ] Status workflow ran once (`gh workflow run Status`)
- [ ] Scheduled sweep routine created (daily from Beta 1)
- [ ] At final release: routine and Status workflow turned off
