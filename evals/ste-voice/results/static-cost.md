# Static context cost (estimated tokens loaded before writing)

| skill / path | baseline | ste | optimized | baseline → optimized |
|---|---|---|---|---|
| write-article: tutorial | 2,706 | 4,272 | 3,844 | +1,138 (+42%) |
| write-article: P2 post | 2,706 | 3,087 | 2,658 | -48 (-2%) |
| ste-pass | - | 2,307 | 2,440 | new |
| sounds-like-me: written draft | 6,825 | 8,228 | 6,814 | -11 (-0%) |
| sounds-like-me: WND teleprompter | 9,727 | 9,945 | 8,139 | -1,588 (-16%) |
| youtube-script: write | 11,806 | 11,806 | 10,417 | -1,389 (-12%) |
| youtube-script: write + deep soak (worst case) | 31,238 | 31,238 | 10,417 | -20,821 (-67%) |
| wnd-script (typical: one sample) | 14,104 | 14,104 | 12,241 | -1,863 (-13%) |
| wp-workshop-scaffold: create | 3,051 | 3,187 | 2,343 | -708 (-23%) |
| wp-workshop-scaffold: audit | 3,051 | 3,187 | 2,925 | -126 (-4%) |
| wp-workshop-scaffold: reformat | 3,051 | 3,187 | 3,340 | +289 (+9%) |
| all devrel skill descriptions (every session) | 1,018 | 1,156 | 676 | -342 (-34%) |
