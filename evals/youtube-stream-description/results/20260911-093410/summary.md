# Summary — 20260911-093410

model=opus · reps=3 · clip=/Users/ryanwelcher/repositories/claude-skills/evals/youtube-stream-description/fixtures/clip.mp4 · scenario=local-recording · claude=2.1.268 (Claude Code)

## Per run

| scenario | version | run | ok | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s | words | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | legacy | run-1 | y | 35,686 | 35,686 | 0 | 97,178 | 1,848 | 22,865 | 0.312 | 4 | 0 | 48 | - | opus-5 |
| local-recording | legacy | run-2 | y | 36,768 | 36,768 | 0 | 133,387 | 2,304 | 23,947 | 0.352 | 6 | 0 | 53 | - | opus-5 |
| local-recording | legacy | run-3 | y | 35,030 | 35,030 | 0 | 61,350 | 1,432 | 22,209 | 0.277 | 4 | 0 | 38 | - | opus-5 |
| local-recording | new | run-1 | y | 32,143 | 32,143 | 80,078 | 85,508 | 1,369 | 19,322 | 0.426 | 5 | 1 | 59 | 1447 | opus-5 |
| local-recording | new | run-2 | y | 32,113 | 32,113 | 37,811 | 85,478 | 1,400 | 19,292 | 0.397 | 5 | 1 | 52 | 1447 | opus-5 |
| local-recording | new | run-3 | y | 32,490 | 32,490 | 37,807 | 118,000 | 1,605 | 19,669 | 0.422 | 6 | 1 | 59 | 1447 | opus-5 |

## Mean (min–max) per version

| scenario | version | n | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | legacy | 3 | 35,828 (35,030–36,768) | 35,828 (35,030–36,768) | 0 (0–0) | 97,305 (61,350–133,387) | 1,861 (1,432–2,304) | 23,007 (22,209–23,947) | 0.314 (0.277–0.352) | 5 (4–6) | 0 (0–0) | 46 (38–53) |
| local-recording | new | 3 | 32,249 (32,113–32,490) | 32,249 (32,113–32,490) | 51,899 (37,807–80,078) | 96,329 (85,478–118,000) | 1,458 (1,369–1,605) | 19,428 (19,292–19,669) | 0.415 (0.397–0.426) | 5 (5–6) | 1 (1–1) | 57 (52–59) |

## Delta vs legacy (mean)

| scenario | version | metric | legacy | this | delta | % |
|---|---|---|---|---|---|---|
| local-recording | new | peak_main_ctx | 35,828 | 32,249 | -3,579 | -10% |
| local-recording | new | final_main_ctx | 35,828 | 32,249 | -3,579 | -10% |
| local-recording | new | fork_tokens | 0 | 51,899 | 51,899 | n/a |
| local-recording | new | total_in | 97,305 | 96,329 | -976 | -1% |
| local-recording | new | total_out | 1,861 | 1,458 | -403 | -22% |
| local-recording | new | cost_usd | 0.314 | 0.415 | 0.101 | +32% |
| local-recording | new | turns | 5 | 5 | 1 | +14% |
| local-recording | new | duration_s | 46 | 57 | 11 | +23% |

_final_main_ctx is the number `/context` would show at the end of an interactive session. Negative delta = the new version is cheaper._
