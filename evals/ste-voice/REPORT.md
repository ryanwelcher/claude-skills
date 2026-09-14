# Adding Simplified Technical English to voice skills: before/after data

Measured 2026-09-13 on Claude Code 2.1.270, Opus 5 main thread, 3 reps per cell, 66 headless runs plus one smoke run (about $33 total). Raw per-run tables: [`results/main/summary.md`](results/main/summary.md). Method and caveats: [`README.md`](README.md).

Three versions of the `devrel` plugin:

| arm | what changed |
|---|---|
| **baseline** | 1.20.1, no STE (`da35236`) |
| **ste** | Added the shared STE card, the `ste-pass` skill, and zone rules in `write-article`, `sounds-like-me`, `wp-workshop-scaffold` |
| **optimized** | `ste` plus efficiency work: refinement logs moved out of voice cards, no full transcripts for `youtube-script`/`wnd-script` (curated excerpts instead), on-demand modes for `wp-workshop-scaffold`, de-duplicated `write-article`, shorter descriptions, `ste-lint.py`, and "don't read the card when STE is off" |

## Headline numbers

| | ste | optimized |
|---|---|---|
| Mean cost across the 8 cases (sum of per-case means) | $4.56 | **$4.28 (-6%)** |
| Tutorial steps at 20 words or fewer | 100% | 100% |
| STE card read for a P2 post (should be never) | 3/3 | **0/3** |
| Full voice transcript read by `wnd-script` | 3/3 | **0/3** |
| Code blocks changed by an STE rewrite | 0 | 0 |
| Action-zone lines rewritten by a voice pass | 0 | 0 |
| Skill descriptions loaded every session | 1,156 tok | **676 tok (-42%)** |

## 1. STE changes the writing where it should

`write-article`, Developer Blog tutorial on `BlockControls`:

| metric | baseline | ste | optimized |
|---|---|---|---|
| Numbered steps | 0 | 22.3 | 19.0 |
| Steps at 20 words or fewer | – | 100% | 100% |
| "Make sure that…" checks | 0.3 | 5.0 | 4.0 |
| WARNING/CAUTION/NOTE blocks | 0 | 1.0 | 0.7 |
| First-person voice outside steps (per 100 words) | 0.5 | 0.9 | 0.8 |
| Voice ban-list hits | 0 | 0 | 0 |
| Words | 879 | 1,333 | 1,271 |
| Cost per draft | $0.32 | $0.46 | $0.43 |

Without STE, the model wrote tutorials as prose with code blocks and no numbered steps at all. With the card, every run produced short, checkable steps, and the intro still opened in first person ("I see a lot of custom blocks that store an image and give users no clean way to remove it."). One `ste` draft opened with "The block toolbar is prime real estate", a phrase the voice card's spirit rejects but its ban list doesn't catch.

The cost is real: about +34% per tutorial draft versus baseline after optimization, mostly from the longer draft (more steps and checks) and the extra card read.

## 2. The first version leaked STE into P2 posts

`write-article`, team P2 discussion post (STE should be off):

| metric | baseline | ste | optimized |
|---|---|---|---|
| STE card read | 0/3 | **3/3** | 0/3 |
| WARNING/CAUTION/NOTE blocks | 0 | 0.3 | 0 |
| "Make sure" phrasing | 0 | 2.7 | 1.7 |
| Peak context | 25,303 | 28,451 | 24,839 |
| Cost | $0.22 | $0.28 | **$0.21** |

The `ste` skill told the model where the card lives before telling it when to use it, so it read the card every time, and one P2 draft picked up a `**NOTE:**` block. One sentence in the optimized version ("When STE is off, don't read the card") fixed it. The optimized P2 run is slightly cheaper than baseline because of the de-duplicated `SKILL.md`.

## 3. The voice/STE conflict didn't happen (on this fixture)

`sounds-like-me` voice pass on a hybrid recipe (voice intro + STE steps), with every finding pre-approved:

| metric | baseline | ste | optimized |
|---|---|---|---|
| Action-zone lines rewritten | 0 | 0 | 0 |
| Voice-zone lines rewritten | 4.0 | 4.0 | 3.7 |
| Code blocks identical | 3/3 | 3/3 | 3/3 |
| Reference tokens read | 5,904 | 7,674 | 5,685 |
| Cost | $0.41 | $0.48 | $0.40 |

I expected the old voice pass to "fix" plain STE steps back into chatty prose. It didn't: even without the zone rule, it only touched voice-zone lines. The zone rule is still worth keeping as a guardrail, but this data doesn't show it preventing a problem. After optimization, the added STE card costs nothing net, because moving the refinement log out of the style card saved more than the card adds.

## 4. `ste-pass`: the linter made audits faster; Sonnet is a mixed result

| case | metric | ste (Opus) | optimized (Opus + lint) | optimized (Sonnet + lint) |
|---|---|---|---|---|
| audit | cost | $0.50 | **$0.40 (-20%)** | **$0.27 (-46%)** |
| audit | duration | 130s | **74s** | 102s |
| audit | findings | 30 | 38 | 20 |
| audit | caught all 3 planted problems | 3/3 | 3/3 | 3/3 |
| audit | file left untouched (findings first) | 3/3 | 3/3 | 3/3 |
| rewrite | cost | $0.93 | $0.85 (-9%) | $0.48 (-48%) |
| rewrite | lines changed (run 1) | – | 74 added / 26 removed | 13 / 13 |
| rewrite | numbered steps after | 9.3 | 11.0 | 2.3 |
| rewrite | code blocks identical | 3/3 | 3/3 | 3/3 |
| trigger from plain English | invoked `ste-pass` | 3/3 | 3/3 | 3/3 |
| trigger | cost | $0.35 | $0.43 (+23%) | $0.40 |

- **The linter paid off on audits.** It printed the mechanical hits up front, so the model spent its output on judgment instead of counting words. Audits got faster and cheaper, and they found more.
- **Sonnet is a good fit for audits, not rewrites.** Sonnet audits caught every planted problem for half the cost. Sonnet rewrites were cheap because they did less: prose instructions stayed prose, and a typo ("completed completed") survived.
- **The linter costs extra on quick asks.** The `trigger` case ("show me what you'd change") got 23% more expensive because the skill now always runs the linter first.
- **`model: sonnet` only applied when the skill was invoked by slash command.** When the model triggered `ste-pass` itself, the session stayed on Opus (see the `trigger` models column).

## 5. Removing transcripts and logs: big on paper, smaller in practice

| case | metric | ste | optimized | delta |
|---|---|---|---|---|
| `wnd-script` | full sample transcript read | 3/3 | 0/3 | |
| `wnd-script` | reference tokens read | 11,325 | 9,454 | -17% |
| `wnd-script` | peak context | 54,843 | 50,741 | -7% |
| `wnd-script` | total input tokens | 215,699 | 175,422 | -19% |
| `wnd-script` | cost | $0.69 | $0.62 | -10% |
| `wnd-script` | branded greeting + "have a good one" | 3/3 | 3/3 | |
| `youtube-script` | full transcript read | 0/3 | 0/3 | |
| `youtube-script` | reference tokens read | 9,938 | 8,545 | -14% |
| `youtube-script` | peak context | 68,372 | 67,515 | -1% |
| `youtube-script` | cost | $0.87 | $0.94 | +8% (output length) |

`wnd-script` shows a clean win: it was told to read a full sample every time, and now it reads excerpts. `youtube-script` never took the optional "deep soak" in these runs, so removing it guards against the worst case (static estimate: 31k → 10k tokens) rather than saving money on a typical run. Its cost rose because the optimized runs happened to write longer scripts (8.4k → 11.2k output tokens), not because of the change. The one ban-list hit in that arm was "genuinely" inside a director note, not a spoken line.

## 6. Static view: what each skill loads before it writes

From `static-cost.py` (bytes/4 estimates; free and deterministic):

