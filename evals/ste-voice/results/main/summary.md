# STE + efficiency eval — main

```
date=2026-09-13T17:26:36
arms=baseline,ste
cases=voice-pass,article-devblog,article-p2
reps=3
model=claude-opus-5
claude=2.1.270 (Claude Code)
---
date=2026-09-13T17:39:43
arms=ste
cases=ste-audit,ste-apply,trigger,youtube-script,wnd-script
reps=3
model=claude-opus-5
claude=2.1.270 (Claude Code)
---
date=2026-09-13T17:48:33
arms=optimized
cases=article-devblog,article-p2,ste-apply,ste-audit,trigger,voice-pass,wnd-script,youtube-script
reps=3
model=claude-opus-5
claude=2.1.270 (Claude Code)
---
date=2026-09-13T17:58:56
arms=optimized-sonnet
cases=ste-audit,ste-apply,trigger
reps=3
model=claude-opus-5
claude=2.1.270 (Claude Code)
---
date=2026-09-13T18:18:53
arms=final
cases=ste-audit,ste-apply,trigger,ste-quick
reps=3
model=claude-opus-5
claude=2.1.270 (Claude Code)
---
date=2026-09-13T18:26:53
arms=optimized
cases=ste-quick
reps=3
model=claude-opus-5
claude=2.1.270 (Claude Code)
---
```

## article-devblog

Mean per arm (booleans as passes/runs).

| arm | n | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | admonitions | draft_saved | first_person_per_100w | full_transcript_read | make_sure | ref_files_read | ste_card_read | step_swap_words | steps | steps_le20_pct | voice_bans | words | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 3 | 3 | 27,879 | 71,928.3 | 5,206.7 | 0.319 | 3 | 69.3 | 1,566 | 0 | 3/3 | 0.5 | 0/3 | 0.3 | 1 | 0/3 | 0 | 0 | - | 0 | 879.3 | opus-5 |
| ste | 3 | 3 | 33,365.7 | 124,383.3 | 7,515 | 0.456 | 7 | 89.9 | 2,845 | 1 | 3/3 | 0.9 | 0/3 | 5 | 2 | 3/3 | 0 | 22.3 | 100 | 0 | 1,333.3 | opus-5 |
| optimized | 3 | 3 | 32,268 | 108,694 | 7,587.7 | 0.434 | 7 | 91.9 | 2,846 | 0.7 | 3/3 | 0.8 | 0/3 | 4 | 2 | 3/3 | 0 | 19 | 100 | 0 | 1,270.7 | opus-5 |

Delta vs `baseline`:

| arm | peak_main_ctx | total_in | cost_usd | ref_tokens_read |
|---|---|---|---|---|
| ste | 5,486.7 (+20%) | 52,455 (+73%) | 0.136 (+43%) | 1,279 (+82%) |
| optimized | 4,389 (+16%) | 36,765.7 (+51%) | 0.114 (+36%) | 1,280 (+82%) |

<details><summary>Per run</summary>

| arm | run | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | skills read |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | run-1 | y | 28,101 | 71,815 | 5,641 | 0.343 | 3 | 67.4 | 1,566 | write-article/references/writing-style.md |
| baseline | run-2 | y | 27,442 | 71,474 | 4,889 | 0.302 | 3 | 79.9 | 1,566 | write-article/references/writing-style.md |
| baseline | run-3 | y | 28,094 | 72,496 | 5,090 | 0.314 | 3 | 60.6 | 1,566 | write-article/references/writing-style.md |
| ste | run-1 | y | 32,067 | 110,967 | 6,583 | 0.424 | 5 | 81.2 | 2,845 | ste-pass/references/ste-card.md, write-article/references/writing-style.md |
| ste | run-2 | y | 34,317 | 148,606 | 8,139 | 0.487 | 9 | 94.1 | 2,845 | ste-pass/references/ste-card.md, write-article/references/writing-style.md |
| ste | run-3 | y | 33,713 | 113,577 | 7,823 | 0.456 | 7 | 94.6 | 2,845 | ste-pass/references/ste-card.md, write-article/references/writing-style.md |
| optimized | run-1 | y | 33,147 | 140,135 | 7,962 | 0.467 | 11 | 96.0 | 2,846 | ste-pass/references/ste-card.md, write-article/references/writing-style.md |
| optimized | run-2 | y | 32,679 | 109,631 | 8,083 | 0.451 | 6 | 97.1 | 2,846 | ste-pass/references/ste-card.md, write-article/references/writing-style.md |
| optimized | run-3 | y | 30,978 | 76,316 | 6,718 | 0.384 | 4 | 82.4 | 2,846 | ste-pass/references/ste-card.md, write-article/references/writing-style.md |

