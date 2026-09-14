# Contributing / editing these skills

This repo (`ryanwelcher/claude-skills`) is the **source of truth** for Ryan's Claude Code
skills. It's published as a plugin marketplace with two plugins: `public` and
`devrel`.

## ⚠️ The one rule: edit the clone, not the cache

When you install these skills as a plugin, Claude Code keeps a **runtime copy** in the plugin
cache:

```
~/.claude/plugins/cache/ryan-claude-skills/<plugin>/<version>/…
```

That cache copy is **not** this git repo. It has no git history, and it is **overwritten on
`/plugin update`**. Skills read from — and sometimes *write to* — that cache copy at runtime
(for example, a script skill appending a dated rule to a voice card's "Refinement log"). Any
edit that lands in the cache lives only there and is **one `/plugin update` away from being
gone forever.**

So:

- ✅ **Make every change in this clone** (`~/repositories/claude-skills`), commit, and push.
- ❌ **Never hand-edit files under `~/.claude/plugins/cache/…`** and expect them to survive.
- After merging, run **`/plugin update`** (or `/plugin marketplace update ryan-claude-skills`)
  so the cache picks up your committed changes.

There is **no automatic sync** from the cache back to this repo. If Claude edits a cached file
during a session, that change is **not** in git until you deliberately port it here and commit.

## Recommended: develop in-place (no cache, no drift)

Marketplace installs — even from a local path — get **copied into the cache**, which is what
causes drift. The fix is to load the plugin **in place** from this clone using a *skills-directory
plugin*, so every edit lands directly in version control and there is no cache copy to diverge.

Symlink the plugin folder (which already has a `.claude-plugin/plugin.json`) into your skills
directory:

```
ln -s ~/repositories/claude-skills/devrel ~/.claude/skills/devrel
```

On the next session it loads as **`devrel@skills-dir`**, discovered in place — **not** copied to
the cache. Now edits to `~/repositories/claude-skills/devrel/…` are live immediately (no
`/plugin update` needed) and already sitting in git; you just commit and push when ready.

To avoid running two copies of the same skills, **disable/uninstall the marketplace-installed
`devrel`** on this machine (`/plugin` → manage) once the `@skills-dir` version is loading. Keep
the GitHub marketplace for **distribution** and **other machines** — this in-place setup is for
the machine where you actually author.

> Optional safety net: a `SessionStart` hook that diffs the cache against this repo and warns on
> drift. Useful if you keep the marketplace install around instead of going in-place.

## Normal workflow (if you keep the marketplace install)

```
cd ~/repositories/claude-skills
git checkout -b my-change
# …edit skills / references…
git add -A && git commit -m "…"
git push -u origin my-change      # open a PR, or push to trunk for your own repo
# after merge:
# /plugin update   (inside Claude Code) to refresh the runtime cache
```

## Adding a new skill

1. Create `./<plugin>/skills/<skill-name>/SKILL.md` (front-matter `name` + `description`).
2. Register it in **both** manifests:
   - `./<plugin>/.claude-plugin/plugin.json` → `skills` array
   - `./.claude-plugin/marketplace.json` → the plugin's `skills` array
3. Bump that plugin's `version` in both files (they must match).

## Checking for drift

If you suspect the cache and this repo have diverged (e.g. rules got edited in the cache during
a session), diff them:

```
diff -rq ~/repositories/claude-skills/devrel/skills \
        ~/.claude/plugins/cache/ryan-claude-skills/devrel/*/skills
```

Anything that only exists in the cache side needs to be copied here and committed before the
next `/plugin update`.
