This is a hybrid STE pass on `fixtures/meme-generator.md`. It only covers the parts where readers take an action. The intro, the explanations and the jokes keep Ryan's voice. I haven't edited anything, and you said not to ask, so there's no approval question at the end.

## Where the rules apply

| Lines | Section | Zone |
|---|---|---|
| 3–9 | Skill level, Overview | Voice |
| 13 | Setup | Action (choosing a setup path) |
| 17–30 | Standalone | Action |
| 34–63 | Repository | Action |
| 67–69 | Step 1 explanation | Voice |
| 71 | Step 1 instruction | Action |
| 104–128 | Step 3 API explanation | Voice |
| 130, 200, 204, 267, 328 | Step 3 instructions and checks | Action |
| 202, 265 (after the first sentence), 398 | Step 3 reasoning | Voice |
| 402 | Step 8 intro | Voice |
| 404–406, 446, 450–452, 494, 498, 543 | Step 8 instructions and checks | Action |
| 444, 547 | Step 8 reasoning and praise | Voice |
| 551–553, 664–666 | Step 9 reasoning | Voice |
| 555, 668–672 | Step 9 instructions and checks | Action |
| 676 | Closing | Voice |

## Findings

### Setup
1. **L13** "You can choose to either use the repository which provides a development environment or to just download the standalone plugin"
   - **Rules broken:** word swap (choose → select), rule 13 (hedge "just"), rule 14 (a choice between options belongs in a table)
   - **Rewrite:**
     > Select one of these setup options:
     >
     > | Option | Use it when |
     > |---|---|
     > | Standalone | You have a local WordPress installation. |
     > | Repository | You want the full development environment. Docker is necessary. |

### Standalone
2. **L17–18** "Instructions / Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation."
   - **Rules broken:** rule 1 (22 words), rule 2 (two actions)
   - **Rewrite:**
     > 1. Open a terminal.
     > 2. Go to the `wp-content/plugins` directory of your local WordPress installation.
     > 3. Run this command:
3. **L24** "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
   - **Rules broken:** word swap (once → after), duplicated word, rule 2 (the `cd` and `npm run start` in the command are two actions)
   - **Rewrite:**
     > 4. After the scaffold is complete, go to the new plugin directory and start the build:
4. **L30** "Finally, make sure to activate the plugin."
   - **Rules broken:** rule 15 (no click path), rule 7 (no final check)
   - **Rewrite:**
     > 5. In the WordPress admin, go to **Plugins > Installed Plugins**. Under **Meme Generator**, click **Activate**.
     > 6. Make sure that **Meme Generator** shows in the block inserter.

### Repository
5. **L47** "Start the development environment (make sure you have Docker installed )"
   - **Rule broken:** rule 6 (a prerequisite is buried after the action)
   - **Rewrite:** Add a prerequisite before step 1: "**NOTE:** Docker must be installed and running." Then the step reads "Start the development environment:"
6. **L35** "Checkout the repository (skip this step if already done)"
   - **Rule broken:** rule 5 (the condition should come first)
   - **Rewrite:** "If you do not have the repository, clone it:"
