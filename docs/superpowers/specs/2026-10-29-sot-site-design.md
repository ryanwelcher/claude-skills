# Source of Truth site skill: design

Date: 2026-10-29. Status: draft for Ryan's approval (builder check done, Ryan's answers in).

## Intent

The WordPress Source of Truth (SoT) is the per-release roundup of every notable change, tagged by
audience. Until now it has been published as a long text post: on Anne McCarthy's blog, nomad.blog (6.2 to
6.6), then on Gutenberg Times (6.7 to 7.1).
The goal is to make one Spacefast site the canonical home for every SoT, so the content is easier
to navigate and nicer to read than a long post with a table of contents.

The current `wp-source-of-truth` skill does two jobs: it tracks what's landing in a release (sweeps,
notes, punted and backlog), and it builds a site. Ryan is splitting it into two skills. This
document covers the first one: **take a release's Google Doc, fill a layout with its content, and
add that release to the single SoT site.** The tracking and notes skill is a separate, later
piece of work.

## Goals

1. **One site, one URL, every release.** A shared header on every page has a version dropdown.
   The newest release shows by default. Older releases stay reachable.
2. **The skill fills a layout from a Google Doc.** Inputs: the Doc for a release, and optionally
   an HTML layout for that release. If there's no layout, the skill uses the generic one. The
   skill puts the Doc's items into the layout's sections.
3. **A generic layout** with a standard section structure, built from Ryan's 7.2 example
   (`~/Downloads/wordpress-7-2-source-of-truth.html`).
4. **Bring in every earlier edition.** Add 6.2 through 7.1 to the site, filled from their
   published posts (nomad.blog and Gutenberg Times) into the generic layout. This proves the
   version switcher and the generic layout across many releases, and makes the site the one
   archive of every SoT.
5. **Run it by hand now, and be able to run it in the cloud later** without changing how it
   works.

## Non-goals

- Sweeps, notes gathering, the Notes, Punted and Backlog tabs, status checks, open questions.
  Those belong to the second skill.
- Designing a custom layout for a release, or adding interactive features (like the 7.2 example's
  style swatches, gallery shuffle, icon search and dev checklist). That may become its own skill
  later. The layout *contract* (below) has to leave room for it.
- Writing to the Google Doc. This skill only reads it.
- Setting up the scheduled cloud run. The skill only has to be able to run there.

## Anti-goals (a failure even if it works)

- The site states something the Doc doesn't. The Doc (or, for the prototype releases, the
  published Gutenberg Times post) is the only source of content. The skill doesn't add facts,
  rewrite copy or "improve" the author's prose.
- Adding a new release changes how an older one looks or reads. Each release renders on its own.
- An item from the Doc silently goes missing from the page. Every item ends up on the page or is
  reported as not placed.
- Working notes, emoji markers or `<!-- -->` comments from the Doc reach the page.

## Decisions Ryan made

- **The site is the canonical home** and replaces Gutenberg Times for future releases.
- **No hidden or draft versions.** While being built, the whole site is private (the current
  Spacefast URL is private and experimental). When it's ready, the whole site goes public. Every
  release in the repo shows in the dropdown, including in-progress ones.
- **Same repo, restructured:** `wptrainingteam/source-of-truth` (local clone
  `~/repositories/source-of-truth`). It stops being one self-contained directory and Spacefast
  site per release, and becomes one site.
- **Layouts are filled with content**, not delivered pre-written. Releases will usually share a
  generic layout with a standard structure. Functionality can be added to layouts later.
- **Older releases:** all of them, 6.2 through 7.1, from nomad.blog and Gutenberg Times, as part
  of the initial work.
- **For 7.2, the Doc wins.** The site is filled from the Google Doc, not from the repo's current
  `7.2/content/post/`. Sweeps changed the repo after the Oct 19 import (Description List and ToC
  hidden, 7.1 carryovers removed, one factual fix), and 11 proposal PRs are open against those
  files. Ryan or Justin checks the Doc has those changes before the first run. The PRs are not
  carried over.
