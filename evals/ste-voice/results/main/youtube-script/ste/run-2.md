I wrote the full production document and saved it to `script.md`. You asked me not to check in, so there was no beat proposal and no questions.

**Structure:**
1. **Cold open:** starts on your face with the problem: you picked the wrong meme image and had to delete the whole block. Then a screen shot of the toolbar with no way to swap the image, then back to camera for your intro.
2. **Where we're starting:** the `if ( ! image )` early return. A button that clears `image` brings the picker back.
3. **What BlockControls is:** a Slot/Fill that renders into the toolbar, framed with a mail-forwarding analogy.
4. **Adding the button:** type-and-narrate for the imports, `ToolbarGroup`, `ToolbarButton`, `label` (why it matters for accessibility) and `onClick`.
5. **Does it work:** click the button, the picker comes back, and the text stays.
6. **The gotcha:** the button only shows in the return you put it in.
7. **Recap and CTA:** a generic subscribe line and no next-video tease, plus your standard sign-off.

The code comes straight from the Step 7 code in `fixtures/meme-generator-full.md`, so it matches the real block. I ran the anti-AI pass and hard-bans check on every VO line.

**Check these before recording** (each is also a `⚠️ CONFIRM` note in the doc):
- **`image: false` on an `object` attribute:** the recipe does this, but make sure it survives save and reload without a validation warning. If it doesn't, use `undefined` and change that VO line to match.
- **"About ten lines of code":** count your final diff. If it's more, there's a softer line in the note.
- **Text after swapping images:** make sure `topText` and `bottomText` really do stay after you pick a new image, since the VO says so on camera.

**Not done:**
- **No teleprompter file:** the format template asks for one alongside the script, but you asked for just `script.md`. I can make it from the finished VO.
- **Placeholders left for you:** keyword metrics, viDIQ scores, tier, publish date, vault links and the end-screen target are `‹TODO›` because there's no content plan entry.