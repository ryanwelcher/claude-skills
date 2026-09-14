I rewrote the steps, requirements, warnings and UI paths in `fixtures/meme-generator.md` in hybrid mode and applied all 26 findings in place. The intros, explanations and closings are unchanged. The linter now reports 0 hits.

**What changed:**
- **One action per step (rules 2, 3):** mixed "save, refresh, open the console" sentences are now numbered steps.
- **Checks at the end (rule 7):** every procedure now ends with a "Make sure that…" check. That covers both setup paths, each `useEffect` change, each set of block.json supports, and the font install.
- **Warnings before the step (rule 6):**
  - Before the first fetch code, a **CAUTION:** now says the fetch runs over and over and can crash the browser. The original only said this after the step.
  - The Docker requirement is now a **NOTE:** at the top of Repository instead of a note inside the step.
  - A new **NOTE:** says the `__experimental` properties can change in a future WordPress release.
- **Clear code locations (rule 16):** each "add the following" now says where the code goes, for example "In edit.js, replace the Edit function…" or "inside the meme_generator_block_init function…".
- **Word swaps and rules 9, 13:** "choose" is now "select", "update" is now "change", "A LOT of" is now "many", "once" is now "after", "open up" is now "open", and I removed "just" and "you should".
- **Table (rule 14):** the explanation of the block.json supports settings is now a Property / Value / Reason table.
  - I added the `html: false` row. The original paragraph never explained that setting, so check that my wording is right.
- **Full UI paths (rules 1, 15):** "the Style section of the Site Editor" is now a step-by-step path: **Appearance > Editor > Styles > Typography**, then **Manage fonts**, then the **Install Fonts** tab. I wrote those labels from memory of WordPress 6.5+, so check them against the current UI before publishing.

**Also added:** steps to activate the plugin under **Plugins > Installed Plugins** in the Standalone setup.

**No refinement-log entries:** every fix used an existing rule on the card.

**Still open (I left these alone):**
- **Headings:** "Setting up…", "Getting the images" and "Formatting the text" break the no -ing openers rule (11). Changing them would break page anchor links.
- **"Stick a fork in it…":** the card uses this exact idiom as a bad example, but it's in the closing, which keeps your voice.
- **Line ~398 typo:** it says `addImages`, but the code uses `allImages`.
- **Typos in explanation text:** "attribute be", "the will", "It we", and a trailing comma.
- **Step numbers:** they jump 1 → 3 → 8 → 9. This looks like an excerpt, so I didn't renumber.