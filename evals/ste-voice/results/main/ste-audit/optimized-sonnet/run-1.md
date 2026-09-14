Now presenting the zone map and findings.

## Zone map — `fixtures/meme-generator.md`

| Lines | Section | Zone |
|---|---|---|
| 1–9 | Title, Skill Level, Overview | **Voice** (intro/tone) |
| 11–13 | Setup (choice of path) | **Action** |
| 15–30 | Standalone setup steps | **Action** |
| 32–63 | Repository setup steps | **Action** |
| 65–69 | Step 1 intro (what the attributes are for) | **Voice** (borderline — explains "why") |
| 71 | "Open the block.json file…" | **Action** |
| 73–100 | code block | Never change |
| 102–128 | Step 3 intro (API explanation) | **Voice** |
| 130–131 | "Add the following to edit.js:" | **Action** |
| 132–198 | code block | Never change |
| 200 | Console-spam warning, after the step | **Action** (misplaced caution) |
| 200 (rest)–202 | useEffect explanation | **Voice** |
| 204 | "Remove the fetch call… and update edit.js…" | **Action** |
| 206–263 | code block | Never change |
| 265 | Dependency-array explanation | **Voice** |
| 267 | "Update the hook with the following:" | **Action** |
| 269–326 | code block | Never change |
| 328 | "Now, you'll see… let's add that into the hook." | **Action** |
| 330–396 | code block | Never change |
| 398 | Result statement | **Voice** |
| 400–402 | Step 8 intro (why we need color/typography controls) | **Voice** (borderline) |
| 404 | "Let's start with choosing the font color." | **Action** |
| 406 | "Open up block.json and add…" | **Action** |
| 408–442 | code block | Never change |
| 444 | Rationale for color supports config | **Voice** (borderline) |
| 446 | "Refresh the block and you should now see…" | **Action** |
| 450 | "Next, let's add some typography controls…" | **Action** |
| 452–492 | instruction + code | **Action** / Never change |
| 494–496 | Result check | **Action** |
| 498 | "Finally, let's add some controls…" | **Action** |
| 500–541 | code block | Never change |
| 543 | Result check | **Action** |
| 549–554 | Step 9 intro | **Voice** |
| 555 | "Open up meme-generator.php and add…" | **Action** |
| 557–662 | code block | Never change |
| 664–666 | Explanation of `wp_register_font_collection` | **Voice** |
| 668 | "Save the change and if you look in the Style section…" | **Action** |
| 670–674 | screenshots + result statement | **Action** |
| 676 | "Stick a fork in it, you're done! Congrats and bon appetite!" | **Voice** (closing — left alone despite idiom) |

## Findings

**Setup**
1. **L13** — "You can choose to either use the repository which provides a development environment or to just download the standalone plugin" — Word swap ("choose" → "select") + Rule 13 (hedge "just"). → "You can select the repository, which provides a development environment, or download the standalone plugin."

**Step 1**
2. **L71** — "Open the block.json file and update it with the following attribute definitions" — Word swap ("update" → "change"). → "Open the block.json file and change it with the following attribute definitions:"

**Step 3**
3. **L200** — "Do you notice that something? There are A LOT of messages from our fetch. In fact, if you leave it long enough you'll crash browser." — Rule 6 (caution appears after the step that causes it) + word swap ("A LOT of" → "many"). This is a `**CAUTION:**` (risk of a crashed browser) and belongs before the fetch code at L151, not after. → Move up and rewrite: "**CAUTION:** Do not leave the block open for long. The uncontrolled fetch call runs many times and can crash the browser."
4. **L204** — "Remove the fetch call (for now) and update edit.js with the following:" — Rule 2 (two actions in one step) + word swap ("update" → "change"). → Split into two steps: "Remove the fetch call. In `edit.js`, change the following:"
5. **L265** — "…every time we select the block in the editor, there is a console message." — Word swap ("trigger" → "start") — *(linter hit is on a different word in this line; verify against source before applying)*.
6. **L267** — "Update the hook with the following:" — Word swap ("Update" → "change"). → "Change the hook with the following:"
7. **L328** — "Now, you'll see that the hook is only run once ever. This is the exact case we want for our initial fetch so let's add that into the hook." — Rule 3 (not imperative — "let's"). → "The hook now runs only once. Add the initial fetch call to the hook:"

**Step 8**
8. **L404** — "Let's start with choosing the font color." — Rule 3 (not imperative) + Rule 11 (-ing as sentence content) + word swap ("choosing" → "select"). → "Select the font color first."
9. **L406** — "Open up block.json and add the following to the supports property:" — Rule 9 (phrasal verb "open up" → "open"). → "Open block.json and add the following to the supports property:"
10. **L446** — "Refresh the block and you should now see the option to choose the text color:" — Rule 13 (hedge "you should") + word swap ("choose" → "select"). → "Refresh the block. Make sure that the option to select the text color shows."
11. **L450** — "Next, let's add some typography controls for the size and alignment of the text." — Rule 3 (not imperative). → "Next, add typography controls for the size and alignment of the text."
12. **L498** — "Finally, let's add some controls to be able to set the font family, style, and weight." — Rule 3 (not imperative) + wordy "to be able to". → "Finally, add controls to set the font family, style, and weight."

**Step 9**
13. **L555** — "Open up meme-generator.php and add the following code inside the init hook callback:" — Rule 9 (phrasal verb). → "Open meme-generator.php and add the following code inside the init hook callback:"
14. **L668** — "Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed" — Rule 5 (condition not first), Rule 15 (vague UI location, no full click path), Rule 1 (26 words > 25). → "Save the change. Go to **Appearance > Editor > Styles**. Make sure that the new fonts are ready to install."

## Borderline

- **L200 caution vs. voice**: the sentence also contains an aside ("Do you notice that something?") that reads like Ryan's voice, but it wraps a real caution. I've treated the caution clause as action-zone and left the rhetorical question as voice-zone filler to drop when the fix is applied — flag if you'd rather keep the question.
- **L402/L444**: Step 8's rationale paragraphs ("Now that we can choose and update the image, you've probably noticed…" / "This configuration allows the user to pick a text color…") triggered linter hits for word swaps, but I classified them as **voice zone** (reasoning/explanation of a design choice) and excluded them from the numbered findings above. Say the word if you want these treated as action zone instead.
- **L328 vs. L398**: "This is the exact case we want for our initial fetch" straddles voice (rationale) and action (leads into the instruction) — I split it, keeping the rationale clause implicit and only rewriting the imperative half.

No edits made. Let me know which numbers to apply.