7. **L41, L53**: Add the location. "Install the dependencies" becomes "Go to the root of the repository. Install the dependencies:"
   - **Rule broken:** rule 15 (the reader has no location yet; `cd` isn't shown after `git clone`)
8. **L59** has the same problem as #3 (word swap once → after, "completed completed").
   - **Rewrite:** "After the scaffold is complete, go to the new plugin directory and start the build:"
9. **End of Repository (L63)**
   - **Rule broken:** rule 7 (no activation step or check)
   - **Rewrite:** Add the same activate and check steps as #4.

### Step 1
10. **L71** "Open the block.json file and update it with the following attribute definitions"
    - **Rules broken:** rule 2 (two actions), word swap (update → change), rule 16 (says "attribute definitions" but shows the whole file)
    - **Rewrite:**
      > 1. Open `block.json`.
      > 2. Replace the contents of the file with this code:
11. **After L100**
    - **Rule broken:** rule 7 (no check)
    - **Rewrite:** "Make sure that the build has no errors in the terminal."

### Step 3
12. **L130** "Add the following to edit.js:"
    - **Rule broken:** rule 16. The block shows a full function, but the text doesn't say whether to replace or add.
    - **Rewrite:** "In `src/edit.js`, replace the `Edit` function with this code:"
13. **Before L130, a missing caution**
    - **Rule broken:** rule 6. Line 200 says the code crashes the browser, but the reader only learns this after running it.
    - **Rewrite:** Put this before the code: "**CAUTION:** Do not keep the editor open for a long time with this code. The request runs in a loop and can crash the browser."
14. **L200** "Save, refresh, and open the console. Do you notice that something? There are A LOT of messages from our fetch. In fact, if you leave it long enough you'll crash browser."
    - **Rules broken:** rule 2 (three actions), rule 8 (a question used for effect), word swap (A LOT of → many), rule 7 (the check is vague)
    - **Rewrite:**
      > 1. Save `edit.js`.
      > 2. Refresh the editor.
      > 3. Open the browser console.
      > 4. Make sure that the console shows many messages from the request.
15. **L204** "Remove the fetch call (for now) and update edit.js with the following:"
    - **Rules broken:** rule 2 (two actions), word swap (update → change)
    - **Rewrite:**
      > 1. In `src/edit.js`, remove the `fetch` call.
      > 2. Replace the `Edit` function with this code:
16. **L265, first sentence** "Save and refresh the page and notice that every time we select the block in the editor, there is a console message."
    - **Rules broken:** rule 2, rule 1 (24 words, which is over the limit for a procedure)
    - **Rewrite:**
      > 1. Save the file.
      > 2. Refresh the editor.
      > 3. Select the block.
      > 4. Make sure that the console shows one message each time you select the block.
17. **L267** "Update the hook with the following:"
    - **Rules broken:** word swap (update → change), rule 16 (the full function is shown but only the dependency array changed)
    - **Rewrite:** "In `src/edit.js`, add an empty dependency array to `useEffect`:" Then show only the `useEffect` block.
18. **L328** "Now, you'll see that the hook is only run once ever. This is the exact case we want for our initial fetch so let's add that into the hook."
    - **Rules broken:** rule 3 ("let's"), rule 7 (the check is mixed into prose), rule 16 (no anchor)
    - **Rewrite:**
      > 1. Refresh the editor. Make sure that the console shows the message one time only.
      > 2. In `src/edit.js`, replace the `console.log` inside `useEffect` with this code:
19. **L398** "being stored in the addImages variable"
    - **Rule broken:** rule 10 (the code uses `allImages`, so the name is wrong)
    - **Rewrite:** "`allImages`"
    - **Note:** This line is in the voice zone, but the variable name is a factual error. Fix it in both modes.

### Step 8
20. **L404** "Let's start with choosing the font color."
    - **Rules broken:** rule 3, rule 11, word swap (choose → select)
    - **Rewrite:** "First, add a text color control."
21. **L406** "Open up block.json and add the following to the supports property:"
    - **Rules broken:** rule 9 ("open up"), rule 2, rule 16 (says "add to supports" but shows the whole file)
    - **Rewrite:**
      > 1. Open `block.json`.
      > 2. In the `supports` property, add this code:
      Then show only the `html` and `color` keys.
22. **L446** "Refresh the block and you should now see the option to choose the text color:"
    - **Rules broken:** rule 13 ("you should"), word swap (choose → select), rule 15 (no location)
    - **Rewrite:**
      > 1. Refresh the editor.
      > 2. Select the block.
      > 3. Make sure that the **Color > Text** control shows in the block sidebar.
23. **L450–452** "Next, let's add some typography controls… Update block.json with the following:"
    - **Rules broken:** rule 3, word swap (update → change), rule 16
    - **Rewrite:** "In `block.json`, in the `supports` property, add the `typography` object:" Then show only that object.
24. **L494** "Refresh the block again and you can now set the font size and control how text is aligned."
    - **Rule broken:** rule 7 (the check is vague)
    - **Rewrite:** "Refresh the editor. Make sure that the **Typography** panel shows the font size and text alignment controls."
25. **L498** "Finally, let's add some controls to be able to set the font family, style, and weight. Do do this we're going to use some experimental properties on block.json"
    - **Rules broken:** rule 3, "Do do" typo, missing instruction, rule 16
    - **Rewrite:** "In `block.json`, in the `supports` property, add these three properties:" Then show only the three `__experimental*` lines.
26. **Before L498, a missing caution**
    - **Rule broken:** rule 6
    - **Rewrite:** "**CAUTION:** Properties that start with `__experimental` can change or stop working in a future WordPress release."
27. **L543** "Refresh and you'll see some new options for controlling the font in the block sidebar"
    - **Rule broken:** rule 7
    - **Rewrite:** "Refresh the editor. Make sure that the **Typography** panel in the block sidebar shows the font family, style, and weight controls."

### Step 9
28. **L555** "Open up meme-generator.php and add the following code inside the init hook callback:"
    - **Rules broken:** rule 9 ("open up"), rule 2, rule 16 (the anchor is vague and the whole file is shown)
    - **Rewrite:**
      > 1. Open `meme-generator.php`.
      > 2. In the `meme_generator_block_init()` function, below `register_block_type( __DIR__ . '/build' );`, add this code:
      Then show only the `wp_register_font_collection()` call.
29. **L668** "Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed"
    - **Rules broken:** rule 1 (26 words), rule 2, rule 15 (the location is vague)
    - **Rewrite:**
      > 1. Save `meme-generator.php`.
      > 2. Go to **Appearance > Editor > Styles > Typography**.
      > 3. Click **Manage fonts**.
      > 4. Open the **Meme fonts** tab.
      > 5. Make sure that Arial, Comic Sans, Impact, and Montserrat show in the list.
30. **L672** "After installing the fonts, they are available in the block."
    - **Rules broken:** rule 11 (starts with an -ing form), rule 2, rule 7
    - **Rewrite:**
      > 6. Select the fonts and click **Install**.
      > 7. In the editor, select the Meme Generator block. Make sure that the new fonts show in the font family control.

## Borderline findings

- **L65, L102, L400 headings** ("Setting up the block attributes", "Getting the images", "Formatting the text"): these use -ing openers (rule 11), and "Setting up" is a phrasal verb (rule 9). Possible rewrites: "Step 1 – Add the block attributes", "Get the images", "Format the text". Headings sit between the two zones, so this is your call.
- **Step numbers jump 1 → 3 → 8 → 9.** Readers who translate or scan will think steps are missing. Either renumber, or add a note that this excerpt skips steps. Step 8 also says "Now that we can choose and update the image", which refers to a step that isn't in the file.
- **L21 `–template`** uses an en dash, not `--`. The command fails if a reader pastes it. The card says never to change code, so I didn't rewrite it, but the typo should be fixed. The code blocks also use curly quotes (`“ ” ‘ ’`), which break JSON, JS and PHP when pasted.
- **L668 "Style section"**: I guessed the click path in #29. Check it against the current Site Editor labels before using it.
- **L676** "Stick a fork in it, you're done! Congrats and bon appetite!" is an idiom (rule 8), but it's a closing, so it's voice zone and stays in hybrid mode. In strict mode it would become "The procedure is complete." ("appetite" should be "appétit" either way.)

I didn't add anything to the refinement log. None of these findings needs a rule the card doesn't already have.