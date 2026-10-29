# Source of Truth scan skill: design

Date: 2026-10-29. Status: draft for Ryan's approval.

## Intent

Every WordPress release has a Source of Truth (SoT) Google Doc. Its Notes tab collects everything
happening in the release, and the author moves what matters from Notes into the Draft. Gathering
those notes by hand is the busy work: re-checking every linked Trac ticket, GitHub issue and dev
note, and hunting for things nobody has added yet.

This skill does that gathering and leaves the results in the Doc, where the author and the people
commenting on the Doc already look. It only reports. A person decides what goes into the Draft.

This is the "tracking and notes" skill that `docs/superpowers/specs/2026-10-29-sot-site-design.md`
calls the second skill. Site generation is a separate skill (`wp-sot-site`), being built in
another session.

## Goals

1. **Check what's linked.** Every Trac ticket, GitHub issue or PR, and dev note linked anywhere
   in the Doc is re-checked, and anything that changed since the last run is reported: merged,
   closed, reopened, punted, milestone moved, dev note published.
2. **Find what's missing.** Search the release's usual sources for candidates that aren't in the
   Doc yet, and report them.
3. **Produce one dated block per run** for the bottom of a named tab in the Doc, Notes by
   default, ready for the editor to paste.
4. **Run by hand, weekly, on the editor's computer.** Justin runs it in Claude Code.
5. **Remove the sweep job from `wp-source-of-truth`.** It edits Notes entries in place and writes
   "Sweep log" and "Proposed for the draft" sections, which Ryan doesn't want anymore. Remove
   that job and its scheduled-sweep instructions, and point sweep and refresh requests to
   `wp-sot-scan`. The site session is also changing `wp-source-of-truth`, so make this a small,
   separate commit and pull first.

## Non-goals

- Running unattended in the cloud. That's a later phase (see "Later: running in the cloud").
- Editing the Draft, or writing a draft from the notes.
- Updating, moving or deleting anything already in the Doc, including earlier scan blocks.
- Maintaining the Punted and Backlog tabs.
- Building or publishing the site.
- Resolving, editing or answering comments.
- Changing the existing `wp-source-of-truth` skill beyond removing its sweep job.

## Anti-goals (a failure even if it works)

- **A comment is lost.** Nothing already in the Doc is ever touched, so nothing anyone commented
  on can disappear.
- **Someone can't tell what the robot wrote.** All automated output lives inside clearly headed,
  dated blocks. Nothing automated appears anywhere else in the Doc.
- **A finding without a source.** Every finding has a link a person can click to check it.
- **A candidate silently drops off.** A new candidate keeps appearing in every block until it's
  in the Doc or struck out.

## Decisions Ryan made

