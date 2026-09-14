I ran an STE audit on `fixtures/meme-generator.md` and haven't changed the file. It uses the default hybrid mode, so only the parts where readers take action are in scope: steps, setup commands, checks and click paths. Intros and explanations keep your voice. Rule numbers refer to the STE card, and "Swap" means a word from its approved word list. All proposed changes are below.

## Zone map

| Lines | Section | Zone |
|---|---|---|
| 1–9 | Title, Overview | Voice |
| 11–13 | Setup | Action (choosing a setup path) |
| 15–30 | Standalone | Action |
| 32–63 | Repository | Action |
| 67–69 | Step 1 intro | Voice |
| 71 | Step 1 instruction | Action |
| 104–106, 128 | Step 3 explanation | Voice |
| 130, 200, 204, 267, 328 | Step 3 instructions and checks | Action |
| 202, 265 (explanation part), 398 | Step 3 reasoning about `useEffect` | Voice |
| 402–404, 444, 450, 547 | Step 8 intro, reasoning, transitions | Voice |
| 406, 446, 452, 494, 498, 543 | Step 8 instructions and checks | Action |
| 551–553, 664–666 | Step 9 reasoning | Voice |
| 555, 668–676 | Step 9 instructions, check, closing | Action (676 is borderline) |

## Findings

### Setup
1. **L13** "You can choose to either use the repository which provides a development environment or to just download the standalone plugin"
   *Swap (choose → select), R13 (just), R1, R14.* Rewrite:
   "Select one of these two setup options:
   - **Standalone:** Download only the plugin.
   - **Repository:** Use the repository. It includes a development environment."

### Standalone
2. **L17–18** "Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation."
   *R2 (two actions), R1.* Split it:
   "1. Open a terminal.
   2. Go to the `wp-content/plugins` directory of your local WordPress installation.
   3. Run this command:"
3. **L24** "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
   *Swap (once → after), R2, "completed" is doubled.* Rewrite:
   "4. After the scaffold is complete, run this command to go to the plugin directory and start the build:"
4. **L30** "Finally, make sure to activate the plugin."
   *R15 (no click path), R7 (no final check).* Rewrite:
   "5. Go to **Plugins > Installed Plugins** and click **Activate** below **Meme Generator**.
   6. Make sure that the plugin shows as active."

### Repository
5. **L35** "Checkout the repository (skip this step if already done)"
   *R5 (condition first).* Rewrite: "1. If you do not have the repository, clone it:"
6. **L41** "Install the dependencies"
   Rewrite: "2. Install the dependencies:" (numbered, ends with a colon).
7. **L47** "Start the development environment (make sure you have Docker installed )"
   *R6 (the requirement is buried after the action).* Move it before the step as a note: "**NOTE:** You must install Docker before you do the next step." Then: "3. Start the development environment:"
8. **L53** "Run the following script from the root of the repository"
   Rewrite: "4. From the root of the repository, run this script:"
9. **L59** "Once the scaffold has completed completed, start the build process…"
   Same fix as #3: "5. After the scaffold is complete, run this command to go to the plugin directory and start the build:"
10. **After L63.** *R7.* There is no final check. Add: "6. Make sure that the build runs with no errors in the terminal."

### Step 1
11. **L71** "Open the block.json file and update it with the following attribute definitions"
    *Swap (update → change), R2.* Rewrite:
    "1. Open `block.json`.
    2. Replace the contents with this code:"
    The code block is the full file, so "replace" is more accurate than "add".
12. **Heading L65** "Setting up the block attributes"
    *R9 (set up), R11 (-ing word).* Rewrite: "Step 1 – Add the block attributes"

### Step 3
13. **Heading L102** "Getting the images"
    *R11.* Rewrite: "Step 3 – Get the images"
14. **L130** "Add the following to edit.js:"
    *R16 (no clear anchor).* The code block is the whole `Edit` function. Rewrite: "In `src/edit.js`, replace the `Edit` function with this code:"
15. **L200** "Save, refresh, and open the console. Do you notice that something? There are A LOT of messages from our fetch. In fact, if you leave it long enough you'll crash browser."
    *R6 (caution comes after the step), R2, R8 (question and shouting), Swap (A LOT of → many).* Rewrite:
    "**CAUTION:** Do not keep the editor open for a long time after this change. The fetch runs many times and can crash the browser.
    1. Save the file.
    2. Refresh the editor.
    3. Open the browser console.
    4. Make sure that the console shows many messages from the fetch."
    The caution goes above the L130 instruction, before the code is added.
16. **L204** "Remove the fetch call (for now) and update edit.js with the following:"
    *R2, Swap (update → change).* Rewrite:
    "1. In `src/edit.js`, remove the `fetch` call.
    2. Replace the `Edit` function with this code:"
17. **L265, first sentence** "Save and refresh the page and notice that every time we select the block in the editor, there is a console message."
    *R2, R1, R7.* Rewrite:
    "3. Save the file and refresh the editor.
    4. Select the block.
    5. Make sure that the console shows one message each time you select the block."
    The rest of L265 stays as voice. It also contains "trigger", a typo ("the will") and "It we". Those are borderline (see B2).
