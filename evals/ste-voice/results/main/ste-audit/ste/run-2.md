**Mode:** Hybrid. The card lists Block Developer Cookbook as hybrid, so this matches. I read the card live from the snapshot path, not the plugin cache. I made no edits.

## Zone map

| Section | Lines | Zone |
|---|---|---|
| Title, Skill Level, time | 1–5 | Metadata (skip) |
| Overview | 9 | Voice |
| Setup | 13 | Action (choose a path) |
| Standalone | 17–30 | Action |
| Repository | 34–62 | Action |
| Step 1 | 67 | Voice (what a meme is) |
|  | 69 | Action: an attribute list written as prose |
|  | 71 | Action |
| Step 3 | 104–106, 128 | Voice (API intro, reasoning) |
|  | 130 | Action |
|  | 200 | Mixed. Action: "Save, refresh, and open the console" and the crash warning. The rest is voice |
|  | 202 | Voice |
|  | 204, 267 | Action |
|  | 265 | Mixed. Action: the first sentence. The rest is voice (how dependencies work) |
|  | 328 | Mixed. Action: the check and "let's add that into the hook" |
|  | 398 | Mixed. Voice summary where the check should be |
| Step 8 | 402, 404, 450, 547 | Voice (transitions, praise) |
|  | 406, 446, 452, 494, 498, 543 | Action |
|  | 444 | Action: a settings list written as prose |
| Step 9 | 551–553, 664–666 | Voice |
|  | 555, 668, 672 | Action |
|  | 676 | Voice (closing) |

## Findings

### Setup
1. **L13** "You can choose to either use the repository… or to just download the standalone plugin"
   *Rules:* 3, 13 ("just"), 14, Word swaps (choose → select)
   *Rewrite:* "Select one of the two setup options:"
   | Option | Use it when |
   |---|---|
   | Standalone | You already have a local WordPress installation. |
   | Repository | You want the included development environment. |

### Standalone
2. **L17–18** "Instructions / Run the following command in a terminal of your choice from inside the plugins directory…"
   *Rule:* 2 (moving to the directory and running the command are two actions)
   *Rewrite:* Delete the stray "Instructions". Then use two steps: "In a terminal, go to the `plugins` directory of your local WordPress installation." and "Run this command:"
3. **L24** "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
   *Rules:* Word swaps (once → when, created → made), 12. Also has a duplicated word.
   *Rewrite:* "When the scaffold is complete, run this command to start the build process in the new plugin:"
4. **L30** "Finally, make sure to activate the plugin."
   *Rules:* 15 (no click path), 3
   *Rewrite:* "Go to **Plugins > Installed Plugins**. Under **Meme Generator**, select **Activate**."
5. **The Standalone steps have no final check.**
   *Rule:* 7
   *Rewrite:* Add "Make sure that the **Meme Generator** block shows in the block inserter."

### Repository
6. **L35** "Checkout the repository (skip this step if already done)"
   *Rules:* 5 (the condition comes last), 9 ("check out")
   *Rewrite:* "If you do not have a local copy of the repository, clone it:"
7. **L47** "Start the development environment (make sure you have Docker installed )"
   *Rule:* 6 (the requirement is inside the step, not before it)
   *Rewrite:* "**CAUTION:** Do not start the environment until Docker is installed and running. If Docker is not running, `npm run env start` fails." Then: "Start the development environment:"
8. **L59** Same sentence as #3.
   *Rewrite:* Same as #3.
9. **The Repository steps have no activation step and no final check.**
   *Rules:* 7, 15
   *Rewrite:* Add "Go to **Plugins > Installed Plugins** and make sure that **Meme Generator** is active."

### Step 1
10. **L69** "The image attribute be an object so we can store various details… topText and bottomText attributes…"
    *Rule:* 14 (an attribute list written as prose)
    *Rewrite:*
    | Attribute | Type | Stores |
    |---|---|---|
    | `image` | `object` | The details of the selected image |
    | `topText` | `string` | The text at the top of the image |
    | `bottomText` | `string` | The text at the bottom of the image |
11. **L71** "Open the block.json file and update it with the following attribute definitions"
    *Rules:* 2, 16, Word swaps (update → change)
    *Rewrite:* "In `block.json`, add these definitions to the `attributes` property:"
12. **Step 1 has no final check.**
    *Rule:* 7
    *Rewrite:* Add "Make sure that the build finishes with no errors."

### Step 3
13. **L130** "Add the following to edit.js:"
    *Rule:* 16 (no anchor, and the whole function is shown)
    *Rewrite:* "In `src/edit.js`, replace the `Edit` function with this code:"
14. **L200** "Save, refresh, and open the console."
    *Rule:* 2 (three actions)
    *Rewrite:* Three steps: "Save `edit.js`." "Refresh the editor." "Open the browser console."
15. **L200** "if you leave it long enough you'll crash browser."
    *Rule:* 6 (the warning comes after the step)
    *Rewrite:* Put this before #14: "**CAUTION:** Do not leave the editor open with this code for a long time. The repeated requests can crash the browser."
16. **L204** "Remove the fetch call (for now) and update edit.js with the following:"
    *Rules:* 2, 16, Word swaps (update → change)
    *Rewrite:* "Remove the `fetch` call from `src/edit.js`." Then: "In `src/edit.js`, replace the `Edit` function with this code:"
17. **L265** "Save and refresh the page and notice that every time we select the block in the editor, there is a console message." (22 words)
    *Rules:* 1, 2, 7, 10 (the file says "refresh the page", "refresh the block", and "refresh")
    *Rewrite:* "Save `edit.js`." "Refresh the editor." "Select the block. Make sure that a console message shows each time you select the block."
