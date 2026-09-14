I applied all 30 findings to `fixtures/meme-generator.md` in hybrid mode. Nothing outside the action zones changed. I didn't reread the whole file after the edits.

**What changed, by card rule:**
- **Warnings before the step (Rule 6):** Step 3 now has a `**CAUTION:**` about the browser crash before the first `edit.js` code block. The Docker requirement is now its own step, before `npm run env start`.
- **One action per step (Rules 2 and 3):** I split the combined save/refresh/open steps, the "open and update" steps and the "remove and update" step into separate lines. The "let's"/"you'll see" wording inside instructions is now plain commands.
- **A check at the end of each procedure (Rule 7):** 14 new "Make sure that…" lines: both setup paths, Step 1, each refresh in Steps 3 and 8, and the font install in Step 9.
- **Full UI paths (Rule 15):** "activate the plugin" now says **Plugins > Installed Plugins**. "The Style section of the Site Editor" is now **Appearance > Editor > Styles > Typography**.
- **Clear code locations (Rule 16):** every instruction now names the file and where the code goes. For example: "In `meme-generator.php`, inside `meme_generator_block_init()`, below `register_block_type()`…"
- **Tables (Rule 14):** four new tables: the two setup options, the `useEffect` dependency parameter, the three `color` properties, and the font sources.
- **Word swaps and Rules 5, 9, 11 and 13:** "once" is now "after", "choose" is "select", "update" is "add"/"replace", and "a lot" is "many". I also removed "open up", "just", the "(skip this step if already done)" note and the "After installing" opener. "Checkout the repository" is now an "Optional: If…" step, and "Run the following script from the root" now leads with the location.

**Refinement log:** no entries. You approved the findings but didn't ask for any new rule, and every fix uses a rule already on the card. The card is in the eval snapshot, not the plugin cache, so nothing will be lost on update.

**Left open (borderline, not applied):**
- **Step headings:** "Setting up…", "Getting…" and "Formatting…" break Rules 9 and 11. I left them because renaming them changes the anchor links.
- **Closing line:** "Stick a fork in it, you're done!" is in a voice zone, even though the card uses it as its idiom example.
- **Full-file code blocks:** Rule 16 says to show only the changed code, but the card also says never to change code. Trimming the blocks is your call.
- **Wrong variable name:** l.398 says `addImages`, but the code uses `allImages`. There are also typos in voice zones ("the will trigger", "It we add", "provded", "overlayed"), and the step numbers jump from 1 to 3 to 8 to 9.
- **Unconfirmed UI labels:** "Open the font library" is a general description; I didn't confirm the button label. I also didn't check the **Color** > **Text** labels against a live editor.