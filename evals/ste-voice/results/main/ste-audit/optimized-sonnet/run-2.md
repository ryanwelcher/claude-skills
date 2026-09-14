## Zone map

| Section (lines) | Zone | Notes |
|---|---|---|
| Title / Skill Level / time (1–5) | Voice | Meta header, not audited |
| Overview (7–9) | Voice | Intro/"why this matters" — swap words, idioms not our concern here |
| Setup (11–13) | Action | Prerequisite/setup instruction |
| Standalone (15–30) | Action | Numbered-in-spirit setup commands |
| Repository (32–63) | Action | Setup commands |
| Step 1 – Setting up the block attributes (65–100) | Mixed | 67–69 explanatory prose (borderline), 71–100 instruction + code = action |
| Step 3 – Getting the images (102–398) | Mixed | Narrative walkthrough functions as action zone throughout; a few encouragement asides are voice |
| Step 8 – Formatting the text (400–547) | Mixed | Action zone; line 547 ("Great work!…") is voice |
| Step 9 – Meme fonts (549–676) | Mixed | Action zone; line 676 closing line is voice (excluded) |

*(Note: the doc jumps from "Step 1" straight to "Step 3" — no Step 2 exists. That's a structural gap, not an STE rule, flagging for your awareness only.)*

## Findings

### Setup (11–13)
1. **L13** — "You can choose to either use the repository... or to just download the standalone plugin" — **Word swap** (choose→select) + **Rule 13** (hedge "just"). Proposed: "Select one of two setup options: the repository (a full development environment) or the standalone plugin."

### Standalone (15–30)
2. **L18** — 20-word single sentence, at the rule-1 limit — no change needed, flagging only as borderline length; leave as is.
3. **L24** — "Once the scaffold has completed completed, start the build process..." — **Word swap** ("Once" meaning "after" → "After"). Proposed: "After the scaffold finishes, start the build process from inside the newly created plugin." (Note: "completed completed" is a duplicate-word typo, not an STE issue — flagging for your awareness, not fixing here.)
4. **L30** — "Finally, make sure to activate the plugin." — **Rule 3** (imperative mood) / **Rule 7** (this reads like a hedge, not an instruction, and the procedure ends without a real check). Proposed: "Activate the plugin. Make sure that it appears in the block inserter."

### Repository (32–63)
5. **L35** — "Checkout the repository (skip this step if already done)" — **Rule 5** (condition first) + **Rule 10** (one word, one meaning — heading says "Checkout" but the command is `git clone`). Proposed: "If you already cloned the repository, skip this step. Otherwise, clone the repository:"
6. **L47** — "Start the development environment (make sure you have Docker installed )" — **Rule 5** (condition first) + **Rule 2** (two actions in one step). Proposed: "Make sure that Docker is installed. Then start the development environment:"

### Step 1 – Setting up the block attributes (65–100)
7. **L69** — "The image attribute be an object so we can store various details about the image and then we need to store a topText and bottomText attributes..." — **Rule 1** (32 words > 25) + **Rule 14** (parameter list written as prose). Proposed: replace with a short lead-in sentence plus a table of the three attributes (name / type / purpose).
8. **L71** — "Open the block.json file and update it with the following attribute definitions" — **Rule 2** (two actions, no location exception applies) + **Word swap** (update→change). Proposed: "Open `block.json`. Change the attributes to the following:"

### Step 3 – Getting the images (102–398)
9. **L128** — "We can use JavaScript's built in fetch function to retrieve the data..." — **Word swap** (retrieve→get).
10. **L151–198 / L200** — The fetch-in-render-body code causes a runaway loop that crashes the browser, but the risk is only disclosed *after* the reader has already added the code (L200: "you'll crash browser"). — **Rule 6** (warnings/cautions must come before the step they apply to). Proposed: add a **CAUTION:** immediately before the code block at L130 — "Do not call `fetch` directly in the render body. It runs on every render and can crash the browser." — then keep the discovery narrative afterward as the "why."
11. **L200** — "There are A LOT of messages" — **Word swap** ("a lot of" → "many").
12. **L204** — "update edit.js with the following" — **Word swap** (update→change).
13. **L265** — "trigger the useEffect to run" — **Word swap** (trigger→start).
14. **L267** — "Update the hook with the following" — **Word swap** (Update→change).

### Step 8 – Formatting the text (400–547)
15. **L404** — "Let's start with choosing the font color." — **Rule 3** (imperative mood, not "let's") + **Rule 11** (-ing as sentence opener). Proposed: "Set the font color first."
16. **L402** — "Now that we can choose and update the image..." (39 words) — **Rule 1** (length) + **Word swaps** (choose→select, update→change).
17. **L406** — "Open up block.json and add the following..." — **Rule 9** (phrasal verb "open up") + **Rule 2** (two actions). Proposed: "Open `block.json`. Add the following to the `supports` property:"
18. **L444** — "This configuration allows the user to pick a text color..." (34 words) — **Rule 1** (length) + **Word swaps** (allows→lets, pick→select).
19. **L446** — "you should now see the option to choose the text color" — **Rule 13** (hedge "you should") + **Word swap** (choose→select). Proposed: "Make sure that the option to select a text color appears."
20. **L452** — "Update block.json with the following" — **Word swap** (Update→change).
21. **L498** — "Finally, let's add some controls... Do do this we're going to use some experimental properties" — **Rule 3** (imperative, not "let's"/"we're going to"). Proposed: "Finally, add controls for font family, style, and weight. Use experimental properties on `block.json` to do this."

### Step 9 – Meme fonts (549–676)
22. **L555** — "Open up meme-generator.php and add the following code..." — **Rule 9** (phrasal verb "open up") + **Rule 2** (two actions). Proposed: "Open `meme-generator.php`. Add the following code inside the `init` hook callback:"
23. **L664** — "There's a lot of code here but the wp_register_font_collection function allows us to..." — **Word swaps** (a lot of→many, allows→lets).
24. **L668** — "Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed" — **Rule 5** (condition first) + **Rule 15** (vague UI path — "look in the Style section" has no click path) + **Rule 2** (multiple actions in one sentence). Proposed: "Save the change. Go to **Site Editor > Styles**. The new fonts appear, ready to install."
25. **Step 9 as a whole** has no final check (**Rule 7**) — it ends on screenshots and a closing joke. Proposed: add "Make sure that the installed font appears in the font family list in the block sidebar." before the closing line.

## Borderline

- **L67–69** — descriptive paragraph about the meme's structure, sitting right before the block.json instruction. Could stay voice (scene-setting) or count as action-zone prerequisite text feeding directly into a parameter table. Flagging rather than deciding.
- **L104–106** — the imgflip API description and sample JSON response: informational/reference rather than instructional. Borderline between voice (context) and action (setup detail the reader needs before writing code).
- **L664** — "The code above shows examples of all three" — mostly voice commentary embedded in an action-heavy paragraph; only the swap words are flagged above, the rest left alone.

Stopping here per instructions — no edits made.