</details>

## article-p2

Mean per arm (booleans as passes/runs).

| arm | n | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | admonitions | draft_saved | first_person_per_100w | full_transcript_read | make_sure | ref_files_read | ste_card_read | step_swap_words | steps | steps_le20_pct | voice_bans | words | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 3 | 3 | 25,302.7 | 69,474 | 2,438 | 0.219 | 3 | 45.8 | 1,566 | 0 | 3/3 | 2.2 | 0/3 | 0 | 1 | 0/3 | 0 | 1.3 | 100 | 0 | 732.3 | opus-5 |
| ste | 3 | 3 | 28,450.7 | 76,225 | 2,733.3 | 0.280 | 4.3 | 57.0 | 2,845 | 0.3 | 3/3 | 2.1 | 0/3 | 2.7 | 2 | 3/3 | 0 | 1.3 | 75 | 0 | 788.7 | opus-5 |
| optimized | 3 | 3 | 24,838.7 | 68,100 | 2,315.7 | 0.211 | 3 | 38.9 | 1,660 | 0 | 3/3 | 2.1 | 0/3 | 1.7 | 1 | 0/3 | 0 | 0 | - | 0 | 677.3 | opus-5 |

Delta vs `baseline`:

| arm | peak_main_ctx | total_in | cost_usd | ref_tokens_read |
|---|---|---|---|---|
| ste | 3,148 (+12%) | 6,751 (+10%) | 0.061 (+28%) | 1,279 (+82%) |
| optimized | -464 (-2%) | -1,374 (-2%) | -0.008 (-4%) | 94 (+6%) |

<details><summary>Per run</summary>

| arm | run | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | skills read |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | run-1 | y | 25,392 | 69,374 | 2,644 | 0.225 | 3 | 43.6 | 1,566 | write-article/references/writing-style.md |
| baseline | run-2 | y | 25,301 | 69,481 | 2,340 | 0.217 | 3 | 55.1 | 1,566 | write-article/references/writing-style.md |
| baseline | run-3 | y | 25,215 | 69,567 | 2,330 | 0.216 | 3 | 38.6 | 1,566 | write-article/references/writing-style.md |
| ste | run-1 | y | 28,335 | 75,913 | 2,819 | 0.261 | 4 | 42.4 | 2,845 | ste-pass/references/ste-card.md, write-article/references/writing-style.md |
| ste | run-2 | y | 28,650 | 76,447 | 2,808 | 0.324 | 5 | 87.6 | 2,845 | ste-pass/references/ste-card.md, write-article/references/writing-style.md |
| ste | run-3 | y | 28,367 | 76,315 | 2,573 | 0.255 | 4 | 40.8 | 2,845 | ste-pass/references/ste-card.md, write-article/references/writing-style.md |
| optimized | run-1 | y | 24,756 | 68,069 | 2,143 | 0.206 | 3 | 36.0 | 1,660 | write-article/references/writing-style.md |
| optimized | run-2 | y | 24,799 | 68,015 | 2,353 | 0.212 | 3 | 39.1 | 1,660 | write-article/references/writing-style.md |
| optimized | run-3 | y | 24,961 | 68,216 | 2,451 | 0.216 | 3 | 41.7 | 1,660 | write-article/references/writing-style.md |

</details>

## ste-apply

Mean per arm (booleans as passes/runs).

| arm | n | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | admonitions | code_identical | fixture_changed | full_transcript_read | make_sure | overview_voice_kept | ref_files_read | ste_card_read | step_swap_words | steps | steps_le20_pct | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ste | 3 | 3 | 53,363.7 | 142,018.3 | 18,828.7 | 0.932 | 29 | 203.6 | 1,185 | 1.7 | 3/3 | 3/3 | 0/3 | 12.3 | 3/3 | 1 | 3/3 | 0 | 9.3 | 100 | opus-5 |
| optimized | 3 | 3 | 49,715.3 | 247,674.3 | 14,892.7 | 0.852 | 27.3 | 168.5 | 2,536 | 2.7 | 3/3 | 3/3 | 0/3 | 11.3 | 3/3 | 2 | 3/3 | 0 | 11 | 100 | opus-5 |
| optimized-sonnet | 3 | 3 | 59,244.3 | 508,906.7 | 19,661.7 | 0.482 | 26.7 | 210.2 | 2,086 | 1 | 3/3 | 3/3 | 0/3 | 5.3 | 3/3 | 1.7 | 3/3 | 0 | 2.3 | 100 | sonnet-5 |
| final | 3 | 3 | 43,674 | 150,332.7 | 8,426 | 0.738 | 21 | 186.2 | 2,536 | 1.3 | 3/3 | 3/3 | 0/3 | 5.3 | 3/3 | 2 | 3/3 | 0 | 14.7 | 100 | opus-5+sonnet-5 |

