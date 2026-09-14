I didn't edit anything. This is a hybrid pass: only the steps, prerequisites, checks and UI paths change, and the intros and explanations keep your voice. I ran the STE linter over those parts and it flagged 11 issues. I dropped one (line 265 is explanation, not a step) and added the problems the linter can't catch.

## Section map

| Lines | Section | Type |
|---|---|---|
| 1–9 | Title, Overview | Voice |
| 11–13 | Setup | Action |
| 15–30 | Standalone | Action |
| 32–63 | Repository | Action |
| 67–69 | Step 1 explanation | Voice |
| 71 | Step 1 instruction | Action |
| 104–128 | Step 3 explanation | Voice |
| 130 | "Add the following to edit.js" | Action |
| 200 | "Save, refresh, and open the console…" | Action (check), with a voice aside |
| 202 | useEffect explanation | Voice |
| 204, 267, 328 | Code instructions | Action |
| 265 | Dependency explanation | Voice, but its first sentence is a check |
| 398, 402, 444, 547, 551–553, 664–666 | Explanations and transitions | Voice |
| 406, 446, 452, 494, 498, 543 | Step 8 instructions and checks | Action |
| 555, 668–674 | Step 9 instructions and checks | Action |
| 676 | Closing | Voice. It could also count as the final check (see Borderline) |

## Proposed changes

### Setup
1. **Line 13:** "You can choose to either use the repository which provides a development environment or to just download the standalone plugin"
   - Rules broken: word swap (choose → select), rule 13 ("just"), and a missing period.
   - → "Select one option: use the repository, which gives you a development environment, or download the standalone plugin."

### Standalone
2. **Lines 17–18:** "Instructions / Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation."
   - Rules broken: rule 1 (21 words) and rule 2 (two things to do: go to the folder, then run the command).
   - → Split into steps:
     1. "Open a terminal."
     2. "Go to the `wp-content/plugins` directory of your local WordPress installation."
     3. "Run this command:"
3. **Line 24:** "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
   - Rules broken: word swap (once → after), the doubled word, and rule 2 (the code runs `cd` and `npm run start`).
   - → "After the scaffold is complete, go to the new plugin directory and start the build:"
   - Stricter version: two steps, "Go to the `meme-generator` directory." and "Start the build:".
4. **Line 30:** "Finally, make sure to activate the plugin."
   - Rules broken: rule 15 (no UI path) and rule 7 (no final check).
   - → "Go to **Plugins > Installed Plugins** and activate **Meme Generator**." Then add: "Make sure that the **Meme Generator** block shows in the block inserter."

### Repository
5. **Line 35:** "Checkout the repository (skip this step if already done)"
   - Rule broken: rule 5 (the condition comes after the action). "Checkout" is also a noun here.
   - → "If you do not have the repository, clone it:"
6. **Line 41:** "Install the dependencies" → "Install the dependencies:" (only the missing colon, which introduces the code).
7. **Line 47:** "Start the development environment (make sure you have Docker installed )"
   - Rule broken: rule 6 (the prerequisite is hidden in parentheses inside the step).
   - → Move it to a prerequisite before step 1 of this section: "**NOTE:** You must install Docker before you start." The step becomes "Start the development environment:".
8. **Line 53:** "Run the following script from the root of the repository" → "From the root of the repository, run this script:" (rule 5, location first).
9. **Line 59:** Same doubled "completed completed" and "Once" as finding 3.
   - → "After the scaffold is complete, go to the new plugin directory and start the build:"
10. **End of the Repository section:** there's no final check (rule 7).
    - → Add: "Make sure that the **Meme Generator** block shows in the block inserter."

### Step 1
11. **Line 71:** "Open the block.json file and update it with the following attribute definitions"
    - Rules broken: rule 2 (two actions), word swap (update → change), and a missing colon.
    - → "In `block.json`, add these attributes:"

### Step 3
12. **Line 130:** "Add the following to edit.js:"
    - Rule broken: rule 16. The code block replaces the whole `Edit` function, so "add" is misleading.
    - → "In `src/edit.js`, replace the `Edit` function with this code:"
13. **Line 200:** "Save, refresh, and open the console. Do you notice that something? There are A LOT of messages… you'll crash browser."
    - Rules broken:
      - Rule 2 (three actions)
      - Rule 6 (the crash risk comes after the step)
      - Rule 8 (rhetorical question)
      - Word swap (A LOT of → many)
    - → Add before line 130: "**CAUTION:** Do not keep the editor open for long after this change. The fetch runs in a loop and can crash the browser."
    - → Then split line 200 into steps:
      1. "Save the file."
      2. "Refresh the editor."
      3. "Open the browser console."
      4. "Make sure that many fetch messages show in the console."
    - The humor can go in the voice paragraph that follows.
14. **Line 204:** "Remove the fetch call (for now) and update edit.js with the following:"
    - Rules broken: rule 2 and word swap (update → change).
    - → "In `src/edit.js`, replace the `Edit` function with this code. This code removes the `fetch` call for now."
