# Summary — 20260911-093129

model=opus · reps=1 · clip=/Users/ryanwelcher/repositories/claude-skills/evals/youtube-stream-description/fixtures/clip.mp4 · scenario=local-recording · claude=2.1.268 (Claude Code)

## Per run

| scenario | version | run | ok | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s | words |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | legacy | run-1 | y | 36,771 | 36,771 | 0 | 133,452 | 2,306 | 36,769 | 0.474 | 6 | 0 | 56 | - |
| local-recording | new | run-1 | y | 32,546 | 32,546 | 59,718 | 85,775 | 1,203 | 19,725 | 0.464 | 5 | 1 | 52 | 1447 |

## Mean (min–max) per version

| scenario | version | n | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | legacy | 1 | 36,771 (36,771–36,771) | 36,771 (36,771–36,771) | 0 (0–0) | 133,452 (133,452–133,452) | 2,306 (2,306–2,306) | 36,769 (36,769–36,769) | 0.474 (0.474–0.474) | 6 (6–6) | 0 (0–0) | 56 (56–56) |
| local-recording | new | 1 | 32,546 (32,546–32,546) | 32,546 (32,546–32,546) | 59,718 (59,718–59,718) | 85,775 (85,775–85,775) | 1,203 (1,203–1,203) | 19,725 (19,725–19,725) | 0.464 (0.464–0.464) | 5 (5–5) | 1 (1–1) | 52 (52–52) |

## Delta new − legacy (mean)

| scenario | metric | legacy | new | delta | % |
|---|---|---|---|---|---|
| local-recording | peak_main_ctx | 36,771 | 32,546 | -4,225 | -11% |
| local-recording | final_main_ctx | 36,771 | 32,546 | -4,225 | -11% |
| local-recording | total_in | 133,452 | 85,775 | -47,677 | -36% |
| local-recording | total_out | 2,306 | 1,203 | -1,103 | -48% |
| local-recording | cost_usd | 0.474 | 0.464 | -0.009 | -2% |
| local-recording | turns | 6 | 5 | -1 | -17% |
| local-recording | duration_s | 56 | 52 | -4 | -6% |

_final_main_ctx is the number `/context` would show at the end of an interactive session. Negative delta = the new version is cheaper._
