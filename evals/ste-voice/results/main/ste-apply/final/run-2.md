I applied all 12 findings to `fixtures/meme-generator.md` in hybrid mode. The file had about 60 lines of prose, so the `ste-audit` helper did the audit. I didn't change any code blocks, links, screenshots or voice zones.

**What changed:**
- **Setup:** the Standalone and Repository sections are now numbered steps with one action each (R2, R3). The "completed completed" typo is fixed and "Once" is now "After" (word swap). The Docker requirement is a NOTE on the step that needs it. The clone step is marked "Optional:" (R13). Both sections end with a check (R7).
- **Step 1:** I split the 32-word sentence about the attributes (R1), and "update" is now "Change" (word swap).
- **Step 3:** "retrieve" is now "get". A CAUTION about the browser crashing now comes before the "open the console" action (R6), and "A LOT of" is now "many".
- **Step 8:** the paragraph about the supports settings is now a table (R14). The three "you should now see" lines are now "Make sure that…" checks (R7, R13). I fixed "Do do" and removed "let's" (R3).
- **Step 9:** "Open up" is split into two steps (R2, R9). The vague "Style section" is now a full path with a check (R15).

**Where I didn't follow the helper exactly:**
- **Finding 10:** I used **Appearance > Editor > Styles** instead of the helper's "Site Editor > Styles". The card's R15 uses that path as its example, and it matches the real WordPress menu.
- **Finding 12:** I kept "Save the file and refresh the page" before "Open the console" so the reader doesn't lose that action.

**Worth checking:**
- **The two setup checks:** the helper made up "Make sure that the plugin/block appears in the block inserter". The original recipe doesn't say this, so confirm it's the right success check.
- **The new CAUTION:** it tells readers "Do not leave the block open", which the original never said. Its only warning was that leaving the page running long enough crashes the browser. Check that the new wording matches what you want readers to do.

**Still open (not applied):**
- **Broken code (not an STE issue):** the `create-block` command has an en dash (`–template`), and every code block uses curly quotes. Both will break the code when readers copy it.
- **Step numbers:** the headings skip from 1 to 3 to 8 to 9.
- **Closing idiom:** "Stick a fork in it…" is in a voice zone, so hybrid mode leaves it.

I didn't add any refinement-log entries, because every fix came from rules already in the card.