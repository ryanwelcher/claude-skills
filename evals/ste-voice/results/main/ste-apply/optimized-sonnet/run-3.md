Ran a final lint pass to confirm. Two remaining flags are false positives worth noting, not further edits:

- **L35** "Check out the repository" — flagged as phrasal verb, but this is the correct git-domain term (`git checkout`), which is a technical verb the card explicitly allows to stay unchanged.
- **L204, L413, L563** "procedure does not end with a check" — these are short 2-step lists (open file → add code) that are immediately followed by a code block and then more instructions/checks later in the same section. The linter treats each isolated list as a complete procedure; the actual final checks exist further down in each of these sections. No edit needed.

## Report

**Mode:** Hybrid (Block Developer Cookbook default — action zones only; confirmed against the card's Destination defaults table).

**Fixes applied** (29 findings, all approved and applied):
- **Setup**: rewrote non-imperative/hedged intro (rule 3/13), fixed "once" swap + duplicate word (word swap), moved conditions before actions (rule 5), moved a Docker prerequisite into a NOTE before the step (rule 6).
- **Step 1**: split an oversized sentence and dropped humor "hilarious" (rules 1, 8); word swap update→change.
- **Step 3**: split oversized sentences (rule 1), word swaps retrieve→get, trigger→start; converted a browser-crash risk into a CAUTION placed *before* the step and split a 3-action sentence into 3 steps (rules 2, 6); fixed non-imperative "let's" phrasing (rule 3); switched a passive sentence to active voice (rule 4).
- **Step 8**: split oversized/multi-swap sentences (rules 1, "choose/update"→"select/change"); split a 2-action "Open up… and add…" step into two steps and dropped the phrasal verb "up" (rules 2, 9); added missing final checks (rule 7) after the color/typography/font-family sub-steps; rewrote a gerund-opening sentence (rule 11).
- **Step 9**: dropped the idiom "at the mercy of" and non-imperative "let's" (rules 3, 8); split "Open up… and add…" into two steps (rules 2, 9); converted a three-source prose comparison into a table (rule 14); dropped "deeper dive" (rule 8/9); fixed UI navigation to a full click path, **Appearance > Editor > Styles** (rule 15); added a missing final check before the closing line (rule 7).

**Refinement log:** No new rules — every fix maps to an existing card rule or word swap, so nothing was added to `ste-card.md` or `refinement-log.md`.

**Left untouched (voice zones, correctly so):** the Overview intro, the "Great work!" and "Stick a fork in it…" closings, and two conceptual "why useEffect exists" explanatory passages (originally flagged as borderline) — these are reasoning asides/closings per the card's Zones table.

**Out of scope (not fixed, flagged for awareness):**
- Smart/curly quotes and an en-dash inside every code block and the `npx` command — these would break the code as written, but "Never change: code blocks, commands" puts them off-limits for this skill.
- Missing "Step 2" and "Step 4–7" headings (numbering jumps from 1→3→8→9) — a structural/content gap, not an STE style issue.
- `allImages`/`addImages` naming mismatch between code and prose — fixed incidentally while rewriting L398 for active voice, but flagging since it's a content-accuracy issue outside STE's remit.