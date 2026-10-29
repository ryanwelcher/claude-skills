---
name: wp-sot-scan
description: |
  Weekly scan for a WordPress release's Source of Truth (SoT) Google Doc. Re-checks every Trac
  ticket, GitHub PR or issue and dev note linked in the Doc, finds new candidates that aren't in
  the Doc yet, and hands over one dated "Automated scan results" block to paste at the bottom of
  the Notes tab (or another named tab). Never edits the Doc itself. Use for "run the SoT scan",
  "scan the 7.x Source of Truth", "sweep", "refresh the notes", "update the notes tab", "what
  changed for 7.x this week". Not for building the site (wp-sot-site) or writing the draft
  (wp-source-of-truth).
---

# Source of Truth scan

Each release's SoT Google Doc has a Notes tab where everything happening in the release is
collected. The author moves what matters from Notes into the Draft. This skill does the weekly
gathering: it checks what the Doc links to, looks for what it's missing, and produces one block
of findings for the editor to paste at the bottom of a tab. Every finding is one line: what
changed, plus a link to the source.

The rules that matter most:

- **Never write to the Doc.** The only change to the Doc is the editor pasting the block. Never
  type into the Doc with Chrome, and never use the Drive connector's `create_file` or
  `update_file` on it.
- **Append only.** Earlier blocks and everything people wrote stay as they are, so no comment is
  ever lost.
- **Every finding has a source link.** If you can't link it, leave it out.
- **Trac only through Justin's Chrome or the timeline feed.** Trac blocks scripts with a browser
  check. Never use a headless browser or a fake User-Agent to get past it.
- **No em-dashes** in anything that goes into the block.

People say no to a candidate by striking it out in the block where it appeared. A struck-out
candidate never comes back. A candidate that isn't struck out keeps appearing in every block
until someone adds it to the Doc.

## Run a scan

Ask which release if the user didn't say and more than one is in progress. The tab defaults to
Notes. Use another tab only when the user names one. Put working files in the session's
scratchpad (written as `$SCRATCH` below).

1. **Find the clone and the release.** The current directory or one of its parents, then
   `~/repositories/source-of-truth` (clone `wptrainingteam/source-of-truth` there if it's
   missing). Run `git pull`. The release directory is `<clone>/<version>/` (for example `7.2/`).
   Create it with an empty `notes/` folder if it doesn't exist.

2. **Get the Doc ID.** `releases/<version>/release.json` → `source.id` when `source.type` is
   `gdoc`. Otherwise `<version>/sot.json` → `googleDoc.id`. Otherwise ask the user for the Doc
   link.

3. **Export the Doc.**
   `curl -sL -o "$SCRATCH/doc.md" "https://docs.google.com/document/d/<DOC_ID>/export?format=md"`

4. **Get the Trac query CSVs through Chrome.** Load the Chrome tools in one ToolSearch call
   (`tabs_context_mcp`, `tabs_create_mcp`, `navigate`, `javascript_tool`, `get_page_text`). Get
   the linked ticket numbers with
   `node <skill-dir>/scripts/prepare.mjs --doc "$SCRATCH/doc.md" --list-trac`.
   Open a new tab at `https://core.trac.wordpress.org/`, wait until the page shows Trac (not
   "Checking your browser"), then run this in the page with `javascript_tool`, once per query,
   and save each result:

   ```js
   await ( await fetch( '/query?milestone=<version>&format=csv&col=id&col=summary&col=status&col=resolution&col=milestone&col=keywords&max=1000' ) ).text()
   ```
   ```js
   await ( await fetch( '/query?id=<comma-separated ids>&format=csv&col=id&col=summary&col=status&col=resolution&col=milestone&col=keywords&max=1000' ) ).text()
   ```

   Save them as `$SCRATCH/trac-milestone.csv` and `$SCRATCH/trac-linked.csv`. Each must start
   with `id,summary`. If one starts with `<`, it's a challenge page: wait and try once more.
   If Chrome isn't connected or a fetch still fails, carry on without the CSVs. The block will
   say that milestone values weren't checked, and the timeline feed still covers closes,
   reopens and "milestone changed".

5. **Pass 1.**
   ```
   node <skill-dir>/scripts/prepare.mjs --release-dir <clone>/<version> --doc "$SCRATCH/doc.md" \
     --tab Notes --trac-linked "$SCRATCH/trac-linked.csv" --trac-milestone "$SCRATCH/trac-milestone.csv" \
     --out "$SCRATCH/work.json"
   ```
   Leave out both `--trac-*` flags if step 4 failed. Exit code 2 means the export is a sign-in
   page or the tab doesn't exist. Tell the user what it printed and stop. Pass 1 takes a minute
   or two, because GitHub search is rate limited.

6. **Pass 2: find new candidates.** Follow
   `../wp-source-of-truth/references/research.md` for sources and for what's in the release:
   Make Core posts tagged for the release and its dev notes, Gutenberg releases in the range,
   iteration issues, the Gutenberg pin commits, wordpress-develop commits for the milestone. Also
   go through `newTickets` in `work.json` (tickets on the milestone that are new since last week).

   List only what meets research.md's "What makes an item" bar, and only with a source link.
   Skip anything whose key is in `docKeys` or `struckKeys` (finish.mjs drops those anyway). Trust
   merged code over PR descriptions. Write `$SCRATCH/candidates.json`:

   ```json
   {
     "checked": "312 Gutenberg PRs, 9 Make Core posts, 14 new milestone tickets",
     "items": [
       { "group": "candidates", "text": "Gutenberg 24.2: Accordion block attributes.", "url": "https://github.com/WordPress/gutenberg/pull/81500" },
       { "group": "changes", "text": "Dev note published: Block Bindings updates.", "url": "https://make.wordpress.org/core/..." }
     ]
   }
   ```

   `checked` says what you went through, so readers can see what was filtered. A dev note about
   something already in the Doc goes in group `changes` as "Dev note published: <title>."
   Everything else is a `candidates` item. Write each `text` as one short sentence ending with a
   period, with no em-dashes and no link (finish.mjs adds the link).

7. **Finish.**
   ```
   node <skill-dir>/scripts/finish.mjs --release-dir <clone>/<version> --work "$SCRATCH/work.json" --candidates "$SCRATCH/candidates.json"
   ```
   It writes `notes/scans/<date>.md` and `notes/scan-state.json`, copies the block to the
   clipboard (with links), and prints it.

8. **Hand it over.** In Chrome, open the Doc at the target tab
   (`https://docs.google.com/document/d/<DOC_ID>/edit`, then pick the tab). Tell the user:
   "The block is on your clipboard. Click at the very bottom of the <tab> tab and paste." Show
   the printed block too, in case the clipboard step failed.

9. **Commit the record.** In the content repo, commit only `<version>/notes/scans/` and
   `<version>/notes/scan-state.json`, with a message like
   `Scan Oct 29: 3 changes, 5 new candidates`. No AI co-author or "generated with" lines. Push to
   `trunk`. Never touch `releases/`, `layouts/`, `scripts/` or `test/`. Those belong to
   wp-sot-site.

## If something goes wrong

- **A finding looks wrong.** Fix it in `candidates.json` (Pass 2), or tell the user which Pass 1
  line is suspect. Don't edit the saved block after it's committed. Next week's block corrects
  it.
- **A block came out but wasn't pasted.** Re-run step 8 from `notes/scans/<date>.md`. Don't
  re-run the scan, or the comparison baseline moves.
- **The user wants to re-run today's scan.** Use `git checkout` to restore
  `notes/scan-state.json` to its state before today's commit, then run again.