15. **Line 265, first sentence:** "Save and refresh the page and notice that every time we select the block in the editor, there is a console message."
    - Rules broken: rule 1 (26 words) and rule 2. This is a check sitting inside a voice paragraph.
    - → Pull it out as steps:
      1. "Save the file."
      2. "Refresh the editor."
      3. "Select the block."
      4. "Make sure that the console shows a message each time you select the block."
    - The rest of the paragraph stays in your voice.
16. **Line 267:** "Update the hook with the following:"
    - Rules broken: word swap (Update → change) and rule 16 (the code is the whole function).
    - → "In `src/edit.js`, add an empty dependency array to `useEffect`:"
17. **Line 328:** "Now, you'll see that the hook is only run once ever. This is the exact case we want for our initial fetch so let's add that into the hook."
    - Rules broken: rule 3 ("let's"), rule 7 (the check isn't separate), and rule 4 (passive "is run").
    - → "Make sure that the console shows the message one time only." Then, on its own line: "Move the `fetch` call into `useEffect`:"
18. **End of Step 3:** there's no final check (rule 7).
    - → "Make sure that the console shows the list of memes one time."

### Step 8
19. **Line 406:** "Open up block.json and add the following to the supports property:"
    - Rules broken: rule 9 (phrasal verb "open up") and rule 2.
    - → "In `block.json`, add these values to the `supports` property:"
20. **Line 446:** "Refresh the block and you should now see the option to choose the text color:"
    - Rules broken: rule 13 ("you should"), word swap (choose → select), rule 2, and rule 15 (no location).
    - → Two steps: "Refresh the editor." and "Select the block. Make sure that the **Color > Text** option shows in the block sidebar."
21. **Line 452:** "Update block.json with the following:"
    - Rule broken: word swap (Update → change).
    - → "In `block.json`, add the `typography` values to `supports`:"
22. **Line 494:** "Refresh the block again and you can now set the font size and control how text is aligned."
    - Rules broken: rule 2 and rule 7 (the check is vague).
    - → Two steps: "Refresh the editor." and "Make sure that the **Typography** panel shows the font size and text alignment controls."
23. **Line 498:** "Finally, let's add some controls to be able to set the font family, style, and weight. Do do this we're going to use some experimental properties on block.json"
    - Rules broken: rule 3 ("let's", "we're going to"), the typo "Do do", and a missing instruction line before the code.
    - → "In `block.json`, add these experimental properties to `supports`:"
    - The "why" sentence can stay in your voice above it.
24. **Line 543:** "Refresh and you'll see some new options for controlling the font in the block sidebar"
    - Rules broken: rule 2 and rule 11 ("controlling").
    - → Two steps: "Refresh the editor." and "Make sure that the block sidebar shows the font family, font style, and font weight controls."

### Step 9
25. **Line 555:** "Open up meme-generator.php and add the following code inside the init hook callback:"
    - Rules broken: rule 9 ("open up") and rule 16. The code is the whole file, so the anchor is wrong.
    - → "In `meme-generator.php`, inside `meme_generator_block_init()`, below `register_block_type()`, add the `wp_register_font_collection()` call:"
26. **Line 668:** "Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed"
    - Rules broken:
      - Rule 1 (26 words)
      - Rule 2
      - Rule 15 (vague location)
      - Rule 5 (the condition is buried)
    - → Three steps:
      1. "Save the file."
      2. "Go to **Appearance > Editor > Styles > Typography** and open the font library."
      3. "Make sure that the **Meme fonts** collection shows."
27. **Line 672:** "After installing the fonts, they are available in the block."
    - Rules broken: rule 11 ("installing") and rule 7.
    - → Two steps: "Install the fonts." and "Make sure that the fonts show in the block's font family control."

## Borderline
- **Line 676:** "Stick a fork in it, you're done! Congrats and bon appetite!" This breaks rule 8 if it counts as an action section, but it reads as a closing. In hybrid mode I'd keep it, because findings 27 and 10 already add the final checks. In strict mode it becomes "The procedure is complete."
- **Line 200's reason sentences:** some of that text is voice. I kept only the warning and the check in the action section.
- **Finding 26's UI path:** I'm assuming the font library sits at **Styles > Typography** in the target WordPress version. The exact label (for example **Manage fonts**) needs checking on screen before we write it in.
- **Finding 12 onward:** the "show only changed code" advice (rule 16) would mean shortening the code blocks. The code itself is off-limits, so I only changed the lead-in sentences to describe what the blocks really contain.

## Not STE, but these will confuse any reader
- **Step numbers:** they jump from 1 to 3 to 8 to 9.
- **Line 398:** it says `addImages`, but the code uses `allImages`.
- **Line 21:** `–template` uses an en dash where it needs `--template`, so the command will fail as written.
- **All code blocks:** they use curly quotes (`“ ” ‘ ’`), so the JSON, JS and PHP won't parse if copied.
- **Line 69:** "The image attribute be an object" is missing "will".
- **Line 444:** "provded" is a typo.
- **Line 664:** the sentence ends with a comma instead of a period.

I couldn't change the code blocks because this pass doesn't touch code, but the dash and quote problems are the most important fixes in the file.