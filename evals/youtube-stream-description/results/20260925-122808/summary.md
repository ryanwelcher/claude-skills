# Summary — 20260925-122808

model=claude-opus-5 · reps=1 · clip=/Users/ryanwelcher/repositories/claude-skills/evals/youtube-stream-description/fixtures/long-58min.mp4 · scenario=local-recording · claude=2.1.282 (Claude Code)

## Per run

| scenario | version | run | ok | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s | words | coverage | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | new | run-1 | y | 42,683 | 42,683 | 47,902 | 164,129 | 4,336 | 31,469 | 0.647 | 8 | 1 | 122 | 8847 | 100% | opus-5+sonnet-5 |
| local-recording | repo | run-1 | y | 32,423 | 32,423 | 47,898 | 116,213 | 3,042 | 18,530 | 0.429 | 6 | 1 | 171 | 8847 | 100% | opus-5+sonnet-5 |

## Mean (min–max) per version

| scenario | version | n | peak_main_ctx | final_main_ctx | fork_tokens | total_in | total_out | cache_create | cost_usd | turns | subagents | duration_s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local-recording | new | 1 | 42,683 (42,683–42,683) | 42,683 (42,683–42,683) | 47,902 (47,902–47,902) | 164,129 (164,129–164,129) | 4,336 (4,336–4,336) | 31,469 (31,469–31,469) | 0.647 (0.647–0.647) | 8 (8–8) | 1 (1–1) | 122 (122–122) |
| local-recording | repo | 1 | 32,423 (32,423–32,423) | 32,423 (32,423–32,423) | 47,898 (47,898–47,898) | 116,213 (116,213–116,213) | 3,042 (3,042–3,042) | 18,530 (18,530–18,530) | 0.429 (0.429–0.429) | 6 (6–6) | 1 (1–1) | 171 (171–171) |

## Delta vs legacy (mean)

| scenario | version | metric | legacy | this | delta | % |
|---|---|---|---|---|---|---|

_final_main_ctx is the number `/context` would show at the end of an interactive session. Negative delta = the new version is cheaper._
