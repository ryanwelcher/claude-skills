I wrote the full production document to `script.md`. The format template says every script gets a read-aloud copy, so I also wrote `teleprompter.md`. It has the same spoken lines, with each block marked as on camera or voiceover.

**How the script runs:** The video opens on your face with the meme block that has no way to remove its image. Then:
1. A quick look at what the block toolbar gives you by default.
2. BlockControls explained as a Slot/Fill, framed as a mail slot in a door, plus the fact that the button renders in a different part of the React tree.
3. Adding the `ToolbarButton`, typed out and narrated.
4. Wiring `onClick` to `setAttributes`, where the payoff is that undo works without extra code.
5. Showing the button only when there's an image.
6. A recap to camera, then a generic CTA. There's no next-video tease and the end-screen target is left as a TODO.

I didn't record anything, so none of the code has been run. Check these before recording (they're also `⚠️ CONFIRM` notes in the script and items on the pre-record checklist):
- **Attribute names:** the code uses `imageId` and `imageUrl`, which I guessed. Match them to the meme block's `block.json`. If the URL is read from the `img` markup, one spoken line about how the block saves needs a small change.
- **Toolbar group wrapper:** I wrote `group="other"` with the `ToolbarButton` directly inside, no `ToolbarGroup`. Check that this works on the WordPress version you record on. If it doesn't, add the wrapper and change one line of voiceover.
- **Selected block only:** the script says BlockControls only shows its button when the block is selected, so you don't need an `isSelected` check. I believe that's right, but check it in the Gutenberg source.
- **Icons package:** `@wordpress/icons` has to be installed in the block's `package.json`, or the build will fail on camera.
- **Links:** three of the resource links in the description are from memory and marked TODO.

Everything only you can supply is left as `‹TODO›`: episode number, publish date, tier, keyword numbers, viDIQ scores, the repo link and the thumbnail references. The voice excerpts were enough for this topic.