# wp-source-of-truth evals

Three cases in the `claude plugin eval` layout. Each one has `prompt.md`, `case.yaml`, one
assertion per file in `graders/`, and its input in `files/`:

| Case | Checks |
|---|---|
| `import-gdoc-draft` | Turns the 7.2 Google Doc export (`files/sot-72-draft.md`) into a `7.2/` release directory that builds, in an empty clone of the shared repo |
| `sweep-after-beta1` | Sweeps the imported `7.2/` release after Beta 1, against live GitHub and the wordpress-develop mirror |
| `add-missed-item` | Adds the Video block GIF-variation removal (#82696) in house style |

`place-files.sh` copies the inputs into the run directory. The import case gets an empty
`source-of-truth` git repo. For the other two it recreates the imported state as one git commit,
because the snapshot is stored without `.git`.

The sweep case uses live data, so the expected facts (Secrets API and embeddings committed,
Description List unmerged) describe the state on October 22, 2026. Later runs will see later
facts.

Iteration 1 (October 22, 2026, one run per configuration, before the move to one shared repo
with a directory per release on October 23; the inputs and prompts have changed since):

| Case | With skill | Without skill |
|---|---|---|
| import-gdoc-draft | 8/8, 79s | 5/8, 287s |
| sweep-after-beta1 | 7/7, 1105s | 6/7, 703s |
| add-missed-item | 5/5, 77s | 5/5, 56s |

The baseline for the sweep and add cases still had the repo's own `CLAUDE.md` and scripts,
because they're part of the input, so only the import case is a clean comparison.

The `files/` folders aren't in git, because they hold an unpublished Source of Truth draft. To
run the cases on another machine, recreate them first:
- `import-gdoc-draft/files/sot-72-draft.md`: a Markdown export of the draft Google Doc.
- The other two cases: a snapshot of `wptrainingteam/source-of-truth` with the 7.2 import
  (`git archive trunk` into `files/source-of-truth/`).
