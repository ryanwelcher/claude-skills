I audited `fixtures/meme-generator.md` in **hybrid** mode, the default for Block Developer Cookbook recipes. The file has about 55 lines of prose outside code blocks, so it was too long for a quick inline check. I sent it to the `ste-audit` helper instead. I haven't changed anything.

## Zone map

| Lines | Zone | Section |
|---|---|---|
| 1–9 | Voice | Title and Overview |
| 11–13 | Action | Setup |
| 15–30 | Action | Standalone |
| 32–63 | Action | Repository |
| 65–69 | Voice | Step 1 intro |
| 71–100 | Action | Step 1 instruction and code |
| 102–128 | Voice | Step 3 API explanation |
| 130–198 | Action | Step 3 instruction and code |
| 200–202 | Voice | Step 3 troubleshooting explanation |
| 204–263 | Action | Step 3 fix instruction and code |
| 265–266 | Voice | Step 3 `useEffect` explanation |
| 267–326 | Action | Step 3 update instruction and code |
| 328 | Voice | Step 3 transition |
| 330–398 | Action | Step 3 final instruction and code |
| 400–405 | Voice | Step 8 intro |
| 406–442 | Action | Step 8 instruction and code |
| 444–445 | Voice | Step 8 explanation |
| 446 | Action | Step 8 check |
| 450–451 | Voice | Step 8 transition |
| 452–492 | Action | Step 8 instruction and code |
| 494 | Action | Step 8 check |
| 498–499 | Voice | Step 8 transition |
| 500–541 | Action | Step 8 instruction and code |
| 543 | Action | Step 8 check |
| 547 | Voice | Step 8 closing |
| 549–553 | Voice | Step 9 intro |
| 555–662 | Action | Step 9 instruction and code |
| 664–666 | Voice | Step 9 explanation |
| 668–674 | Action | Step 9 instruction and check |
| 676 | Voice | Step 9 closing |

## Findings

### Setup

**1. L13**: Rule 14 (use tables for comparisons), the "choose → select" swap, and rule 13 (no "just")
> You can choose to either use the repository which provides a development environment or to just download the standalone plugin

→ Select one of these setup methods:

| Method | Use when |
|---|---|
| Standalone | You want the plugin only, with no development environment |
| Repository | You want the full development environment |

**2. L17–30 (Standalone)**: Rules 2 and 7 (one instruction per step, end with a check), the "once → after" swap, and a repeated word ("completed completed")
> Instructions / Run the following command… / Once the scaffold has completed completed, start the build process… / Finally, make sure to activate the plugin.

→
1. In a terminal, from the plugins directory of your local WordPress installation, run: *(code block unchanged)*
2. After the scaffold finishes, start the build process from inside the new plugin directory: *(code block unchanged)*
3. Activate the plugin.

Make sure that the plugin is active before you continue.

**3. L34–63 (Repository)**: Rules 2, 5, 6 and 7 (one instruction per step, condition first, warning before the step, end with a check), plus the repeated "completed completed"
> Checkout the repository (skip this step if already done) … Start the development environment (make sure you have Docker installed ) … Once the scaffold has completed completed…

→
1. If you have not already cloned the repository, run: *(code unchanged)*
2. Install the dependencies: *(code unchanged)*
3. **NOTE:** This step needs Docker. Start the development environment: *(code unchanged)*
4. From the root of the repository, run: *(code unchanged)*
5. After the scaffold finishes, start the build process from inside the new plugin directory: *(code unchanged)*

Make sure that the build process starts with no errors.

### Step 1

**4. L71**: The "update → change" swap and rule 7 (end with a check)
> Open the block.json file and update it with the following attribute definitions

→ Open `block.json`. Change it to the following attribute definitions:
Add after the code block (L100): Make sure that `block.json` saves with no errors.

### Step 3

**5. L204**: Rule 2 (one instruction per step) and the "update → change" swap
> Remove the fetch call (for now) and update edit.js with the following:

→ Remove the fetch call. Change `edit.js` to the following:

### Step 8

**6. L406 (and L555 in Step 9)**: Rule 9 (no phrasal verbs: "open up")
> Open up block.json and add the following to the supports property:
> Open up meme-generator.php and add the following code inside the init hook callback:

→ Open `block.json`. Add the following to the `supports` property:
→ Open `meme-generator.php`. Add the following code inside the `init` hook callback:

**7. L446**: Rule 13 (no hedging: "you should") and the "choose → select" swap
> Refresh the block and you should now see the option to choose the text color:

→ Refresh the block. The option to select the text color now shows:

### Step 9

**8. L668**: Rule 15 (full paths for UI navigation)
> Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed

→ Save the change. Go to **Site Editor > Styles > Typography**. Make sure that the new fonts show in the list.

## Borderline

- **L200**: "Do you notice that something? There are A LOT of messages…" is mostly a voice passage leading into the fix. If you treat it as an action zone: → Save the file. Refresh the page. Open the console. **CAUTION:** Do not leave the block selected for long: the fetch runs on every render and can crash the browser.
- **L328**: This line mixes a voice transition with an unstated instruction. Only the instruction part would change: → Add the fetch call to the hook.
- **L676**: "Stick a fork in it, you're done!" is an idiom (rule 8), and the recipe has no final check. But it's the closing, a voice zone, so hybrid mode leaves it alone. In strict mode it would become: → "The procedure is complete. Make sure that the meme block shows the selected image, text, and font."

I'd confirm a few things before applying fixes:
- **Finding 8:** The helper guessed the Site Editor path (**Styles > Typography**). Check the real labels on screen.
- **Finding 4:** The check it adds ("saves with no errors") is weak.
- **Step numbers:** The headings jump from Step 1 to Step 3 to Step 8. STE doesn't cover this, but readers will notice.