| skill / path | baseline | ste | optimized |
|---|---|---|---|
| write-article: tutorial | 2,706 | 4,272 | 3,844 |
| write-article: P2 post | 2,706 | 3,087 | 2,658 |
| ste-pass | – | 2,307 | 2,440 |
| sounds-like-me: written draft | 6,825 | 8,228 | 6,814 |
| sounds-like-me: WND teleprompter | 9,727 | 9,945 | 8,139 |
| youtube-script: write | 11,806 | 11,806 | 10,417 |
| youtube-script: write + deep soak (worst case) | 31,238 | 31,238 | 10,417 |
| wnd-script (typical) | 14,104 | 14,104 | 12,241 |
| wp-workshop-scaffold: create | 3,051 | 3,187 | 2,343 |
| wp-workshop-scaffold: reformat | 3,051 | 3,187 | 3,340 |
| all devrel descriptions (every session) | 1,018 | 1,156 | 676 |

`reformat` got slightly more expensive (it now loads two mode files); `create`, the common path, got cheaper.

## 7. Follow-up: moving the audit into a Sonnet fork made it worse

Based on section 4, 1.22.0 (`final` arm) split `ste-pass`: files go to a new `ste-audit` helper with `context: fork` and `model: sonnet`, and short passages skip the linter. 15 more runs, same fixtures:

| case | metric | optimized (Opus inline + lint) | final (Sonnet fork) |
|---|---|---|---|
| audit | cost | **$0.40** | $0.57 (+43%) |
| audit | duration | **74s** | 175s |
| audit | tokens inside the fork | – | 210,774 |
| audit | caught all 3 planted problems | 3/3 | 3/3 |
| rewrite | cost | $0.85 | **$0.74 (-13%)** |
| rewrite | numbered steps after | 11 | **15** |
| rewrite | lines changed | 106 | 70 |
| rewrite | "make sure" checks | 11 | 5 |
| trigger | cost | **$0.43** | $0.55 (+28%) |
| trigger | helper actually used | – | 3/3 (Sonnet ran) |
| quick passage | cost | $0.18 | $0.17 |
| quick passage | linter run | 0/3 | 0/3 |

- **The fork cost more than it saved.** In section 4, the Sonnet audit was cheap because the whole session ran on Sonnet. As a fork, Opus still runs the parent, and the fork starts a second full context that it re-sends on every turn. The same thing happened with `analyze-stream-recording` on Opus: a fork only pays when it keeps a very large payload out of the parent, and an STE audit's payload is small.
- **Sonnet as a fork did fix the model problem.** The helper ran on Sonnet in 3/3 auto-triggered runs, where `model:` on the inline skill had been ignored.
- **Rewrites improved.** Telling the helper to propose complete rewrites (not word swaps) produced more numbered steps than Opus inline, at 13% less cost, though with fewer final checks.
- **The quick path changed nothing.** Opus had already skipped the linter on a pasted passage in every optimized run, so the new rule wrote down behavior that already happened.

Recommendation: revert the fork for audits (keep Opus inline with the linter, the optimized version) and keep the helper only for rewrites, or drop it. Re-measure either way.

## Takeaways

1. **Put the "when" before the "where".** If a skill names a file before saying when to read it, the model reads it every time. That one ordering mistake cost 28% on every P2 post.
2. **Measure the problem before you guard against it.** The voice/STE conflict was the reason for the zone rule, and it never showed up.
3. **Static estimates overstate savings on optional paths.** Removing the transcript "deep soak" cut the worst case by 67% but changed nothing in three typical runs. Required reads (the WND sample) are where the real savings are.
4. **Move deterministic work into a script.** The linter cut audit time by 43%, but it adds a turn to quick asks. Put it where the work is heavy.
5. **A cheaper model can pass the checks and still do less.** Sonnet matched Opus on every pass/fail check for audits. On rewrites it passed the checks too, and only the diff size showed it did a fraction of the work.
6. **A cheaper model in a fork is not a cheaper model.** Moving a small, chatty job into a Sonnet fork added a second context and cost 43% more than doing it inline on Opus.
