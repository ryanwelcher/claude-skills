I ran a hybrid STE pass on `fixtures/meme-generator.md`. That means only the parts where readers act, such as steps, commands and checks, get the Simplified Technical English rules. The intro and the closing keep your voice. The file has about 59 lines of prose, so the audit ran on the full path. **I didn't edit the file.** Below are the changes I would make. Where I think the helper got something wrong, I changed its rewrite and said so.

## Zone map
| Lines | Zone | Section |
|---|---|---|
| 1–9 | voice | Title / Overview |
| 11–63 | action | Setup, Standalone, Repository |
| 65–398 | action | Step 1, Step 3 |
| 400–547 | action | Step 8 – Formatting the text |
| 549–675 | action | Step 9 – Meme fonts |
| 676 | voice | Closing |

## Proposed changes

### Setup
**1. L13**: "You can choose to either use the repository… or to just download the standalone plugin"
Rules: use numbered steps instead of prose, no hedging ("just"), and use "select" instead of "choose".
→ "Use one of these two setups:
- **Repository**: includes a full development environment.
- **Standalone**: installs only the plugin."

**2. L17–30 (Standalone)**: split the prose into numbered steps. Remove the repeated word "completed completed" and add a check at the end.
1. Open a terminal in the `plugins` directory of your local WordPress installation.
2. Run this command: *(code block unchanged)*
3. After the scaffold completes, start the build process in the new plugin directory: *(code block unchanged)*
4. Activate the plugin.
5. Make sure that the **Meme Generator** block shows in the block inserter. *(I changed the helper's version: the block shows in the inserter, not the plugin.)*

**3. L34–63 (Repository)**: the same fix, plus the Docker requirement moves in front of the step it applies to.
1. Optional: clone the repository. Skip this step if you already cloned it.
2. Install the dependencies.
3. **NOTE:** Make sure that Docker is installed before you do the next step.
4. Start the development environment.
5. From the root of the repository, run this script:
6. After the scaffold completes, start the build process in the new plugin directory:
7. Make sure that the build process starts with no errors.

### Step 1
**4. Heading L65**: "Setting up the block attributes"
Rules: no -ing words as openers, and no phrasal verbs ("set up").
→ "Step 1 – Configure the block attributes". The same fix applies to "Getting the images" → "Get the images" and "Formatting the text" → "Format the text".

**5. L69–71**: the first sentence has 32 words and bad grammar ("attribute be"). The instruction also says "update".
→ "The `image` attribute is an object that stores details about the image. The `topText` and `bottomText` attributes store the meme text.
1. Open `block.json`.
2. Change the attribute definitions to the following:"

### Step 3
**6. L128**: "…to retrieve the data but we need to store the results somewhere. We can use Reacts useState hook store…"
→ "Use the JavaScript `fetch` function to get the data. Use the React `useState` hook to store the list of images."

**7. L200**: four sentences in one line, "A LOT of", a missing article, and a risk that shows up after the step instead of before it.
→ "**CAUTION:** Do not leave the page open for a long time after this step. The repeated requests can crash the browser.
1. Save the file.
2. Refresh the page.
3. Open the browser console.
4. Make sure that the console shows many messages from the fetch call."

**8. L204**: "Remove the fetch call (for now) and update edit.js with the following:"
→ "1. Remove the `fetch` call. You add it again later.
2. Change `edit.js` to the following:"

**9. L265–267**: sentences that are too long, typos ("the will", "It we"), and "trigger".
→ "Save the file and refresh the page. When you select the block, the console shows a message. The `useEffect` hook has a dependency parameter that controls when the hook runs:

| Dependency parameter | When the hook runs |
|---|---|
| Not set | After every change to the component |
| `[]` (empty array) | Only when the component first renders |

Change the hook to the following:"

**10. L328**: there's a code block but no instruction.
→ "The hook now runs only one time. In `edit.js`, move the `fetch` call into the hook:"

**11. L398**: the variable name doesn't match the code (`addImages`).
→ "The data now loads one time, and the `allImages` variable stores it."

### Step 8
**12. L402–406**: a 39-word sentence, "choose/update", "each image are", "Let's", and "Open up".
→ "Each image has different colors and a different layout, so the text needs its own controls. First, add a text color control.
1. Open `block.json`.
2. Add the following to the `supports` property:"

**13. L444**: sentences of 34 words or more, "allows/pick", and a typo ("provded").
→ "This configuration lets the user select a text color from the active theme. Background color is on by default, so the block turns it off because it is not needed. The block also turns off the contrast checker. The checker compares the text color with the theme background color, which can give a false warning."

**14. L446**: → "Refresh the block. Make sure that the text color control shows."

**15. L450–452**: "let's" and "Update".
→ "Add typography controls for font size and text alignment. Change `block.json` to the following:"

**16. L494**: → "Refresh the block. Make sure that the font size and alignment controls show."

**17. L498**: "let's", "Do do this", and "to be able to". *(I changed the helper's version: it dropped the first sentence.)*
→ "Add controls for font family, font style, and font weight. These controls use experimental properties. Change `block.json` to the following:"

**18. L543**: → "Refresh the block. Make sure that the new font controls show in the block sidebar."

### Step 9
**19. L555**: "Open up" is a phrasal verb.
→ "1. Open `meme-generator.php`.
2. In the `init` hook callback, add the following code:"

**20. L664**: "a lot of", "allows us", and a sentence that ends in a comma. *(I changed the helper's version: it kept "a lot of".)*
→ "The `wp_register_font_collection` function registers a group of fonts that users can install. The fonts can come from the system, from Google Fonts, or from a font file in a plugin. The code above shows all three."

**21. L668–672**: a vague UI location ("look in the Style section") and no check at the end.
→ "1. Save the file.
2. Go to **Appearance > Editor > Styles > Typography** and open the font library.
3. Install the fonts.
4. Make sure that the fonts show in the block's font family control."
*The helper suggested a different click path ("Site Editor > Styles > Typography > Fonts"). Neither path has been checked against a real site, so confirm the exact labels in your WordPress version before using either.*

## Borderline (not proposed)
- **L676** "Stick a fork in it… bon appetite!": this is the closing, a voice zone, so hybrid mode leaves it alone. Strict mode would change it to "The procedure is complete." Also, "appetite" is a typo for "appétit". That fix isn't about STE.
- **L67–69**: this could count as explanation (a voice zone) rather than instructions. If so, keep only the grammar fix ("attribute be" → "attribute is").
- **Step numbering**: the headings go 1, 3, 8, 9. That's not an STE rule, but the gaps will confuse any reader who follows the steps in order.