I read the card and ran `ste-lint.py` on the action-zone line ranges from the map below. The mode is **hybrid**, because the card's default for the Block Developer Cookbook is hybrid. I made no edits.

## Zone map

| Lines | Section | Zone |
|---|---|---|
| 1–5 | Title and metadata | Voice (not audited) |
| 9 | Overview | Voice |
| 13 | Setup: choosing between the two methods | **Action** |
| 17–30 | Standalone: commands and activating the plugin | **Action** |
| 34–63 | Repository: commands | **Action** |
| 65 | Step 1 heading | **Action** (heading) |
| 67–69 | Step 1: what a meme is and why the attributes exist | Voice |
| 71 | Step 1: `block.json` instruction | **Action** |
| 102 | Step 3 heading | **Action** (heading) |
| 104–106, 128 | Step 3: the API and why we use `useState` | Voice |
| 130 | Step 3: "Add the following to edit.js" | **Action** |
| 200 (first sentence) | Save / refresh / console | **Action** |
| 200 (rest), 202 | The crash, why we use `useEffect` | Voice (the crash sentence is really a caution, see #9) |
| 204 | Remove `fetch` / change `edit.js` | **Action** |
| 265 (first sentence) | Save, refresh, watch the console | **Action** |
| 265 (rest) | The dependency array explained | Voice |
| 267, 328 | Change the hook, add `fetch` | **Action** |
| 398 | "At this point…" wrap-up | Voice (the procedure has no final check here) |
| 400 | Step 8 heading | **Action** (heading) |
| 402–404, 450, 547 | Transitions and praise | Voice |
| 406, 446, 452, 494, 498, 543 | `block.json` changes and refresh checks | **Action** |
| 444 | What the `supports` settings do | Voice prose that holds a parameter list (see #20) |
| 551–553, 664–666 | Why fonts matter, the font-collection explanation | Voice |
| 555 | `meme-generator.php` instruction | **Action** |
| 668–672 | Site Editor fonts path and install | **Action** |
| 676 | Closing | Voice (see B1) |

**Linter hits I dropped:** L200 "A LOT of" and L265 "trigger" are both in voice-zone explanation, not in instructions.

## Findings

### Setup

1. **L13:** "You can choose to either use the repository which provides a development environment or to just download the standalone plugin"
   - **Rule:** Word swaps (choose), R13 (just), R14 (a choice between two options written as prose)
   - **Rewrite:** "Use one of these setup methods:" followed by a two-row table:

     | Method | Use when |
     |---|---|
     | **Standalone** | You have a local WordPress installation. |
     | **Repository** | You want the included development environment. Docker is required. |

### Standalone

2. **L17–18:** "Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation."
   - **Rule:** R2 (two actions: go to the directory, then run the command), R13 ("of your choice")
   - **Rewrite:**
     1. "In a terminal, go to the `plugins` directory of your local WordPress installation."
     2. "Run this command:"
3. **L24:** "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
   - **Rule:** Word swaps (once → after). The word "completed" is also doubled.
   - **Rewrite:** "After the scaffold completes, start the build process from the new plugin directory:"
4. **L30:** "Finally, make sure to activate the plugin."
   - **Rule:** R15 (no click path), R7 (the procedure has no final check)
   - **Rewrite:**
     1. "Go to **Plugins > Installed Plugins**."
     2. "Under **Meme Generator**, select **Activate**."
     3. "Make sure that **Meme Generator** shows as active."

### Repository

5. **L35:** "Checkout the repository (skip this step if already done)"
   - **Rule:** R5 (condition first), R13 (optional step not marked). The command is `git clone`, so "Checkout" is also the wrong word.
   - **Rewrite:** "Optional: If you do not have the repository, clone it:"
6. **L47:** "Start the development environment (make sure you have Docker installed )"
   - **Rule:** R6 (the prerequisite comes after the instruction, in parentheses)
   - **Rewrite:** Put "**CAUTION:** Do not start the environment without Docker. The command fails if Docker is not installed and running." above "Start the development environment:"
7. **L59:** "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
   - **Rule:** Word swaps (once). Same doubled word as #3.
   - **Rewrite:** "After the scaffold completes, start the build process from the new plugin directory:"
8. **L63 (end of Setup):** Neither setup method ends with a check.
   - **Rule:** R7
   - **Rewrite:** Add "Make sure that the build process shows no errors and that **Meme Generator** is active." at the end of both methods.

### Step 1 – Setting up the block attributes

9. **L65 heading:** "Setting up the block attributes"
   - **Rule:** R9 (set up), R11 (-ing opener)
   - **Rewrite:** "Step 1 – Add the block attributes"
10. **L71:** "Open the block.json file and update it with the following attribute definitions"
    - **Rule:** R2 (two actions), Word swaps (update)
    - **Rewrite:** "In `block.json`, replace the contents with this code:"

### Step 3 – Getting the images

11. **L102 heading:** "Getting the images"
    - **Rule:** R11
    - **Rewrite:** "Step 3 – Get the images"
12. **L130 and L200:** The browser-crash warning on L200 comes **after** the code that causes the crash.
    - **Rule:** R6
    - **Rewrite:** Put "**CAUTION:** Do not leave the editor open for long after this step. The `fetch` call runs on each render and can crash the browser." above L130.
13. **L130:** "Add the following to edit.js:"
    - **Rule:** R16 (the code block replaces the whole `Edit` function, but the text doesn't say where it goes)
    - **Rewrite:** "In `src/edit.js`, replace the `Edit` function with this code:"
14. **L200, first sentence:** "Save, refresh, and open the console."
    - **Rule:** R2 (three actions), R7 (no check)
    - **Rewrite:**
      1. "Save `src/edit.js`."
      2. "Refresh the editor."
      3. "Open the browser console."
      4. "Make sure that the console shows many messages from `fetch`."
15. **L204:** "Remove the fetch call (for now) and update edit.js with the following:"
    - **Rule:** R2 (two actions), Word swaps (update)
    - **Rewrite:**
      1. "In `src/edit.js`, remove the `fetch` call."
      2. "Replace the `Edit` function with this code:"
16. **L265, first sentence:** "Save and refresh the page and notice that every time we select the block in the editor, there is a console message."
    - **Rule:** R2, R3 (not imperative), R7 (the check is written as narration)
    - **Rewrite:**
      1. "Save `src/edit.js`."
      2. "Refresh the editor."
      3. "Select the block."
      4. "Make sure that the console shows a message each time you select the block."
17. **L267:** "Update the hook with the following:"
    - **Rule:** Word swaps (update), R16 (only `, []` changes, and the text gives no anchor)
    - **Rewrite:** "In `src/edit.js`, add an empty array `[]` as the second argument of `useEffect`:"
18. **L328:** "Now, you'll see that the hook is only run once ever. This is the exact case we want for our initial fetch so let's add that into the hook."
    - **Rule:** R7 (the check is narration), R3 ("let's")
    - **Rewrite:**
      1. "Refresh the editor."
      2. "Make sure that the console shows the message one time only."
      3. "Move the `fetch` call into the `useEffect` callback:"
19. **L398:** The procedure ends with no check.
    - **Rule:** R7
    - **Rewrite:** Add "Refresh the editor. Make sure that the console shows the `data.memes` array one time." Split it into two steps under R2.

### Step 8 – Formatting the text

20. **L400 heading:** "Formatting the text"
    - **Rule:** R11
    - **Rewrite:** "Step 8 – Format the text"
21. **L406:** "Open up block.json and add the following to the supports property:"
    - **Rule:** R9 (open up), R2
    - **Rewrite:** "In `block.json`, add the following to the `supports` property:"
22. **L444:** Explains `html`, `color.text`, `color.background` and `enableContrastChecker` in prose.
    - **Rule:** R14. Also word swaps: allows, pick, choosing, enabled.
    - **Rewrite:** Keep a one-line voice intro, then add a table:

      | Property | Value | Why |
      |---|---|---|
      | `html` | `false` | Blocks HTML editing of the block. |
      | `color.text` | `true` | Lets the user select a text color from the theme. |
      | `color.background` | `false` | This block does not use a background color. |
      | `color.enableContrastChecker` | `false` | The checker compares against the theme background and can show a false warning. |

23. **L446:** "Refresh the block and you should now see the option to choose the text color:"
    - **Rule:** R13 (you should), Word swaps (choose), R3
    - **Rewrite:** "Refresh the editor. Make sure that the **Color** panel shows the **Text** option:" Split it into two steps under R2.
24. **L452:** "Update block.json with the following:"
    - **Rule:** Word swaps (update), R16 (no anchor)
    - **Rewrite:** "In `block.json`, add a `typography` object to `supports`:"
25. **L494:** "Refresh the block again and you can now set the font size and control how text is aligned."
    - **Rule:** R3, R7 (the check is narration)
    - **Rewrite:**
      1. "Refresh the editor."
      2. "Make sure that the **Typography** panel shows the font size and text alignment controls."
26. **L498:** "Finally, let's add some controls to be able to set the font family, style, and weight. Do do this we're going to use some experimental properties on block.json"
    - **Rule:** R3 (no imperative), R16 (no anchor). "Do do" is also a typo.
    - **Rewrite:** "In `block.json`, add these `__experimental` properties to `supports`:"
27. **L543:** "Refresh and you'll see some new options for controlling the font in the block sidebar"
    - **Rule:** R7 (the check is narration), R11 (controlling)
    - **Rewrite:**
      1. "Refresh the editor."
      2. "Make sure that the block sidebar shows the font family, style, and weight controls."

### Step 9 – Meme fonts

28. **L555:** "Open up meme-generator.php and add the following code inside the init hook callback:"
    - **Rule:** R9 (open up), R2, R16 (the code block is the whole file, but the text says "inside the callback")
    - **Rewrite:** "In `meme-generator.php`, inside `meme_generator_block_init()`, below `register_block_type()`, add this code:"
29. **L668:** "Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed"
    - **Rule:** R1 (26 words), R15 (vague UI location), R2, R5
    - **Rewrite:**
      1. "Save `meme-generator.php`."
      2. "Go to **Appearance > Editor > Styles > Typography**."
      3. "Select **Manage fonts**."
      4. "Select the **Install Fonts** tab, then **Meme fonts**."
30. **L672:** "After installing the fonts, they are available in the block."
    - **Rule:** R11 (-ing), R3. The install step is also missing, and there is no final check (R7).
    - **Rewrite:**
      1. "Install the fonts that you want to use."
      2. "Make sure that the new fonts show in the block's font family control."

## Borderline

- **B1, L676:** "Stick a fork in it, you're done! Congrats and bon appetite!" This is a closing, so it's a voice zone and hybrid mode keeps it. The card uses this exact phrase as its R8 example, though. It only needs a rewrite if you treat it as the end of the procedure.
- **B2, L668–672:** I wrote the UI labels in #29 and #30 (**Manage fonts**, **Install Fonts**, the **Meme fonts** tab) from the current Font Library. Check them against the WordPress version the recipe targets before applying.
- **B3, #12:** The caution adds new content where there was only an aside. The alternative is to keep L200 as voice and add nothing.
- **B4, #26:** A `**NOTE:** Properties that start with __experimental can change in a future WordPress release.` would help, but it's new content too.
- **Out of STE scope, flagged only:**
  - **Wrong identifier:** L398 says `addImages` but the code uses `allImages`.
  - **Code typo:** L21 uses an en dash in `–template` where the command needs `--template`. That's code, so I left it alone.
  - **Step numbering:** the steps jump from 1 to 3 to 8 to 9.
  - **Voice-zone typos:** "the will" and "It we" on L265, and "three," on L664.
  - **Empty metadata:** "Skill Level:" on L3 has no value.