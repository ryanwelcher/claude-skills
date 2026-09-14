# wp-workshop-scaffold — mode: `audit`

Loaded on demand from `SKILL.md` (and by `reformat` for the checks). The canonical shape and authoring principles live there.

### Step 1 — Determine source

Ask: local path or git URL?

- **Local path**: ask for absolute path; refuse if missing. (Audit does not require a git repo — any directory works.)
- **Git URL**: shallow-clone to a temp dir for read-only inspection.
  1. Create a temp dir: `mktemp -d -t wp-workshop-audit.XXXXXX`
  2. `git clone --depth 1 <url> <tempdir>`
  3. Run the audit against `<tempdir>` (Step 2 below).
  4. **Always** remove the temp dir afterward with `rm -rf <tempdir>` — even if the audit errors. Use a trap or explicit cleanup so it never lingers.

### Step 2 — Run the audit

Run the **Conformance checks** below and print the report in the **Report format** below, without the proposed-changes list. Then stop. No branch, no writes, no confirmation prompts.

## Conformance checks

For each canonical file/dir, check presence and basic shape:

| Path | Check |
|------|-------|
| `plugin.php` / `style.css` / `block.json` | At least one exists; detect target |
| `package.json` | Exists; has `scripts.build` and `scripts.start` |
| `.editorconfig`, `.eslintrc`, `.gitignore` | Exist |
| `blueprint.json` | Exists; has `preferredVersions.wp` |
| `README.md` | Exists; has a "Pre-Workshop Setup" or equivalent heading |
| `facilitator-notes.md` | Exists |
| `slides-outline.md` | Exists |
| `workshop-outline/` | Exists; contains at least one `section-*.md` |
| `code-reference/` | Optional; if absent, note it |
| `code-reference/section-*` chaining | If `code-reference/` exists, snapshots must be numbered consecutively starting at the first coding section (no gaps). Each `code-reference/section-N/` is treated as the starting state of section N+1; flag any gap as misshapen (breaks the build-up chain — see Authoring principles). |
| `assets/`, `includes/`, `src/` | Exist |

## Report format


```
## Audit report

✅ Conforms:
  - <path>
  ...

⚠️  Missing:
  - <path> — <why it matters / what will be added>
  ...

🛠 Misshapen:
  - <path> — <what's off / proposed fix>
  ...

Proposed changes (will only apply after you say "go"):
  - CREATE  workshop-outline/section-1.md
  - CREATE  facilitator-notes.md
  - ...
```
