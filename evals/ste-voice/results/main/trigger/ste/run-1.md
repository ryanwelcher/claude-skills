I didn't edit the file. The Block Developer Cookbook defaults to **hybrid** mode, so I only rewrote the parts where readers do something: steps, prerequisites, checks and UI paths. The intros, explanations and the closing stay in your voice. You told me not to ask anything, so there's no approval question here. Tell me which numbers to apply.

## Zone map

| Section | Zone |
|---|---|
| Header ("Skill Level", "⏲️ 25 minutes") | Voice |
| Overview | Voice |
| Setup | Action |
| Standalone | Action |
| Repository | Action |
| Step 1: intro (lines 67–69) | Voice |
| Step 1: "Open the block.json file…" (71) | Action |
| Step 3: explanation (104–106, 128) | Voice |
| Step 3: "Add the following…" / "Save, refresh…" / "Remove the fetch call…" / "Update the hook…" (130, 200, 204, 265 first sentence, 267, 328) | Action |
| Step 3: useEffect explanation (202, rest of 265, 398) | Voice |
| Step 8: intro (402, 404) | Voice |
| Step 8: instructions and checks (406, 446, 452, 494, 498, 543) | Action |
| Step 8: config explanation (444), "Great work!" (547) | Voice |
| Step 9: intro (551–553), explanation (664–666) | Voice |
| Step 9: instructions and checks (555, 668, 672) | Action |
| Closing (676) | Voice |

## Findings

### Setup
1. **"You can choose to either use the repository which provides a development environment or to just download the standalone plugin"**
   Breaks: Word swaps (choose), rule 13 ("just"), rule 1.
   → "Use one of these two options. **Standalone:** download the plugin only. **Repository:** get the plugin and a development environment."

### Standalone
2. **"Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation."** (21 words)
   Breaks: rules 1 and 2.
   → "1. Open a terminal. 2. Go to the `wp-content/plugins` directory of your local WordPress installation. 3. Run this command:"
3. **"Once the scaffold has completed completed, start the build process from inside the newly created plugin"**
   Breaks: Word swaps (once, create), rule 2. The word "completed" also appears twice.
   → "4. When the scaffold is complete, go to the new plugin directory and start the build:" This keeps the chained `cd && npm run start` as one command. Stricter option: split it into two steps.
4. **"Finally, make sure to activate the plugin."**
   Breaks: rule 15 (no click path), rule 7 (no check).
   → "5. Go to **Plugins > Installed Plugins** and select **Activate** below **Meme Generator**. 6. Make sure that the plugin shows as active."
5. The heading is followed by a stray "Instructions" label.
   → Remove it, or use "Instructions" as the heading.

### Repository
6. **"Checkout the repository (skip this step if already done)"**
   Breaks: rule 5 (the condition comes last), rule 9 ("checkout" is also used as a verb here).
   → "1. Optional: If you do not have the repository, clone it:"
7. **"Install the dependencies"** → "2. Install the dependencies:" (numbered, with a colon).
8. **"Start the development environment (make sure you have Docker installed )"**
   Breaks: rule 6. The prerequisite appears after the step, inside it.
   → Add a **Prerequisites** list at the top of Setup: "Docker is installed and running." Then: "3. Start the development environment:"
9. **"Run the following script from the root of the repository"**
   Breaks: rule 5.
   → "4. In the root directory of the repository, run this script:"
10. **"Once the scaffold has completed completed, start the build process…"** Same problem as #3.
    → "5. When the scaffold is complete, go to the new plugin directory and start the build:"
11. The procedure has no final check (rule 7).
    → "6. Make sure that the build runs and shows no errors."

### Step 1
12. **Heading "Setting up the block attributes"**
    Breaks: rule 9 (set up), rule 11 (-ing).
    → "Step 1 – Add the block attributes"
13. **"Open the block.json file and update it with the following attribute definitions"**
    Breaks: rule 2 (two actions), Word swaps (update).
    → "1. Open `block.json`. 2. Add these attributes to the `attributes` property:"

### Step 3
14. **Heading "Getting the images"** (rule 11) → "Step 3 – Get the images"
15. **"Add the following to edit.js:"**
    Breaks: rule 16 (no anchor; the block shows the whole function).
    → "In `src/edit.js`, replace the `Edit` function with this code:"
16. **"Save, refresh, and open the console. Do you notice that something? There are A LOT of messages from our fetch. In fact, if you leave it long enough you'll crash browser."**
    Breaks: rule 2 (three actions), rule 6 (the risk comes after the step), Word swaps (a lot of), rule 8.
    → Put this before the Save step: "**CAUTION:** Do not leave the editor open for a long time with this code. The request runs again and again and can crash the browser." Then: "1. Save the file. 2. Refresh the editor. 3. Open the browser console. 4. Make sure that you see many messages from the `fetch` call."
17. **"Remove the fetch call (for now) and update edit.js with the following:"**
    Breaks: rule 2, Word swaps (update), rule 16.
    → "1. In `src/edit.js`, remove the `fetch` call. 2. Below `useState( [] )`, add this `useEffect` hook:"
