Mode is **hybrid** (action zones only), which is the card's default for Block Developer Cookbook recipes. I read the card and `fixtures/meme-generator.md` from disk. I haven't edited anything.

## Zone map

| Section | Lines | Zone |
|---|---|---|
| Header (Skill Level, ⏲️ 25 minutes) | 3–5 | Metadata, skipped |
| Overview | 9 | Voice |
| Setup | 13 | Action (picking a path) |
| Standalone | 17–30 | Action |
| Repository | 34–63 | Action |
| Step 1 – Setting up the block attributes | 67–69 | Voice (why) |
| | 71 | Action |
| Step 3 – Getting the images | 104–106, 128 | Voice (why) |
| | 130 | Action |
| | 200 | Mixed: "Save, refresh, and open the console" and the crash warning are action. The rhetorical question is voice. |
| | 202 | Voice |
| | 204 | Action |
| | 265 | Mixed: the first sentence (steps plus a check) is action. The `useEffect` explanation is voice. |
| | 267 | Action |
| | 328 | Mixed: the check and "let's add that into the hook" are action |
| | 398 | Action (the end-of-procedure check) |
| Step 8 – Formatting the text | 402, 404, 444, 450, 547 | Voice |
| | 406, 446, 452, 494, 498, 543 | Action |
| Step 9 – Meme fonts | 551–553, 664, 666, 676 | Voice |
| | 555, 668, 672 | Action |

## Findings

### Setup
**1.** L13: "You can choose to either use the repository which provides a development environment or to just download the standalone plugin"
- **Rules:** Word swaps (choose → select); Rule 13 ("just"); Rule 3 ("You can"); Rule 1 (24 words).
- **Rewrite:** "Select one of the two options below. The **Repository** option includes a development environment. The **Standalone** option gives only the plugin."

### Standalone
**2.** L18: "Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation."
- **Rule:** Rule 1 (23 words).
- **Rewrite:** "Open a terminal in the plugins directory of your local WordPress installation." Then: "Run this command:"

**3.** L24: "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
- **Rules:** Word swaps (once → after, created → made/new); the word "completed" is doubled.
- **Rewrite:** "After the scaffold completes, run this command to open the plugin directory and start the build:"

**4.** L30: "Finally, make sure to activate the plugin."
- **Rules:** Rule 3 (the card keeps "make sure" for checks, not for instructions); Rule 15 (no UI path); Rule 7 (no final check).
- **Rewrite:**
  1. "Go to **Plugins > Installed Plugins**."
  2. "Under **Meme Generator**, click **Activate**."
  3. "Make sure that the plugin shows as active."

### Repository
**5.** L47: "Start the development environment (make sure you have Docker installed )"
- **Rule:** Rule 6. The requirement sits inside the step and should come before the procedure.
- **Rewrite:** Put this before L35: "**CAUTION:** Do not start this procedure without Docker. The `npm run env start` command fails if Docker is not installed and running." Then L47 becomes "Start the development environment:"

**6.** L35: "Checkout the repository (skip this step if already done)"
- **Rules:** Rule 5 (the condition comes last); "Checkout" is not the git action used here.
- **Rewrite:** "If you already have the repository, skip this step. Clone the repository:"

**7.** L59: "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
- **Rules:** Same as #3.
- **Rewrite:** "After the script completes, run this command to open the plugin directory and start the build:"

**8.** The Repository procedure (ends at L63) has no final check.
- **Rule:** Rule 7.
- **Rewrite:** Add "Make sure that the build starts with no errors."

### Step 1
**9.** L71: "Open the block.json file and update it with the following attribute definitions"
- **Rules:** Rule 2 (two actions); Word swaps (update → change); Rule 16 (no anchor, and the whole file is shown).
- **Rewrite:** "In `block.json`, add this `attributes` property:" Show only the `attributes` object.

### Step 3
**10.** L130: "Add the following to edit.js:"
- **Rule:** Rule 16. There is no anchor, and the code actually replaces the whole `Edit` function.
- **Rewrite:** "In `src/edit.js`, replace the `Edit` function with this code:"

