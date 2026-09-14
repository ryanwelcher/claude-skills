I ran an STE pass on `fixtures/meme-generator.md` in **hybrid mode**, the default for Block Developer Cookbook recipes. It covers only the parts where readers act. I didn't edit anything. Finding numbers match line numbers in the file.

## Zone map

| Lines | Section | Zone |
|---|---|---|
| 1–9 | Title, Overview | Voice |
| 13 | Setup | Action (choosing a setup path) |
| 17–30 | Standalone | Action |
| 34–63 | Repository | Action |
| 67–69 | Step 1 intro | Voice (explains the attributes) |
| 71 | Step 1 instruction | Action |
| 104–106, 128 | Step 3 intro | Voice |
| 130, 200, 204, 265 (first sentence), 267, 328, 398 | Step 3 instructions and checks | Action |
| 202, 265 (rest) | Step 3 `useEffect` explanation | Voice |
| 402–404, 450, 498 (first sentence), 547 | Step 8 transitions | Voice |
| 406, 446, 452, 494, 498 (second sentence), 543 | Step 8 instructions and checks | Action |
| 444 | Step 8 `supports` explanation | Voice, but it is really a parameter list |
| 551–553, 664–666 | Step 9 intro and explanation | Voice |
| 555, 668–672 | Step 9 instructions and checks | Action |
| 676 | Closing | Voice |

## Findings

### Setup
**1.** L13: "You can choose to either use the repository which provides a development environment or to just download the standalone plugin"
- **Rules:** Word swaps (choose → select), 13 (no "just"), 14 (a choice between two options belongs in a table).
- **Rewrite:**
  > Select one of these two options:
  >
  > | Option | Use it when |
  > |---|---|
  > | Standalone | You have a local WordPress installation. |
  > | Repository | You want the full development environment. You need Docker for this option. |

### Standalone
**2.** L17–18: a stray "Instructions" label, then "Run the following command in a terminal of your choice from inside the plugins directory…" (20 words, and two ideas).
- **Rules:** 1, 2. These are steps, so they belong in a numbered list.
- **Rewrite:**
  > 1. Open a terminal in the `wp-content/plugins` directory of your local WordPress installation.
  > 2. Run this command:

**3.** L24: "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
- **Rules:** Word swaps (once → when). It also has a doubled word.
- **Rewrite:**
  > 3. When the scaffold is complete, start the build process in the new `meme-generator` directory:

**4.** L30: "Finally, make sure to activate the plugin."
- **Rules:** 15 (no click path), 7 (no final check).
- **Rewrite:**
  > 4. Go to **Plugins > Installed Plugins**.
  > 5. Under **Meme Generator**, select **Activate**.
  > 6. Make sure that the **Meme Generator** block shows in the block inserter.

### Repository
**5.** L34–35: "Checkout the repository (skip this step if already done)"
- **Rules:** 5 (the condition goes first), 13 (use "Optional:").
- **Rewrite:**
  > 1. Optional: If you do not have the repository, clone it:

**6.** L41: "Install the dependencies"
- **Rule:** Use a numbered list.
- **Rewrite:**
  > 2. Install the dependencies:

**7.** L47: "Start the development environment (make sure you have Docker installed )"
- **Rule:** 6. The requirement is tucked inside the step, so readers may miss it until the command fails.
- **Rewrite:**
  > **CAUTION:** Do not run this command without Docker. The command fails if Docker is not installed.
  >
  > 3. Start the development environment:

**8.** L53: "Run the following script from the root of the repository"
- **Rule:** 5 (location first).
- **Rewrite:**
  > 4. From the root of the repository, run this script:

**9.** L59: the same text as finding 3.
- **Rules:** Word swaps, doubled word, 7 (no final check).
- **Rewrite:**
  > 5. When the scaffold is complete, start the build process in the `plugins/meme-generator` directory:
  >
  > *(code block unchanged)*
  >
  > 6. Make sure that the terminal shows no build errors.

### Step 1
**10.** L69: "The image attribute be an object so we can store various details… topText and bottomText attributes…" (36 words, and the grammar is broken)
- **Rule:** 14 (a parameter list written as prose).
- **Rewrite:**
  > | Attribute | Type | Stores |
  > |---|---|---|
  > | `image` | object | Details about the selected image |
  > | `topText` | string | The text at the top of the image |
  > | `bottomText` | string | The text at the bottom of the image |