- **Manual first, on the editor's computer.** Justin runs it each week in Claude Code. This
  removes the hard parts of a cloud run (Doc write access, Trac's bot check, network settings)
  while the format gets refined. Cloud comes later.
- **One block per run, at the bottom of the tab**, for now. Where blocks go may change once the
  team has lived with it.
- **The tab is an input**, defaulting to Notes. A separate tab (for example "Scan results") must
  work the same way.
- **Append only.** Older blocks stay in place so their comments survive. The run doesn't change
  existing notes, because someone opening the Doc couldn't tell what was changed.
- **A finding is what changed plus a link to the source.**
- **Both passes every run:** re-check linked items and find new ones.
- **Repeat new candidates** in every block until they're in the Doc or struck out.
- **Saying no is a strikethrough.** To reject a candidate, a person strikes it out in the block
  it appeared in. A struck-out candidate never appears in a later block.
- **Candidates must meet the "what makes an item" bar** in
  `wp-source-of-truth/references/research.md`. Claude filters, rather than listing every merged
  PR in the range. Each block says how much it checked (for example "312 PRs checked, 14
  candidates") so readers can see what was filtered.
- **Weekly runs** for now.
- **One skill.** No second skill for writing to the Doc.

## How a run works

Justin asks Claude Code for a scan ("run the SoT scan for 7.2", optionally naming a tab).

1. **Pick the release.** The one named, or the only one still in progress. Ask if there's more
   than one. The Doc ID comes from the release's config in the repo. The repo is being
   restructured by the site skill (`releases/<version>/release.json`), so read the Doc ID from
   wherever that work puts it. `git pull` first.
2. **Read the Doc** with the Markdown export
   (`https://docs.google.com/document/d/<ID>/export?format=md`), the same way the site skill
   does. If it returns a sign-in page, stop and say so. Check the target tab exists (the export
   shows tab names). If it doesn't, stop before scanning and say so, which catches a typo right
   away.
3. **Pass 1, linked items.** Pull every Trac, GitHub and dev-note link out of the Doc (every tab,
   outside the scan blocks), look up each one's current state, and compare with the state saved
   by the previous run. Report only what changed.
4. **Pass 2, new candidates.** Search the sources in `wp-source-of-truth/references/research.md`
   (Make Core release and dev-note tags, Gutenberg releases in the release's range, iteration
   issues, the Gutenberg pin commits, wordpress-develop commits for the milestone, and new Trac
   tickets on the milestone). A candidate is "in the Doc" when its PR, issue or ticket number
   appears anywhere in the Doc **outside the scan blocks**. A candidate struck out in any
   earlier block is skipped. Only candidates that meet the "what makes an item" bar are listed.
5. **Save the record.** Write the block as Markdown and the state this run saw to the repo,
   commit and push to `trunk`. That gives a history of every scan and the baseline for next
   week's comparison.
6. **Hand over the block.** Put the block on the clipboard as formatted text (a real heading,
   bullet list, clickable links), open the Doc at the target tab in Chrome, and tell Justin to
   click at the very bottom of the tab and paste. Also print the block in the session, in case
   the clipboard step fails.

### Trac

Trac's "Checking your browser" page blocks scripted requests: ticket pages, ticket and report
CSV/RSS exports, milestone pages and queries all return 403 (checked Oct 29, 2026). Running on
Justin's computer gets around this the legitimate way: Claude in Chrome opens Trac in Justin's
own browser, at human pace, with a couple of page loads a week.

- **Milestone query in Chrome:** one query for the release milestone
  (`query?milestone=7.2&format=csv&col=id&col=summary&col=status&col=milestone&col=keywords`)
  and one for every linked ticket (`query?id=66187,66208,…&format=csv&col=id&col=status&col=milestone`).
  This gives milestone values (so punts show as "moved to 7.3"), status, keywords, and new
  tickets on the milestone.
- **Timeline RSS as a fallback.** The timeline feed isn't blocked:
  `https://core.trac.wordpress.org/timeline?format=rss&ticket=on&ticket_details=on&changeset=on&from=MM/DD/YY&daysback=1&max=5000`,
  one day per request (a busy day is about 400 events, and one request caps at 2000). It shows
  created, closed (with resolution), reopened, changesets, and *that* a milestone, status,
  owner or keyword changed, but not the old or new values. If Chrome isn't connected, use this
  plus GitHub (wordpress-develop commits and PRs that reference a ticket), and say in the block
  that milestone values weren't checked.
- Don't get around the browser check with a headless browser or a spoofed User-Agent.

### The block

```
Automated scan results: October 29, 2026
Checked 26 linked tickets and PRs, 312 Gutenberg PRs, 9 Make Core posts.

Changes to linked items
- Reopened: #66187 Secrets API. https://core.trac.wordpress.org/ticket/66187
- Moved to 7.3: #61234 Font Library uploads. https://core.trac.wordpress.org/ticket/61234
- Dev note published: Block Bindings updates. https://make.wordpress.org/core/...

New candidates (not in the Doc yet)
- Gutenberg 24.2: new Accordion block attributes. https://github.com/WordPress/gutenberg/pull/81500

End of automated scan results: October 29, 2026
```

The wording above is illustrative. The fixed parts: a heading with the date, a line saying what
was checked, the two groups, one line per finding, a clickable link on every line, and a footer
line. If a group is empty, say so in one line ("No changes to linked items"), so readers can see
the run happened.

## Claude's calls (Ryan can overrule any of these)

1. **Skill name:** `wp-sot-scan`, in `claude-skills/wp-sot/skills/`, next to `wp-sot-site`.
2. **Reuse, don't edit, `wp-source-of-truth`.** Its research guide and status checker
   (`check-status.mjs`) are the starting point. The status checker reads the repo's Markdown, not
   the Doc, so it needs adapting or a sibling script that reads the Doc export.
3. **Paste, don't type.** Claude in Chrome could type the block into the Doc, but typing into
   Google Docs that way is fragile. The editor pastes, which takes seconds and keeps a person
   in control of the only write.
4. **Where block files and saved state live** in the repo is the builder's choice, as long as it
   sits with the release's notes (not in the content the site skill reads) and survives the site
   skill's restructure.
5. **Scan blocks don't count as "in the Doc" for either pass.** Pass 1 only checks links a
   person put in the Doc. Otherwise a candidate becomes a "linked item" after its first
   appearance. The skill still reads earlier blocks, but only to find struck-out candidates.
6. **Every block ends with a footer line**, so the skill can tell exactly where a block stops in
   the Markdown export. Anything a person writes below a footer counts as part of the Doc.
7. **Strikethrough must survive the Markdown export** (as `~~text~~`). Check on the first real
   run. If the export drops it, read the Doc through Chrome or the Drive connector instead.
8. **No em-dashes in the block,** matching Ryan's writing rules.

## Constraints

- Justin's machine needs: Claude Code with the `wp-sot` plugin from `claude-skills`, `gh` signed
  in with push access to `wptrainingteam/source-of-truth`, Node, and the Claude in Chrome
  extension.
- The clipboard step assumes macOS. Confirm Justin's OS before building it.
- The Doc must stay shared as "anyone with the link can comment", for the export to work.

## Left to the builder

- Exact file names and paths for blocks, state and scripts.
- How "changed since last run" is stored and compared.
- How the block becomes formatted clipboard content.

## Later: running in the cloud

Not part of this work. Recorded so the design holds up when it's time:

- A weekly Claude Code cloud routine runs the same skill. Its environment needs network access
  to `core.trac.wordpress.org`, `make.wordpress.org` and `docs.google.com` added.
- Writing to the Doc: a standalone Apps Script under Ryan's Google account appends new blocks
  from the repo to the target tab on an hourly trigger. Needs the repo public (it's internal
  today), and may hit Automattic Workspace limits on Apps Script.
- Trac: a cloud run has no browser, so it needs approved access from the Systems team. A draft
  request for two read-only query CSVs a week is ready.

## Follow-ups (not in this work)

- Revisit block placement (bottom of Notes, or a separate tab) after a few weeks of real use.
