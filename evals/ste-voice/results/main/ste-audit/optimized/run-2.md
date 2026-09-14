**Mode:** Hybrid. The Block Developer Cookbook defaults to Hybrid on the card, so I checked only the action zones. I read the card and the file on disk as they are now.

## Zone map

| Lines | Section | Zone |
|---|---|---|
| 1–5 | Title, skill level, time | Voice (metadata) |
| 7–9 | Overview | Voice |
| 11–13 | Setup | Action (a choice between two paths) |
| 15–30 | Standalone | Action |
| 32–63 | Repository | Action |
| 65–69 | Step 1: intro to attributes | Voice |
| 71 | Step 1: "Open the block.json file…" | Action |
| 102–128 | Step 3: API explanation and the fetch/useState reasoning | Voice |
| 130 | "Add the following to edit.js:" | Action |
| 200 | "Save, refresh, and open the console." + the crash explanation | Action (first sentence), voice (the rest) |
| 202 | useEffect explanation | Voice |
| 204 | "Remove the fetch call… update edit.js" | Action |
| 265 | Line 265: "Save and refresh…" + the dependency-array explanation | Action (first clause), voice (the rest) |
| 267 | "Update the hook…" | Action |
| 328 | "Now, you'll see… let's add that into the hook." | Action (check + instruction) |
| 398 | Recap | Voice |
| 400–404 | Step 8: intro | Voice |
| 406, 446, 452, 494, 498, 543 | Step 8: instructions and checks | Action |
| 444 | Explanation of the supports config | Voice |
| 547 | "Great work!" | Voice |
| 549–553 | Step 9: intro | Voice |
| 555 | "Open up meme-generator.php…" | Action |
| 664–666 | Font collection explanation, link to the blog | Voice |
| 668–674 | Save, click path, install check | Action |
| 676 | Closing | Voice. It is also the procedure's end, so it needs a check (finding 22). |

## Findings

### Setup
1. **L13:** "You can choose to either use the repository which provides a development environment or to just download the standalone plugin"
   - **Breaks:** Word swaps (choose → select), R13 (hedge "just"), R3 (not imperative), R14 (a comparison written as prose)
   - **Rewrite:** "Select one of these setup methods:" followed by a table:

     | Method | Use it when |
     |---|---|
     | Standalone | You have a local WordPress installation. |
     | Repository | You want the included development environment. |

### Standalone
2. **L17–18:** "Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation."
   - **Breaks:** R1 (21 words, over the 20-word limit for procedural sentences), R2 (two locations and an action in one sentence)
   - **Rewrite:**
     - "1. Open a terminal in the `wp-content/plugins` directory of your local WordPress installation."
     - "2. Run this command:"
3. **L24:** "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
   - **Breaks:** Word swaps (once → after), R2 (move into the directory, then run the build), R5 (the doubled "completed" is a typo)
   - **Rewrite:** "After the scaffold completes, start the build process in the `meme-generator` directory:"
4. **L30:** "Finally, make sure to activate the plugin."
   - **Breaks:** R15 (no click path), R7 (no final check)
   - **Rewrite:**
     - "Go to **Plugins > Installed Plugins** and select **Activate** below **Meme Generator**."
     - "Make sure that the plugin shows as active."

### Repository
5. **L35:** "Checkout the repository (skip this step if already done)"
   - **Breaks:** R5 (condition last), R13 (the step is optional but not marked "Optional:"), R12 (missing article)
   - **Rewrite:** "Optional: If you do not have the repository, clone it:"
6. **L41:** "Install the dependencies"
   - **Breaks:** Missing location for the step (R2 exception, R15)
   - **Rewrite:** "In the root of the repository, install the dependencies:"
7. **L47:** "Start the development environment (make sure you have Docker installed )"
   - **Breaks:** R6 (the prerequisite comes inside the step, not before it)
   - **Rewrite:** Add a new step above it: "Make sure that Docker is installed and running." Then: "Start the development environment:"
8. **L59:** "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
   - **Breaks:** Same as finding 3
   - **Rewrite:** "After the scaffold completes, start the build process in the `plugins/meme-generator` directory:"
9. **L63 (end of Setup):** The procedure has no final check.
   - **Breaks:** R7
   - **Rewrite:** Add "Make sure that the **Meme Generator** block shows in the block inserter."

### Step 1
10. **L71:** "Open the block.json file and update it with the following attribute definitions"
    - **Breaks:** R2 (two actions), Word swaps (update → change)
    - **Rewrite:**
      - "1. Open `src/block.json`."
      - "2. Replace the contents with the following attribute definitions:"

### Step 3
11. **L130:** "Add the following to edit.js:"
    - **Breaks:** R16. The code block holds the whole file, but the line reads as a partial add with no anchor.
    - **Rewrite:** "In `src/edit.js`, replace the `Edit` function with:"
12. **L200:** "Save, refresh, and open the console."
    - **Breaks:** R2 (three actions in one step)
    - **Rewrite:**
      - "1. Save `src/edit.js`."
      - "2. Refresh the editor."
      - "3. Open the browser console."
13. **L200:** "if you leave it long enough you'll crash browser." This is a crash risk, but readers only learn about it after they are told to run the code.
    - **Breaks:** R6 (the caution comes after its step)
    - **Rewrite:** Put this before the L130 step: "**CAUTION:** Do not leave the editor open for long after this step. The fetch call runs on every render and can crash the browser."
14. **L204:** "Remove the fetch call (for now) and update edit.js with the following:"
    - **Breaks:** R2 (two actions), Word swaps (update → change)
    - **Rewrite:** "In `src/edit.js`, replace the `Edit` function with the following code. This code removes the fetch call for now:"