**11.** L71: "Open the block.json file and update it with the following attribute definitions"
- **Rules:** 2 (two actions), Word swaps (update).
- **Rewrite:**
  > Replace the contents of `block.json` with this code:

### Step 3
**12.** L130: "Add the following to edit.js:"
- **Rules:** 16 (no clear anchor; the code block is actually the whole file), 6 (the crash warning only comes later, at L200).
- **Rewrite:**
  > **CAUTION:** Do not leave the editor open for a long time with this code. The `fetch` call runs on every render, and the browser can crash.
  >
  > Replace the contents of `src/edit.js` with this code:

**13.** L200: "Save, refresh, and open the console. Do you notice that something? There are A LOT of messages… you'll crash browser."
- **Rules:** 2 (three actions in one sentence), 7, Word swaps (A LOT of). The warning moves up to finding 12.
- **Rewrite:**
  > 1. Save `src/edit.js`.
  > 2. Refresh the editor.
  > 3. Open the browser console.
  > 4. Make sure that the console shows many messages from the `fetch` call.

**14.** L204: "Remove the fetch call (for now) and update edit.js with the following:"
- **Rules:** 2, Word swaps (update).
- **Rewrite:**
  > 1. In `src/edit.js`, remove the `fetch` call. You add it again in a later step.
  > 2. Replace the contents of `src/edit.js` with this code:

**15.** L265, first sentence: "Save and refresh the page and notice that every time we select the block in the editor, there is a console message."
- **Rules:** 1, 2, 7.
- **Rewrite:**
  > 1. Save `src/edit.js`.
  > 2. Refresh the editor.
  > 3. Select the block.
  > 4. Make sure that the console shows `useEffect is running` each time you select the block.

**16.** L265, rest of the paragraph: "This parameter accepts an array of dependencies the will trigger… It we add an empty array…"
- **Rules:** 14 (a comparison written as prose), Word swaps (trigger).
- **Rewrite:** keep one voice sentence, then add:
  > | Second parameter of `useEffect` | When the hook runs |
  > |---|---|
  > | Not added | After every render |
  > | `[]` | One time, when the block first renders |
  > | `[ value ]` | When `value` changes |

**17.** L267: "Update the hook with the following:"
- **Rules:** Word swaps, 16.
- **Rewrite:**
  > Replace the contents of `src/edit.js` with this code. The only change is `[]`, added as the second parameter of `useEffect`:

**18.** L328: "Now, you'll see that the hook is only run once ever. This is the exact case we want for our initial fetch so let's add that into the hook."
- **Rules:** 3 ("let's"), 7, 1.
- **Rewrite:**
  > 1. Refresh the editor.
  > 2. Make sure that the console shows `useEffect is running` one time only.
  > 3. Replace the contents of `src/edit.js` with this code. It moves the `fetch` call into the `useEffect` callback:

**19.** L398: "At this point, we have the data being loaded once and then being stored in the addImages variable."
- **Rules:** 11 (-ing forms), 7. The variable name is also wrong: it should be `allImages`.
- **Rewrite:**
  > Refresh the editor. Make sure that the console shows the `data.memes` array one time. The block stores this array in `allImages`.

### Step 8
**20.** L406: "Open up block.json and add the following to the supports property:"
- **Rules:** 9 ("open up"), 2.
- **Rewrite:**
  > In `block.json`, add `html` and `color` to the `supports` property:

**21.** L444: the `supports` explanation (three long sentences, with "allows", "pick", "Choosing").
- **Rules:** 14, Word swaps, 11.
- **Rewrite:**
  > | Property | Value | Result |
  > |---|---|---|
  > | `html` | `false` | The user cannot edit the block as HTML. |
  > | `color.text` | `true` | The user can select a text color from the theme palette. |
  > | `color.background` | `false` | Turns off the background color. It is on by default, and this block does not use it. |
  > | `color.enableContrastChecker` | `false` | Turns off the contrast checker. It compares the text with the theme background, not the image, so it can show false warnings. |

**22.** L446: "Refresh the block and you should now see the option to choose the text color:"
- **Rules:** 13 ("you should"), Word swaps (choose), 7.
- **Rewrite:**
  > 1. Refresh the editor.
  > 2. Select the block.
  > 3. Make sure that the **Color** panel in the block sidebar shows a **Text** option.