Delta vs `ste`:

| arm | peak_main_ctx | total_in | cost_usd | ref_tokens_read |
|---|---|---|---|---|
| optimized | -3,648.3 (-7%) | 105,656 (+74%) | -0.080 (-9%) | 1,351 (+114%) |
| optimized-sonnet | 5,880.7 (+11%) | 366,888.3 (+258%) | -0.449 (-48%) | 901 (+76%) |
| final | -9,689.7 (-18%) | 8,314.3 (+6%) | -0.194 (-21%) | 1,351 (+114%) |

<details><summary>Per run</summary>

| arm | run | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | skills read |
|---|---|---|---|---|---|---|---|---|---|---|
| ste | run-1 | y | 52,013 | 105,089 | 17,664 | 0.871 | 28 | 188.2 | 1,185 | ste-pass/references/ste-card.md |
| ste | run-2 | y | 53,809 | 213,621 | 19,239 | 0.982 | 29 | 209.3 | 1,185 | ste-pass/references/ste-card.md |
| ste | run-3 | y | 54,269 | 107,345 | 19,583 | 0.942 | 30 | 213.4 | 1,185 | ste-pass/references/ste-card.md |
| optimized | run-1 | y | 50,546 | 285,903 | 15,374 | 0.891 | 29 | 174.1 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| optimized | run-2 | y | 48,943 | 183,811 | 13,800 | 0.785 | 28 | 152.4 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| optimized | run-3 | y | 49,657 | 273,309 | 15,504 | 0.880 | 25 | 178.9 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| optimized-sonnet | run-1 | y | 53,385 | 178,245 | 15,220 | 0.391 | 18 | 155.7 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| optimized-sonnet | run-2 | y | 56,303 | 332,361 | 15,929 | 0.378 | 24 | 166.5 | 1,186 | ste-pass/references/ste-card.md |
| optimized-sonnet | run-3 | y | 68,045 | 1,016,114 | 27,836 | 0.679 | 38 | 308.4 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| final | run-1 | y | 48,173 | 155,958 | 12,093 | 0.911 | 25 | 257.5 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| final | run-2 | y | 41,140 | 147,549 | 6,473 | 0.658 | 16 | 161.7 | 2,536 | ste-audit/../ste-pass/scripts/ste-lint.py, ste-pass/references/ste-card.md |
| final | run-3 | y | 41,709 | 147,491 | 6,712 | 0.644 | 22 | 139.5 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |

</details>

## ste-audit

Mean per arm (booleans as passes/runs).

| arm | n | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | caught_choose | caught_fetch_loop | caught_ui_path | findings | fixture_unchanged | full_transcript_read | has_zone_map | ref_files_read | ste_card_read | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ste | 3 | 3 | 32,223 | 53,016 | 11,308.7 | 0.498 | 3 | 130.3 | 1,185 | 3/3 | 3/3 | 3/3 | 30 | 3/3 | 0/3 | 3/3 | 1 | 3/3 | opus-5 |
| optimized | 3 | 3 | 33,495.7 | 86,579.3 | 6,102 | 0.397 | 4 | 74.1 | 2,536 | 3/3 | 3/3 | 3/3 | 38.3 | 3/3 | 0/3 | 3/3 | 2 | 3/3 | opus-5 |
| optimized-sonnet | 3 | 3 | 40,792.7 | 189,384 | 9,771 | 0.270 | 6.7 | 102.1 | 2,536 | 3/3 | 3/3 | 3/3 | 20 | 3/3 | 0/3 | 3/3 | 2 | 3/3 | sonnet-5 |
| final | 3 | 3 | 33,077.7 | 103,331.3 | 3,421.3 | 0.571 | 4.3 | 175.0 | 2,986 | 3/3 | 3/3 | 3/3 | 20.3 | 3/3 | 0/3 | 3/3 | 2.3 | 3/3 | opus-5+sonnet-5 |

