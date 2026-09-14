# STE + context-efficiency eval

Before/after measurement for two changes to the `devrel` plugin (1.20.1 → 1.21.0):

1. **STE integration.** A shared Simplified Technical English card (`ste-pass/references/ste-card.md`), a new `ste-pass` skill, and zone rules in `write-article`, `wp-workshop-scaffold`, and `sounds-like-me`, so the steps readers act on use STE and everything else keeps Ryan's voice.
2. **Context efficiency.** Refinement logs moved out of the voice cards, `youtube-script` no longer reads 15–20k-token transcripts, `wnd-script` reads curated excerpts instead of a full sample, `wp-workshop-scaffold` loads `reformat`/`audit` on demand, `write-article` no longer duplicates its style reference, shorter skill descriptions, and a deterministic `ste-lint.py` for `ste-pass`.

## Arms

Frozen copies of the plugin in `snapshots/` (gitignored; rebuild from git as below).

| arm | what it is | rebuild |
|---|---|---|
| `baseline` | 1.20.1, before any of this (`da35236`) | `git archive da35236 devrel \| tar -x -C snapshots/baseline --strip-components=1` |
| `ste` | STE integration only (`0c32831`) | `git archive 0c32831 devrel \| tar -x -C snapshots/ste --strip-components=1` |
| `optimized` | STE + efficiency changes (`a8f62c9`) | `git archive a8f62c9 devrel \| tar -x -C snapshots/optimized --strip-components=1` |
| `final` | `optimized` + audit split into a Sonnet fork (`ste-audit`) and a quick path with no linter (1.22.0) | `cp -R ../../devrel snapshots/final` at that commit |
| `<arm>-sonnet` | same, with `model: sonnet` patched into `ste-pass` | built by `run.sh` |

## Cases

| case | skill | what it proves |
|---|---|---|
| `ste-audit` | `ste-pass` | Findings first (fixture untouched), zone map shown, known problems caught |
| `ste-apply` | `ste-pass` | Code blocks byte-identical after a rewrite; step metrics; intro voice kept |
| `voice-pass` | `sounds-like-me` | **The conflict test.** On a hybrid doc, how many action-zone vs voice-zone lines a voice pass rewrites |
| `article-devblog` | `write-article` | Drafting a Developer Blog tutorial: step length, cautions, checks, voice bans |
| `article-p2` | `write-article` | STE stays off for P2 (no admonitions, card not read). The prompt and raw outputs aren't in this repo because they use internal team context; `results/main/summary.md` keeps the metrics. |
| `trigger` | `ste-pass` | A natural-language request triggers `ste-pass` |
| `youtube-script` | `youtube-script` | Context cost of writing a script; whether a full transcript is read |
| `wnd-script` | `wnd-script` | Context cost of a WND teleprompter; series conventions intact |

`youtube-script` and `wnd-script` are identical in `baseline` and `ste`, so they run on `ste` only.

## Run

```bash
bash run.sh --arms baseline,ste --cases voice-pass,article-devblog --reps 3 --parallel 4 --out main
bash run.sh --arms ste --cases ste-audit,ste-apply,trigger,youtube-script,wnd-script --reps 3 --parallel 4 --out main
bash run.sh --arms optimized --cases all --reps 3 --parallel 4 --out main
bash run.sh --arms optimized-sonnet --cases ste-audit,ste-apply,trigger --reps 3 --parallel 4 --out main
python3 static-cost.py baseline ste optimized > results/static-cost.md
bash regrade.sh main   # after changing check.py: re-grade every run (needs the gitignored work/ dirs)
```

Each run is `claude -p` headless with `--plugin-dir <snapshot>`, the installed `devrel` disabled, `--strict-mcp-config` (no MCP servers), `AskUserQuestion`/`WebFetch`/`WebSearch`/`Agent` disallowed, and edits auto-accepted inside a throwaway copy of `fixtures/`. Prompts pre-answer every intake question.

## Output

`results/<name>/summary.md` has one table per case. Per run: `run-N.md` (final message), `run-N.out/` (documents the run wrote), `run-N.check.json` (graders), `run-N.jsonl` (raw trace, gitignored).

| column | meaning |
|---|---|
| peak_main_ctx | largest prompt the main thread sent (input + cache read + cache creation) |
| total_in / total_out | whole-session tokens from the result event |
| cost_usd, turns, duration_s | from the result event (duration includes parallel contention) |
| ref_tokens_read | estimated tokens (bytes/4) of skill files the run actually read |
| everything else | `check.py` graders — see that file for each regex/diff |

`results/static-cost.md` is the free, deterministic view: what each skill's instructions tell it to load, per snapshot.

## Caveats

- Three reps per cell. Treat small differences as noise; the transcript and log removals are large enough to show clearly.
- Token estimates in `static-cost.md` and `ref_tokens_read` are bytes/4, not tokenizer counts. `peak_main_ctx` and `total_in` are real.
- Voice quality is **not** auto-graded beyond a ban-list count. Read `run-N.out/` side by side for that.
- Your user-level `CLAUDE.md`, memory, and other plugins still load in every run. They are the same across arms, so deltas are fair, but absolute numbers include them.