15. **L265:** "Save and refresh the page and notice that every time we select the block in the editor, there is a console message."
    - **Breaks:** R1 (23 words), R2 (save, refresh, and observe in one sentence), R4 ("we")
    - **Rewrite:**
      - "1. Save and refresh the editor."
      - "2. Select the block."
      - "3. Make sure that the console shows `useEffect is running` each time you select the block."
16. **L267:** "Update the hook with the following:"
    - **Breaks:** Word swaps (Update → change), R16 (the full function is shown, but the anchor points at the hook)
    - **Rewrite:** "In `src/edit.js`, add an empty dependency array to `useEffect`:"
17. **L328:** "Now, you'll see that the hook is only run once ever. This is the exact case we want for our initial fetch so let's add that into the hook."
    - **Breaks:** R7 (the check is not phrased as a check), R3 ("let's"), R16 (no anchor)
    - **Rewrite:**
      - "Make sure that the console shows `useEffect is running` one time only."
      - "In `src/edit.js`, move the fetch call into the `useEffect` callback:"
18. **Step 3 end (L398):** The procedure has no final check. L398 is a recap.
    - **Breaks:** R7
    - **Rewrite:** Add "Make sure that the console shows the `memes` array one time."

### Step 8
19. **L406:** "Open up block.json and add the following to the supports property:"
    - **Breaks:** R9 ("open up"), R2 (two actions)
    - **Rewrite:**
      - "1. Open `src/block.json`."
      - "2. In the `supports` property, add the `html` and `color` keys:"
20. **L446:** "Refresh the block and you should now see the option to choose the text color:"
    - **Breaks:** R13 ("you should"), Word swaps (choose → select), R7 (the check is not phrased as one), R15 (no location)
    - **Rewrite:**
      - "Refresh the editor and select the block."
      - "Make sure that **Color > Text** shows in the block sidebar."
21. **L452:** "Update block.json with the following:"
    - **Breaks:** Word swaps (Update → change), R16 (no anchor)
    - **Rewrite:** "In `src/block.json`, below the `color` key, add the `typography` key:"
22. **L494:** "Refresh the block again and you can now set the font size and control how text is aligned."
    - **Breaks:** R2 (action and check in one sentence), R7
    - **Rewrite:**
      - "Refresh the editor."
      - "Make sure that the font size and text alignment controls show."
23. **L498:** "Finally, let's add some controls to be able to set the font family, style, and weight. Do do this we're going to use some experimental properties on block.json"
    - **Breaks:** R3 ("let's"), R16 (no anchor), typo ("Do do")
    - **Rewrite:** "In `src/block.json`, below the `typography` key, add the `__experimentalFontFamily`, `__experimentalFontStyle`, and `__experimentalFontWeight` properties:"
24. **L543:** "Refresh and you'll see some new options for controlling the font in the block sidebar"
    - **Breaks:** R7 (the check is not phrased as one), R2
    - **Rewrite:**
      - "Refresh the editor."
      - "Make sure that the block sidebar shows the font family, style, and weight controls."

### Step 9
25. **L555:** "Open up meme-generator.php and add the following code inside the init hook callback:"
    - **Breaks:** R9 ("open up"), R2 (two actions), R16 (the anchor is vague because the full file is shown)
    - **Rewrite:**
      - "1. Open `meme-generator.php`."
      - "2. In `meme_generator_block_init()`, below `register_block_type()`, add the `wp_register_font_collection()` call:"
26. **L668:** "Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed"
    - **Breaks:** R1 (26 words), R2, R5 (condition in the middle), R15 (vague UI location)
    - **Rewrite:**
      - "1. Save `meme-generator.php`."
      - "2. Go to **Appearance > Editor > Styles > Typography**."
      - "3. Make sure that the **Meme fonts** collection shows."
27. **L672:** "After installing the fonts, they are available in the block."
    - **Breaks:** R11 ("installing" used as a noun), no install step, R7
    - **Rewrite:**
      - "Install the fonts from the **Meme fonts** collection."
      - "Make sure that the fonts show in the block's font family control."
28. **L676:** "Stick a fork in it, you're done!" The procedure ends on an idiom, not a check.
    - **Breaks:** R8 in the card's own example. This is a voice-zone closing, so only the missing check is in scope.
    - **Rewrite:** Keep the closing, and put finding 27's check directly above it.

## Borderline
- **B1, L200** "There are A LOT of messages": linter swap (A LOT of → many). The sentence is descriptive commentary next to a check, and the capitals are part of your voice. Leave it unless you want the check-plus-explanation line in the action zone.
- **B2, L265** "trigger": the linter flagged it, but it sits in the dependency-array explanation, which is voice zone. I dropped it.
- **B3, L204/267/452** "update → change": the swap is correct, but "replace … with" fits better when a full code block follows. That is why the rewrites above use "replace".
- **B4, L444** "allows the user to pick… Choosing… enabled": explains config options (voice zone). It could also count as a parameter list that belongs in a table under R14 (`text`, `background`, `enableContrastChecker`, each with its effect).
- **B5, L65/102/400 headings** "Setting up", "Getting", "Formatting": R9 and R11 would give "Configure the block attributes", but a heading may count as voice.
- **B6, content issues outside STE:** the steps jump from 1 to 3 to 8 to 9. L398 says `addImages` but the code uses `allImages`. L664 ends with a comma. The `–template` on L21 uses an en dash, and the code blocks use curly quotes. These are code, so I did not propose edits, but the command will fail as written.

Stopped here as you asked. I made no edits.