Delta vs `ste`:

| arm | peak_main_ctx | total_in | cost_usd | ref_tokens_read |
|---|---|---|---|---|
| optimized | 1,272.7 (+4%) | 33,563.3 (+63%) | -0.101 (-20%) | 1,351 (+114%) |
| optimized-sonnet | 8,569.7 (+27%) | 136,368 (+257%) | -0.228 (-46%) | 1,351 (+114%) |
| final | 854.7 (+3%) | 50,315.3 (+95%) | 0.072 (+14%) | 1,801 (+152%) |

<details><summary>Per run</summary>

| arm | run | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | skills read |
|---|---|---|---|---|---|---|---|---|---|---|
| ste | run-1 | y | 32,223 | 53,016 | 10,814 | 0.486 | 3 | 124.3 | 1,185 | ste-pass/references/ste-card.md |
| ste | run-2 | y | 32,223 | 53,016 | 11,291 | 0.498 | 3 | 130.8 | 1,185 | ste-pass/references/ste-card.md |
| ste | run-3 | y | 32,223 | 53,016 | 11,821 | 0.511 | 3 | 135.7 | 1,185 | ste-pass/references/ste-card.md |
| optimized | run-1 | y | 33,458 | 86,509 | 8,572 | 0.459 | 4 | 103.3 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| optimized | run-2 | y | 33,480 | 86,580 | 5,281 | 0.377 | 4 | 63.9 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| optimized | run-3 | y | 33,549 | 86,649 | 4,453 | 0.357 | 4 | 55.0 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| optimized-sonnet | run-1 | y | 42,724 | 277,885 | 8,012 | 0.298 | 9 | 93.2 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| optimized-sonnet | run-2 | y | 41,238 | 126,896 | 8,865 | 0.271 | 5 | 99.5 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| optimized-sonnet | run-3 | y | 38,416 | 163,371 | 12,436 | 0.241 | 6 | 113.5 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| final | run-1 | y | 32,987 | 102,895 | 4,030 | 0.590 | 4 | 159.3 | 3,886 | ste-audit/../ste-pass/scripts/ste-lint.py, ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| final | run-2 | y | 32,131 | 101,511 | 2,909 | 0.567 | 4 | 191.6 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| final | run-3 | y | 34,115 | 105,588 | 3,325 | 0.555 | 5 | 174.1 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |

</details>

## ste-quick

Mean per arm (booleans as passes/runs).

| arm | n | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | caught_choose | caught_doubled_word | findings | full_transcript_read | helper_used | lint_used | ref_files_read | ste_card_read | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| optimized | 3 | 3 | 22,375 | 42,640 | 2,555.7 | 0.181 | 2 | 38.1 | 1,186 | 3/3 | 3/3 | 4.3 | 0/3 | 0/3 | 0/3 | 1 | 3/3 | opus-5 |
| final | 3 | 3 | 22,324 | 42,540 | 2,226.3 | 0.172 | 2 | 30.0 | 1,186 | 3/3 | 3/3 | 0 | 0/3 | 0/3 | 0/3 | 1 | 3/3 | opus-5 |

Delta vs `optimized`:

| arm | peak_main_ctx | total_in | cost_usd | ref_tokens_read |
|---|---|---|---|---|
| final | -51 (-0%) | -100 (-0%) | -0.009 (-5%) | 0 (+0%) |

<details><summary>Per run</summary>

| arm | run | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | skills read |
|---|---|---|---|---|---|---|---|---|---|---|
| optimized | run-1 | y | 22,375 | 42,640 | 2,751 | 0.186 | 2 | 40.3 | 1,186 | ste-pass/references/ste-card.md |
| optimized | run-2 | y | 22,375 | 42,640 | 2,339 | 0.175 | 2 | 32.4 | 1,186 | ste-pass/references/ste-card.md |
| optimized | run-3 | y | 22,375 | 42,640 | 2,577 | 0.181 | 2 | 41.6 | 1,186 | ste-pass/references/ste-card.md |
| final | run-1 | y | 22,432 | 42,756 | 2,164 | 0.172 | 2 | 30.2 | 1,186 | ste-pass/references/ste-card.md |
| final | run-2 | y | 22,270 | 42,432 | 2,419 | 0.176 | 2 | 31.7 | 1,186 | ste-pass/references/ste-card.md |
| final | run-3 | y | 22,270 | 42,432 | 2,096 | 0.168 | 2 | 28.1 | 1,186 | ste-pass/references/ste-card.md |

