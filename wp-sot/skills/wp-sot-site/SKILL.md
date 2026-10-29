---
name: wp-sot-site
description: |
  Build and update the one-site WordPress Source of Truth (every release, 6.2 onward, in one
  static site on Spacefast) from a release's Google Doc. Use to add a release to the site, to
  re-import a release after the Doc changed, to rebuild and publish the site, to give a release
  its own layout, or to check the layout slot contract. Trigger on "build/update the Source of
  Truth site", "add 7.3 to the SoT site", "import the SoT doc into the site", "change the SoT
  layout", "SoT site help". Not for tracking what lands in a release (sweeps, Notes tab,
  proposals): that is wp-source-of-truth.
---

# WordPress Source of Truth site

One site holds every WordPress Source of Truth. It lives in the `wptrainingteam/source-of-truth`
repo (local clone: `~/repositories/source-of-truth`). Each release is `releases/<version>/`
(Markdown plus a `release.json`), and `npm run build` turns all of them into `dist/`: a page per
release at `/<major>-<minor>/`, with the newest also at `/`. Spacefast rebuilds on every push to
`trunk`.

The Google Doc is the source for a release. The site never edits content: it imports the Doc,
and a fix means fixing the Doc and importing again. This skill only builds and publishes. The
tracking work (sweeps, Notes tab, proposals) belongs to `wp-source-of-truth`.

Read the clone's `README.md` (release table, commands) and `CLAUDE.md` (content rules) before you
change anything. They are the source of truth for both, so this file points to them instead of
repeating them.

## Pick the job

| Request sounds like | Job |
|---|---|
| "Add 7.3 to the SoT site", "import the doc", "rebuild 7.2 from the Doc", "update the SoT site" | **Add or update a release** |
| "Change the layout", "give 7.3 its own layout", "does my layout work" | **Layouts** |
| "Help", "how does the site work", "what's set up" | **Help** |

Before any job, find the clone: the current directory or one of its parents, then
`~/repositories/source-of-truth`. If there's none, run
`gh repo clone wptrainingteam/source-of-truth ~/repositories/source-of-truth`. Then `git pull`,
and `npm ci` if `node_modules` is missing.

## Add or update a release

1. Get the Doc: a link or ID. If the user has a custom layout file for this release, ask for its
   path too.
2. Run `npm run -s import:doc -- <doc-id-or-url>`. It writes `releases/<version>/` and keeps an
   existing `release.json` and `layout/`. If the export comes back as a sign-in page, or has no
   "WordPress X.Y Source of Truth" heading (a single tab was exported), it stops with a message: ask the user to share the Doc as "anyone with the link can
   view", or to download it as Markdown (**File > Download > Markdown**) and pass that path
   instead.
3. If there is a layout file, copy it to `releases/<version>/layout/layout.html` and set
   `"layout": "own"` in that release's `release.json`. Check it against the slot contract below.
4. Check coverage. Compare the count of H2 and H3 headings in the Doc with the sections and items
   in `releases/<version>/content/`. The only allowed differences are the dropped kinds
   (Changelog, guidelines, Overview, Tags, Resources/Assets) and 🏈 items. Any other gap is a
   splitter bug: fix `scripts/lib/split.mjs` with a new test in `test/split.test.mjs`, re-import,
   and check again.
5. Run `npm test` and `npm run build`. A leak (a marker or comment that reached a page) or a
   layout missing a slot fails the build. Fix the cause, never the check. Look at the page
   (`npx serve dist`) at desktop width and at 375px.
6. Commit with a message that names the release and the source, for example
   `Import 7.3 from its Google Doc (Nov 12 draft)`. No AI co-author or "generated with" lines in
   this repo.
7. Push to `trunk` after the user confirms. In an interactive run, always confirm before the push
   and before any Spacefast action (creating a space, connecting a repo, sharing a link). The
   repo is visible to the whole wptrainingteam org.

