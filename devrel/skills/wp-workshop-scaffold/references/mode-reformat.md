# wp-workshop-scaffold — mode: `reformat`

Loaded on demand from `SKILL.md`. The canonical shape and authoring principles live there.

### Step 1 — Determine source

Ask: local path or git URL?

- **Local path**: ask for absolute path; refuse if missing or not a git repo.
- **Git URL**: ask for URL; default clone destination is `<cwd>/<repo-name>` (derive repo name from URL basename minus `.git`); confirm with user before cloning; refuse if destination exists; run `git clone <url> <dest>`.

`cd` into the source directory (use absolute paths in tool calls — don't actually `cd`).

### Step 2 — Refuse if dirty

Run `git status --porcelain`. If non-empty, stop and tell the user to commit/stash first. **Never** discard their changes.

### Step 3 — Audit

Read `mode-audit.md` next to this file. Run its **Conformance checks** and build the report in its **Report format**, including the proposed changes.

Stop and wait for explicit "go" / "yes" / "proceed".

### Step 4 — Branch + apply

On approval:
1. Ask for branch name via `AskUserQuestion` — recommended option labeled `planning` (the first option, marked Recommended). Allow "Other" for custom.
2. If `git rev-parse --verify <branch>` succeeds → branch already exists. Stop and ask the user to pick a different name. Never delete or force.
3. `git checkout -b <branch>`
4. Apply only the **proposed changes** from the report. Never overwrite an existing file unless the user explicitly confirmed it in the report step.
5. Run `git status` and `git diff <original-branch>...<branch> --stat`. Print the diff summary.
6. Remind: nothing has been pushed. Original branch is untouched.