</details>

## trigger

Mean per arm (booleans as passes/runs).

| arm | n | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | fixture_unchanged | full_transcript_read | ref_files_read | ste_card_read | ste_pass_invoked | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ste | 3 | 3 | 32,334 | 72,450 | 4,997 | 0.352 | 5 | 61.1 | 1,185 | 3/3 | 0/3 | 1 | 3/3 | 3/3 | haiku-4-5+opus-5 |
| optimized | 3 | 3 | 33,131.3 | 118,463.7 | 6,834.7 | 0.429 | 6.7 | 84.5 | 2,536 | 3/3 | 0/3 | 2 | 3/3 | 3/3 | haiku-4-5+opus-5 |
| optimized-sonnet | 3 | 3 | 33,392.3 | 119,079.7 | 5,387 | 0.396 | 6.7 | 69.2 | 2,536 | 3/3 | 0/3 | 2 | 3/3 | 3/3 | haiku-4-5+opus-5 |
| final | 3 | 3 | 35,062.7 | 125,125 | 3,745 | 0.554 | 7 | 155.2 | 2,536 | 3/3 | 0/3 | 2 | 3/3 | 3/3 | haiku-4-5+opus-5+sonnet-5 |

Delta vs `ste`:

| arm | peak_main_ctx | total_in | cost_usd | ref_tokens_read |
|---|---|---|---|---|
| optimized | 797.3 (+2%) | 46,013.7 (+64%) | 0.077 (+22%) | 1,351 (+114%) |
| optimized-sonnet | 1,058.3 (+3%) | 46,629.7 (+64%) | 0.043 (+12%) | 1,351 (+114%) |
| final | 2,728.7 (+8%) | 52,675 (+73%) | 0.202 (+57%) | 1,351 (+114%) |

<details><summary>Per run</summary>

| arm | run | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | skills read |
|---|---|---|---|---|---|---|---|---|---|---|
| ste | run-1 | y | 32,364 | 72,510 | 4,555 | 0.342 | 5 | 55.3 | 1,185 | ste-pass/references/ste-card.md |
| ste | run-2 | y | 32,338 | 72,458 | 4,972 | 0.352 | 5 | 61.9 | 1,185 | ste-pass/references/ste-card.md |
| ste | run-3 | y | 32,300 | 72,382 | 5,464 | 0.364 | 5 | 66.1 | 1,185 | ste-pass/references/ste-card.md |
| optimized | run-1 | y | 32,935 | 104,066 | 5,143 | 0.378 | 6 | 65.5 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| optimized | run-2 | y | 33,290 | 125,723 | 5,179 | 0.393 | 7 | 66.6 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| optimized | run-3 | y | 33,169 | 125,602 | 10,182 | 0.517 | 7 | 121.4 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| optimized-sonnet | run-1 | y | 33,347 | 125,946 | 5,147 | 0.393 | 7 | 67.0 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| optimized-sonnet | run-2 | y | 33,258 | 125,820 | 5,452 | 0.399 | 7 | 73.6 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| optimized-sonnet | run-3 | y | 33,572 | 105,473 | 5,562 | 0.395 | 6 | 67.2 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |
| final | run-1 | y | 35,823 | 126,255 | 3,421 | 0.586 | 7 | 185.6 | 2,536 | ste-audit/../ste-pass/scripts/ste-lint.py, ste-pass/references/ste-card.md |
| final | run-2 | y | 35,122 | 125,114 | 4,115 | 0.547 | 7 | 151.6 | 2,536 | ste-audit/../ste-pass/scripts/ste-lint.py, ste-pass/references/ste-card.md |
| final | run-3 | y | 34,243 | 124,006 | 3,699 | 0.530 | 7 | 128.6 | 2,536 | ste-pass/references/ste-card.md, ste-pass/scripts/ste-lint.py |

</details>

## voice-pass

Mean per arm (booleans as passes/runs).