- **Copy that isn't in the source is built mechanically or left out** (option b). The generic
  layout's hero, stats, timeline and resources blocks are filled only from things that can be
  derived: dates and the Gutenberg range from `release.json`, item and section counts, and the
  standard Make Core links for the version. The hero headline and intro come from the source's
  Overview. Hand-written per-release copy (a headline, curated stats) is out of scope until
  custom layouts arrive. Items render with their full text from the source, not condensed card
  summaries.
- **Running:** by hand for now. Cloud is the target later.

## Claude's calls (Ryan can overrule any of these)

1. **Keep the Markdown step.** Doc → Markdown, one file per item (the existing
   `scripts/import-gdoc.mjs` already does this) → rendered into the layout. It gives every run a
   reviewable git diff and lets the prototype releases use the same render path (their source is
   a Gutenberg Times post converted to the same Markdown shape).
2. **Pages per release at their own path**, for example `/7-2/`, `/7-1/`. The root `/` serves or
   redirects to the newest release. Switching versions is a normal page load, so each release's
   CSS and scripts never mix with another's.
3. **The shared header is injected by the build**, not written into each layout. A layout marks
   where the header goes. The header holds the site name, the version dropdown, and nothing that
   depends on a release's design beyond inheriting a few CSS custom properties.
4. **The generic layout is the 7.2 example minus the one-off demos.** It keeps the look and the
   structure: hero, "at a glance" stats, release timeline (only when `release.json` has
   milestones; older releases may not), audience filter, table of contents, sections, punted
   block, resources and footer. Every block follows the "built mechanically or left out" rule.
5. **One build at the repo root** (`npm run build` → `dist/`, with one subdirectory per
   release), one Spacefast space, one `sf.jsonc`.
6. **The existing 7.2 site is retired** once the combined site works: its Spacefast space,
   `/draft/` page and per-release `sf.jsonc`. The rest of the `7.2/` folder, including
   `content/post/`, `scripts/check-status.mjs`, the notes and the `Status 7.2` workflow, stays
   exactly where it is, so the status checks keep working for the second skill. The new site
   reads only `releases/`.
7. **Reading the Doc** uses the public Markdown export
   (`https://docs.google.com/document/d/<ID>/export?format=md`), which needs the Doc shared as
   "anyone with the link". It works the same locally and in a cloud run, where the Drive
   connector may not be available. If the export returns a sign-in page, the skill stops and
   asks for a downloaded Markdown file.
8. **Skill name:** `wp-sot-site`, living next to `wp-source-of-truth` in
   `claude-skills/devrel/skills/`. `wp-source-of-truth` keeps its other jobs until the second
   skill replaces it. Its site-building and publishing jobs point to the new skill.

## The layout contract

A layout is one HTML file (plus optional CSS and JS beside it) that the build fills. The contract
is the part this design fixes. The exact markup is the builder's.

- **Header slot:** where the shared header goes.
- **Release fields:** version, release date, Gutenberg range, byline, updated date, reading time.
  These come from the release's config.
- **Section slots,** in the standard section order (Priority items, New blocks, Improved blocks,
  Editor enhancements, Admin and workflow, Developer goodies), plus Punted, Resources and the
  Changelog. Each slot says how to render one item: title, tags, body and links.
- **Every rendered item** carries `data-tags`, `data-title` and an `id`, because the audience
  filter and the table of contents run off those (as in the 7.2 example).
