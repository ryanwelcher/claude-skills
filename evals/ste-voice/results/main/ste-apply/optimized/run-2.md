I rewrote the action zones of `fixtures/meme-generator.md` in hybrid mode and applied all 26 findings in place. A re-run of the linter found 0 hits. That second run only checks lines already formatted as steps, bullets, notes, or tables, so it proves less than the first run over the full line ranges.

**What changed, by card rule:**
- **Word swaps and hedging (R13):** changed "choose", "update", "a lot of", "once", "you should" and "just" to the approved words.
- **One action per step (R2) and condition first (R5):** split the combined instructions in Setup, Step 1 and Step 3. "Skip this step if already done" now comes before the clone step.
- **Warnings before the step (R6):** added a CAUTION before the step for Docker and one for the fetch loop that crashes the browser. Before this, both came after the step.
- **Final checks (R7):** added "Make sure that…" lines after the plugin activation, the build, each `useEffect` change, each `supports` change, and the font install.
- **Anchors and UI paths (R15, R16):** every code step now names its file (`block.json`, `src/edit.js`, `meme-generator.php`) and where the code goes. "Look in the Style section" is now **Appearance > Editor > Styles > Typography**.
- **Tables (R14):** the two setup options and the `color` support settings are now tables instead of prose.
- **Other:** added a NOTE that `__experimental` properties can change, and removed the "Do do this" typo from the same sentence.

I left all voice zones alone: the overview, the explanations of why `useEffect` works this way, "Great work!", and the other asides.

**Borderline findings, listed but not applied:**
- **B1:** The headings ("Setting up…", "Getting…", "Formatting…") break R9 and R11. Changing them could break existing anchor links.
- **B2:** "Stick a fork in it…" is in the closing, which is a voice zone.
- **B3:** The font library path and the **Meme fonts** label may differ between WordPress versions. Check them against a screenshot.

**Problems outside STE (not changed):**
- The `create-block` command uses an en dash (`–template`), so it will fail when copied. I didn't touch it because the card says never to change commands.
- The recipe's quotes are curly, which breaks the JSON, JS and PHP when copied.
- The step numbers skip (1, 3, 8, 9).
- The explanation paragraph near the end of Step 3 says `addImages`, but the code uses `allImages`.

**Refinement log:** I added no entries because every fix matched a rule already on the card.