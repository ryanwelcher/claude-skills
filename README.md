# Ryan's Claude Code Skills

A personal [Claude Code](https://claude.com/claude-code) plugin marketplace for syncing
skills across machines. This repo is the source of truth.

How Claude loads the skills depends on the machine:
- **Other machines** install the plugins from the marketplace, and Claude runs them from its
  own **cache** (it does *not* read this repo directly there — `/plugin update` refreshes it).
- **The authoring machine** loads them **in place** from a local clone (see
  [Authoring in place](#authoring-in-place-no-cache-no-drift) below), so edits are live and
  version-controlled with no cache and no drift.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full rationale (skills read from the cache at
runtime, and cache edits are lost on `/plugin update` — so never hand-edit the cache).

## Plugins

| Plugin | Version | Visibility | Skills |
|---|---|---|---|
| `public` | 1.0.0 | Safe to share with anyone | _(empty — placeholder for future shareable skills)_ |
| `devrel` | 1.22.0 | Personal developer-advocacy work | `wp-workshop-scaffold`, `youtube-script`, `write-article`, `write-social-post`, `youtube-stream-description`, `analyze-stream-recording`, `done`, `wnd-script`, `sounds-like-me`, `ste-pass`, `ste-audit` |

### `public` skills

_None yet — placeholder for future shareable skills._

### `devrel` skills

| Skill | What it does |
|---|---|
| `wp-workshop-scaffold` | Scaffold a new WordPress workshop repo (or reformat / audit an existing one) to the canonical WCPT-style structure with a north-star artifact arc. |
| `youtube-script` | Write or audit/rework a YouTube video script in Ryan's voice (conversational, dev-to-dev, not AI-sounding). |
| `write-article` | Write long-form articles, blog posts, or P2 updates in Ryan's voice. |
| `write-social-post` | Draft promotional LinkedIn / X / Facebook posts with the WP-DevRel persona, platform-specific formatting, and hashtags. |
| `youtube-stream-description` | Draft the YouTube description text for `@ryanwelchercodes` live streams using the standard template (hook, Stream Together blurb, Connect/Projects, hashtags). Accepts a topic, a published URL, or a local recording path. |
| `analyze-stream-recording` | Internal forked helper for `youtube-stream-description`: transcribes a local recording on-device and returns only a recap, a YouTube-valid chapter list, and any links mentioned. Not user-invocable. |
| `done` | Save a structured recap of the current Claude Code session (Summary / Key Decisions / Files Changed / Open Questions / Follow-ups) to the DevRel Obsidian vault. Triggers on phrases like "save the output", "save this conversation", "log this session". |
| `wnd-script` | Write the script for an episode of the monthly *What's New for Developers* (WND) video series — a talking-head walkthrough of that month's Developer Blog post, in Ryan's voice. |
| `sounds-like-me` | Audit an existing script/teleprompter/draft for Ryan's voice: check every line against the style card (+ series cards), surface findings for approval, then fix in place and log new rules to the right refinement log. |
| `ste-pass` | Audit/rewrite existing tutorials, recipes, and workshop steps against Simplified Technical English (STE). Hybrid by default: STE in action zones, Ryan's voice everywhere else. Owns `references/ste-card.md`, which `write-article`, `wp-workshop-scaffold`, and `sounds-like-me` read live. |
| `ste-audit` | Internal forked helper for `ste-pass`, pinned to Sonnet: maps zones, runs `ste-lint.py`, and returns findings with full rewrites. Not user-invocable. |

## Context patterns

How to keep a skill's token cost down. Worked example: `youtube-stream-description` (see
[the 1.19.0 change](https://github.com/ryanwelcher/claude-skills/compare/aaea534...main)).

Ask these four questions about every step in a skill, in order:

1. **Is the output read once and mostly noise?** Trim it at the source. Print only the fields
   the model uses (`--print` templates), cut boilerplate with `awk`, silence progress and
   warnings (`--quiet`, `--no-warnings`, `-loglevel error`), and end with one line that says
   what was cut so the model doesn't go looking for it. This is always the first and cheapest
   fix. Example: `fetch-recent.sh` drops everything from `Connect:` onward, since
   `TEMPLATE.md` already has it. Roughly 2–4k tokens down to a few hundred.

2. **Is the output large but the parent only needs a derived result?** Move that step into a
   second skill with `context: fork` and give it a hard allow-list of return sections. Have
   its scripts print a *pointer* (a file path plus line/word counts), never the payload, so
   even the fork's own tool results stay small; the fork reads the file in chunks. Set
   `background: false` when the parent needs the answer before continuing, and
   `user-invocable: false` so it stays out of the `/` menu. Example:
   `analyze-stream-recording` turns a 15–25k-token transcript into a recap, a chapter list,
   and a link list of a few hundred tokens. The transcript never enters the main context.

3. **Does the fork need a different model, tools, or permissions?** Only then write a custom
   agent in `<plugin>/agents/*.md` (`model`, `tools`, `permissionMode`, `maxTurns`). Not
   used yet. A plain `model:` line on the fork's frontmatter covers the model case:
   `analyze-stream-recording` runs on `sonnet` (measured below; `haiku` was too vague).

4. **Does the step need to talk to the user?** It stays in the parent, always. Subagents
   cannot use `AskUserQuestion`. That includes offering to install missing dependencies:
   check first in the parent (`check-deps.sh <scenario>`), ask, install on yes, and only
   then spawn the fork. A fork that hits a missing tool returns one `ERROR:` line and stops.

Other small leaks worth fixing while you're there: reference bundled files with
`${CLAUDE_SKILL_DIR}/...` (not `~/.claude/skills/...`, which is wrong for a plugin install
and costs hunting tool calls), and don't keep a hardcoded copy of anything a live fetch
already supplies.

Measuring: `evals/youtube-stream-description/run.sh` runs the same prompt through each version
headlessly (`claude -p --output-format stream-json`) and reads token usage, cost, and turns off
the trace. Results, 2026-09-11, Opus 5 main thread, 3 reps per cell. "Forked + Haiku" is the
forked version with `model: haiku` added to `analyze-stream-recording`.

| recording | transcript words | version | peak main context | cost/run | wall |
|---|---|---|---|---|---|
| 8 min | 1.4k | legacy | 35.8k | $0.31 | 46s |
| | | forked | 32.2k | $0.42 | 57s |
| | | forked + Haiku | 32.2k | $0.29 | 61s |
| 22 min | 4.4k | legacy | 39.6k | $0.33 | 55s |
| | | forked | 32.4k | $0.45 | 72s |
| | | forked + Haiku | 33.9k | $0.34 | 90s |
| 58 min | 11.5k | legacy | 53.0k | $0.53 | 111s |
| | | forked | 40.7k | $0.65 | 127s |
| | | forked + Haiku | 37.2k | $0.39 | 125s |

After fixing the leak (helper no longer returns transcript paths), 58-minute recording, 5 reps:

| version | peak main context | cost/run | chapters | runs that read the transcript |
|---|---|---|---|---|
| forked, fixed, Opus helper | 32.6k | $0.55 | 11–12 | 0 of 5 |
| forked, fixed, Sonnet helper | 32.8k | $0.40 | 10–12 | 0 of 5 |

What this shows:

- **Context: the fork wins, and the gap grows with length.** Legacy main context grows with
  the transcript. The forked version holds near 32k at every length when it behaves.
- **Cost: the fork on Opus never paid for itself** up to 58 minutes. A fork is a second full
  context (~18k system prompt) billed on each of its turns, and that costs more than re-sending
  the transcript in the parent. The gap narrows in percentage terms as streams get longer.
- **Haiku fixes cost but hurts quality on long streams.** It was the cheapest arm at 8 and
  58 minutes. But on the 58-minute stream it returned 6–7 generic chapters, one run with a
  19-minute gap, against 11–12 specific ones from the Opus fork. Fine for short clips.
- **Leak (fixed): the parent used to read the transcript anyway.** In 4 of 18 forked runs the
  parent took the path from the helper's old `## Source` section and read `condensed.txt`
  itself. With the paths removed, 0 of 10 runs leaked, and the fixed Opus version cost about
  the same as legacy.
- **Sonnet is the sweet spot for the helper.** Same main context as Opus, about 28% cheaper,
  and chapters close to Opus quality. Haiku was cheaper still but too vague on long streams.

Second worked example: adding Simplified Technical English (STE) to the writing skills, then
trimming what the voice skills load. `evals/ste-voice/` compares three plugin snapshots
(baseline 1.20.1, STE added, STE + efficiency work) across 8 cases, 66 runs. Full write-up in
[`evals/ste-voice/REPORT.md`](evals/ste-voice/REPORT.md). The short version:

| finding | before | after |
|---|---|---|
| Tutorial steps at 20 words or fewer (`write-article`) | 0 steps (prose) | 100% of ~19 steps |
| STE card read for a P2 post (should be never) | 3 of 3 | 0 of 3 |
| `wnd-script` full sample transcript read | 3 of 3, $0.69/run | 0 of 3, $0.62/run |
| `ste-pass` audit with `ste-lint.py` | $0.50, 130s | $0.40, 74s (Sonnet: $0.27) |
| Skill descriptions loaded every session | 1,156 tok | 676 tok |

Two more patterns came out of it:

5. **Say when before where.** A skill that names a reference file before saying when to use
   it gets that file read every time. `write-article` read the STE card for P2 posts until one
   sentence ("When STE is off, don't read the card") moved the condition first.
6. **Required reads are where the savings are.** Removing an *optional* 20k-token transcript
   read cut the static worst case by 67% but changed nothing in real runs. Replacing a
   *required* full sample with curated excerpts cut `wnd-script` input tokens by 19%.

## Install on a new machine

```shell
# Register this marketplace (use your git remote, or a local path)
/plugin marketplace add ryanwelcher/claude-skills

# Install the plugins you want on this machine
/plugin install public@ryan-claude-skills
/plugin install devrel@ryan-claude-skills
```

To sync updates after pushing changes from another machine:

```shell
/plugin marketplace update ryan-claude-skills
```

## Sharing these skills

This repo is public. Work-internal skills live in a separate private marketplace, so
nothing here depends on company tools or channels. Install `public` and `devrel` as shown
above. The `devrel` skills carry Ryan's voice and persona, so treat them as examples to
adapt rather than drop-in skills.

## Authoring in place (no cache, no drift)

On the machine where you actually edit these skills, **don't** use the marketplace install —
it copies into the cache, and cache edits are lost on `/plugin update`. Instead, load each
plugin **in place** from a local clone so edits are live and version-controlled.

One-time setup (already done on Ryan's primary machine — July 2026):

```shell
# 1. Clone the repo to your normal dev location
git clone https://github.com/ryanwelcher/claude-skills.git ~/repositories/claude-skills

# 2. Symlink each plugin folder (each has a .claude-plugin/plugin.json) into your skills dir.
#    Claude loads any such folder as "<name>@skills-dir" — discovered in place, NOT cached.
ln -s ~/repositories/claude-skills/devrel     ~/.claude/skills/devrel
ln -s ~/repositories/claude-skills/public     ~/.claude/skills/public

# 3. Disable the marketplace-installed copies so you don't run duplicates.
#    In ~/.claude/settings.json, under "enabledPlugins", set each to false:
#      "devrel@ryan-claude-skills": false
#      "public@ryan-claude-skills": false
```

Restart Claude Code and the plugins load from the clone. From then on: **edit under
`~/repositories/claude-skills/<plugin>/skills/<name>/`, and it's live immediately** — no
`/plugin update`. Commit and push when you want to back up or sync other machines. Reverse it
by flipping the `enabledPlugins` flags back to `true` and removing the symlinks.

## Editing skills (either setup)

Edit the `SKILL.md` (and any `scripts/`/`references/`) under `<plugin>/skills/<name>/`. When
adding a new skill, register it in **both** `<plugin>/.claude-plugin/plugin.json` and the root
`.claude-plugin/marketplace.json`, and bump that plugin's version in both. Commit and push;
run `/plugin marketplace update` on any machine still using the marketplace install. Full
details in [CONTRIBUTING.md](CONTRIBUTING.md).
