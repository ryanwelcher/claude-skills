# WordPress X.Y Source of Truth

The source for the WordPress X.Y Source of Truth. Live site: see `sot.json` → `spacefast.liveUrl`.

- `content/post/`: the post, one Markdown file per item, in filename order
- `notes/`: research, sweep log, open questions, punted items (not published)
- `proposals/`: see open PRs named `proposal/…` for items waiting for review

```bash
npm install
npm run build        # dist/index.html (clean post) and dist/draft/index.html (review copy)
npm run status       # re-check every linked PR and Trac ticket
```

Pushing to `trunk` redeploys the site.
