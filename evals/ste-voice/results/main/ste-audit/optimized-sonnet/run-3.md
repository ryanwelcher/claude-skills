## Zone Map — `fixtures/meme-generator.md`

Destination: **Block Developer Cookbook** → card default is **Hybrid** (action zones only). No override requested, so hybrid stands.

| Section | Lines | Zone |
|---|---|---|
| Title / Skill Level | 1–5 | metadata (n/a) |
| Overview | 7–9 | **Voice** |
| Setup (intro) | 11–13 | **Action** (setup choice) |
| Standalone | 15–30 | **Action** |
| Repository | 32–63 | **Action** |
| Step 1 – Setting up the block attributes | 65–100 | **Mixed** — 67–69 intro is voice-leaning (borderline), 71–100 is action |
| Step 3 – Getting the images | 102–398 | **Mixed** — explanatory asides about `fetch`/`useEffect` (102–104, 128b, 202, 265b, 328b) are voice; instructions + code are action |
| Step 8 – Formatting the text | 400–547 | **Mixed** — instructions/code are action; reasoning paragraphs (e.g. 444b) are voice |
| Step 9 – Meme fonts | 549–676 | **Mixed** — 555–663 instructions/code are action; 664–668 narrative and 666 reference aside are voice-leaning (borderline); 676 closing is **Voice** (out of scope) |

## Findings

### Setup
1. **L13** — "You can choose to either use the repository which provides a development environment or to just download the standalone plugin" — *Word swaps* (choose→select), *Rule 13* (hedge "just"), *Rule 3* (imperative mood).
   → "Select one of two setup options: the repository, which includes a development environment, or the standalone plugin."

### Standalone
2. **L18** — "Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation." — *Rule 1* (21 words > 20 procedural max).
   → "Run the following command in a terminal, from inside the plugins directory of your local WordPress installation."
3. **L24** — "Once the scaffold has completed completed, start the build process from inside the newly created plugin" — *Word swaps* ("Once" meaning "after" → "After"/"When").
   → "After the scaffold finishes, start the build process from inside the new plugin."

### Repository
4. **L35** — "Checkout the repository (skip this step if already done)" — *Rule 5* (condition must come first), *Rule 10* (one word, one meaning — prose says "checkout," code says `clone`).
   → "If you already cloned the repository, skip this step. Otherwise, clone the repository:"
5. **L47** — "Start the development environment (make sure you have Docker installed )" — *Rule 6* (prerequisite must precede the step, as a NOTE).
   → "**NOTE:** Make sure that Docker is installed.
   Start the development environment:"
6. **L59** — same text as #3 (duplicate step). Same fix: "After the scaffold finishes, start the build process from inside the new plugin."

### Step 1 – Setting up the block attributes
7. **L69** — "The image attribute be an object so we can store various details about the image and then we need to store a topText and bottomText attributes to save our hilarious meme text." — *Rule 1* (32 words > 25 descriptive max).
   → "The `image` attribute stores details about the image. The `topText` and `bottomText` attributes store the meme text."
8. **L71** — "Open the block.json file and update it with the following attribute definitions" — *Word swaps* (update→change), *Rule 2* (two actions in one step).
   → "Open `block.json`. Change it to add the following attribute definitions:"

### Step 3 – Getting the images
9. **L128** — "...to retrieve the data..." — *Word swaps* (retrieve→get).
   → "...to get the data..."
10. **L200** — "Save, refresh, and open the console. Do you notice that something? There are A LOT of messages from our fetch. In fact, if you leave it long enough you'll crash browser." — *Rule 2* (three actions in one step), *Rule 3* (rhetorical question, not imperative), *Word swaps* (A LOT of→many), *Rule 6* (caution appears after the step it applies to).
    → "**CAUTION:** Do not leave the block open for long. The repeated fetch calls can crash the browser.
    Save the file. Refresh the page. Open the browser console. The console shows many messages from the fetch call."
11. **L204** — "Remove the fetch call (for now) and update edit.js with the following:" — *Rule 2* (two actions), *Word swaps* (update→change).
    → "Remove the fetch call. Change `edit.js` to the following:"
12. **L265** — "Save and refresh the page and notice that every time we select the block in the editor, there is a console message." — *Rule 2* (multiple actions), *Word swaps* (trigger→start, later in paragraph).
    → "Save the file. Refresh the page. Select the block in the editor. Notice the console message that appears each time."
13. **L267** — "Update the hook with the following:" — *Word swaps* (Update→change).
    → "Change the hook to the following:"
14. **L328** — "Now, you'll see that the hook is only run once ever. This is the exact case we want for our initial fetch so let's add that into the hook." — *Rule 3* (imperative mood — "let's").
    → "The hook now runs only once. Add the fetch call to the hook."

### Step 8 – Formatting the text
15. **L402** — "Now that we can choose and update the image, you've probably noticed that each image are pretty different in color and layout and we need some control over how the text looks and where it sits on the image." — *Rule 1* (39 words), *Word swaps* (choose→select, update→change).
    → "Each image has a different color and layout. Control the text position and appearance to match."
16. **L444** — "This configuration allows the user to pick a text color from the list of colors provded by the active theme. ... We also disable the contrast checker as it will appear based on the contrast between the text color and the default theme background color which might show a false positive and confuse the user." — *Rule 1* (34-word sentence), *Word swaps* (allows→lets, pick→select).
    → "This configuration lets the user select a text color from the list of colors from the active theme." / "We disable the contrast checker. It compares the text color to the default theme background color and can show a false positive that confuses users."
17. **L446** — "Refresh the block and you should now see the option to choose the text color:" — *Word swaps* (choose→select), *Rule 13* (hedge "you should").
    → "Refresh the block. The option to select the text color now appears."
18. **L452** — "Update block.json with the following:" — *Word swaps* (Update→change).
    → "Change `block.json` to the following:"

### Step 9 – Meme fonts
19. **L555** — "Open up meme-generator.php and add the following code inside the init hook callback:" — *Rule 9* (phrasal verb "open up"→"open"), *Rule 2* (two actions).
    → "Open `meme-generator.php`. Add the following code inside the `init` hook callback:"
20. **L664** — "There's a lot of code here but the wp_register_font_collection function allows us to register a group of fonts that are available to be installed." — *Word swaps* (a lot of→many, allows→lets).
    → "This code registers a group of fonts that are available to install, using the `wp_register_font_collection` function."
21. **L668** — "Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed" — *Rule 1* (26 words), *Rule 15* (vague UI location, no click path), *Rule 2* (two actions).
    → "Save the change. Go to **Styles > [exact path]** in the Site Editor. The new fonts are ready to install." *(exact click path unverified — see Borderline C)*

## Borderline

- **A. L67–69** — Step 1's intro sentence describing the meme layout: could stay voice-zone scene-setting or count as action-zone descriptive text since it precedes the attribute steps.
- **B. L102–104, 202, 664 (narrative portions)** — explanatory asides about *why* `fetch`/`useEffect`/font registration work the way they do, sitting inside otherwise action-zone sections. Left as voice per the card's mixed-zone allowance.
- **C. L668** — "the Style section of the Site Editor" needs the real UI path (e.g. **Styles > Typography > Font**) confirmed against the actual editor before the rewrite in finding #21 can be finalized.
- **D. L35** — "Checkout" vs. the code's `git clone`: flagged as a word-swap/consistency issue rather than a "Never change" technical term, since it's prose, not a literal command name.