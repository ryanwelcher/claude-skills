I wrote the full production document to `script.md`. I also saved a `teleprompter.md` read copy, because the format template asks for one alongside every script. It's just the spoken lines from `script.md`, word for word, with each block marked on-camera or voiceover.

**How it's built**
- **Beats:** Cold open (stuck with a bad meme) → The problem → How BlockControls works → Writing the button → Does it work? → The caveat (`false` vs. `undefined`) → Recap + CTA. None of the beats have timestamps, and the chapter times in the description are placeholders.
- **The code** comes straight from Step 7 of the Cookbook meme generator in `fixtures/meme-generator-full.md`: `icon="remove"`, the label "Remove Meme Image", and `setAttributes( { image: false } )`. What's on screen will match the recipe.
- **Technical depth:** the mail-slot analogy sets it up, and then the script explains the real mechanism: BlockControls is a Slot/Fill that renders into the block toolbar. It also covers why the button only exists in the branch that renders the image.
- **The CTA is generic** ("more block development stuff coming"). There's no next-video tease, and the end-screen target is left as a `‹TODO›`.
- I ran the anti-AI and hard-ban pass on every spoken line. The script avoids label-style openers and stacked fragments, and "caveat" appears inside a full sentence.

**Check these before you record (they're `⚠️ CONFIRM` notes in the script):**
1. **Selected block only:** the script says BlockControls only renders for the selected block without an `isSelected` check. I believe that's right, but test it on current trunk.
2. **`false` vs. `undefined`:** the script says setting `image: undefined` leaves the attribute out of the saved block comment, and that setting `false` on an object-typed attribute doesn't cause a validation notice.
3. **Text survives:** the demo line says the top and bottom text stay after you remove the image and pick a new one.
4. **Docs link:** I'm not sure the ToolbarButton docs URL is right.

**Your calls**
- **The caveat beat is optional.** If the video runs long, cut it and move the `undefined` tip into the pinned comment.
- **The Slot/Fill diagram needs to be made.** It's on the checklist.
- **Pick a really bad meme for the first take.** The problem beat's joke depends on it.
- **The voice excerpts were enough for this one.** It's a short demo, and the stream excerpts had the type-and-narrate rhythm it needed.