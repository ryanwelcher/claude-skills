**Mode:** hybrid. The Block Developer Cookbook defaults to Hybrid on the card, so no destination check was needed. No edits made.

## 1. Zone map

| Section | Lines | Zone |
|---|---|---|
| Title, Skill Level, ⏲️ time | 1–5 | Voice (metadata) |
| Overview | 9 | Voice |
| Setup | 13 | Action (choice of setup option) |
| Standalone | 17–30 | Action |
| Repository | 34–63 | Action |
| Step 1 | 67–69 | Voice (what a meme is, why the attributes exist) |
| | 71 | Action |
| Step 3 | 104–106, 128 | Voice (API intro, why `useState`) |
| | 130, 200 | Action (instruction, check, crash risk) |
| | 202 | Voice (why `useEffect`) |
| | 204 | Action |
| | 265 | **Mixed:** sentence 1 is an action check; the rest is voice |
| | 267 | Action |
| | 328 | **Mixed:** sentence 1 is a check, sentence 2 is an instruction |
| | 398 | Action (end-of-procedure check) |
| Step 8 | 402–404, 450, 547 | Voice (transitions, praise) |
| | 406, 446, 452, 494, 498, 543 | Action |
| | 444 | Voice (explains the `supports` settings), but it lists parameters |
| Step 9 | 551–553, 666 | Voice |
| | 555, 668, 672 | Action |
| | 664 | Voice, but it lists font sources |
| | 676 | Voice (closing) |

## 2. Findings

### Setup
1. **"You can choose to either use the repository which provides a development environment or to just download the standalone plugin"**. Breaks: rule 3, rule 13 ("just"), Word swaps (choose → select).
   → "Select one setup option: **Standalone** (the plugin only) or **Repository** (the plugin and a development environment)."

### Standalone
2. **"Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation."** Breaks: rule 2 (two actions: change directory, run command) and rule 1 (20 words, at the limit).
   → "1. In a terminal, go to the `wp-content/plugins` directory of your local WordPress installation." / "2. Run this command:"
3. **"Once the scaffold has completed completed, start the build process from inside the newly created plugin"**. Breaks: Word swaps (once → after). "completed" is also doubled.
   → "After the scaffold is complete, run this command. The command opens the new plugin directory and starts the build."
4. **"Finally, make sure to activate the plugin."** Breaks: rule 15 (no click path) and rule 7 (the procedure has no check).
   → "Go to **Plugins > Installed Plugins**." / "Under **Meme Generator**, click **Activate**." / "Make sure that the **Meme Generator** block is in the block inserter."

### Repository
5. **Docker requirement:** "Start the development environment (make sure you have Docker installed )". Breaks: rule 6 (the requirement sits inside the step it applies to, not before it).
   → At the top of the section: "**NOTE:** The development environment needs Docker. Make sure that Docker is installed and running before you start." Step: "Start the development environment:"
6. **"Checkout the repository (skip this step if already done)"**. Breaks: rule 5 (condition first), rule 13 (optional step), rule 10 ("checkout" but the command is `git clone`).
   → "If you do not have the repository, clone it:"
7. **Missing step between clone and install.** Breaks: rule 2 / rule 16 (no location). `npm install` must run from the repository root, but the recipe never says so.
   → Add after the clone: "Go to the `block-developer-cookbook` directory."
8. **"Once the scaffold has completed completed, start the build process from inside the newly created plugin"** (line 59). Breaks: Word swaps (once → after). "completed" is doubled here too.
   → Same rewrite as #3.
