# The Google Doc

The Google Doc is the working draft for the whole release cycle, and the copy people read and
comment on. The repo doesn't replace it. The repo runs the status checks, keeps a Markdown mirror
of the Doc, and later builds the Spacefast site. When the Doc and the repo disagree, the Doc wins.

Record the Doc in `sot.json` under `googleDoc` (`id`, `url`). If it's empty, ask the user for
the Doc in an interactive session. A scheduled run adds an open question and works on the repo
mirror alone. The link must stay "anyone with the
link can comment". The SoT exists so that news organizations and the Make teams get the facts
right, so the draft is never private.

## Contents

1. Tabs
2. Notes tab format
3. Reading the Doc
4. Writing to the Doc
5. Keeping comments safe
6. Release timeline

## 1. Tabs

| Tab | Holds | Who writes it |
|---|---|---|
| **Draft** | The post itself, in the layout of `content-format.md` | The author. A sweep makes factual corrections only (section 5). Claude writes a first draft only when asked. |
| **Notes** | Everything happening in the release, merged or not, each entry with its emoji status and links. It's usually longer than the Draft. | Sweeps. This is the main job. |
| **Punted** | Items punted from **this** release, with the reason and a link, so the next release knows to check them | Sweeps, when a punt is confirmed |
| **Backlog** | Items punted from the **previous** release. Copy it from the previous release's Punted tab when the release starts, and check each item during research. | Start of release, then sweeps as items land or punt again |

Gathering the notes is most of the work, so it comes first. Writing the Draft from the notes
comes second, and only after a person has spot-checked the notes. Claude sometimes says a
feature is going in when it isn't.

## 2. Notes tab format

Start the tab with the emoji key, then the release basics, then one entry per candidate grouped
under the same section headings as the post:

```
Emoji key: ✏️ to be edited · 🙏 blessed (developed during Beta) · 🔍 to-do or double-check · 🎨 visuals · 🏈 punted · ✅ merged/committed · 🚧 in progress

Release basics: Beta 1 …, Beta 2 …, RC 1 …, Final …. Gutenberg range: 24.0 – 24.3 (🔍 until the Beta 1 pin).

## Proposed for the draft
(dated proposals from sweeps: new items and rewrites, waiting for the author)

## Sweep log
(newest first, same format as references/sweep.md)

## Editor enhancements
### Notes in the canvas margin ✅
Merged in #81234 (Gutenberg 24.1). Dev note: <link>. Tags: end user, site admin.
```

The Notes tab covers everything, including open PRs and early ideas, because it tracks the
whole release. The rule in the ground rules, that only merged, committed or blessed work goes
into the post, applies to the **Draft** tab.

Proposals live in the Notes tab under "Proposed for the draft", not in proposal PRs, because the
Draft is edited in the Doc. The author moves an accepted proposal into the Draft. Delete a
proposal once it's in the Draft or the author rejects it.

## 3. Reading the Doc

- **Content and comments:** the Google Drive connector's `read_file_content` with
  `includeComments: true`. Read comments every time: an open comment on an item is often the
  answer to an open question, or a sign not to touch that text.
- **Markdown export for the repo mirror:**
  `curl -sL -o draft.md "https://docs.google.com/document/d/<DOC_ID>/export?format=md"`, then
  `node <skill-dir>/scripts/import-gdoc.mjs draft.md <release-dir>`. The importer expects the
  tabs as H1 blocks (Draft, then `# **Notes**`, Punted, Backlog). Check on the first run that the
  export includes every tab. If it only has the first one, report that before you trust the
  mirror.

## 4. Writing to the Doc

> **Not set up yet.** The Google Drive connector can read a Doc but can't edit its contents.
> Its `update_file` only changes metadata. `create_file` makes a new file, which drops every
> comment, so never use it to "update" the Doc.

The write path this skill expects is the Google Docs API, `documents.batchUpdate`, with each
request's `location` or `range` carrying the tab's `tabId` (get the IDs with `documents.get`
and `includeTabsContent=true`). A scheduled sweep runs in the cloud with no one at the keyboard,
so it needs credentials there: a service account the Doc is shared with as an editor, and its
key available to the routine. None of this exists yet.

Until it does, every job that would write to the Doc does this instead:

1. Make the change in the repo mirror as usual, so the status checks and sweep log stay right.
2. Write the Doc changes, grouped by tab, to `notes/doc-updates.md` under today's date, newest
   first, ready to paste: the exact text to add, and for an edit the old text and the new text.
3. Tell the user the Doc wasn't updated and point them to `notes/doc-updates.md`. A scheduled
   run says so in its commit message.

## 5. Keeping comments safe

Losing comments is the one failure people won't forgive, so every write follows these rules:

- Insert and append. Never clear a tab and rewrite it, and never replace a whole entry when a
  few words changed.
- Make a factual correction (the same test as in `SKILL.md`) with a replace on just the changed
  words.
- If the text you'd change has an open comment on it, don't change it. Add the new fact as a
  proposal in the Notes tab, and mention the comment in the report.
- Don't resolve, edit or delete comments. Answer a comment's question in the sweep log, and let
  the person who asked resolve it.

## 6. Release timeline

| When | The Doc |
|---|---|
| Cycle start | Create the Doc with the four tabs. Copy the previous release's Punted tab into Backlog. Sweeps start filling Notes. |
| Beta 1 | First draft done. The Doc goes to people who work in Core and to news organizations, who know it's still in progress. |
| About Beta 3 | The SoT is shared publicly on Gutenberg Times. |
| RC 1 | The SoT is done. The Developer Field Guide goes live, so link it. |
| Final release | Gutenberg Times has the text version. The Spacefast site goes public as the interactive version, linked from the top of the Gutenberg Times post (see `publishing.md`). |

Take the dates from the release's Make Core schedule and record them in `sot.json` →
`milestones`.
