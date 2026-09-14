I applied all 16 STE fixes to `fixtures/meme-generator.md` in hybrid mode, using the full path through the `ste-audit` helper. All the edits matched the file, and I didn't change any code blocks, links, or voice zones.

**What changed:**
- **Setup, Standalone, Repository:**
  - The setup choice is now a two-item list (R2).
  - The loose "Instructions" lines are now numbered steps (R2).
  - The Docker requirement now comes before the step that needs it (R6).
  - I fixed "completed completed" and added a check at the end of each procedure (R7).
- **Long sentences split to fit the word limits (R1):** lines 69, 200, 402, 444 and 668.
- **Word swaps:**
  - update → change
  - allow → let
  - choose/pick → select
  - "a lot of" → many (in the fetch-loop warning)
- **Other rules:**
  - "you should now see" is gone (R13).
  - "Open up" is now "Open" (R9).
  - "the Style section" is now a full path (R15).
- **Grammar and typos:** "The image attribute be", "the will trigger", "provded", "crash browser".

**Where I changed the helper's rewrite:**
- **#10 (line 402):** The helper suggested "Select and change the image to control how the text looks." That changes the meaning, so I used: "The block needs controls for how the text looks and where it sits on the image."
- **#16:** The helper's path was **Site Editor > Styles > Typography**, which isn't a real menu path. I used **Appearance > Editor > Styles > Typography**. Check it against the current WordPress screen.

**Still open (I didn't touch these):**
- **Broken command on line 21:** `–template` uses an en dash, so the `npx` command fails as written. It needs to be `--template`. It's inside a code block, which this pass never changes, so fix it by hand.
- **Closing line:** "Stick a fork in it…" is an idiom, but it's in a voice zone, so hybrid mode leaves it alone.
- **Step numbers:** the headings jump from Step 1 to 3, 8 and 9, which suggests steps 2 and 4–7 are missing from the draft.
- **Section headings:** they still start with -ing words ("Setting up", "Getting", "Formatting"). The helper didn't flag them.

I didn't add anything to the refinement log, because every fix used an existing card rule.