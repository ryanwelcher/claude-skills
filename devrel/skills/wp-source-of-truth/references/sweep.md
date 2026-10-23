# Sweep procedure

A sweep brings one release directory up to date with what has happened since the last sweep. It runs the same
way whether the user asks for it or a scheduled routine starts it. The only difference is the
last step: an interactive sweep reports to the user, and a scheduled one reports in its commit
and PR.

## Steps

### 1. Sync and collect

Run everything from the release directory (for example `~/repositories/source-of-truth/7.2`).

```bash
git checkout trunk && git pull --ff-only
npm install --silent
```

Then bring the mirror up to date with the Doc (`sot.json` → `googleDoc`), because people edit
the Doc between sweeps. Export it and run the importer (`references/google-doc.md`, section 3),
then read the Doc's comments with the Drive connector. `git diff` shows what people changed in
the Doc since the last sweep. Keep those changes: they're the author's, not something to undo.

```bash
npm run status            # writes notes/status.json and prints what changed
```

If the release's `Status X.Y` workflow already ran today, skip `npm run status` and read
`notes/status-report.md` instead. That's the normal case for scheduled sweeps. Running the
script again would compare against the workflow's results, so the "changes" would come back
empty.

If you want to be thorough, run `node scripts/check-status.mjs --all` instead. It also checks
links in notes and proposals, which catches candidates that have since merged.

The script compares the results with the previous `notes/status.json`, so the "Ref changes"
section lists what moved since the last sweep. On the first run, every ref shows as `NEW`. In
that case, use "Open, unmerged PRs" and the milestones to decide.

Also look at the things the script doesn't cover:

- The Make Core posts in `signals.release_posts` since the last sweep date. Read any Beta or RC
  announcement in full: it confirms the Gutenberg version in the package and often lists
  blessed and punted items.
- The new dev notes in the script output. Each one is a `Read more:` link for an item, and
  sometimes a new item.
- The open questions in `notes/open-questions.md` and the open comments in the Doc. Try to
  answer each one with what you collected.
- The Backlog tab. Check each item carried over from the previous release: did it land, or did
  it punt again?

If lookups fail (rate limits, network), say so in the sweep log and don't treat a failed lookup
as a state change.

### 2. Reconcile each item

Work through every item that has a changed ref, a 🔍 flag, or a working note that a new fact
could answer. For each one, decide with the rules in `research.md` ("Deciding whether a PR is in
the release"), then do the matching action:

| Finding | Action (direct) |
|---|---|
| A PR merged after the range is now confirmed in a Beta/RC post or backported | Delete the "confirm it's in Beta N" note. Clear `check` if nothing else needs it. |
| A PR the item depends on is still open after Beta 1, and the feature isn't blessed | Set `published: false` and add a note with the date and the reason. Add an open question if someone has to decide. |
| A Beta/RC post or the tracking issue says the feature moved to the next release | Move the file's content into `notes/punted.md` (title, reason, link) and delete the file. |
| A Trac ticket now has a `Fixes` commit | Update the working note. If the item said "if it lands", clear that caveat from the note. |
| A dev note was published for an item | Add or update its `Read more:` line. |
| A tracking issue was renamed or replaced | Update the link and its text. |
| A working note or open question is answered | Delete the note or question, and record the answer in the sweep log. |
| A fact in a sentence is now wrong (a version number, a date, "proposed" when it's committed, a renamed setting) | Swap the fact in place and cite the source in the sweep log. Keep the rest of the sentence as it is. |
| A working note says "remove if it shipped in X.Y-1", and it did | Remove that clause or sentence. |

Removing or hiding an item changes what readers see, so it also needs a changelog line once the
post is published.

Every candidate in the Notes tab gets its status updated too, merged or not (✅ 🚧 🔍 🙏 🏈). A
new PR or Make post that belongs to the release gets a new Notes entry directly. Notes are the
sweep's to write. Only the Draft is the author's.

These need judgment, so they go in the Notes tab's "Proposed for the draft" section (step 4)
instead of the Draft:

- A merged PR or a dev note that no item covers yet. Draft the new item.
- An item whose description is now wrong, beyond a single fact. For example, the feature
  changed shape before merging, so the paragraph needs rewriting and not a one-word swap. Draft
  the rewrite.
- A change to the priority list or the Overview narrative.

Keep the reconcile step strictly factual. If you notice copy you'd write differently, mention it
in the sweep report, but leave it alone.

### 3. Log, build, commit

Add an entry at the top of `notes/sweep-log.md`:

```markdown
## Sweep: October 27, 2026 (Beta 2)

**Checked:** 194 refs, 3 new Make Core posts, 1 new dev note. Lookups failed for: none.

**Changed in the post:**
* Secrets API: committed in [r63120](…) (Fixes #66187). Cleared the "remove if punted" note.
* Description List: still unmerged after Beta 1 and not blessed. Hidden (`published: false`).

**Resolved questions:** #3 (Secrets API: 7.2, committed Oct 14).

**Proposed for the draft:** new item for `@wordpress/core-actions`; rewrite of the Notes item now that reactions landed.

**Doc:** updated Notes, Punted. Skipped 1 correction with an open comment (Secrets API, see proposals).

**Merged but not added:** [#84856](…) List View nesting (internal).
```

If readers will see the changes and `sot.json` has a `published` date, add a changelog bullet
under today's date in `00-intro.md`.

Apply the same changes to the Doc: the Notes tab (statuses, new entries, proposals, the sweep log
entry), Punted, Backlog, and factual corrections in the Draft. Follow the comment rules in
`references/google-doc.md`, section 5. While the write path isn't set up, write them to
`notes/doc-updates.md` instead (section 4), and say "Doc not updated" in the commit message.

Then run:

```bash
npm run build             # must succeed; read the warnings
git add -A . && git commit -m "Sweep Oct 27: <the two or three biggest changes>"
git pull --rebase         # another release's sweep or Status run may have pushed
git push                  # Spacefast rebuilds and republishes this release from trunk
```

If the sweep found nothing, still add a short log entry ("No changes. Checked 194 refs."), so
the log shows the routine ran. You don't need a changelog line for that.

### 4. Proposals

Add each proposal to the Notes tab under "Proposed for the draft", dated, with the full text of
the new item or rewrite and why it belongs (what merged, milestone, who it affects, sources).
The author moves accepted ones into the Draft. Before you add one, check that section for a
proposal on the same item. If there is one, add the new facts to it instead of adding a
duplicate.

### 5. Report

**Interactive sweep:** tell the user what changed in the Notes and Draft, what you proposed,
which open questions remain, whether the Doc was updated, and the Doc URL from `sot.json`. Keep
it short. The sweep log has the detail.

**Scheduled sweep:** the commit message, sweep log entry and Doc are the report. There's no one
to ask, so don't stop to ask questions. When a decision needs a person, record it as an open
question, and the next interactive session will surface it.