18. **L267** "Update the hook with the following:"
    *Rules:* Word swaps (update → change), 16
    *Rewrite:* "In `src/edit.js`, add an empty array (`[]`) as the second argument of `useEffect`:"
19. **L328** "Now, you'll see that the hook is only run once ever."
    *Rules:* 4, 7 (the check has no refresh step)
    *Rewrite:* "Refresh the editor. Make sure that the console message shows only one time."
20. **L328** "…so let's add that into the hook."
    *Rules:* 3, 16
    *Rewrite:* Keep the first sentence in voice. Add the step: "In `src/edit.js`, move the `fetch` call into the `useEffect` callback:"
21. **L398** "we have the data being loaded once and then being stored…"
    *Rules:* 7, 4
    *Rewrite:* Add a check: "Refresh the editor. Make sure that the console shows the `memes` array one time."

### Step 8
22. **L406** "Open up block.json and add the following to the supports property:"
    *Rules:* 9 ("open up"), 2
    *Rewrite:* "In `block.json`, add these settings to the `supports` property:"
23. **L444** "This configuration allows the user to pick a text color… Choosing the background color… is enabled by default…"
    *Rules:* 14, Word swaps (allows → lets, pick/choosing → select), 11
    *Rewrite:*
    | Setting | Value | Result |
    |---|---|---|
    | `html` | `false` | Removes the **Edit as HTML** option. |
    | `color.text` | `true` | Lets the user select a text color from the active theme. |
    | `color.background` | `false` | Removes the background color control. The block does not use it. |
    | `color.enableContrastChecker` | `false` | Removes the contrast warning. The checker compares the text with the theme background, not the image, so the warning can be false. |
24. **L446** "Refresh the block and you should now see the option to choose the text color:"
    *Rules:* 2, 7, 10, 13 ("should"), Word swaps (choose → select)
    *Rewrite:* "Refresh the editor." "Select the block." "Make sure that a text color control shows in the block sidebar."
25. **L452** "Update block.json with the following:"
    *Rules:* Word swaps (update → change), 16
    *Rewrite:* "In `block.json`, add a `typography` object to the `supports` property:"
26. **L494** "Refresh the block again and you can now set the font size and control how text is aligned."
    *Rules:* 2, 7, 10
    *Rewrite:* "Refresh the editor. Make sure that the block sidebar shows the font size and text alignment controls."
27. **L498** "Finally, let's add some controls… Do do this we're going to use some experimental properties on block.json"
    *Rules:* 3, 6, 16
    *Rewrite:* "**CAUTION:** Do not expect `__experimental` properties to stay the same. WordPress can change or remove them in a future release." Then: "In `block.json`, add these properties to the `supports` property:"
28. **L543** "Refresh and you'll see some new options for controlling the font in the block sidebar"
    *Rules:* 3, 7, 11
    *Rewrite:* "Refresh the editor. Make sure that the block sidebar shows the font family, font style, and font weight controls."

### Step 9
29. **L555** "Open up meme-generator.php and add the following code inside the init hook callback:"
    *Rules:* 9, 2, 16
    *Rewrite:* "In `meme-generator.php`, inside `meme_generator_block_init()`, below `register_block_type()`, add:"
30. **L668** "Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed" (26 words)
    *Rules:* 1, 2, 5, 15
    *Rewrite:* "Save `meme-generator.php`." "Go to **Appearance > Editor > Styles > Typography**." "Select **Manage fonts**." "Select the **Meme fonts** tab. Make sure that Arial, Comic Sans, Impact, and Montserrat show." (Check the UI labels against the screen.)
31. **L672** "After installing the fonts, they are available in the block."
    *Rules:* 11, 7 (there is no install step)
    *Rewrite:* "Select the fonts to install." "Select **Install**." "Make sure that the installed fonts show in the block's font family control."

## Borderline

- **B1, L404** "Let's start with choosing the font color." This could be a voice transition or an action lead-in. If it's action, it breaks Rules 3 and 11 and the choose → select swap.
- **B2, L676** "Stick a fork in it, you're done!" This is the closing, so it's voice in hybrid mode. But the card's Rule 8 uses this exact line as its example.
- **B3, L265** The dependency explanation compares no array, an empty array, and an array with values. It could be a Rule 14 table, but it reads as reasoning (voice).
- **B4, L398** The text says "addImages" but the code says `allImages`. This is a technical-name mismatch. Fixing it changes a technical name, so it's your call.
- **B5, L13** "download the standalone plugin": the Standalone path runs `create-block` and doesn't download anything. Changing the wording changes the meaning.
- **B6, Rule 16:** Every code block repeats the whole file or function instead of only the changed lines. Cutting them down means changing code blocks, which the card says never to change.
- **B7, headings:** "Setting up the block attributes", "Getting the images", and "Formatting the text" break Rules 9 and 11 if headings count as action zones. The step numbers also skip: 1, 3, 8, 9.
- **B8, Repository:** After `git clone` there's no step to go into `block-developer-cookbook`. Adding one adds content that isn't there now.
- **B9, #27 and #7:** Both add a CAUTION that isn't in the source now.

## Code problems (not STE, not changed)

These don't break STE rules, but some of them will break the recipe:
- **L21:** `–template` uses an en dash, so the command fails.
- **All code blocks:** They use curly quotes, so the JSON, JS, and PHP won't parse.
- **L532–534:** The `__experimentalFont*` keys sit directly under `supports` instead of under `typography`.
- **`edit.js`:** There are no imports for `useState` or `useEffect`.
- **Font categories:** Some font families use `serif` or `monospace`, but those categories are never registered.