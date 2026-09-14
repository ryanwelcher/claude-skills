## Zone map: `fixtures/meme-generator.md` (hybrid, Block Developer Cookbook)

| Lines | Section | Zone |
|---|---|---|
| 1–9 | Title, Skill Level, Overview | Voice |
| 13 | Setup: choosing a path | Action (a choice between procedures) |
| 17–30 | Standalone | Action |
| 34–62 | Repository | Action |
| 67–69 | Step 1: what a meme is, why the attributes | Voice |
| 71 | Step 1: open block.json | Action |
| 104–106, 128 | Step 3: API background, fetch and useState reasoning | Voice |
| 130 | Step 3: add to edit.js | Action |
| 200 | Save, refresh, open the console | **Mixed**: first sentence is action, the rest is voice |
| 202 | Why useEffect | Voice |
| 204 | Remove fetch, change edit.js | Action |
| 265 | Save and refresh… | **Mixed**: first clause is action, the rest (dependency array) is voice |
| 267 | Change the hook | Action |
| 328 | Add fetch into the hook | Action (worded as voice) |
| 398 | Recap | Voice |
| 402–404 | Step 8 intro | Voice |
| 406, 446, 452, 494, 498, 543 | Step 8: block.json edits and refresh checks | Action |
| 444, 450, 547 | Step 8: what the config does, transitions, praise | Voice |
| 551–553 | Step 9 intro | Voice |
| 555 | Open meme-generator.php | Action |
| 664–666 | What the font collection does, further reading | Voice |
| 668–672 | Site Editor path, install check | Action |
| 676 | Closing | Voice (so "Stick a fork in it" stays) |

## Findings

**Setup**
1. L13: "You can choose to either use the repository… or to just download the standalone plugin". This breaks the Word swaps rule (choose → select) and R13 (just). Rewrite: "Select one setup method: the repository, which includes a development environment, or the standalone plugin."

**Standalone**
2. L17–18: "Run the following command in a terminal of your choice from inside the plugins directory…" This breaks R13 ("of your choice" is filler) and R1. Rewrite: "In a terminal, go to the `plugins` directory of your local WordPress installation. Run this command:"
3. L24: "Once the scaffold has completed completed, start the build process from inside the newly created plugin". This breaks the Word swaps rule (once → after) and R2 (two actions: go into the folder, start the build). It also repeats "completed". Rewrite: "After the scaffold is complete, start the build from inside the new plugin directory:"
4. L30: "Finally, make sure to activate the plugin." This breaks R15 (no click path) and R7 (the procedure has no check). Rewrite: "Go to **Plugins > Installed Plugins** and activate **Meme Generator**. Make sure that the plugin shows as active."

**Repository**
5. L35: "Checkout the repository (skip this step if already done)". This breaks R5 (the condition comes after the instruction). Rewrite: "If you do not have the repository, clone it:"
6. L47: "Start the development environment (make sure you have Docker installed )". This breaks R6 (the requirement comes after the step). Rewrite: "**NOTE:** Docker must be installed and running before you do this step." Then: "Start the development environment:"
7. L53: "Run the following script from the root of the repository". This breaks R16 (the location is at the end, not stated first as an anchor). Rewrite: "From the root of the repository, run this script:"
8. L59: "Once the scaffold has completed completed, start the build process…". This is the same issue as #3, with the same rewrite.
9. L62 (end of Setup): this procedure has no final check, so it breaks R7. Add: "Make sure that the **Meme Generator** block shows in the block inserter."

**Step 1**
10. L71: "Open the block.json file and update it with the following attribute definitions". This breaks R2 (two actions) and the Word swaps rule (update → change). Rewrite: "Open `block.json`." Then: "Replace the file contents with the following:"
11. After L100: Step 1 has no check, so it breaks R7. Add: "Make sure that the build finishes without errors."