- **Sections in source order (Claude's call):** the generic layout renders whatever sections
  the source has, in its order and with its headings. It doesn't map them onto a fixed list. That
  keeps each author's structure (6.9 has "Command Palette everywhere", "A closer look at
  performance optimizations" and others) and means nothing goes unplaced. The source's Overview
  becomes the intro. Its "Important note/guidelines" and Tags legend are left out, because the
  audience filter replaces them. The Changelog is kept.
- **Unplaced items:** a custom layout with fixed slots fails the build with a clear message when
  the source has a section it has no slot for, instead of dropping it.
- **Punted (Claude's call):** the punted block shows the Doc's Punted tab and is left out when
  that tab is empty or missing (the published posts have none). This skill only reads that tab.
  Items still flagged 🏈 inside a section are not shown.
- A custom layout may add its own markup and scripts around the slots (the later "functionality"
  work). The build leaves anything outside the slots alone.

## Repo shape (after the restructure)

```
package.json, sf.jsonc          one build, one Spacefast site
scripts/build.mjs               renders every release into dist/<slug>/ and writes the header
layouts/generic/                the generic layout
releases/<version>/             one per release:
  release.json                  version, dates, Gutenberg range, byline, Doc ID, layout name, source
  content/                      Markdown items from the Doc (or the GT post)
  layout/                       optional: this release's own layout, overriding generic
<version>/notes/ etc.           the 7.2 notes and status files stay as they are for the second skill
```

The builder may change names and paths, as long as each release stays self-contained in its
content and layout choice.

## What the skill does

1. **Add or update a release:** given a Doc link (and optionally a layout file), export the Doc,
   run the importer into `releases/<version>/content/`, record the Doc and layout in
   `release.json`, build, and report what changed, including any items that weren't placed.
   The importer used by this skill writes only into `releases/<version>/`. It must not write the
   notes files (`notes/research.md`, `sweep-log.md`, `open-questions.md`, `punted.md`), which
   belong to the second skill.
2. **One-time migration, not a skill job** (for earlier editions, decided after approval): a repo script in `scripts/migrate/`, given a nomad.blog or Gutenberg Times SoT
   URL, convert the published post to the same Markdown shape and record it with its `source`
   (`nomadblog` or `gutenbergtimes`) and URL. Keep the post's own changelog.
3. **Build and publish:** build the whole site, commit, push. Spacefast rebuilds from the repo.
   Creating the space, connecting it and any sharing step are confirmed with Ryan first.
4. **Help:** explain how it works and what's set up.

Each run is a git commit with a message that says which release changed and from what source.

## Running in the cloud later

Nothing in the skill may depend on a local-only tool or the Drive connector. It needs: Node, `gh`
or git push access, the public Doc export, and a Spacefast autodeploy on push (so a cloud run only
has to push). The skill's `SKILL.md` and the repo's `CLAUDE.md` carry the rules, so a cloud
routine can run it with a one-line prompt.

## Sources for each release

| Version | Source |
|---|---|
| 6.2 | https://nomad.blog/2023/03/01/wordpress-6-2-source-of-truth/ |
| 6.3 | https://nomad.blog/2023/07/17/wordpress-6-3-source-of-truth/ |
| 6.4 | https://nomad.blog/2023/10/09/wordpress-6-4-source-of-truth/ |
| 6.5 | https://nomad.blog/2024/03/13/wordpress-6-5-source-of-truth/ |
| 6.6 | https://nomad.blog/2024/06/26/wordpress-6-6-source-of-truth/ |
| 6.7 | https://gutenbergtimes.com/6-7-source-of-truth/ |
| 6.8 | https://gutenbergtimes.com/source-of-truth-wordpress-6-8/ |
| 6.9 | https://gutenbergtimes.com/wordpress-6-9-source-of-truth/ |
| 7.0 | https://gutenbergtimes.com/wordpress-7-0-source-of-truth/ |
| 7.1 | https://gutenbergtimes.com/wordpress-7-1-source-of-truth/ |
| 7.2 | The Google Doc (in Bifrost Drive) and the example layout |

Old posts may use their own section names and structure. Older nomad.blog posts likely differ more
from the current format than the Gutenberg Times ones do.

The site republishes other people's posts (Anne's and the Gutenberg Times authors'), so each
release page credits its original author and links its original post. Confirm with Anne and
Birgit before the site goes public.

## Left to the builder

- The exact layout slot markup and how the build fills it (template syntax, or a DOM pass).
- How the shared header and dropdown look, within the 7.2 example's style.
- How to convert a Gutenberg Times post into the Markdown shape (export, scrape or REST API).
- Whether `/` redirects to the newest release or renders it.
- The Spacefast space name and URL (the private one can be reused or replaced).
