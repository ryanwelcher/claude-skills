I ran an STE pass on `fixtures/meme-generator.md` and haven't edited the file. It's a Block Developer Cookbook recipe, so the pass only touches the parts where readers do something: setup, steps, checks and UI paths. The intro, the explanations and the closing jokes stay as they are.

## Setup (lines 11–63)

**1. Line 13:** "You can choose to either use the repository… or to just download the standalone plugin"
Uses "choose", hedges with "just", and gives two options in one sentence.
→ "Select a setup option:" followed by a two-item list: **Standalone** (download the plugin) and **Repository** (use the repository, which includes a development environment).

**2. Standalone (lines 17–30):** the steps are written as paragraphs, "completed completed" is repeated, and "Once" is used to mean "after".
→
1. Open a terminal in the `plugins` directory of your local WordPress installation.
2. Run the following command: *(code block unchanged)*
3. After the scaffold completes, go to the new plugin directory and start the build process: *(code block unchanged)*
4. Activate the plugin.

Make sure that the plugin shows as active in the Plugins list.

**3. Repository (lines 34–63):** same problems as the Standalone section. Docker also appears as an aside in brackets in the middle of a step.
→ Put a prerequisite before the list: "**Requirement:** Docker must be installed."
1. Optional: if you do not have the repository, clone it: *(code)*
2. Install the dependencies: *(code)*
3. Start the development environment: *(code)*
4. From the root of the repository, run: *(code)*
5. After the scaffold completes, go to the new plugin directory and start the build process: *(code)*

Make sure that the build process finishes with no errors.

## Step 1 (line 71)

**4.** "Open the block.json file and update it with the following attribute definitions"
Two actions in one step, and "update" should be "change".
→ "1. Open `block.json`. 2. Change the attributes to match the following:"

## Step 3 (lines 200–398)

**5. Line 200:** "Save, refresh, and open the console. Do you notice that something? There are A LOT of messages… you'll crash browser."
The risk of a browser crash is mentioned only after the step, and it's phrased as a question with slang.
→ Put a caution **before** the "Add the following to edit.js" step (line 130): "**CAUTION:** Do not leave the editor open for a long time with this code. The repeated requests can crash the browser."
Then line 200 becomes: "Save and refresh the page. Open the browser console. Make sure that the console shows many repeated messages from the fetch call."

**6. Line 204:** "Remove the fetch call (for now) and update edit.js with the following:"
→ "1. Remove the fetch call. 2. Change `edit.js` to match the following:"

**7. Line 267:** "Update the hook with the following:" → "Change the hook to match the following:"

**8. Line 328:** "Now, you'll see that the hook is only run once ever… so let's add that into the hook."
→ "Make sure that the console message shows only one time. Add the fetch call to the hook:"

**9. Line 398:** "stored in the addImages variable". The code uses `allImages`, so this name is wrong in the text. Readers who don't speak English well will depend on the name matching the code exactly.
→ "…stored in the `allImages` variable."

## Step 8 (lines 406–547)

**10. Line 406:** "Open up block.json and add the following to the supports property"
"Open up" is a phrasal verb, and there are two actions.
→ "1. Open `block.json`. 2. In the `supports` property, add the following:"

**11. Line 444:** one sentence is 34 words (the limit is 25). It also uses "allows" and "pick", and "provded" is misspelled.
→ "This configuration lets the user select a text color from the theme's color palette. Text background color is on by default. This configuration turns it off because the block does not use it. The contrast checker is also off. It compares the text color with the theme background color, so it can show an incorrect warning."

**12. Line 446:** "Refresh the block and you should now see the option to choose the text color:"
→ "Refresh the page. Make sure that the text color option shows in the block settings."

**13. Line 452:** "Update block.json with the following:" → "Change `block.json` to match the following:"

**14. Line 494:** "Refresh the block again and you can now set the font size…"
→ "Refresh the page. Make sure that the font size and text alignment options show."

**15. Line 498:** "Do do this we're going to use some experimental properties on block.json" ("Do do" is a typo, and "we're going to" isn't an instruction).
→ "In `block.json`, add the experimental font properties to `supports`:"

**16. Line 543:** "Refresh and you'll see some new options for controlling the font in the block sidebar"
→ "Refresh the page. Make sure that the font family, style, and weight options show in the block sidebar."

## Step 9 (lines 555–674)

**17. Line 555:** "Open up meme-generator.php and add the following code inside the init hook callback:"
→ "1. Open `meme-generator.php`. 2. In the `init` hook callback, add the following code:"

**18. Line 668:** "Save the change and if you look in the Style section of the Site Editor…" is 26 words and doesn't give a full UI path.
→ "Save the change. Go to **Appearance > Editor > Styles > Typography**. Make sure that the new fonts show as ready to install." *(Check the menu labels against the WordPress version you target before publishing.)*

**19. Line 672:** "After installing the fonts, they are available in the block."
This sentence has no named actor and no check.
→ "Install the fonts. Make sure that the fonts show in the block's font family list."

## Borderline

- **Heading numbers skip:** Step 1, then 3, then 8, then 9. If no steps are missing, number them 1 to 4.
- **Line 444 zone:** it explains *why* the settings are what they are, so you could treat it as your own voice and leave it alone. I included it only because it's long and has a typo.
- **Line 21, outside STE scope:** `–template` uses an en dash, so the command will fail if someone copies it. It should be `--template`. The code blocks also use curly quotes (`“ ”`, `‘ ’`), which break JSON, JS and PHP when copied. I didn't propose fixes for these because the STE rules don't allow changes to code. They're still real bugs.

The intro (line 9), "Great work!" (line 547) and "Stick a fork in it… bon appetite!" (line 676) are your voice, so I left them out of this pass.