**11.** L200: "In fact, if you leave it long enough you'll crash browser."
- **Rules:** Rule 6 (the caution comes after the step it applies to); Rule 12 (missing "the").
- **Rewrite:** Put this before the L130 code: "**CAUTION:** Do not leave the editor open for a long time with this code. The code sends requests in a loop and can crash the browser."

**12.** L200: "Save, refresh, and open the console."
- **Rules:** Rule 2 (three actions); Rule 15 (no path to the console); Rule 7 (no check).
- **Rewrite:**
  1. "Save `src/edit.js`."
  2. "Refresh the editor."
  3. "Open the browser console (in Chrome: **View > Developer > JavaScript Console**)."
  4. "Make sure that the console shows many messages from the `fetch` request."

**13.** L204: "Remove the fetch call (for now) and update edit.js with the following:"
- **Rules:** Rule 2; Word swaps (update → change); Rule 16.
- **Rewrite:**
  1. "In `src/edit.js`, remove the `fetch` call."
  2. "Below `useState()`, add this `useEffect` hook:"

  Then: "**NOTE:** You add the `fetch` call again later in this step."

**14.** L265: "Save and refresh the page and notice that every time we select the block in the editor, there is a console message."
- **Rules:** Rule 2; Rule 1 (24 words); Rule 3 ("we").
- **Rewrite:**
  1. "Save `src/edit.js`."
  2. "Refresh the editor."
  3. "Select the block."
  4. "Make sure that the console shows a message each time you select the block."

**15.** L267: "Update the hook with the following:"
- **Rules:** Word swaps (update → change); Rule 16.
- **Rewrite:** "In `src/edit.js`, add an empty array (`[]`) as the second argument of `useEffect`:"

**16.** L328: "Now, you'll see that the hook is only run once ever."
- **Rules:** Rule 7 (a check written as a description); Rule 4 (passive voice).
- **Rewrite:** "Save `src/edit.js` and refresh the editor. Make sure that the console shows the message one time only."

**17.** L328: "This is the exact case we want for our initial fetch so let's add that into the hook."
- **Rules:** Rule 3 ("let's"); Rule 16 (no anchor).
- **Rewrite:** "In the `useEffect` callback, replace the `console.log()` call with the `fetch` call:"

**18.** L398: "At this point, we have the data being loaded once and then being stored in the addImages variable."
- **Rules:** Rule 7 (no check); Rule 11 ("being loaded", "being stored").
- **Rewrite:** "Save `src/edit.js` and refresh the editor. Make sure that the console shows the `data.memes` array one time."
- **Also:** the text says `addImages`, but the code uses `allImages`.

### Step 8
**19.** L406: "Open up block.json and add the following to the supports property:"
- **Rules:** Rule 9 ("open up"); Rule 2; Rule 16 (the whole file is shown).
- **Rewrite:** "In `block.json`, add these properties to the `supports` object:" Show only `html` and `color`.

**20.** L446: "Refresh the block and you should now see the option to choose the text color:"
- **Rules:** Rule 2; Rule 13 ("should"); Word swaps (choose → select); Rule 15 (no UI location); Rule 7.
- **Rewrite:**
  1. "Refresh the editor."
  2. "Select the block."
  3. "Make sure that the **Color** panel in the block sidebar shows a **Text** option."

**21.** L452: "Update block.json with the following:"
- **Rules:** Word swaps (update → change); Rule 16.
- **Rewrite:** "In `block.json`, in the `supports` object, below `color`, add:" Show only `typography`.

**22.** L494: "Refresh the block again and you can now set the font size and control how text is aligned."
- **Rules:** Rule 2; Rule 7; Rule 15.
- **Rewrite:**
  1. "Refresh the editor."
  2. "Select the block."
  3. "Make sure that the **Typography** panel shows **Size** and the block toolbar shows **Align text**."

**23.** L498: "Do do this we're going to use some experimental properties on block.json"
- **Rules:** Rule 3 ("we're going to"); Rule 16; Rule 6 (the risk of using experimental APIs has no caution before the step). "Do do" is a typo.
- **Rewrite:** First: "**CAUTION:** Do not depend on `__experimental` properties in production. WordPress can change or remove them." Then: "In `block.json`, in the `supports` object, below `typography`, add:"

