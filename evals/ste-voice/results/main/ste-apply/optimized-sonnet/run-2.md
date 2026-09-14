All 19 fixes applied. Report:

**Mode:** Hybrid (action zones only) — matches the card's default for Block Developer Cookbook.

**Note:** the linter (`scripts/ste-lint.py`) lives outside this session's allowed directories, so I couldn't run it — all findings came from manual judgment against the card's rules.

**Fixes applied**, tied to card rules:
- Setup comparison → table (Rule 14)
- "once" → "after" swap, duplicate word (×2, Standalone/Repository)
- Docker prerequisite moved before the step it gates (Rule 6)
- Split two-action steps into single-action steps (Rule 2): block.json open+update, fetch remove+update, "open up" + add (×2), save+check style path
- Removed phrasal verb "open up" → "open" (Rule 9)
- Added missing `**CAUTION:**` before the unguarded fetch call, moved ahead of the code it warns about (Rule 6)
- Replaced rhetorical/non-imperative narration ("Do you notice that something?", "let's… Do do this we're going to use…") with direct imperatives (Rule 3)
- "A LOT of" → "many" (word swap)
- "update"/"choose" → "change"/"select" (word swaps, several places)
- Removed hedging ("you should now see", "you can now see") for direct "Make sure that…" checks (Rules 7, 13)
- Vague "Style section of the Site Editor" → full path **Appearance > Editor > Styles** (Rule 15)
- "-ing" as noun ("for controlling the font") → "to control the font" (Rule 11)
- Idiom "Stick a fork in it… bon appetite!" → "The procedure is complete." (Rule 8's own example, applied as this step's final check)

**Left untouched (voice zones):** the overview, all "why we're doing this" explanations, transitions ("Let's start with…", "Next, let's add…"), and the closing "Great work!" line — those stay in Ryan's voice per hybrid mode.

**Not touched (out of scope for STE):** curly quotes inside JSON/PHP code blocks and the `–template` en-dash in the CLI command are pre-existing bugs, not STE violations — "Never change code/commands" protects them here, but you may want a separate pass to fix the broken syntax. Also left the "Step 3/8/9" heading-number gap alone — that's a structural issue, not a card rule.

**Borderline, resolved:**
- Line 328 ("Now, you'll see…let's add that into the hook") — left as voice-zone transition, not rewritten.
- The final "Stick a fork in it" line — resolved as action-zone (procedure-end check) since it matches the card's Rule 8 example exactly.

No new rules came out of this pass, so nothing was added to the card or `refinement-log.md`.