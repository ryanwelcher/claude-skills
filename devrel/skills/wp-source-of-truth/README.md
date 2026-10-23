# wp-source-of-truth

Builds and maintains the **WordPress X.Y Source of Truth**, the per-release post that lists
every notable change with audience tags and links. Each release gets its own GitHub repo of
Markdown. Spacefast turns the repo into a standalone site and rebuilds it on every push. The
reference for the finished format is the
[WordPress 7.1 Source of Truth](https://gutenbergtimes.com/wordpress-7-1-source-of-truth/).

You use it by talking to Claude. This guide covers what to say, what happens, and how to set up
the automatic updates. Claude reads it too, when you ask for help.

## Contents

1. What you get
2. Where the information comes from
3. What to say
4. A release from start to finish
5. Setup checklist
6. Reviewing changes
7. Troubleshooting

## 1. What you get

One repo per release, named `wp-<major>-<minor>-source-of-truth`:

| Path | What it is |
|---|---|
| `content/post/` | The post: one Markdown file per item, in section folders |
| `notes/` | Research, the sweep log, open questions, punted items, and status data. Never published. |
| `sot.json` | Release version, dates, Gutenberg range, byline, and Spacefast links |
| `scripts/build.mjs` | Builds the site |
| `scripts/check-status.mjs` | Re-checks every linked PR and Trac ticket |
| `.github/workflows/status.yml` | Runs the status check every morning |
| `CLAUDE.md` | Rules for any Claude session working in the repo, including scheduled ones |

Each build makes two pages:

- **`/`, the clean post** for readers: byline, reading time, numbered table of contents,
  and audience filter buttons. With an audience turned on, readers see only the items tagged for
  that audience.
- **`/draft/`, the review copy**: working notes as yellow callouts, markers as badges, hidden
  items greyed out, and the open questions at the end. Search engines don't index it.

## 2. Where the information comes from

- **Research when a release starts:** Make Core posts for the release (cycle page, roadmap,
  release squad, dev notes), Gutenberg release posts and GitHub release notes, open iteration
  issues, Trac, and the previous release's punted list. An item goes into the post only when
  there's merged or committed work behind it. Every claim links to its source.
- **The status check on each sweep:** it looks up every PR and issue link on GitHub (state,
  merged date, milestone, labels) and every Trac ticket. Trac blocks scripts, so tickets are
  checked through `Fixes #N` commits and PRs in `WordPress/wordpress-develop`. It also reads
  the latest Gutenberg releases, new dev notes, and Make Core posts tagged for the release,
  then writes `notes/status-report.md` with what changed since the last run.
- **Proof of inclusion:** the `wordpress-develop` commit that pins Gutenberg for each Beta or RC
  lists every PR in that package. A merged PR's milestone (`Gutenberg 24.3`) shows which plugin
  version it ships in.
- **You:** anything you ask for directly.

## 3. What to say

| You say | Claude does |
|---|---|
| "Start the 7.3 Source of Truth" | Creates the repo from the template, researches the release, writes the first items |
| "Import this doc: <Google Doc link>" | Downloads the doc as Markdown and splits it into the repo layout |
| "Sweep the 7.3 SoT" / "What changed since last week?" | Re-checks everything, applies status fixes, opens proposal PRs, and logs the sweep |
| "Add <feature> to the SoT" | Researches it, writes it in house style, and commits it |
| "Set up Spacefast for the 7.3 SoT" | Connects the repo, publishes, and creates the reader and reviewer links |
| "Schedule the sweeps" | Creates the daily cloud routine |
| "SoT help" / "What's set up for 7.3?" | Explains how it works and checks which setup steps are done for that repo |

## 4. A release from start to finish

| When | What happens |
|---|---|
| Cycle starts (roadmap post) | Start the repo. The first research pass fills `notes/research.md` and a first draft. Run weekly sweeps. |
| Beta 1 | Confirm the Gutenberg range from the Beta 1 post. Switch sweeps to daily. Items that missed Beta 1 and aren't blessed get hidden. |
| Beta 2 – RC 1 | Daily sweeps. Merge or close proposal PRs, answer open questions, add visuals. Dev notes land and become `Read more:` links. |
| RC 1 | Link the Field Guide. Get `npm run build:strict` passing (no markers or placeholders left in published text). Fill in the byline and `published` date in `sot.json`. |
| Publish | Make the reader link public if you want. From now on, every change readers can see gets a Changelog line. |
| Final release | Turn off the routine and the Status workflow. Carry the punted list over to the next release's repo. |

## 5. Setup checklist

Do this once per release. Claude can run each step for you and asks before anything that
creates or shares something.

1. **Node 20.3+** and **`gh`** signed in (`gh auth status`).
2. **Create the repo:** run `gh repo create <owner>/wp-X-Y-source-of-truth --private --source . --push`
   from the repo folder.
3. **Sign in to Spacefast:** `npx spacefast login`, then check with `npx spacefast whoami`.
4. **First publish, which creates the site:** `npm run build && npx spacefast publish ./dist --prebuilt --json`.
   Save the space id and live URL in `sot.json`.
5. **Autodeploy:** `npx spacefast git connect --space <space> --provider github --repository <owner>/<repo> --production-branch trunk --sync`.
   Push a small commit and confirm that `npx spacefast versions --space <space>` shows a new
   version.
6. **Share links:** one for readers (`/`) and one for reviewers (`/draft/**`). Open the reader
   link in a private window and confirm it can't reach `/draft/`. The exact commands are in
   `references/publishing.md`.
7. **Status workflow:** it ships in the repo and runs at 11:00 UTC every day. Check it with
   `gh workflow list`, and run it once by hand with `gh workflow run Status`.
8. **Scheduled sweep:** run `/schedule` to create a cloud routine on the repo, daily from Beta 1
   and an hour after the Status workflow. Use the routine prompt in `references/publishing.md`.

If Spacefast's GitHub connection doesn't build correctly, `references/publishing.md` has a
GitHub Actions publish workflow to use instead.

## 6. Reviewing changes

A sweep applies only changes you can check against a link: markers, working notes, hidden or
punted items, dev-note links, and **factual corrections** (a version number, a date,
"proposed" → committed). It logs each one with its source in `notes/sweep-log.md`.

Anything editorial comes to you as a **proposal PR** on a `proposal/<date>-<slug>` branch: new
items, rewritten sentences, priority changes, and the Overview. Spacefast builds a preview of
each branch, so you can read the change rendered before you merge. Merging deploys it.

Questions that need a person (blessed or punted? which tracking issue?) go in
`notes/open-questions.md`, and the draft page lists them at the end.

## 7. Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Trac lookups say `403` | Trac's browser check. The checker falls back to the GitHub mirror automatically. A ticket with no commits or PRs there shows `no-activity`. |
| Status check is slow or reports rate limits | GitHub search allows 30 requests a minute, and the checker waits and retries. Without `gh` signed in or a `GITHUB_TOKEN`, anonymous GitHub allows only 60 requests an hour, which isn't enough. |
| Build warns "working marker in published text" | An emoji marker is in reader-visible text. It's stripped, so readers don't see it, but move it into `flags` or a `<!-- -->` note. Fine while drafting. `build:strict` fails on it. |
| An item doesn't appear under an audience filter | It isn't tagged for that audience. The filter is strict, so add the tag to the item's frontmatter. |
| An item is missing from the page entirely | Check for `published: false` in its frontmatter. The draft page shows hidden items with a label. |
| Site didn't update after a push | Run `npx spacefast versions --space <space>` to see whether a build ran, then check the build log in the Spacefast dashboard. |
