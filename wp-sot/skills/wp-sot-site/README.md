# wp-sot-site

Builds and publishes the **one-site WordPress Source of Truth**: every release from 6.2 onward in
a single static site on Spacefast, each at `/<major>-<minor>/` (for example `/7-2/`), with the
newest at `/`. A version dropdown in the header switches between them.

The content comes from each release's Google Doc, imported as Markdown into
[`wptrainingteam/source-of-truth`](https://github.com/wptrainingteam/source-of-truth) (local
clone: `~/repositories/source-of-truth`). The skill never writes copy. To change what a page says,
fix the Doc and import again.

This skill only builds and publishes. Tracking what lands in a release (sweeps, the Notes tab,
proposals) is [`wp-source-of-truth`](../wp-source-of-truth/README.md).

You use it by talking to Claude. The clone's own `README.md` and `CLAUDE.md` hold the release
table, commands and content rules, and Claude reads them first.

## What to say

| You say | What happens |
|---|---|
| "Add 7.3 to the SoT site" (with the Doc link) | Imports the Doc into `releases/7.3/`, checks coverage, builds, commits |
| "Import the SoT doc into the site" | Same, for the release the Doc describes |
| "Update the SoT site" | Pulls the clone, re-imports the release you name, rebuilds, commits |
| "Give 7.3 its own layout" (with an HTML file) | Copies it to `releases/7.3/layout/layout.html`, sets `"layout": "own"`, checks the slots, builds |
| "Change the SoT layout" | Edits the generic layout, then rebuilds every release to check nothing else moved |
| "SoT site help" | Explains how it works and reports which setup steps are done |

Claude asks before it pushes to `trunk` or does anything on Spacefast, because the repo is visible
to the whole wptrainingteam org.

## Custom layouts

A layout is an HTML file with comment slots such as `<!-- sot:sections -->`. Keep all of them
and the build will fill them in. The full list is in `SKILL.md`. A layout changes how a release
looks, never what it says.

## Setup checklist

- [ ] The release's Google Doc is shared as "anyone with the link can view". If it can't be,
  export it with **File > Download > Markdown** and give Claude the path.
- [ ] `~/repositories/source-of-truth` is cloned and `npm ci` has run.
- [ ] Spacefast is connected to the repo (a build with `npm ci`, `npm run build`, output `dist`,
  set in the repo's `sf.jsonc`) and you are signed in.
- [ ] Run `bin/link-skills` in `claude-skills` so this skill is loaded on your machine.

## Automatic updates

A routine can keep a release in step with its Doc. Use this prompt: "Update the X.Y release of
the Source of Truth site from its Google Doc. Follow CLAUDE.md." No Drive connector is needed,
only the public Doc link.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Import says the export is a sign-in page | Share the Doc as "anyone with the link can view", or export it as Markdown and pass the file |
| Import says no "WordPress X.Y Source of Truth" heading was found | Export the whole Doc with all tabs, not a single tab |
| Build fails with a leak | A marker or comment got past the importer. Fix the cause in the Doc or the splitter |
| Build fails naming a slot | The release's own layout is missing that slot. Add it back |
| A section or item is missing from a page | Run the coverage check in `SKILL.md`. A gap means a splitter bug |
