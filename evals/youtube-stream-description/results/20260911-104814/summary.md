# Summary — 20260911-104814

model=claude-opus-5 · reps=5 · clip=/Users/ryanwelcher/repositories/claude-skills/evals/youtube-stream-description/fixtures/long-58min.mp4 · scenario=local-recording · claude=2.1.268 (Claude Code)

## Per run

| scenario | version | run | ok | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s | words | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | repo | run-1 | y | 32,333 | 32,333 | 37,921 | 85,916 | 1,736 | 19,512 | 0.573 | 5 | 1 | 111 | 11533 | opus-5 |
| local-recording | repo | run-2 | y | 32,868 | 32,868 | 37,924 | 118,782 | 2,047 | 20,047 | 0.556 | 6 | 1 | 118 | 11533 | opus-5 |
| local-recording | repo | run-3 | y | 32,442 | 32,442 | 37,745 | 86,309 | 1,946 | 19,621 | 0.530 | 5 | 1 | 112 | 11533 | opus-5 |
| local-recording | repo | run-4 | y | 32,447 | 32,447 | 37,762 | 86,368 | 1,929 | 19,626 | 0.528 | 5 | 1 | 114 | 11533 | opus-5 |
| local-recording | repo | run-5 | y | 32,996 | 32,996 | 76,550 | 119,352 | 2,069 | 20,175 | 0.584 | 6 | 1 | 123 | 11533 | opus-5 |

## Mean (min–max) per version

| scenario | version | n | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | repo | 5 | 32,617 (32,333–32,996) | 32,617 (32,333–32,996) | 45,580 (37,745–76,550) | 99,345 (85,916–119,352) | 1,945 (1,736–2,069) | 19,796 (19,512–20,175) | 0.554 (0.528–0.584) | 5 (5–6) | 1 (1–1) | 115 (111–123) |

## Delta vs legacy (mean)

| scenario | version | metric | legacy | this | delta | % |
|---|---|---|---|---|---|---|

_final_main_ctx is the number `/context` would show at the end of an interactive session. Negative delta = the new version is cheaper._