18. **L267** "Update the hook with the following:"
    *Swap (Update → change), R16.* Rewrite: "In `src/edit.js`, add an empty dependency array `[]` to `useEffect`:"
19. **After L326.** *R7.* Add: "Refresh the editor. Make sure that the console shows the message only one time."
20. **L328** "Now, you'll see that the hook is only run once ever. This is the exact case we want for our initial fetch so let's add that into the hook."
    *R3 ("let's"), R2.* Keep the first sentence as voice. Replace the second with: "In `useEffect`, add the `fetch` call:"
21. **After L396.** *R7.* Add: "Refresh the editor. Make sure that the console shows the list of memes one time."

### Step 8
22. **Heading L400** "Formatting the text"
    *R11.* Rewrite: "Step 8 – Format the text"
23. **L404–406** "Let's start with choosing the font color. Open up block.json and add the following to the supports property:"
    *R3, Swap (choose → select), R9 ("open up"), R16.* Rewrite: "In `block.json`, add the `html` and `color` properties to `supports`:"
24. **L446** "Refresh the block and you should now see the option to choose the text color:"
    *R13 (you should), Swap (choose → select), R15, R7.* Rewrite:
    "Refresh the editor and select the block. Make sure that the block settings sidebar shows a **Text** color option."
    Confirm that the label matches the screen.
25. **L452** "Update block.json with the following:"
    *Swap, R16.* Rewrite: "In `block.json`, add the `typography` property to `supports`:"
26. **L494** "Refresh the block again and you can now set the font size and control how text is aligned."
    *R7.* Rewrite: "Refresh the editor. Make sure that the sidebar shows the font size control and the toolbar shows the text alignment control."
27. **L498** "Finally, let's add some controls to be able to set the font family, style, and weight. Do do this we're going to use some experimental properties on block.json"
    *R3, R1.* "Do do" is also a typo. Keep a short voice lead-in, then: "In `block.json`, add these three experimental properties to `supports`:"
    A table (R14) would help here:

    | Property | Control |
    |---|---|
    | `__experimentalFontFamily` | Font family |
    | `__experimentalFontStyle` | Font style |
    | `__experimentalFontWeight` | Font weight |
28. **L543** "Refresh and you'll see some new options for controlling the font in the block sidebar"
    *R7, R11.* Rewrite: "Refresh the editor. Make sure that the block sidebar shows the font family, font style, and font weight controls."

### Step 9
29. **L555** "Open up meme-generator.php and add the following code inside the init hook callback:"
    *R9 ("open up"), R16.* The code block is the full file. Rewrite: "In `meme-generator.php`, in the `meme_generator_block_init()` function, below `register_block_type()`, add the `wp_register_font_collection()` call:"
30. **L668** "Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed"
    *R1 (26 words), R2, R15 (vague UI location), R5.* Rewrite:
    "1. Save the file.
    2. Go to **Appearance > Editor > Styles > Typography** and click **Manage fonts**.
    3. Select the **Meme fonts** tab.
    4. Make sure that the four fonts show."
    Confirm the exact click path against current WordPress.
31. **L672** "After installing the fonts, they are available in the block."
    *R11, R2, R7.* Rewrite:
    "5. Install the fonts.
    6. Select the Meme Generator block. Make sure that the fonts show in the font family control."
32. **L676** "Stick a fork in it, you're done! Congrats and bon appetite!"
    *R8 (idiom).* This is the example the card itself uses. Rewrite: "The procedure is complete." See B3 for another option.

## Borderline

- **B1: L21, the command uses an en dash (`–template`) instead of `--template`.** This is code, so it is not an STE change. It is still a real bug: the command fails if a reader copies it. The file also uses curly quotes throughout the JSON, JS and PHP blocks, which breaks any code a reader copies.
- **B2: Voice-zone lines that stay as they are in hybrid mode but may confuse non-native readers.** L9 has emoji and heavy idioms ("whipping up", "spice up", "grab your spatula"). L69 has a typo ("The image attribute be"). L202 has "Luckily for us". L265 has "trigger", "the will" and "It we". L398 says "addImages", but the variable is `allImages`. L402 has "each image are" and "choose and update". Fixing typos and the wrong variable name is worth doing no matter which mode you use.
- **B3: L676, closing.** It could count as a voice-zone closing, which would keep the joke. A middle option is to keep a short "Congrats!" after a plain completion line.
- **B4: Step numbers jump from 1 to 3 to 8 to 9.** The file looks incomplete: Steps 2 and 4–7 are missing, and Step 8 starts with "Now that we can choose and update the image", which is never covered. This isn't an STE rule, but readers following numbered steps will get lost.
- **B5: L444 is a parameter explanation written as prose** (`text`, `background`, `enableContrastChecker`). R14 would turn it into a table, but it reads as reasoning (voice zone). A compromise is a small table plus one sentence of reasoning.

I didn't apply anything and didn't add any refinement-log entries. The biggest improvements for non-native readers are #2–#10 (setup), #15 (the crash warning belongs before the step), #30 (the vague "Style section" location) and B1 (a broken command).