9. **No final check in the Repository procedure.** Breaks: rule 7.
   → "Make sure that the **Meme Generator** block is in the block inserter." (Add an activation step first if the environment doesn't activate the plugin for you.)

### Step 1
10. **"Open the block.json file and update it with the following attribute definitions"**. Breaks: rule 2, Word swaps (update → change), rule 16 (the block holds the full file but the text says to add definitions).
   → "Replace the contents of `block.json` with this code. The code adds the `topText`, `bottomText`, and `image` attributes."

### Step 3
11. **Crash warning comes after the step.** "if you leave it long enough you'll crash browser" (line 200) follows the code at line 130. Breaks: rule 6 and rule 8.
   → Before line 130: "**CAUTION:** Do not leave the editor open for a long time after you add this code. The code sends requests in a loop, and the browser can crash. The next steps fix this problem."
12. **"Add the following to edit.js:"** Breaks: rule 16 (no anchor; the block holds the whole `Edit` function).
   → "In `src/edit.js`, replace the `Edit` function with this code:"
13. **"Save, refresh, and open the console. Do you notice that something? There are A LOT of messages from our fetch."** Breaks: rule 2 (three actions), rule 8 (question, all caps), Word swaps (a lot of → many), rule 7.
   → "Save `edit.js`." / "Refresh the editor." / "Open the browser console." / "Make sure that the console shows many messages from the `fetch()` call."
14. **"Remove the fetch call (for now) and update edit.js with the following:"** Breaks: rule 2, rule 13 ("for now"), Word swaps (update → change), rule 16.
   → "In `src/edit.js`, replace the `Edit` function with this code. This code removes the `fetch()` call and adds `useEffect`."
15. **"Save and refresh the page and notice that every time we select the block in the editor, there is a console message."** Breaks: rule 1 (24 words), rule 2, rule 3 ("we"), rule 7.
   → "Save `edit.js`." / "Refresh the editor." / "Select the block." / "Make sure that the console shows `useEffect is running` each time you select the block."
16. **"Update the hook with the following:"** Breaks: Word swaps (update → change) and rule 16.
   → "In `src/edit.js`, replace the `Edit` function with this code. The code adds an empty dependency array (`[]`) to `useEffect`."
17. **"Now, you'll see that the hook is only run once ever. … so let's add that into the hook."** Breaks: rule 7 (a check with no save/refresh step), rule 4 (passive), rule 3 ("let's").
   → "Save `edit.js` and refresh the editor." (then split per rule 2) / "Make sure that the console shows `useEffect is running` one time." / Keep "This is the exact case we want for our initial fetch." as voice. / "In `src/edit.js`, replace the `Edit` function with this code. The code moves the `fetch()` call into `useEffect`."
18. **"At this point, we have the data being loaded once and then being stored in the addImages variable."** Breaks: rule 7, rule 11 ("being loaded", "being stored"), rule 4.
   → "Refresh the editor." / "Make sure that the console shows the `data.memes` array one time."

### Step 8
19. **"Open up block.json and add the following to the supports property:"** Breaks: rule 9 ("open up"), rule 2, rule 16 (the block holds the full file).
   → "Replace the contents of `block.json` with this code. The change is in the `supports` property."
20. **Line 444 lists three `color` settings in prose.** Breaks: rule 14.
   → Table:
   | Property | Value | Reason |
   |---|---|---|
   | `text` | `true` | Lets the user select a text color from the theme palette. |
   | `background` | `false` | The block does not use a background color. |
   | `enableContrastChecker` | `false` | The checker compares against the theme background, not the image, so it can show false warnings. |
21. **"Refresh the block and you should now see the option to choose the text color:"** Breaks: rule 2, rule 13 ("should"), Word swaps (choose → select), rule 7 (vague check).
   → "Refresh the editor." / "Select the block." / "Make sure that the **Color** panel in the block sidebar shows a **Text** option."
22. **"Update block.json with the following:"** Breaks: Word swaps (update → change) and rule 16.
   → "Replace the contents of `block.json` with this code. The change adds the `typography` property to `supports`."
23. **"Refresh the block again and you can now set the font size and control how text is aligned."** Breaks: rule 2, rule 7, rule 15.
   → "Refresh the editor." / "Select the block." / "Make sure that the **Typography** panel shows a font size control and the block toolbar shows a text alignment control."
24. **Experimental properties have no caution.** Breaks: rule 6.
   → Before the code block: "**CAUTION:** Do not rely on the `__experimental` properties staying the same. A future WordPress release can change or remove them."
25. **"Finally, let's add some controls to be able to set the font family, style, and weight. Do do this we're going to use some experimental properties on block.json"** Breaks: rule 3 ("let's", "we're"), no explicit instruction, rule 16. "Do do" is also a typo.
   → "Replace the contents of `block.json` with this code. The change adds three `__experimental` font properties to `supports`."
26. **"Refresh and you'll see some new options for controlling the font in the block sidebar"** Breaks: rule 2, rule 7, rule 11 ("controlling"), rule 15.
   → "Refresh the editor." / "Select the block." / "Make sure that the **Typography** panel shows the **Font** and **Appearance** controls."

### Step 9
27. **"Open up meme-generator.php and add the following code inside the init hook callback:"** Breaks: rule 9 ("open up"), rule 2, rule 16 (vague anchor; the block holds the full file).
   → "In `meme-generator.php`, replace the contents with this code. The change adds `wp_register_font_collection()` below `register_block_type()` in `meme_generator_block_init()`."
28. **"The code above shows examples of all three,"** Breaks: rule 14 (a list of font sources written as prose).
   → Table:
   | Font source | Example in the code |
   |---|---|
   | System font | Arial, Comic Sans |
   | Font file in the plugin | Impact |
   | Google Fonts | Montserrat |
29. **"Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed"** Breaks: rule 2, rule 15 ("Style section"), rule 7.
   → "Save `meme-generator.php`." / "Go to **Appearance > Editor > Styles > Typography**." / "Open **Manage fonts**." / "Select the **Install Fonts** tab." / "Make sure that the **Meme fonts** collection is in the list."
30. **"After installing the fonts, they are available in the block."** Breaks: rule 11 ("installing"), a missing install step, rule 7.
   → "Select the fonts to use, then click **Install**." / "Select the Meme Generator block." / "Make sure that the new fonts are in the **Font** list of the **Typography** panel."

## 3. Borderline
- **B1. Step headings:** "Setting up the block attributes", "Getting the images", "Formatting the text". These break rule 11 (and rule 9 for "Setting up"), but headings could count as voice. Possible rewrites: "Add the block attributes", "Get the images", "Format the text".
- **B2. Line 265, sentences 2–5:** the dependency-array behavior (no array, empty array, array of values) could become a rule-14 table. It reads as explanation, so it may be voice.
- **B3. Line 444:** if you treat it as action, it also has word swaps (allows → lets, pick → select) and rule 11 ("Choosing"). #20 would replace it anyway.
- **B4. Line 398 `addImages`:** the code uses `allImages`. This is a technical name, so it's under Never change, but it looks like a typo. Please confirm.
- **B5. Line 676 "Stick a fork in it, you're done!":** this is the closing, so it's voice zone in hybrid and I left it alone. It would change only in strict mode.
- **B6. UI labels in #21, #23, #26, #29, #30:** confirm these against the current editor screens and the screenshots before applying.
- **B7. Outside STE scope, not proposed as edits:**
  - Line 21 has an en dash in `–template`.
  - Every code block has curly quotes, so copy-paste will fail.
  - Code blocks repeat the whole file, which conflicts with rule 16.
  - Steps are numbered 1, 3, 8, 9.
  - Line 69 has a grammar error ("The image attribute be an object"), but it's voice zone, so it's for `sounds-like-me`.