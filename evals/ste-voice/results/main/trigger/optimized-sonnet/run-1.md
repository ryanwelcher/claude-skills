I ran an STE pass on `fixtures/meme-generator.md` in **hybrid mode**. That means I changed only the parts where readers act: steps, prerequisites, warnings and UI paths. The intros and asides stay in Ryan's voice. I made no edits to the file.

## Zone map

| Lines | Section | Zone |
|---|---|---|
| 3–9 | Title, time, Overview | Voice |
| 13 | Setup | Action (a choice of path) |
| 17–30 | Standalone | Action |
| 34–62 | Repository | Action |
| 67–69 | Step 1 explanation | Voice |
| 71 | Step 1 instruction | Action |
| 104–106, 128 | Step 3 API explanation | Voice |
| 130, 200, 204 | Step 3 instructions and the crash note | Action |
| 202 | useEffect explanation | Voice |
| 265 | Mixed: an instruction, then an explanation | Action + Voice |
| 267, 328 | Instructions | Action |
| 398, 402–404, 444, 450, 547 | Transitions and explanations | Voice |
| 406, 446, 452, 494, 498, 543 | Step 8 instructions and checks | Action |
| 551–553, 664–666 | Step 9 explanations | Voice |
| 555, 668–674 | Step 9 instructions and checks | Action |
| 676 | Closing | Voice |

## Findings

### Setup
1. **L13** "You can choose to either use the repository which provides a development environment or to just download the standalone plugin"
   *Rules: Word swaps (choose), R13 (just), R1, R14.*
   → "Select one of the two setup options below:" followed by a table:
   | Option | Use it when |
   |---|---|
   | **Standalone** | You already have a local WordPress installation. |
   | **Repository** | You want a full development environment. Docker is necessary. |

### Standalone
2. **L18** "Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation."
   *Rules: R2 (two actions), R13 ("of your choice").*
   → Two steps: "1. Open a terminal." "2. Go to the `wp-content/plugins` directory of your local WordPress installation." Then: "3. Run this command:"
3. **L24** "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
   *Rules: Word swaps (once), R2, and a repeated word.*
   → "4. When the command is complete, go to the `meme-generator` directory and start the build:"
4. **L30** "Finally, make sure to activate the plugin."
   *Rules: R15 (no click path), R7 (no check).*
   → "5. In the WordPress dashboard, go to **Plugins > Installed Plugins**. Select **Activate** below **Meme Generator**." Then: "6. Make sure that the **Meme Generator** block shows in the block inserter."

### Repository
5. **L35** "Checkout the repository (skip this step if already done)"
   *Rules: R5 (condition first), R3.*
   → "1. If you do not have the repository, clone it:"
6. **L41** "Install the dependencies"
   → "2. Install the dependencies:" (add a number and a colon, the same as the other steps)
7. **L47** "Start the development environment (make sure you have Docker installed )"
   *Rule: R6. This prerequisite comes after the point where the reader needs it.*
   → Move a **Prerequisites** line to the top of the section: "**Prerequisites:** Docker must be installed and running." Then: "3. Start the development environment:"
8. **L53** "Run the following script from the root of the repository"
   *Rule: R5 (location first).*
   → "4. From the root of the repository, run this script:"
9. **L59** "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
   *Rules: Word swaps (once), R2, and a repeated word.*
   → "5. When the script is complete, go to `plugins/meme-generator` and start the build:"
10. **After L63.** The procedure has no final check. *Rule: R7.*
    → "6. Make sure that the **Meme Generator** block shows in the block inserter."

### Step 1
11. **L71** "Open the block.json file and update it with the following attribute definitions"
    *Rules: R2, Word swaps (update).*
    → "1. Open `block.json`." "2. Replace the file contents with this code:"

### Step 3
12. **Before L130.** The crash risk is only mentioned at L200, after the reader has already run the code. *Rule: R6.*
    → Add before "Add the following to edit.js:":
    "**CAUTION:** Do not leave the editor open for a long time with this code. The `fetch` call runs again and again and can crash the browser."
13. **L130** "Add the following to edit.js:"
    *Rule: R16 (unclear anchor: replace or add?).*
    → "In `src/edit.js`, replace the `Edit` function with this code:"
14. **L200** "Save, refresh, and open the console. Do you notice that something? There are A LOT of messages from our fetch. In fact, if you leave it long enough you'll crash browser."
    *Rules: R2 (three actions), R8 (rhetorical question), Word swaps (A LOT of).*
    → "1. Save the file." "2. Refresh the editor page." "3. Open the browser console." "4. Make sure that the console shows many messages from the `fetch` call." The crash sentence moves up into the CAUTION in finding 12.
