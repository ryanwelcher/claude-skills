I used **hybrid** mode on the **full** path, because the file has far more than 40 lines of prose. I haven't edited anything.

## Zone map

| Lines | Zone | Section |
|---|---|---|
| 1–6 | voice | Title and skill level |
| 7–9 | voice | Overview |
| 11–13 | action | Setup (pick a path) |
| 15–30 | action | Standalone |
| 32–63 | action | Repository |
| 65–100 | action | Step 1: Block attributes |
| 102–198 | action | Step 3: Getting the images (fetch) |
| 200–263 | action | Introducing useEffect |
| 265–326 | action | The useEffect dependency array |
| 328–398 | action | Moving the fetch into useEffect |
| 400–547 | action | Step 8: Formatting the text |
| 549–676 | action | Step 9: Meme fonts and closing |

Possible misclassification: lines 547 ("Great work!…") and 676 ("Stick a fork in it…") are sign-offs in your voice, not steps. I'd move them to voice. If you agree, finding 18 goes away.

## Findings

### Setup
1. **L13**: "You can choose to either use the repository… or to just download the standalone plugin"
   - **Rule:** Write instructions as steps; word swap; hedge
   - **Rewrite:** "Select one of these options:" followed by a list: **Standalone** (download the plugin only) and **Repository** (clone the full development environment).

### Standalone
2. **L17–30**: The steps are written as prose, "completed completed" repeats a word, and there's no final check.
   - **Rule:** Number the steps; add a check
   - **Rewrite:**
     1. Run the command from the plugins directory.
     2. After the scaffold completes, start the build from inside the new plugin folder.
     3. Activate the plugin.
     4. Make sure that the plugin appears in the block inserter.

### Repository
3. **L34–63**: The steps are written as prose. "Checkout" should be "check out", there's a stray space in "installed )", "completed completed" repeats a word, and there's no final check.
   - **Rule:** Number the steps; add a check
   - **Rewrite:**
     1. Optional: check out the repository.
     2. Install the dependencies.
     3. Make sure that Docker is installed, then start the environment.
     4. Run the prep script from the repository root.
     5. After the scaffold completes, start the build.
     6. Make sure that the block editor loads without errors.

### Step 1: Block attributes
4. **L69–71**: "The image attribute be an object so we can store… hilarious meme text." / "Open the block.json file and update it with…"
   - **Rule:** R1 (32 words); grammar; one action per step
   - **Rewrite:** "The `image` attribute is an object that stores the image details. The `topText` and `bottomText` attributes store the meme text." Then: 1. Open `block.json`. 2. Change the attribute definitions to the following:

### Step 3: Getting the images
5. **L128**: "…built in fetch function to retrieve the data but we need to store the results somewhere."
   - **Rule:** Word swap (retrieve → get)
   - **Rewrite:** "We can use JavaScript's built-in `fetch` function to get the data. We need to store the results in state."

### Introducing useEffect
6. **L200–204**: "Save, refresh, and open the console. Do you notice that something?… you'll crash browser." / "Remove the fetch call (for now) and update edit.js…"
   - **Rule:** One action per step; grammar; warn before the risk
   - **Rewrite:** 1. Save the file. 2. Refresh the page. 3. Open the browser console. "Make sure that you see many repeated messages from the fetch call." **CAUTION:** The repeated fetch calls can crash the browser. 4. Remove the fetch call for now. 5. Change `edit.js` to the following:
   - I changed the helper's CAUTION wording. It said "Do not leave the block open", which doesn't match what the original says.

### The useEffect dependency array
7. **L265**: "Save and refresh the page and notice that…" plus the typos "the will trigger" and "It we add"
   - **Rule:** One action per step; grammar; word swap
   - **Rewrite:** 1. Save the file. 2. Refresh the page. "Make sure that a console message appears every time you select the block." "The dependency parameter controls when `useEffect` runs. It accepts an array of dependencies that start the hook. If the parameter is missing, the hook runs when anything changes. If the array is empty, the hook runs only when the component first renders."
   - This rewrite drops the reason for the step: "we only want the useEffect to run when the block is first mounted." Add that back as a sentence if you approve this one.
8. **L267**: "Update the hook with the following:"
   - **Rule:** Word swap (update → change)
   - **Rewrite:** "Change the hook to the following:"

### Moving the fetch into useEffect
9. **L328**: "Now, you'll see that the hook is only run once ever… so let's add that into the hook."
   - **Rule:** Use the imperative
   - **Rewrite:** "Make sure that the hook runs only once. Add the fetch call to the hook."
10. **L398**: "…being stored in the addImages variable."
    - **Rule:** Wrong name (the code uses `allImages`)
    - **Rewrite:** "Make sure that the data loads once and is stored in the `allImages` variable."

### Step 8: Formatting the text
11. **L402–406**: "…each image are pretty different in color and layout and we need some control…" / "Open up block.json and add…"
    - **Rule:** R1 (39 words); grammar; word swaps; one action per step
    - **Rewrite:** "Each image differs in color and layout. Control the look and position of the text with the following steps." Then: 1. Open `block.json`. 2. Add the following to the `supports` property:
12. **L444**: "This configuration allows the user to pick… provded… which might show a false positive and confuse the user."
    - **Rule:** R1 (34 words); typo; word swaps
    - **Rewrite:** "This configuration lets the user select a text color from the list of colors provided by the active theme. The background color option is on by default. Disable it because it is not used." Then: **NOTE:** "The contrast checker compares the text color against the default theme background color. This can produce a false result, so disable the checker."
13. **L446**: "Refresh the block and you should now see the option to choose the text color:"
    - **Rule:** One action per step; hedge; word swap
    - **Rewrite:** 1. Refresh the block. 2. Make sure that the option to select the text color appears.
14. **L450**: "Next, let's add some typography controls…"
    - **Rule:** Use the imperative
    - **Rewrite:** "Next, add typography controls for the text size and alignment."
15. **L452**: "Update block.json with the following:"
    - **Rule:** Word swap (update → change)
    - **Rewrite:** "Change `block.json` to the following:"

### Step 9: Meme fonts
16. **L664**: "There's a lot of code here but the wp_register_font_collection function allows us… examples of all three,"
    - **Rule:** Word swaps; trailing comma
    - **Rewrite:** "The `wp_register_font_collection` function lets you register a group of fonts that are available to install. Fonts can come from the system, from Google Fonts, or from a font file provided by a plugin."
    - This rewrite drops "The code above shows examples of all three." Keep that sentence if you approve this one.
17. **L668**: "Save the change and if you look in the Style section of the Site Editor, you can see…"
    - **Rule:** R1 (26 words); one action per step; vague UI path
    - **Rewrite:** 1. Save the change. 2. Go to **Site Editor > Styles**. 3. Make sure that the new fonts are ready to install.
    - This changes "Style" to "Styles". Check that this matches the current label in the Site Editor.
18. **L676**: "Stick a fork in it, you're done! Congrats and bon appetite!"
    - **Rule:** Idiom (card rule 8); no final check
    - **Rewrite:** "Make sure that the fonts are installed and available in the block."
    - I'd drop this finding and keep the sign-off as voice, as noted under the zone map.

## Borderline
- **L17, L34:** The leftover "Instructions" labels. Once the steps are numbered, remove them.
- **L406:** "Open up" should be "Open". This finding is covered by #11.
- **L21:** `–template` uses an en dash instead of `--template`, so the command fails if someone copies it. It's a bug in the code block, so it's outside this pass, but you should fix it.
- **Not STE issues:** The step headings skip numbers (1, 3, 8, 9), and "bon appetite" should be "bon appétit".