The old editions (6.2 to 7.1) were imported once from their published posts. That migration is
done and isn't a job. Rebuild them like any other release.

## Layouts

A release uses `layouts/generic/` unless its `release.json` says `"layout": "own"`, in which
case it uses `releases/<version>/layout/layout.html`. A layout is plain HTML with these comment
slots. `renderPage` replaces each one, and the build throws if a slot the content needs is
missing:

| Slot | Filled with |
|---|---|
| `<!-- sot:head -->` | `<title>`, description, canonical link |
| `<!-- sot:header -->` | Shared site header with the version dropdown |
| `<!-- sot:hero -->` | Eyebrow, H1, intro, byline, reading time, original-post link |
| `<!-- sot:stats -->` | Up to four stats: release date, sections, items, Gutenberg range |
| `<!-- sot:timeline -->` | Milestones from `release.json`, empty when there are none |
| `<!-- sot:filter -->` | One audience pill per tag used on the page |
| `<!-- sot:toc -->` | Numbered list of sections, items nested |
| `<!-- sot:sections -->` | Every section and its items, with `data-tags` and `data-title` |
| `<!-- sot:punted -->` | The Doc's Punted tab, empty when there is none |
| `<!-- sot:changelog -->` | The Changelog |
| `<!-- sot:resources -->` | Make Core cycle page, dev notes tag, original post link |

Rules for a custom layout:

- Keep every slot. Style them freely, but don't drop one.
- Leave `data-tags` and `data-title` alone on sections and items: `site.js` (or the layout's own
  script) filters from them.
- Put any `.js` or `.css` files next to `layout.html`. The build copies them beside the page.
- A layout changes how a release looks, never what it says. Content stays as imported.

## Help

Answer "how does it work" questions from the clone's `README.md` and this skill's `README.md`,
quoting the part that fits. For "what's set up", check the real state and give a short checklist
(done, not done, couldn't check):

| Step | How to check |
|---|---|
| Clone | `~/repositories/source-of-truth` exists and `git status` is clean |
| Release imported | `releases/<version>/release.json` exists, `source.id` is the Doc |
| Builds | `npm test` and `npm run build` pass |
| Pushed | `git log origin/trunk -1 -- releases/<version>/` shows it |
| Spacefast site | `sf.jsonc` is at the repo root, and the site's latest version is newer than the last push |
| Doc sharing | The Doc is "anyone with the link can view", or exported as Markdown by hand |

If a check needs a sign-in you don't have, such as Spacefast, say so and don't guess.

## Ground rules

- **Content comes only from the source.** No invented copy, no rewritten prose, no summaries.
  Blocks not in the Doc are built mechanically from data (dates, counts, standard Make Core
  links) or left out.
- **Never hand-edit imported Markdown.** Fix the Doc and import again.
- **Nothing marked ✏️ 🙏 🔍 🎨 🏈, no `<!-- -->` comments, and none of the Notes, Backlog,
  guidelines or Tags legend reaches a page.** 🏈 items are hidden. The Punted block comes only
  from the Doc's Punted tab.
- **Sections stay in source order**, with the source's own headings.
- **One release never changes another's output.** Importing or re-importing 7.3 leaves 7.2's page
  alone, apart from the header's version list.
- **Never touch `7.2/` or `.github/workflows/status-7-2.yml`** in the clone. They belong to
  `wp-source-of-truth`.
- **Run `npm test` and `npm run build` before every commit.**
- **Never create a branch** without asking. Commit on `trunk`.

## Cloud runs

A scheduled or cloud run uses one prompt: "Update the X.Y release of the Source of Truth site
from its Google Doc. Follow CLAUDE.md." No Drive connector is needed: the importer downloads the
Doc's public export, so the Doc has to be shared as "anyone with the link can view". If it isn't,
the run stops with the sign-in message and reports that instead of guessing. In a cloud run there
is no person to confirm with, so follow the clone's `CLAUDE.md` for what may be pushed.
