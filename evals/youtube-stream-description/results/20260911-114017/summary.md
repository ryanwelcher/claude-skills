# Summary — 20260911-114017

model=claude-opus-5 · reps=5 · clip=/Users/ryanwelcher/repositories/claude-skills/evals/youtube-stream-description/fixtures/long-58min.mp4 · scenario=local-recording · claude=2.1.268 (Claude Code)

## Per run

| scenario | version | run | ok | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s | words | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | repo-sonnet | run-1 | y | 32,888 | 32,888 | 49,164 | 86,606 | 1,982 | 20,067 | 0.421 | 5 | 1 | 121 | 11533 | opus-5+sonnet-5 |
| local-recording | repo-sonnet | run-2 | y | 32,458 | 32,458 | 49,343 | 84,411 | 1,928 | 19,637 | 0.380 | 5 | 1 | 118 | 11533 | opus-5+sonnet-5 |
| local-recording | repo-sonnet | run-3 | y | 32,939 | 32,939 | 49,371 | 117,210 | 1,995 | 20,118 | 0.409 | 5 | 1 | 138 | 11533 | opus-5+sonnet-5 |
| local-recording | repo-sonnet | run-4 | y | 32,998 | 32,998 | 49,150 | 84,815 | 2,002 | 20,177 | 0.393 | 5 | 1 | 128 | 11533 | opus-5+sonnet-5 |
| local-recording | repo-sonnet | run-5 | y | 32,499 | 32,499 | 49,353 | 84,452 | 1,897 | 19,678 | 0.386 | 5 | 1 | 119 | 11533 | opus-5+sonnet-5 |

## Mean (min–max) per version

| scenario | version | n | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | repo-sonnet | 5 | 32,756 (32,458–32,998) | 32,756 (32,458–32,998) | 49,276 (49,150–49,371) | 91,499 (84,411–117,210) | 1,961 (1,897–2,002) | 19,935 (19,637–20,177) | 0.398 (0.380–0.421) | 5 (5–5) | 1 (1–1) | 125 (118–138) |

## Delta vs legacy (mean)

| scenario | version | metric | legacy | this | delta | % |
|---|---|---|---|---|---|---|

_final_main_ctx is the number `/context` would show at the end of an interactive session. Negative delta = the new version is cheaper._
