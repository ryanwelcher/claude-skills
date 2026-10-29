# WordPress X.Y Source of Truth

The repo mirror of the WordPress X.Y Source of Truth. The working draft is the Google Doc
(`sot.json` → `googleDoc`), and it wins over this directory. Every push to `trunk` that changes
this directory rebuilds the Spacefast site, which goes public at the final release.

- Live post: `sot.json` → `spacefast.liveUrl` (reader link: in Spacefast, ID in `spacefast.shareLinkId`)
- Draft review copy, with working notes and hidden items: `/draft/` (reviewer link: ID in `spacefast.draftLinkId`)

## Working on it

Ask Claude, which uses the `wp-source-of-truth` skill or, without it, this directory's `CLAUDE.md`:

- "Scan the X.Y SoT" (the `wp-sot-scan` skill): re-checks every PR, Trac ticket and dev note
  linked in the Doc, finds new candidates, and gives you one dated block to paste at the bottom
  of the Notes tab.
- "Add <feature> to the SoT": researches it and adds it to the Draft in house style.
- "Write the draft from the notes": drafts the merged and blessed items, after you've
  spot-checked the notes.
- "SoT help" / "What's set up?": explains the workflow and checks the setup steps below.

To edit by hand, edit the Google Doc. The next import picks it up.

## Layout

- `content/post/`: the post, one Markdown file per item, in filename order
- `notes/`: research, scan results, open questions, punted items, status data (never published)
- `notes/doc-updates.md`: Doc changes waiting to be pasted in, while the Doc write path isn't set up
- `../.github/workflows/status-X-Y.yml`: the daily status check for this release

```bash
npm ci
npm run build          # dist/index.html (clean post) and dist/draft/index.html (review copy)
npm run build:strict   # also fails on markers or placeholders left in published text
npm run status         # re-check every linked PR and Trac ticket
```

## Setup status

Tick these off as you go. The full steps are in the skill's README, section 5.

- [ ] Google Doc linked in `sot.json` → `googleDoc`, with Draft, Notes, Punted and Backlog tabs
- [ ] Release directory committed and pushed
- [ ] Spacefast site created (`sot.json` → `spacefast.space`)
- [ ] Autodeploy connected (`sf git connect`, root directory `X.Y`, production branch `trunk`)
- [ ] Reader and reviewer share links created, and the reader link checked against `/draft/`
- [ ] Status workflow ran once (`gh workflow run "Status X.Y"`)
- [ ] At final release: Status workflow turned off
