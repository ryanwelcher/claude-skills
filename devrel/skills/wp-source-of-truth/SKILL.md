---
name: wp-source-of-truth
description: |
  Create and maintain the "WordPress X.Y Source of Truth" post (the big per-release roundup of
  every feature, tagged by audience) as Markdown in the wptrainingteam/source-of-truth repo, one
  directory per release, each building a standalone site on Spacefast. Use to start a new release's Source of Truth (from research or by importing a Google
  Doc draft), to sweep or refresh it (re-check PRs, Trac tickets, dev notes, Beta/RC inclusion and
  update status), to add or propose items, to publish or redeploy the site, or to schedule
  automatic sweeps, or to explain how it works and check which setup steps are done. Trigger on
  "source of truth", "SoT", "refresh/sweep the 7.x draft", "what changed for 7.x since last week",
  "SoT help", or any request to track what's landing in a WordPress release, even if the user
  doesn't name the skill.
---

# WordPress Source of Truth

The Source of Truth (SoT) is a long post, published for each major WordPress release, that lists
every notable change with a short description, audience tags, and links to learn more. The
WordPress 7.1 edition on Gutenberg Times is the reference for what the finished post looks like:
https://gutenbergtimes.com/wordpress-7-1-source-of-truth/

This skill keeps every SoT in one GitHub repo, `wptrainingteam/source-of-truth` (local clone:
`~/repositories/source-of-truth`). Each release has its own self-contained directory named for
the version (`7.2/`, `7.3/`), with one Markdown file per item. A build script turns a release
directory into two pages: the clean post at `/` for readers, and a draft review copy at `/draft/`
that shows the working notes, flags, hidden items and open questions. Each release is its own
Spacefast site, which rebuilds and republishes both pages on every push that changes its
directory. So "updating the site" always means changing files in the repo and pushing. Nothing
is uploaded by hand.

Run every command from inside the release directory, and don't touch another release's directory
unless the user asks. A release directory holds:

```
content/post/     what readers see: 00-intro.md, NN-section/ folders of NNN-item.md, 99-outro.md
notes/            research, sweep-log.md, open-questions.md, punted.md, status.json (never published)
proposals/        new items and rewrites waiting for approval (never published)
scripts/          build.mjs (→ dist/index.html), check-status.mjs (→ notes/status.json)
sot.json          version, dates, Gutenberg range, byline, Spacefast space
sf.jsonc          Spacefast build settings
```

Read `references/content-format.md` before you write or edit any content file. It has the item
format, tag vocabulary, working markers and house style, and those are what make the page build
correctly and read like the published SoT.

## Pick the job

Work out which of these the user wants. Most requests are a sweep.

| Request sounds like | Job |
|---|---|
| "Start the 7.3 SoT", "set up the repo" | **1. Start a release** |
| "Here's the Google Doc / import the draft" | **1b. Import a draft** |
| "Sweep", "refresh", "what changed", "update the statuses", a scheduled run | **2. Sweep** |
| "Add X", "we missed Y", "rewrite the Notes item" | **3. Add or propose items** |
| "Publish it", "set up Spacefast", "share link", "run it every day" | **4. Publish and schedule** |
| "Help", "how does this work", "what's set up?", "where does it get its info?" | **5. Help and setup status** |

Before any job, find the clone: the current directory or one of its parents, then
`~/repositories/source-of-truth`. If there's no clone, run
`gh repo clone wptrainingteam/source-of-truth ~/repositories/source-of-truth`. Then pick the
release directory. If the user didn't name a version and more than one release is still in
progress (no `published` date in its `sot.json`), ask which one. `git pull` first, because a
scheduled sweep or the Status workflow may have pushed since.

### 1. Start a release

1. Copy `assets/release-template/` into the clone as a directory named for the version (for
   example `7.3/`), and fill in `sot.json`. Copy `assets/status-workflow.yml` to
   `.github/workflows/status-<major>-<minor>.yml` at the repo root (GitHub only runs workflows
   from there). Add the release to the table in the root `README.md`.
2. Replace `X.Y` / `X-Y` placeholders in the workflow file, and in the release directory's
   `README.md`, `CLAUDE.md`, `content/post/00-intro.md`, the priority section's `_section.md`,
   and the notes files.
3. Research the release with `references/research.md`. Write candidates into `notes/research.md`
   first. A candidate goes into `content/post/` only once there's merged or committed work, or a
   "blessed" feature (mark those 🙏). That keeps the post honest from the first draft.
4. Create the section folders in the usual order (see `references/content-format.md`) and write
   the items.
5. Run `npm install && npm run build` and fix every warning you can.
6. Commit the release directory, the workflow and the root README together, and push to `trunk`.
   The repo is visible to the whole wptrainingteam org, so confirm with the user before the first
   push of a new release. Then continue with job 4.

### 1b. Import a Google Doc draft

The usual case: a draft already exists in Google Docs in the SoT layout (post first, then a
`# **Notes**` H1, then punted and backlog H1s).

1. Download the doc as Markdown without the Drive connector:
   `curl -sL -o draft.md "https://docs.google.com/document/d/<DOC_ID>/export?format=md"`.
   This works when the doc is shared as "anyone with the link". If the result is an HTML sign-in
   page, ask the user to export it with **File > Download > Markdown** and give you the path.
2. Set up the release directory and workflow (job 1, steps 1 and 2 for the workflow and root
   README), then run `node <skill-dir>/scripts/import-gdoc.mjs draft.md <release-dir>`. The
   importer fills `sot.json` and the release directory's placeholders.
