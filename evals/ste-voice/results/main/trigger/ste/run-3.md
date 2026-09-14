I used the `ste-pass` skill in hybrid mode, which is the default for Block Developer Cookbook recipes. It rewrites only the parts readers act on (steps, prerequisites, warnings, UI paths, checks) and leaves the explanation in your voice. Code, commands, UI labels and technical names stay as they are. Nothing below has been applied.

## Zone map

| Section | Zone |
|---|---|
| Header (Skill Level, time) | Metadata, no changes |
| Overview | Voice |
| Setup | Action (a choice between two paths) |
| Standalone | Action |
| Repository | Action |
| Step 1: explanation (lines 67–69) | Voice |
| Step 1: instruction (line 71) | Action |
| Step 3: API explanation (lines 104–106, 128) | Voice |
| Step 3: instructions and checks (lines 130, 200, 204, 265, 267, 328, 398) | Action (lines 200, 202, 265 mix voice and action) |
| Step 8: explanation (lines 402, 444) | Voice |
| Step 8: instructions and checks (lines 404–406, 446, 450–452, 494, 498, 543) | Action |
| Step 8: line 547 | Voice |
| Step 9: explanation (lines 551–553, 664–666) | Voice |
| Step 9: instructions and checks (lines 555, 668, 672) | Action |
| Line 676 | Closing, but it is also the last line of the procedure (see #34) |

## Findings

### Setup
1. **"You can choose to either use the repository which provides a development environment or to just download the standalone plugin"** breaks rules 13 and 14 (hedging with "just") and the word swap "choose → select". It is also a comparison written as prose.
   **Rewrite:** "Select one of these two setup options:" followed by a table:
   | Option | Use it when |
   |---|---|
   | **Standalone** | You have a local WordPress installation. |
   | **Repository** | You want the full development environment. You need Docker. |

### Standalone
2. **"Instructions"** is a stray label. Remove it.
3. **"Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation."** has 21 words (rule 1), and "of your choice" is filler.
   **Rewrite:** Split into numbered steps. "1. Open a terminal. 2. Go to the `wp-content/plugins` directory of your local WordPress installation. 3. Run this command:"
4. **"Once the scaffold has completed completed, start the build process from inside the newly created plugin"** repeats a word, uses "once" (word swap), and holds two actions (rule 2).
   **Rewrite:** "4. When the command is complete, go to the new `meme-generator` directory and start the build:" I kept this as one step because it matches the single `cd … && npm run start` command. Splitting the command itself is a code change.
5. **"Finally, make sure to activate the plugin."** has a vague UI location (rule 15) and no final check (rule 7).
   **Rewrite:** "5. In the WordPress admin, go to **Plugins > Installed Plugins**. 6. Under **Meme Generator**, click **Activate**. 7. Make sure that the plugin shows as active."

### Repository
6. **"Instructions"** is a stray label. Remove it.
7. **"Checkout the repository (skip this step if already done)"** puts the condition last (rule 5). "Checkout" is also the noun form, and "clone" is the correct technical verb.
   **Rewrite:** "1. If you do not have the repository, clone it:"
8. **"Install the dependencies"** is missing a number and punctuation. **Rewrite:** "2. Install the dependencies:"
9. **"Start the development environment (make sure you have Docker installed )"** has its prerequisite after the step (rule 6) and uses a phrasal-style aside.
   **Rewrite:** Add a prerequisite before step 1: "**NOTE:** This option needs Docker. Install Docker before you start." Then: "3. Start the development environment:"
10. **"Run the following script from the root of the repository"** becomes "4. From the root of the repository, run this script:" (rule 5, anchor first).
11. **"Once the scaffold has completed completed, start the build process from inside the newly created plugin"** has the same problems as #4.
    **Rewrite:** "5. When the script is complete, go to `plugins/meme-generator` and start the build:"
12. The procedure has no final check (rule 7). **Add:** "6. Make sure that the terminal shows no build errors." Also add the activation steps from #5 if this path needs them.

### Step 1: Setting up the block attributes
13. The heading **"Setting up the block attributes"** uses an -ing word (rule 11) and a phrasal verb (rule 9). **Rewrite:** "Step 1 – Add the block attributes"
14. **"Open the block.json file and update it with the following attribute definitions"** has two actions (rule 2) and uses "update" (word swap).
    **Rewrite:** "1. Open `block.json`. 2. Replace the contents with these attribute definitions:"
15. There is no check after the code (rule 7). **Add:** "3. Save the file. Make sure that the build shows no errors."

### Step 3: Getting the images
16. The heading uses an -ing word (rule 11). **Rewrite:** "Step 3 – Get the images"
17. **"Add the following to edit.js:"** has no anchor (rule 16), and the code block is the full component. **Rewrite:** "In `src/edit.js`, replace the `Edit` function with this code:"
18. **"Save, refresh, and open the console."** has three actions (rule 2).
    **Rewrite:** "1. Save the file. 2. Refresh the editor. 3. Open the browser console."
19. **"Do you notice that something? There are A LOT of messages from our fetch. In fact, if you leave it long enough you'll crash browser."** is a warning that comes after the step it applies to (rule 6). It also uses humor and caps (rule 8) and the swap "a lot of → many".
    **Rewrite:** Put a caution **before** the "Add the following to edit.js" step: "**CAUTION:** Do not leave the editor open for a long time with this code. The request runs many times and can crash the browser." After step 3: "The console shows many messages from the request."
20. **"Remove the fetch call (for now) and update edit.js with the following:"** has two actions (rule 2) and uses "update" (word swap). "(for now)" is also unclear.
    **Rewrite:** "1. In `src/edit.js`, remove the `fetch` call. You add it again later. 2. Replace the `Edit` function with this code:"
21. **"Save and refresh the page and notice that every time we select the block in the editor, there is a console message."** has 23 words (rule 1), several actions (rule 2), and is not imperative (rule 3).
    **Rewrite:** "1. Save the file. 2. Refresh the editor. 3. Select the block. 4. Make sure that the console shows a message each time you select the block."
22. **"This parameter accepts an array of dependencies the will trigger the useEffect to run."** uses "trigger" (word swap) and has a typo ("the" for "that"). This sentence is borderline because it is explanation.
    **Rewrite:** "This parameter accepts an array of dependencies. When a dependency changes, `useEffect` runs."
23. **"If the parameter is not added as we have done, the hook is run when ANYTHING is changed. It we add an empty array, it will only run when the component is first rendered."** uses passive voice (rule 4), caps, a typo ("It we"), and "rendered" (word swap).
    **Rewrite:** "If you do not add the parameter, the hook runs after every change. If you add an empty array, the hook runs only one time, when the component first shows."
24. **"Update the hook with the following:"** uses "update" and has no anchor (rules 16 and 10). **Rewrite:** "In `src/edit.js`, add an empty array as the second argument of `useEffect`:"
25. **"Now, you'll see that the hook is only run once ever. This is the exact case we want for our initial fetch so let's add that into the hook."** has no check phrasing (rule 7), a "let's" instruction (rule 3), and the phrasal "add … into". It is also missing an instruction line before the code block.
    **Rewrite:** "1. Save the file and refresh the editor. 2. Make sure that the console shows the message one time only. 3. In `src/edit.js`, move the `fetch` call inside `useEffect`:"
26. **"At this point, we have the data being loaded once and then being stored in the addImages variable."** has -ing forms (rule 11) and no check (rule 7). The variable name is also wrong: the code uses `allImages`.
    **Rewrite:** "Make sure that the console shows the list of memes one time. The block stores the list in `allImages`."

### Step 8: Formatting the text
27. The heading uses an -ing word (rule 11). **Rewrite:** "Step 8 – Format the text"
28. **"Let's start with choosing the font color. Open up block.json and add the following to the supports property:"** uses "let's" (rule 3), an -ing word (rule 11), the phrasal "open up" (rule 9) and "choose" (swap).
    **Rewrite:** "To add a text color control: 1. Open `block.json`. 2. In the `supports` property, add the `html` and `color` settings:"
29. **"Refresh the block and you should now see the option to choose the text color:"** has two clauses, a hedge ("should") (rule 13) and "choose" (swap).
    **Rewrite:** "3. Refresh the editor. 4. Select the block. 5. Make sure that the block settings sidebar shows a **Text** color option." Match the label to what the screen shows.
30. **"Next, let's add some typography controls… Update block.json with the following:"** uses "let's" and "update" (rule 3, swap).
    **Rewrite:** "To add font size and text alignment controls, in `block.json`, add the `typography` property to `supports`:"
31. **"Refresh the block again and you can now set the font size and control how text is aligned."** needs to become a check (rule 7).
    **Rewrite:** "Refresh the editor. Make sure that the sidebar shows the font size and text alignment controls."
32. **"Finally, let's add some controls to be able to set the font family, style, and weight. Do do this we're going to use some experimental properties on block.json"** has more than 20 words total, a typo ("Do do"), and no clear instruction.
    **Rewrite:** Put a note first: "**NOTE:** These properties are experimental. Their names can change in a future WordPress release." Then: "To add font family, style, and weight controls, in `block.json`, add these three properties to `supports`:"
33. **"Refresh and you'll see some new options for controlling the font in the block sidebar"** is not a check (rule 7) and uses an -ing word (rule 11).
    **Rewrite:** "Refresh the editor. Make sure that the block sidebar shows the font family, style, and weight controls."

### Step 9: Meme fonts
34. **"Open up meme-generator.php and add the following code inside the init hook callback:"** uses a phrasal verb (rule 9) and has two actions (rule 2).
    **Rewrite:** "1. Open `meme-generator.php`. 2. In `meme_generator_block_init()`, below `register_block_type()`, add the `wp_register_font_collection()` call:"
35. **"Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed"** has a vague UI location (rule 15), more than 20 words (rule 1), and two actions.
    **Rewrite:** "3. Save the file. 4. Go to **Appearance > Editor > Styles > Typography**. 5. Open the font library. 6. Make sure that the **Meme fonts** collection shows." See borderline item B1.
36. **"After installing the fonts, they are available in the block."** has an -ing opener (rule 11) and no install step.
    **Rewrite:** "7. Install the fonts from the **Meme fonts** collection. 8. Select the meme block. 9. Make sure that the font family control shows the new fonts."
37. **"Stick a fork in it, you're done! Congrats and bon appetite!"** is an idiom (rule 8). Because it closes the procedure, readers whose first language isn't English will hit it right after the last step.
    **Rewrite:** "The procedure is complete." If you want to keep a closing in your voice, put it after an explicit completion line. "Appetite" is also a typo for "appétit".

## Borderline
- **B1 (#35):** I need to check the exact Site Editor path and labels (for example **Manage fonts** or **Install Fonts**) against the current WordPress release before using them. UI labels have to match the screen.
- **B2 (lines 202, 265, 444, 664):** The `useEffect`, dependency array, `supports` and font collection explanations are voice zone, but they carry concepts readers need to follow the steps. In strict mode I would split them into sentences under 25 words and remove "Luckily for us", "deeper dive" and "at the mercy of". In hybrid mode I left them alone, except for #22 and #23, which sit inside the steps.
- **B3:** "Refresh the block" appears in several places. You can't refresh a block, so I used "Refresh the editor" (rule 10, one word per meaning). Tell me if you meant something else.

## Outside STE scope (the card says don't change these, but readers will get stuck)
- **Line 21:** `–template` uses an en dash, so the command fails when copied. It should be `--template`.
- **Code blocks throughout:** They use curly quotes (`“ ” ‘ ’`) and `…blockProps` with an ellipsis character. The JSON, JS and PHP are invalid if copied.
- **Step numbers:** They jump from 1 to 3 to 8 to 9, and a reader can't tell whether content is missing. Either renumber or restore the missing steps (the image picker that Step 8 mentions is not in the file).
- **Line 13:** "download the standalone plugin" doesn't match the Standalone section, which uses `npx` to scaffold the plugin.