**23.** L452: "Update block.json with the following:"
- **Rule:** Word swaps.
- **Rewrite:**
  > In `block.json`, add `typography` to the `supports` property:

**24.** L494: "Refresh the block again and you can now set the font size and control how text is aligned."
- **Rules:** 2, 7.
- **Rewrite:**
  > 1. Refresh the editor.
  > 2. Make sure that the **Typography** panel shows a **Font size** control.
  > 3. Make sure that the block toolbar shows a text alignment control.

**25.** L498, second sentence: "Do do this we're going to use some experimental properties on block.json"
- **Rules:** 6 (the risk of experimental APIs is never stated), 3. It also has a typo.
- **Rewrite:**
  > **CAUTION:** Do not use `__experimental` properties in production without testing. WordPress can change or remove them in a later release.
  >
  > In `block.json`, add these three properties to `supports`:

**26.** L543: "Refresh and you'll see some new options for controlling the font in the block sidebar"
- **Rules:** 7, 15.
- **Rewrite:**
  > 1. Refresh the editor.
  > 2. Make sure that the **Typography** panel shows **Font** and **Appearance** options.
  > 3. If an option is not visible, add it from the **Typography options** menu.

### Step 9
**27.** L555: "Open up meme-generator.php and add the following code inside the init hook callback:"
- **Rules:** 9, 16 (the anchor is vague), 6 (the font file requirement is never stated).
- **Rewrite:**
  > **NOTE:** The Impact font needs the file `assets/fonts/impact.ttf` in the plugin.
  >
  > In `meme-generator.php`, in the `meme_generator_block_init()` function, below `register_block_type()`, add the `wp_register_font_collection()` call:

**28.** L664: "The code above shows examples of all three,"
- **Rule:** 14.
- **Rewrite:** add a table after the explanation:
  > | Font | Source |
  > |---|---|
  > | Arial, Comic Sans | System font. No `fontFace` is needed. |
  > | Impact | Font file in the plugin |
  > | Montserrat | Google Fonts |

**29.** L668: "Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed" (26 words)
- **Rules:** 1, 2, 15 (no click path). The steps to install the fonts are also missing.
- **Rewrite:**
  > 1. Save `meme-generator.php`.
  > 2. Go to **Appearance > Editor > Styles > Typography**.
  > 3. Select **Manage fonts**.
  > 4. Select the **Meme fonts** collection.
  > 5. Select a font.
  > 6. Select **Install**.

**30.** L672: "After installing the fonts, they are available in the block."
- **Rules:** 11 (-ing form), 7.
- **Rewrite:**
  > 7. Select the Meme Generator block.
  > 8. Make sure that the **Font** option in the **Typography** panel shows the installed fonts.

## Borderline

- **B1, L676:** "Stick a fork in it, you're done! Congrats and bon appetite!" This is the card's own example of an idiom (rule 8). It's in the closing, though, which is a voice zone, so hybrid mode leaves it alone. "bon appetite" should be "bon appétit" either way.
- **B2, findings 10, 16, 21 and 28:** these tables replace explanation paragraphs. The paragraphs read as voice, but they hold parameter lists and comparisons. Readers whose first language isn't English would likely gain the most from these changes.
- **B3, rule 16 (show only changed code):** every code block in Step 3 and Step 8 repeats the whole file. Showing only the changed lines would help readers most, but it means cutting the code blocks down. The code itself wouldn't change. My rewrites above keep the full files and add a "The only change is…" sentence instead.
- **B4, finding 29:** Font Library labels (**Manage fonts**, the collection tabs) differ between WordPress versions. Check them against the version the recipe targets.

## Outside STE scope, but they will confuse readers

These are code or structure problems, so I only flagged them:
- The step numbers skip: Step 1, then 3, 8 and 9. Readers will think content is missing.
- All the code blocks use curly quotes (`“ ” ‘ ’`) and `…blockProps` with an ellipsis character. Pasted code will not run.
- L21 has an en dash in `–template`. It should be `--template`.
- "Skill Level:" (L3) is empty.
- The `edit.js` code blocks have no `import` lines for `useState`, `useEffect`, `RichText`, `useBlockProps` and `__`.
- Typos: "provded" (L444), "Reacts", "hook store" (L128), "hooks entire purpose" (L202).