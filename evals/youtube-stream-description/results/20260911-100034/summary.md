# Summary — 20260911-100034

model=claude-opus-5 · reps=3 · clip=/Users/ryanwelcher/repositories/claude-skills/evals/youtube-stream-description/fixtures/long-58min.mp4 · scenario=local-recording · claude=2.1.268 (Claude Code)

## Per run

| scenario | version | run | ok | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s | words | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | legacy | run-1 | y | 52,850 | 52,850 | 0 | 145,218 | 2,535 | 40,029 | 0.516 | 5 | 0 | 109 | - | opus-5 |
| local-recording | legacy | run-2 | y | 54,193 | 54,193 | 0 | 166,066 | 3,149 | 41,372 | 0.555 | 6 | 0 | 115 | - | opus-5 |
| local-recording | legacy | run-3 | y | 52,035 | 52,035 | 0 | 143,979 | 2,758 | 39,214 | 0.514 | 6 | 0 | 107 | - | opus-5 |
| local-recording | new | run-1 | y | 37,276 | 37,276 | 37,843 | 123,317 | 2,345 | 24,455 | 0.607 | 6 | 1 | 128 | 11533 | opus-5 |
| local-recording | new | run-2 | y | 33,008 | 33,008 | 37,845 | 118,913 | 1,991 | 20,187 | 0.604 | 6 | 1 | 129 | 11533 | opus-5 |
| local-recording | new | run-3 | y | 51,796 | 51,796 | 37,846 | 137,652 | 2,252 | 38,975 | 0.751 | 6 | 1 | 123 | 11533 | opus-5 |
| local-recording | new-haiku | run-1 | y | 37,976 | 37,976 | 32,740 | 128,274 | 2,344 | 25,155 | 0.404 | 6 | 1 | 128 | 11533 | haiku-4-5+opus-5 |
| local-recording | new-haiku | run-2 | y | 32,102 | 32,102 | 32,744 | 85,752 | 1,391 | 19,281 | 0.312 | 4 | 1 | 106 | 11533 | haiku-4-5+opus-5 |
| local-recording | new-haiku | run-3 | y | 41,414 | 41,414 | 32,706 | 165,367 | 2,535 | 28,593 | 0.460 | 6 | 1 | 140 | 11533 | haiku-4-5+opus-5 |

## Mean (min–max) per version

| scenario | version | n | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | legacy | 3 | 53,026 (52,035–54,193) | 53,026 (52,035–54,193) | 0 (0–0) | 151,754 (143,979–166,066) | 2,814 (2,535–3,149) | 40,205 (39,214–41,372) | 0.528 (0.514–0.555) | 6 (5–6) | 0 (0–0) | 111 (107–115) |
| local-recording | new | 3 | 40,693 (33,008–51,796) | 40,693 (33,008–51,796) | 37,845 (37,843–37,846) | 126,627 (118,913–137,652) | 2,196 (1,991–2,345) | 27,872 (20,187–38,975) | 0.654 (0.604–0.751) | 6 (6–6) | 1 (1–1) | 127 (123–129) |
| local-recording | new-haiku | 3 | 37,164 (32,102–41,414) | 37,164 (32,102–41,414) | 32,730 (32,706–32,744) | 126,464 (85,752–165,367) | 2,090 (1,391–2,535) | 24,343 (19,281–28,593) | 0.392 (0.312–0.460) | 5 (4–6) | 1 (1–1) | 125 (106–140) |

## Delta vs legacy (mean)

| scenario | version | metric | legacy | this | delta | % |
|---|---|---|---|---|---|---|
| local-recording | new | peak_main_ctx | 53,026 | 40,693 | -12,333 | -23% |
| local-recording | new | final_main_ctx | 53,026 | 40,693 | -12,333 | -23% |
| local-recording | new | fork_tokens | 0 | 37,845 | 37,845 | n/a |
| local-recording | new | total_in | 151,754 | 126,627 | -25,127 | -17% |
| local-recording | new | total_out | 2,814 | 2,196 | -618 | -22% |
| local-recording | new | cost_usd | 0.528 | 0.654 | 0.126 | +24% |
| local-recording | new | turns | 6 | 6 | 0 | +6% |
| local-recording | new | duration_s | 111 | 127 | 16 | +15% |
| local-recording | new-haiku | peak_main_ctx | 53,026 | 37,164 | -15,862 | -30% |
| local-recording | new-haiku | final_main_ctx | 53,026 | 37,164 | -15,862 | -30% |
| local-recording | new-haiku | fork_tokens | 0 | 32,730 | 32,730 | n/a |
| local-recording | new-haiku | total_in | 151,754 | 126,464 | -25,290 | -17% |
| local-recording | new-haiku | total_out | 2,814 | 2,090 | -724 | -26% |
| local-recording | new-haiku | cost_usd | 0.528 | 0.392 | -0.136 | -26% |
| local-recording | new-haiku | turns | 6 | 5 | -0 | -6% |
| local-recording | new-haiku | duration_s | 111 | 125 | 14 | +13% |

_final_main_ctx is the number `/context` would show at the end of an interactive session. Negative delta = the new version is cheaper._
