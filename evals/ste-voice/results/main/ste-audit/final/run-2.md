I used hybrid mode on the full path, because the file has well over 40 lines of prose. The `ste-audit` helper returned the results below. I haven't changed anything yet.

## Zone map

| Lines | Zone | Section |
|---|---|---|
| 1–9 | voice | Title, Skill Level, Overview |
| 11–13 | action | Setup (pick an install path) |
| 15–30 | action | Standalone install |
| 32–63 | action | Repository install |
| 65–70 | voice | Step 1 intro (why these attributes) |
| 71–100 | action | Step 1 instruction and `block.json` code |
| 102–129 | voice | Step 3 API intro |
| 130–198 | action | Step 3 fetch instruction and code |
| 200–204 | action | Step 3 caution and "remove the fetch" instruction |
| 205–263 | action | First `useEffect` code |
| 265–266 | action | Dependency-array explanation (leads into the next step) |
| 267–326 | action | "Update the hook" instruction and code |
| 328–396 | action | Fetch inside the hook: instruction and code |
| 398 | voice | Step 3 closing |
| 400–405 | voice | Step 8 intro |
| 406–442 | action | Color supports instruction and code |
| 444–445 | voice | Why background color and the contrast checker are off |
| 446 | action | Refresh and check |
| 450–496 | action | Typography supports: instruction, code, check |
| 498–541 | action | Font-family supports: instruction and code |
| 543 / 547 | action / voice | Refresh and check / "Great work!" |
| 549–554 | voice | Step 9 intro |
| 555–662 | action | PHP font registration: instruction and code |
| 664–666 | voice | Why the fonts come from different sources |
| 668 | action | Save and check |
| 670–676 | voice | Closing screenshots and sign-off |

## Findings

**Setup (L11–63)**

1. **L11–63**: the setup instructions are loose prose, and their conditions come after the steps. **Rule:** use numbered steps and put each condition or prerequisite before its step. **Rewrite:**
   - **Standalone**
     1. Open a terminal in the plugins directory of your local WordPress installation.
     2. Run the command.
     3. After the scaffold completes, go to the new plugin directory and start the build process.
     4. Activate the plugin.
     - Check: make sure the Meme Generator block shows in the block inserter.
   - **Repository**
     1. Optional: clone the repository. Skip this step if you already have it.
     2. Install the dependencies.
     3. Make sure Docker is installed, then start the development environment.
     4. Run the script from the repository root.
     5. After the scaffold completes, go to the new plugin directory and start the build process.
     - Check: make sure the plugin builds without errors.
   - All code blocks stay as they are.
2. **L24, L59**: "Once the scaffold has completed completed…" **Rule:** fix the typo and swap "once" for "after." **Rewrite:** "After the scaffold completes, go to the new plugin directory and start the build process:" (Finding 1 already includes this.)

**Step 1**

3. **L71**: "Open the block.json file and update it with the following attribute definitions" **Rule:** swap "update" for "change," and end the step with a check. **Rewrite:** "Open `block.json`. Change it to match the following attribute definitions:" Then add after the code: "Make sure that the `image`, `topText`, and `bottomText` attributes appear in `block.json`."

**Step 3**

4. **L200–204**: the warning comes after the reader has already caused the problem ("…you'll crash browser"). **Rule:** put cautions before the step. **Rewrite:** "**CAUTION:** Do not leave the fetch call in the component body. It runs on every render and can crash the browser." Then:
   1. Save the file and refresh the editor.
   2. Open the browser console.
   3. Check: make sure that you do not see repeated fetch messages.
   4. Remove the fetch call from the component body, then change `edit.js` to match the following:
5. **L267**: "Update the hook with the following:" **Rule:** swap "update" for "change." **Rewrite:** "Change the hook to match the following:"

**Step 8**

6. **L446**: "Refresh the block and you should now see the option to choose the text color:" **Rule:** no hedging with "should," and swap "choose" for "select." **Rewrite:** "Refresh the block. Make sure that the text color option shows in the block sidebar:"
7. **L452**: "Update block.json with the following:" **Rule:** swap "update" for "change." **Rewrite:** "Change `block.json` to match the following:"

**Step 9**

8. **L555**: "Open up meme-generator.php and add the following code inside the init hook callback:" **Rule:** make the scope clear and end the step with a check. **Rewrite:** "Open `meme-generator.php`. Inside the `init` hook callback, add the following code:" Then add after the code: "Make sure that the function runs without a PHP error."
9. **L668**: "Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed" **Rule:** one action per step, a clear UI path, and 25 words or fewer per sentence. **Rewrite:**
   1. Save `meme-generator.php`.
   2. Go to **Appearance > Editor > Styles**.
   3. Check: make sure the Meme fonts collection shows in the list.
   - ⚠️ The helper made up the menu path in step 2. Your original only says "Style section of the Site Editor," so check the real path before you apply this one.

## Borderline

- **L128** ("retrieve"), **L444** ("allows"), **L664** ("a lot of", "allows"): the linter flagged these words, but all three sentences explain why, so they're voice zones. I dropped them.
- **L676** "Stick a fork in it… bon appetite!": this is exactly the kind of idiom the card warns against. It's in the closing, though, so hybrid mode leaves it alone. Separately, "appetite" is a typo for "appétit."
- **L35** "Checkout the repository (skip this step if already done)": the condition comes after the instruction. Finding 1 fixes this. It's listed here in case you keep that step as a separate line.

The helper didn't flag some problems outside STE that you might want to fix:
- The step headings jump from Step 1 to Step 3 to Step 8 to Step 9.
- L398 says "addImages," but the variable is `allImages`.
- L200 has "Do you notice that something?" and "crash browser."
- L498 says "Do do this."