3. Read the summary it prints, and open a few item files. Items under Developer Goodies often
   have no tags of their own, which is normal: they filter by the section's tags. Check that H4
   groups (like "Global Styles and theme.json") stayed together in one file.
4. Build, then commit with a message like `Import 7.2 draft from Google Docs (Oct 19 sweep)`.
   Push as in job 1, step 6.
5. Tell the user the Google Doc is now a snapshot. From here on, edits go in the repo.

### 2. Sweep

This job runs most often and is the one that runs on a schedule. Follow `references/sweep.md`
step by step. In short: run `npm run status`, compare the results with what each item claims,
apply the status-level changes directly, log the sweep, build, then commit and push to `trunk`
(which redeploys the site). Anything that needs editorial judgment goes into a proposal PR
instead.

The split between direct changes and proposals is the main safety rule of the skill:

- **Apply directly:**
  - Markers (🔍 🎨 🏈 🙏 ✏️) and `<!-- -->` working notes.
  - Resolved open questions, the sweep log, and `notes/status.json`.
  - Links that changed: a dev note was published, or a tracking issue moved.
  - Moving a confirmed-punted item out of the post into `notes/punted.md`.
  - **Factual corrections**: a sourced swap of a fact that's now wrong, inside an existing
    sentence. Examples: a version number (1.4.0 → 1.5.0), "proposed" → committed, a date, a
    renamed setting, or removing a clause that a working note said to drop if it shipped
    earlier.
- **Propose, don't apply:** new items, new paragraphs, rewritten sentences, reordering priority
  items, and the Overview narrative.

To test whether something is a factual correction: could the author check it against one link
in the commit message and accept it without re-reading the paragraph? If yes, apply it and cite
the source in the sweep log. If it changes what the paragraph says, or how it says it, propose
it. The line sits there because facts are checkable and reversible, but prose is the author's
voice and their name is on the byline. A sweep that rewrites copy unasked makes every diff
something the author has to re-read closely, and then they stop trusting the automation. A sweep
that leaves "1.4.0" wrong for a week is just as bad.

### 3. Add or propose items

1. Research the item (`references/research.md`) and collect the PR, issue, Trac and dev-note
   links.
2. Write it in the item format and house style (`references/content-format.md`). Put it in the
   right section folder with an order number between its neighbours (`025-…` fits between `020`
   and `030`).
3. If the user asked for it in this session, commit it to `trunk`. If a sweep or another
   automated run found it, put it on a `proposal/<version>/<date>-<slug>` branch and open a PR with
   `gh pr create`. Write the PR body as the reason it belongs: what merged, which milestone, and
   who it affects. Merging the PR deploys it.

### 4. Publish and schedule

Read `references/publishing.md`. It covers connecting a release directory to its own Spacefast
site (`sf git connect` with a root directory), creating the share links, the GitHub Actions fallback, and setting up a
scheduled sweep. Creating a Spacefast space, connecting a repo, and sharing a link are visible to
other people, so confirm with the user before each one, unless they've already asked for that
exact step.

### 5. Help and setup status

The user-facing guide is this skill's `README.md`. Answer "how does it work" questions from it,
quoting the part that fits instead of the whole file.

When the question is about a particular release ("what's set up for 7.3?", "why isn't it
updating?"), check the real state of that release and report it against README section 5:

| Step | How to check |
|---|---|
| Pushed | `git log origin/trunk -1 -- <version>/` shows the release directory |
| Spacefast site | `sot.json` → `spacefast.space` / `liveUrl`, then `npx spacefast versions --space <space>` |
| Autodeploy | Is the latest version newer than the last push that changed `<version>/`? |
| Share links | `sot.json` → `spacefast.shareLink` / `draftLink` |
| Status workflow | `gh workflow list` and `gh run list --workflow "Status <version>" --limit 3` |
| Scheduled sweep | Is there a recent sweep entry in `notes/sweep-log.md`? Is a routine listed under `/schedule`? |

Give a short checklist (done, not done, couldn't check), then offer to do the next step that
isn't done. If a check needs a sign-in you don't have, such as Spacefast, say so and don't guess.

## Ground rules

- **Facts come from sources, not memory.** Every claim in an item needs a PR, ticket, commit or
  Make post behind it. Your training data predates most of what goes into an SoT, so if you
  can't link it, it goes in `notes/` with a 🔍, not in the post.
- **Trust the merged code over the PR description.** Descriptions are written before review and
  often promise behaviour that was cut. For a claim about what a change does, check the merged
  diff (`gh pr diff <n> -R WordPress/gutenberg`) or the commit. If they disagree, go with the
  code and leave the claim out.
- **Punted items never appear in the post.** They move to `notes/punted.md` with the reason and
  a link. If one lands again later, it comes back through a proposal.
- **Reader-visible changes get a changelog line.** Once the post is published (`sot.json` has a
  `published` date), any sweep that changes what readers see adds a bullet under today's date in
  the intro's Changelog, newest date first.
- **Builds must pass.** Run `npm run build` before every commit. A warning about a working marker
  or placeholder in published text is fine during the draft stage. Before the first publish,
  `npm run build:strict` must pass. Commit `package-lock.json` whenever it changes, because
  Spacefast installs with `npm ci`.
- **Commit messages describe the change** ("Sweep Oct 27: 6 items confirmed in Beta 2, Secrets
  API committed"). Don't add AI co-author trailers or "generated with" lines.