| arm | n | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | action_lines_changed | code_identical | full_transcript_read | ref_files_read | ste_card_read | voice_lines_changed | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 3 | 3 | 36,471.3 | 152,634 | 3,849 | 0.409 | 10.7 | 53.5 | 5,904 | 0 | 3/3 | 0/3 | 1.3 | 0/3 | 4 | haiku-4-5+opus-5 |
| ste | 3 | 3 | 40,715.7 | 166,432.7 | 4,487.7 | 0.476 | 12.7 | 59.7 | 7,673.7 | 0 | 3/3 | 0/3 | 2.7 | 3/3 | 4 | haiku-4-5+opus-5 |
| optimized | 3 | 3 | 36,441 | 135,460 | 4,149 | 0.402 | 11.3 | 51.6 | 5,685 | 0 | 3/3 | 0/3 | 2.3 | 3/3 | 3.7 | haiku-4-5+opus-5 |

Delta vs `baseline`:

| arm | peak_main_ctx | total_in | cost_usd | ref_tokens_read |
|---|---|---|---|---|
| ste | 4,244.3 (+12%) | 13,798.7 (+9%) | 0.067 (+16%) | 1,769.7 (+30%) |
| optimized | -30.3 (-0%) | -17,174 (-11%) | -0.007 (-2%) | -219 (-4%) |

<details><summary>Per run</summary>

| arm | run | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | skills read |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | run-1 | y | 35,185 | 128,177 | 3,624 | 0.389 | 10 | 46.6 | 5,382 | youtube-script/references/style-card.md |
| baseline | run-2 | y | 38,813 | 167,903 | 4,349 | 0.446 | 12 | 56.2 | 6,948 | write-article/references/writing-style.md, youtube-script/references/style-card.md |
| baseline | run-3 | y | 35,416 | 161,822 | 3,574 | 0.391 | 10 | 57.7 | 5,382 | youtube-script/references/style-card.md |
| ste | run-1 | y | 42,043 | 176,699 | 4,995 | 0.513 | 14 | 64.8 | 8,227 | ste-pass/references/ste-card.md, write-article/references/writing-style.md, youtube-script/references/style-card.md |
| ste | run-2 | y | 41,687 | 177,209 | 4,531 | 0.482 | 13 | 59.0 | 8,227 | ste-pass/references/ste-card.md, write-article/references/writing-style.md, youtube-script/references/style-card.md |
| ste | run-3 | y | 38,417 | 145,390 | 3,937 | 0.432 | 11 | 55.3 | 6,567 | ste-pass/references/ste-card.md, youtube-script/references/style-card.md |
| optimized | run-1 | y | 35,070 | 106,633 | 3,718 | 0.364 | 10 | 47.2 | 5,175 | ste-pass/references/ste-card.md, youtube-script/references/style-card.md |
| optimized | run-2 | y | 39,426 | 171,320 | 5,378 | 0.479 | 14 | 65.1 | 6,705 | ste-pass/references/ste-card.md, youtube-script/references/refinement-log.md, youtube-script/references/style-card.md |
| optimized | run-3 | y | 34,827 | 128,427 | 3,351 | 0.363 | 10 | 42.5 | 5,175 | ste-pass/references/ste-card.md, youtube-script/references/style-card.md |

</details>

## wnd-script

Mean per arm (booleans as passes/runs).

| arm | n | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | branded_greeting | full_transcript_read | have_a_good_one | ref_files_read | samples_read | ste_card_read | teleprompter_saved | voice_bans | words | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ste | 3 | 3 | 54,843.3 | 215,698.7 | 6,956.3 | 0.686 | 10 | 87.1 | 11,325 | 3/3 | 3/3 | 3/3 | 4 | 1 | 0/3 | 3/3 | 0 | 2,219.7 | opus-5 |
| optimized | 3 | 3 | 50,741 | 175,422.3 | 6,549 | 0.617 | 9.7 | 80.8 | 9,454 | 3/3 | 0/3 | 3/3 | 4 | 0 | 0/3 | 3/3 | 0 | 2,183.7 | opus-5 |

Delta vs `ste`:

| arm | peak_main_ctx | total_in | cost_usd | ref_tokens_read |
|---|---|---|---|---|
| optimized | -4,102.3 (-7%) | -40,276.3 (-19%) | -0.069 (-10%) | -1,871 (-17%) |

<details><summary>Per run</summary>

