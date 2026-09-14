The full script is saved to `script.md`. I also saved a matching `teleprompter.md`, since the format template calls for one with every script. It's the spoken lines only, with each block marked on camera or voiceover.

**How it runs:** it opens on your face with the pain ("wrong meme, no way to change it, and yeah, I shipped it like that for a while"). It cuts to the toolbar, then back to camera for your intro. From there:
1. **The setup:** clearing `image` brings the picker back.
2. **How it works:** `BlockControls` is a Slot/Fill, framed with a "forwarding your mail" comparison and then the real detail.
3. **Adding the button:** you narrate as you type the `ToolbarGroup` and `ToolbarButton`.
4. **Try it:** you click the button and the picker comes back.
5. **Recap, then a plain subscribe ask** and "Thanks for watching and I'll see you in the next one."

There's no next-video tease. The end-screen video is left as a TODO.

**Check these before you record (they're flagged in the doc):**
- **`image: false`:** the Cookbook code sets an attribute of type `object` to `false`. That works in the editor, but on reload a value of the wrong type probably gets dropped. Either say that on camera or switch the demo to `undefined`.
- **Only the selected block:** the script says the toolbar shows your button only on the selected block. Check that against the Gutenberg source.
- **Text survives the swap:** make sure the setup and punchline text is still there after you remove and re-pick the image.
- **Doc links:** the `BlockControls` and `ToolbarButton` doc links are TODOs. I didn't want to guess the URLs.

The demo code comes straight from Step 7 of `fixtures/meme-generator-full.md`. The keyword numbers, viDIQ scores, publish date, tier and vault links are all TODO placeholders.

The voice samples have nothing short and edited like this, only stream footage. A few lines from an edited tip video would help anchor this kind of script.