18. **"Save and refresh the page and notice that every time we select the block in the editor, there is a console message."** (21 words)
    Breaks: rules 1, 2 and 3.
    → "1. Save the file. 2. Refresh the editor. 3. Select the block. 4. Make sure that the console shows a message each time you select the block."
19. **"Update the hook with the following:"**
    Breaks: Word swaps (update), rule 16.
    → "In the `useEffect` hook, add an empty array as the second argument:"
20. **"Now, you'll see that the hook is only run once ever. This is the exact case we want for our initial fetch so let's add that into the hook."**
    Breaks: rule 3 ("let's"), rule 7, and there's no instruction before the code block.
    → "1. Make sure that the console shows the message one time only. 2. In the `useEffect` hook, replace the `console.log` line with the `fetch` call:"
21. **"…being stored in the addImages variable."** The variable name doesn't match the code (`allImages`). That's a correctness bug, not just an STE issue.
    → "…stored in the `allImages` variable."

### Step 8
22. **Heading "Formatting the text"** (rule 11) → "Step 8 – Format the text"
23. **"Open up block.json and add the following to the supports property:"**
    Breaks: rule 9 (open up), rule 2, rule 16.
    → "1. Open `block.json`. 2. Change the `supports` property to this:"
24. **"Refresh the block and you should now see the option to choose the text color:"**
    Breaks: rule 2, rule 13 ("should"), Word swaps (choose), rule 15.
    → "3. Refresh the editor. 4. Select the block. 5. Make sure that the **Color** panel in the block settings sidebar shows a **Text** option."
25. **"Update block.json with the following:"** (Word swaps, rule 16)
    → "In `block.json`, add the `typography` object to the `supports` property:"
26. **"Refresh the block again and you can now set the font size and control how text is aligned."**
    Breaks: rules 2 and 7.
    → "1. Refresh the editor. 2. Make sure that the **Typography** panel shows font size and text alignment options."
27. **"…Do do this we're going to use some experimental properties on block.json"**
    Breaks: rule 3, and there's a typo ("Do do").
    → "In `block.json`, add these experimental properties to the `supports` property:" Put this before the code block.
28. The experimental APIs come with no warning (rule 6).
    → Put this before #27: "**CAUTION:** Do not use `__experimental` properties in production code without tests. WordPress can change or remove them in a future release."
29. **"Refresh and you'll see some new options for controlling the font in the block sidebar"**
    Breaks: rules 2, 7 and 15.
    → "1. Refresh the editor. 2. Make sure that the **Typography** panel in the block settings sidebar shows font family, style, and weight options."

### Step 9
30. **"Open up meme-generator.php and add the following code inside the init hook callback:"**
    Breaks: rule 9, rule 2, rule 16. The code block also shows the whole file.
    → "1. Open `meme-generator.php`. 2. In `meme_generator_block_init()`, below `register_block_type()`, add this code:"
31. **"Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed"**
    Breaks: rules 1, 2, 5 and 15.
    → "3. Save the file. 4. Go to **Appearance > Editor > Styles > Typography** and select **Manage fonts**. 5. Select the **Meme fonts** tab. 6. Install the fonts." I need you to confirm those UI labels against the current UI.
32. **"After installing the fonts, they are available in the block."**
    Breaks: rule 11, rule 7 (not phrased as a check).
    → "7. Make sure that the new fonts show in the font family list of the block."

## Borderline

- **B1. Step numbers skip from 1 to 3, 8 and 9.** A reader may think steps are missing. Renumber to 1–4, or add the missing steps.
- **B2. Line 21, `–template`, is an en dash.** Pasted as-is, the command fails; it needs `--template`. This is inside a code block, so the card says don't change it. It's a real bug, though, so you should fix it yourself.
- **B3. All code blocks use curly quotes (`“ ” ‘ ’`) and `…blockProps`.** Copied code won't run. Same situation as B2: outside what this pass may change, but worth fixing.
- **B4. Lines 265 and 202 mix explanation with a hidden instruction.** For example, "It we add an empty array…" contains the "It/If" typo and uses "trigger" (Word swaps → "run"). I left these as voice, but a short action sentence could be pulled out of each.
- **B5. Line 444 (the config explanation)** uses "allows", "pick", "Choosing" and "enabled". It's a voice zone, but it explains a parameter list. A small table would suit rule 14: `text: true` = users select a text color; `background: false` = off, not used; `enableContrastChecker: false` = off, can show a false warning.
- **B6. Line 664, "The fonts can be available on the system, loaded from Google fonts, or even from a font file…"** This is a comparison of three sources, so it's a candidate for a table (rule 14). It's in a voice zone.
- **B7. Line 666 says "read the related article" but has no link.** Add the URL.
- **B8. Line 676, "Stick a fork in it…"** The card's own example says to rewrite this. It sits in the closing (a voice zone), so hybrid mode keeps it. If you want strict mode: "The procedure is complete."