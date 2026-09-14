I didn't edit the file. I used hybrid mode, the default for Block Developer Cookbook content, so only the parts where readers act were checked: steps, setup commands and UI paths. The intro and the explanations keep your voice. I made small corrections to a few of the helper's suggested rewrites; they're marked below.

## Which parts get the rules

| Lines | Kind | Section |
|---|---|---|
| 1–13 | Voice (left alone) | Title, Overview, Setup intro |
| 15–63 | Steps | Standalone and Repository install |
| 65–398 | Steps | Step 1, Step 3 |
| 400–676 | Steps | Step 8, Step 9 |

## Proposed changes

**Install sections (L17–63)**

1. **L17–30:** Turn this into numbered steps, one action each. Also fix the doubled word "completed completed":
   1. Open a terminal and go to the `plugins` directory of your local WordPress installation.
   2. Run the following command: *(code block)*
   3. After the scaffold completes, go to the new plugin directory and start the build process: *(code block)*
   4. Activate the plugin.
   5. Make sure that the plugin shows as active in the **Plugins** list.
2. **L47:** "(make sure you have Docker installed )" sits after the step it applies to. Move it before that step: **NOTE:** This step requires Docker. Install Docker before you continue.
3. **L59:** Same doubled word as in 1: "After the scaffold completes, go to the new plugin directory and start the build process:"

**Step 1 and Step 3 (L71–398)**

4. **L71:** "Open the block.json file and update it…" becomes two steps: "1. Open `block.json`. 2. Change the `attributes` property to the following:"
5. **L128:** "retrieve" becomes "get": "Use the `fetch` function to get the data. Store the results with the `useState` hook."
6. **L200:** The crash warning comes after the step that causes the crash. Put a caution before L130: **CAUTION:** This code sends requests without a limit and can crash the browser. Close the tab after you look at the console. Then split L200 into "1. Save `edit.js`. 2. Refresh the page. 3. Open the browser console." *(I changed the helper's wording here.)*
7. **L204:** "1. Remove the `fetch` call. 2. Change `edit.js` to the following:"
8. **L265:** Split "Save and refresh the page and notice…" into "1. Save the file. 2. Refresh the page. 3. Select the block." Fix the typos "the will" and "It we": "This parameter accepts an array of dependencies that make `useEffect` run. If you add an empty array, the hook runs only when the component first renders." *(I changed "trigger" to "make … run", following the word list.)*
9. **L328:** Replace "let's add that into the hook" with "Add the `fetch` call to the hook:"
10. **L398:** The text says `addImages`, but the code uses `allImages`: "At this point, the data loads once and is stored in the `allImages` state variable."

**Step 8 (L402–547)**

11. **L402:** 39 words, "choose/update", and "each image are". Rewrite: "Each meme image has a different color and layout. Add controls for how the text looks and where it sits on the image." *(I changed the helper's wording here.)*
12. **L406:** "Open up" becomes two steps: "1. Open `block.json`. 2. Add the following to the `supports` property:"
13. **L444:** 34 words, "allows/pick", and the typo "provded". Rewrite: "This configuration lets the user select a text color from the active theme's colors. The background color and the contrast checker are off because the block does not use them."
14. **L446:** "Refresh the block. Make sure that the text color option shows in the block sidebar."
15. **L452:** "Change `block.json` to the following:"
16. **L494:** "Refresh the block. Make sure that the font size and text alignment options show."
17. **L498:** Doubled "Do do" and "let's". Rewrite: "Add controls for font family, style, and weight. These controls use experimental properties in `block.json`:"
18. **L543:** "Refresh the block. Make sure that the font family, style, and weight options show in the block sidebar." *(The helper made up a **Settings > Typography** path. I dropped it because the steps should only name menus that are actually on screen.)*

**Step 9 (L555–676)**

19. **L555:** "1. Open `meme-generator.php`. 2. Add the following code inside the `init` hook callback:"
20. **L664–666:** "a lot of" becomes "many". Rewrite: "The `wp_register_font_collection` function registers a group of fonts that users can install. The fonts can come from the system, from Google Fonts, or from a font file in the plugin." Also link the Developer Blog article instead of just mentioning it. The helper suggested a placeholder URL; put the real one in.
21. **L668:** "look in the Style section" is too vague. Make it "1. Save the file. 2. Go to **Appearance > Editor > Styles > Typography**. 3. Make sure that the meme fonts are ready to install." Check this menu path on a real site first.
22. **L676:** "Stick a fork in it… bon appetite!" is an idiom, and the recipe has no final check. Replace it with "The procedure is complete. Make sure that the meme block shows the image, the meme text, and the installed font."

## Borderline
- **Setup intro (L13)** reads as a transition, so I left it in your voice.
- **The "why" paragraphs (L104, L202, L551–553)** could be treated as explanation in your voice rather than steps. Only findings 5, 10 and 20 touch that kind of text.

## Outside this pass, but they break the recipe
- **Broken code:** Every code block has curly quotes (`“ ” ‘ ’`), and the `npx` command uses `–template` instead of `--template`. The JSON, JS, PHP and the command won't run as written. This pass doesn't change code, so fix these on their own.
- **Step numbering:** Step 1 jumps to 3, then to 8 and 9. Step 2 and Steps 4–7 are missing.
- **Placeholders:** The screenshots are still `![screenshot](image)` placeholders, and "Skill Level:" is empty.