| arm | run | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | skills read |
|---|---|---|---|---|---|---|---|---|---|---|
| ste | run-1 | y | 54,209 | 197,046 | 6,520 | 0.660 | 9 | 82.8 | 11,325 | wnd-script/references/wnd-format.md, wnd-script/references/wnd-series-card.md, wnd-script/references/wnd-voice-samples/2026-01-january.txt, youtube-script/references/style-card.md |
| ste | run-2 | y | 55,855 | 252,723 | 7,552 | 0.729 | 12 | 92.9 | 11,325 | wnd-script/references/wnd-format.md, wnd-script/references/wnd-series-card.md, wnd-script/references/wnd-voice-samples/2026-01-january.txt, youtube-script/references/style-card.md |
| ste | run-3 | y | 54,466 | 197,327 | 6,797 | 0.669 | 9 | 85.5 | 11,325 | wnd-script/references/wnd-format.md, wnd-script/references/wnd-series-card.md, wnd-script/references/wnd-voice-samples/2026-01-january.txt, youtube-script/references/style-card.md |
| optimized | run-1 | y | 51,578 | 193,134 | 7,239 | 0.651 | 11 | 88.9 | 9,454 | wnd-script/references/wnd-format.md, wnd-script/references/wnd-series-card.md, wnd-script/references/wnd-voice-samples/excerpts.md, youtube-script/references/style-card.md |
| optimized | run-2 | y | 50,735 | 191,929 | 6,465 | 0.623 | 10 | 81.1 | 9,454 | wnd-script/references/wnd-format.md, wnd-script/references/wnd-series-card.md, wnd-script/references/wnd-voice-samples/excerpts.md, youtube-script/references/style-card.md |
| optimized | run-3 | y | 49,910 | 141,204 | 5,943 | 0.577 | 8 | 72.3 | 9,454 | wnd-script/references/wnd-format.md, wnd-script/references/wnd-series-card.md, wnd-script/references/wnd-voice-samples/excerpts.md, youtube-script/references/style-card.md |

</details>

## youtube-script

Mean per arm (booleans as passes/runs).

| arm | n | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | full_transcript_read | next_one_signoff | ref_files_read | script_saved | ste_card_read | voice_bans | words | models |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ste | 3 | 3 | 68,372.3 | 256,432 | 8,445.3 | 0.872 | 9.7 | 110.2 | 9,938 | 0/3 | 3/3 | 3 | 3/3 | 0/3 | 0 | 2,116 | opus-5 |
| optimized | 3 | 3 | 67,514.7 | 266,811 | 11,162.3 | 0.937 | 10.7 | 138.0 | 8,545 | 0/3 | 3/3 | 3 | 3/3 | 0/3 | 0.3 | 2,033 | opus-5 |

Delta vs `ste`:

| arm | peak_main_ctx | total_in | cost_usd | ref_tokens_read |
|---|---|---|---|---|
| optimized | -857.7 (-1%) | 10,379 (+4%) | 0.065 (+7%) | -1,393 (-14%) |

<details><summary>Per run</summary>

| arm | run | ok | peak_main_ctx | total_in | total_out | cost_usd | turns | duration_s | ref_tokens_read | skills read |
|---|---|---|---|---|---|---|---|---|---|---|
| ste | run-1 | y | 79,086 | 276,119 | 8,192 | 0.978 | 11 | 106.2 | 9,938 | youtube-script/references/format-template.md, youtube-script/references/style-card.md, youtube-script/references/voice-samples/excerpts.md |
| ste | run-2 | y | 78,823 | 315,342 | 8,189 | 0.995 | 11 | 109.8 | 9,938 | youtube-script/references/format-template.md, youtube-script/references/style-card.md, youtube-script/references/voice-samples/excerpts.md |
| ste | run-3 | y | 47,208 | 177,835 | 8,955 | 0.645 | 7 | 114.6 | 9,938 | youtube-script/references/format-template.md, youtube-script/references/style-card.md, youtube-script/references/voice-samples/excerpts.md |
| optimized | run-1 | y | 47,387 | 172,155 | 11,883 | 0.717 | 8 | 145.0 | 8,545 | youtube-script/references/format-template.md, youtube-script/references/style-card.md, youtube-script/references/voice-samples/excerpts.md |
| optimized | run-2 | y | 77,673 | 351,609 | 9,810 | 1.043 | 14 | 122.9 | 8,545 | youtube-script/references/format-template.md, youtube-script/references/style-card.md, youtube-script/references/voice-samples/excerpts.md |
| optimized | run-3 | y | 77,484 | 276,669 | 11,794 | 1.053 | 10 | 146.1 | 8,545 | youtube-script/references/format-template.md, youtube-script/references/style-card.md, youtube-script/references/voice-samples/excerpts.md |

</details>