15. **L204** "Remove the fetch call (for now) and update edit.js with the following:"
    *Rules: R2, Word swaps (update).*
    → "In `src/edit.js`, replace the `Edit` function with this code. This code removes the `fetch` call for now."
16. **L265, first sentence** "Save and refresh the page and notice that every time we select the block in the editor, there is a console message."
    *Rules: R2, R1 (24 words), and the check is hidden in prose (R7).*
    → "1. Save the file." "2. Refresh the page." "3. Select the block. Make sure that the console shows a message each time you select the block."
    The rest of L265 is voice-zone explanation and stays as it is. The linter flagged "trigger" there, but it is in the explanation part, so I dropped that hit.
17. **L267** "Update the hook with the following:"
    *Rules: Word swaps (update), R16.*
    → "In `src/edit.js`, add an empty array as the second argument of `useEffect`:"
18. **L328** "Now, you'll see that the hook is only run once ever. This is the exact case we want for our initial fetch so let's add that into the hook."
    *Rules: R7 (check written as prose), R3 ("let's"), and no anchor.*
    → "Make sure that the console shows the message only one time." Then, as a new step: "In `src/edit.js`, move the `fetch` call into the `useEffect` callback:"

### Step 8
19. **L406** "Open up block.json and add the following to the supports property:"
    *Rules: R9 ("open up"), R2.*
    → "1. Open `block.json`." "2. In the `supports` property, add the `html` and `color` keys shown below:"
20. **L446** "Refresh the block and you should now see the option to choose the text color:"
    *Rules: R13 (you should), Word swaps (choose), R15.*
    → "3. Refresh the editor and select the block." "4. Make sure that **Styles > Color > Text** shows in the block sidebar."
21. **L452** "Update block.json with the following:"
    *Rules: Word swaps (update), R16.*
    → "5. In `block.json`, add the `typography` key to the `supports` property:"
22. **L494** "Refresh the block again and you can now set the font size and control how text is aligned."
    *Rule: R7 (the check is not explicit).*
    → "6. Refresh the editor. Make sure that the block sidebar shows the font size and text alignment controls."
23. **L498** "Finally, let's add some controls to be able to set the font family, style, and weight. Do do this we're going to use some experimental properties on block.json"
    *Rules: R3, R1, and a typo ("Do do").*
    → "7. In `block.json`, add the three `__experimental` font properties to `supports`:"
24. **L543** "Refresh and you'll see some new options for controlling the font in the block sidebar"
    *Rules: R7, and -ing ("controlling", R11).*
    → "8. Refresh the editor. Make sure that the block sidebar shows the font family, font style, and font weight controls."

### Step 9
25. **L555** "Open up meme-generator.php and add the following code inside the init hook callback:"
    *Rules: R9 ("open up"), R2, R16.*
    → "1. Open `meme-generator.php`." "2. In `meme_generator_block_init()`, below `register_block_type()`, add the `wp_register_font_collection()` call:"
26. **L668** "Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed"
    *Rules: R1 (26 words), R2, R15 (vague UI path), R5.*
    → "3. Save the file." "4. Go to **Appearance > Editor > Styles > Typography**." "5. Select **Manage fonts**, then open the **Meme fonts** tab."
27. **L672** "After installing the fonts, they are available in the block."
    *Rules: R11 (-ing opener), and the install step is missing.*
    → "6. Select the fonts and select **Install**." "7. Make sure that the fonts show in the block's font family control."

## Borderline

- **L676** "Stick a fork in it, you're done! Congrats and bon appetite!" This is a closing (voice zone), but the card uses this exact idiom as its R8 example. It is hard to read in a second language. A light fix keeps the tone: "The recipe is complete. Congrats, and bon appétit!" ("appetite" is also misspelled.)
- **Step headings** ("Setting up…", "Getting the images", "Formatting the text") break R11 (-ing). Possible fixes: "Step 1 – Add the block attributes", "Step 3 – Get the images", "Step 8 – Format the text". Headings sit between zones.
- **Step numbering jumps** from 1 to 3 to 8 to 9. L104 also refers to text fields that the recipe never adds. Steps may be missing. This is a content problem, not STE, but a non-native reader will get lost here first.
- **"update" → "change"**. In the code-change steps I suggested "replace" or "add" instead of "change". That tells the reader exactly what to do with the code.
- **L668 UI path.** "Manage fonts" and the Meme fonts tab are my best guess at the current Site Editor labels. Check them against the screen before using them.

## Outside STE scope (code, not changed)

These are code bugs, so this pass does not change them, but you should fix them:
- **L21** has an en-dash in `–template`. It must be `--template`.
- The JSON, JS and PHP blocks use curly quotes (`“ ”`, `‘ ’`), so readers who copy and paste them will get errors.