# Summary — 20260911-094604

model=claude-opus-5 · reps=3 · clip=/Users/ryanwelcher/repositories/claude-skills/evals/youtube-stream-description/fixtures/clip.mp4 · scenario=local-recording · claude=2.1.268 (Claude Code)

## Per run

| scenario | version | run | ok | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s | words | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | new-haiku | run-1 | y | 32,172 | 32,172 | 52,157 | 85,814 | 1,524 | 19,351 | 0.294 | 5 | 1 | 67 | 1447 | haiku-4-5+opus-5 |
| local-recording | new-haiku | run-2 | y | 32,164 | 32,164 | 32,673 | 85,806 | 1,345 | 19,343 | 0.283 | 5 | 1 | 58 | 1447 | haiku-4-5+opus-5 |
| local-recording | new-haiku | run-3 | y | 32,199 | 32,199 | 52,169 | 85,841 | 1,359 | 19,378 | 0.297 | 5 | 1 | 58 | 1447 | haiku-4-5+opus-5 |

## Mean (min–max) per version

| scenario | version | n | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | new-haiku | 3 | 32,178 (32,164–32,199) | 32,178 (32,164–32,199) | 45,666 (32,673–52,169) | 85,820 (85,806–85,841) | 1,409 (1,345–1,524) | 19,357 (19,343–19,378) | 0.292 (0.283–0.297) | 5 (5–5) | 1 (1–1) | 61 (58–67) |

## Delta vs legacy (mean)

| scenario | version | metric | legacy | this | delta | % |
|---|---|---|---|---|---|---|

_final_main_ctx is the number `/context` would show at the end of an interactive session. Negative delta = the new version is cheaper._