**24.** L543: "Refresh and you'll see some new options for controlling the font in the block sidebar"
- **Rules:** Rule 2; Rule 7; Rule 11 ("controlling"); Rule 15.
- **Rewrite:**
  1. "Refresh the editor."
  2. "Select the block."
  3. "Make sure that the **Typography** panel shows the **Font** and **Appearance** options."

### Step 9
**25.** L555: "Open up meme-generator.php and add the following code inside the init hook callback:"
- **Rules:** Rule 9 ("open up"); Rule 2; Rule 16 (vague anchor, and the whole file is shown).
- **Rewrite:** "In `meme-generator.php`, in `meme_generator_block_init()`, below `register_block_type()`, add:" Show only the `wp_register_font_collection()` call.

**26.** L668: "Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed"
- **Rules:** Rule 15 (this is the card's own "Style section" example); Rule 2; Rule 5; Rule 7.
- **Rewrite:**
  1. "Save `meme-generator.php`."
  2. "Go to **Appearance > Editor > Styles > Typography**."
  3. "Next to **Fonts**, click **Add fonts**."
  4. "Make sure that the Font Library shows a **Meme fonts** tab."

**27.** L672: "After installing the fonts, they are available in the block."
- **Rules:** Rule 11 ("installing"); an install step is missing; Rule 7.
- **Rewrite:**
  1. "In the **Meme fonts** tab, select the fonts."
  2. "Click **Install**."
  3. "Make sure that the **Font** option in the block sidebar shows the new fonts."

## Borderline

- **A. Step headings** (L65 "Setting up", L102 "Getting", L400 "Formatting"): these break Rules 9 and 11. Headings help readers find their place, but they aren't steps. A possible rewrite is "Step 1 – Add the block attributes".
- **B. L265, the `useEffect` explanation:** this is a list of parameter behaviors written as prose, so Rule 14 applies. It's also voice-zone reasoning. It could become a table: no array → runs after every render; `[]` → runs one time, on mount; `[deps]` → runs when `deps` change. The paragraph also uses "trigger" (Word swaps) and has the typos "the will" and "It we".
- **C. L444, the supports explanation:** also a parameter list in prose (`text`, `background`, `enableContrastChecker`), so a table fits Rule 14. It also breaks Word swaps ("allows", "pick", "Choosing", "enabled"). Typo: "provded".
- **D. L664, the three font sources** (system, Google Fonts, plugin file): a table candidate under Rule 14, in a voice paragraph. It also uses "allows".
- **E. L128 and L402:** voice-zone sentences with swap words ("retrieve", "choose and update").
- **F. L404 and L450** ("Let's start with…", "Next, let's add…"): these are voice transitions, but they also introduce steps. If they stay voice, the steps that follow (#19, #21) carry the instruction.
- **G. L676, "Stick a fork in it, you're done! Congrats and bon appetite!":** this is word for word the card's Rule 8 example. It's a closing, though, so hybrid mode leaves it alone. It also has a typo: "appetite" should be "appétit".
- **H. UI labels in #20, #22, #24, and #26** ("Align text", "Appearance", "Add fonts"): these depend on the WordPress version. Check them against the target version before applying, since the card says to keep labels exactly as they appear on screen.

## Problems outside STE scope (the card says never to change code, so I only flagged these)

- **Code blocks:** every JSON, JS, and PHP block uses curly quotes (`“ ” ‘ ’`) and `…blockProps`, so none of them will parse. L21 uses `–template` (an en dash) where `--template` is needed.
- **Missing steps:** the step numbers go 1, 3, 8, 9, so Steps 2 and 4–7 are missing. The L130 code uses `useState` and `useEffect` but no step imports them.
- **Font placement:** at L532–534, the `__experimentalFont*` keys sit at the top level of `supports`. Current WordPress expects them under `typography`.
- **Font category:** at L623, Impact uses the `monospace` category, but that category is never registered.
- **Missing link:** L666 promises a related article but doesn't link to it.