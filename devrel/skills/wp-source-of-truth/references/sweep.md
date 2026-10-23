# Sweep procedure

A sweep brings the repo up to date with what has happened since the last sweep. It runs the same
way whether the user asks for it or a scheduled routine starts it. The only difference is the
last step: an interactive sweep reports to the user, and a scheduled one reports in its commit
and PR.

## Steps

### 1. Sync and collect

```bash
git checkout trunk && git pull --ff-only
npm install --silent
npm run status            # writes notes/status.json and prints what changed
```

If the repo's Status workflow already ran today, skip `npm run status` and read
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
- The open questions in `notes/open-questions.md`. Try to answer each one with what you
  collected.

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

These need judgment, so they go in a proposal PR (step 4) instead of `trunk`:

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

**Proposed (PR #12):** new item for `@wordpress/core-actions`; rewrite of the Notes item now that reactions landed.

**Merged but not added:** [#84856](…) List View nesting (internal).
```

If readers will see the changes and `sot.json` has a `published` date, add a changelog bullet
under today's date in `00-intro.md`.

Then run:

```bash
npm run build             # must succeed; read the warnings
git add -A && git commit -m "Sweep Oct 27: <the two or three biggest changes>"
git push                  # Spacefast rebuilds and republishes from trunk
```

If the sweep found nothing, still add a short log entry ("No changes. Checked 194 refs."), so
the log shows the routine ran. You don't need a changelog line for that.

### 4. Proposals

Put each proposal on its own branch from the updated `trunk`, so the user can merge them one at
a time:

```bash
git checkout -b proposal/2026-10-27-core-actions
# write or edit the item file(s)
npm run build
git commit -am "Propose: Core actions registered on the server"
git push -u origin HEAD
gh pr create --title "Propose: Core actions registered on the server" --body "<why it belongs: what merged, milestone, who it affects, sources>"
git checkout trunk
```

Before you open a PR, check `gh pr list` for an open proposal that covers the same item. If one
exists, add a comment there with the new facts instead of opening a duplicate.

### 5. Report

**Interactive sweep:** tell the user what changed in the post, what you proposed (with PR links),
which open questions remain, and the live URL from `sot.json`. Keep it short. The sweep log has
the detail.

**Scheduled sweep:** the commit message, sweep log entry and PRs are the report. There's no one
to ask, so don't stop to ask questions. When a decision needs a person, record it as an open
question, and the next interactive session will surface it.
