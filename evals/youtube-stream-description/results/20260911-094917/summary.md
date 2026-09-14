# Summary — 20260911-094917

model=claude-opus-5 · reps=3 · clip=/Users/ryanwelcher/repositories/claude-skills/evals/youtube-stream-description/fixtures/full-22min.mp4 · scenario=local-recording · claude=2.1.268 (Claude Code)

## Per run

| scenario | version | run | ok | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s | words | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | legacy | run-1 | y | 39,757 | 39,757 | 0 | 66,094 | 1,771 | 26,936 | 0.333 | 4 | 0 | 58 | - | opus-5 |
| local-recording | legacy | run-2 | y | 39,572 | 39,572 | 0 | 65,909 | 1,543 | 26,751 | 0.326 | 3 | 0 | 55 | - | opus-5 |
| local-recording | legacy | run-3 | y | 39,579 | 39,579 | 0 | 65,916 | 1,642 | 26,758 | 0.328 | 3 | 0 | 53 | - | opus-5 |
| local-recording | new | run-1 | y | 32,366 | 32,366 | 37,847 | 85,765 | 1,350 | 19,545 | 0.484 | 5 | 1 | 71 | 4362 | opus-5 |
| local-recording | new | run-2 | y | 32,381 | 32,381 | 37,852 | 85,780 | 1,411 | 19,560 | 0.434 | 5 | 1 | 71 | 4362 | opus-5 |
| local-recording | new | run-3 | y | 32,363 | 32,363 | 37,845 | 85,762 | 1,442 | 19,542 | 0.445 | 5 | 1 | 75 | 4362 | opus-5 |
| local-recording | new-haiku | run-1 | y | 37,265 | 37,265 | 50,004 | 157,720 | 2,578 | 24,444 | 0.441 | 6 | 1 | 110 | 4362 | haiku-4-5+opus-5 |
| local-recording | new-haiku | run-2 | y | 32,313 | 32,313 | 32,716 | 85,963 | 1,370 | 19,492 | 0.294 | 5 | 1 | 78 | 4362 | haiku-4-5+opus-5 |
| local-recording | new-haiku | run-3 | y | 32,201 | 32,201 | 32,699 | 85,851 | 1,504 | 19,380 | 0.295 | 4 | 1 | 81 | 4362 | haiku-4-5+opus-5 |

## Mean (min–max) per version

| scenario | version | n | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | legacy | 3 | 39,636 (39,572–39,757) | 39,636 (39,572–39,757) | 0 (0–0) | 65,973 (65,909–66,094) | 1,652 (1,543–1,771) | 26,815 (26,751–26,936) | 0.329 (0.326–0.333) | 3 (3–4) | 0 (0–0) | 55 (53–58) |
| local-recording | new | 3 | 32,370 (32,363–32,381) | 32,370 (32,363–32,381) | 37,848 (37,845–37,852) | 85,769 (85,762–85,780) | 1,401 (1,350–1,442) | 19,549 (19,542–19,560) | 0.454 (0.434–0.484) | 5 (5–5) | 1 (1–1) | 72 (71–75) |
| local-recording | new-haiku | 3 | 33,926 (32,201–37,265) | 33,926 (32,201–37,265) | 38,473 (32,699–50,004) | 109,845 (85,851–157,720) | 1,817 (1,370–2,578) | 21,105 (19,380–24,444) | 0.343 (0.294–0.441) | 5 (4–6) | 1 (1–1) | 90 (78–110) |

## Delta vs legacy (mean)

| scenario | version | metric | legacy | this | delta | % |
|---|---|---|---|---|---|---|
| local-recording | new | peak_main_ctx | 39,636 | 32,370 | -7,266 | -18% |
| local-recording | new | final_main_ctx | 39,636 | 32,370 | -7,266 | -18% |
| local-recording | new | fork_tokens | 0 | 37,848 | 37,848 | n/a |
| local-recording | new | total_in | 65,973 | 85,769 | 19,796 | +30% |
| local-recording | new | total_out | 1,652 | 1,401 | -251 | -15% |
| local-recording | new | cost_usd | 0.329 | 0.454 | 0.125 | +38% |
| local-recording | new | turns | 3 | 5 | 2 | +50% |
| local-recording | new | duration_s | 55 | 72 | 17 | +31% |
| local-recording | new-haiku | peak_main_ctx | 39,636 | 33,926 | -5,710 | -14% |
| local-recording | new-haiku | final_main_ctx | 39,636 | 33,926 | -5,710 | -14% |
| local-recording | new-haiku | fork_tokens | 0 | 38,473 | 38,473 | n/a |
| local-recording | new-haiku | total_in | 65,973 | 109,845 | 43,872 | +66% |
| local-recording | new-haiku | total_out | 1,652 | 1,817 | 165 | +10% |
| local-recording | new-haiku | cost_usd | 0.329 | 0.343 | 0.014 | +4% |
| local-recording | new-haiku | turns | 3 | 5 | 2 | +50% |
| local-recording | new-haiku | duration_s | 55 | 90 | 34 | +62% |

_final_main_ctx is the number `/context` would show at the end of an interactive session. Negative delta = the new version is cheaper._