**Step 3**
12. L130: "Add the following to edit.js:". This breaks R16. The block replaces the whole `Edit` function, so "Add the following" has no anchor. Rewrite: "In `src/edit.js`, replace the `Edit` function with the following:"
13. L200 (action part): "Save, refresh, and open the console." This breaks R2 (three actions in one sentence). Rewrite as three steps: "Save `edit.js`." / "Refresh the editor." / "Open the browser console."
14. L200: "if you leave it long enough you'll crash browser". This is a risk that appears **after** the step, so it breaks R6. Before L204, add: "**CAUTION:** Do not leave the editor open with this code. The repeated requests can crash the browser."
15. L204: "Remove the fetch call (for now) and update edit.js with the following:". This breaks R2 (two actions) and the Word swaps rule (update → change). Rewrite: "In `src/edit.js`, remove the `fetch` call." Then: "Replace the `Edit` function with the following:"
16. L265 (action part): "Save and refresh the page and notice that every time we select the block…" This breaks R2 (three actions) and R3 (not imperative). Rewrite: "Save the file and refresh the editor. Select the block. Make sure that the console shows a message each time you select it."
17. L267: "Update the hook with the following:". This breaks the Word swaps rule (Update → Change). Rewrite: "Change the `useEffect` call to the following:"
18. L328: "Now, you'll see that the hook is only run once ever… so let's add that into the hook." This breaks R7 (the check is buried in prose), R3 ("let's"), and R16 (no anchor). Rewrite: "Refresh the editor. Make sure that the console shows the message one time only." Then: "In `src/edit.js`, move the `fetch` call inside `useEffect`:"
19. After L396: the step has no check, so it breaks R7. Add: "Refresh the editor. Make sure that the console shows the list of memes one time."

**Step 8**
20. L406: "Open up block.json and add the following to the supports property:". This breaks R9 ("Open up" is a phrasal verb) and R2. Rewrite: "Open `block.json`." Then: "Add the following to the `supports` property:"
21. L446: "Refresh the block and you should now see the option to choose the text color:". This breaks R13 (you should), the Word swaps rule (choose → select), and R15 (no UI location). Rewrite: "Refresh the editor and select the block. Make sure that **Color > Text** shows in the block sidebar."
22. L452: "Update block.json with the following:". This breaks the Word swaps rule. Rewrite: "In `block.json`, change the `supports` property to the following:"
23. L494: "Refresh the block again and you can now set the font size and control how text is aligned." This breaks R7 (weak check) and R15. Rewrite: "Refresh the editor. Make sure that the **Typography** panel shows the font size and text alignment controls."
24. L498: "Finally, let's add some controls… Do do this we're going to use some experimental properties on block.json". This breaks R3 ("let's", "we're going to"). It also has the typo "Do do". Rewrite: "In `block.json`, add the experimental font properties to `supports`:"
25. L498 (before the code): a caution is missing, so this breaks R6. Add: "**CAUTION:** `__experimental` properties can change or be removed in a future WordPress release."
26. L543: "Refresh and you'll see some new options for controlling the font in the block sidebar". This breaks R7 and R15. Rewrite: "Refresh the editor. Make sure that the **Typography** panel shows the font family, font style, and font weight controls."

**Step 9**
27. L555: "Open up meme-generator.php and add the following code inside the init hook callback:". This breaks R9, R2, and R16 (the block replaces the whole file, not just code "inside" the callback). Rewrite: "Open `meme-generator.php`." Then: "Replace the file contents with the following:"
28. L668: "Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed". This breaks R1 (26 words), R2, R15 (vague UI location), and R5. Rewrite: "Save the file." / "Go to **Appearance > Editor > Styles > Typography > Manage fonts**." / "Select the **Meme fonts** tab and install the fonts."
29. L672: "After installing the fonts, they are available in the block." This breaks R11 (an -ing word opens the sentence) and R7. Rewrite: "Select the Meme Generator block. Make sure that the meme fonts show in **Typography > Font**."

## Borderline
- **B1.** L13 as a whole: it could be read as an intro sentence in the voice zone. I classified it as action because the reader picks a procedure there.
- **B2.** L265 "the will trigger the useEffect to run": the linter flagged `trigger` → start, but the line is in the voice part of L265. Hybrid mode leaves it. It also has the typos "the will" and "It we add".
- **B3.** L200 "A LOT of messages": the linter flagged it, but it is in the voice sentence. Leave it, unless the caution in #14 replaces that sentence.
- **B4.** L402 "choose and update the image" and L444 "allows… pick… Choosing… enabled": these are swap words, but they are in the voice zone, so leave them. "Update the image" also refers to a step (Steps 4–7) that is missing from the file. Step numbers jump from 1 to 3 to 8, and the Step 3 text refers to "text fields" from a missing Step 2. This is a content gap, not an STE issue.
- **B5.** L398 "addImages variable" should be `allImages`. This is a technical accuracy problem, not an STE issue.
- **B6.** The UI paths in #4, #21, #28, and #29 are my best guesses at the current WordPress labels. Check them against the screen before you apply those fixes.