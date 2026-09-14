I wrote the full production document and saved it to `script.md`. The demo code is taken from Step 7 of `fixtures/meme-generator-full.md`, so what you type on screen matches the cookbook recipe.

**How it runs:** it opens on your face with the problem: you picked the wrong meme image and the only fix was deleting the block. There's a quick cut to the toolbar with no button, then back to camera for the intro. From there:
1. A short look at the starting code.
2. How `BlockControls` works, on camera. It's a Slot/Fill: you write it in your block's code, it shows up in the toolbar, and only when your block is selected. I used mail forwarding as the comparison.
3. You type the button in and narrate it.
4. The payoff: you click the button, pick a new image, and the text you already typed is still there.
5. A caveat, a recap, and a generic CTA with no next-video tease or end-screen target, as you asked.

Every beat is named, with no timestamps. I checked all the spoken lines against the style card's banned phrases and AI tells.

**Needs your eyes before recording:**
- **The `image: false` caveat:** the attribute is typed as an object and the demo sets it to `false`. I claim the value gets saved and then thrown out when the post is loaded again, and that `undefined` is the tidier choice. I didn't test this, so it's marked ⚠️ CONFIRM. The checklist says to cut the beat if it doesn't hold up.
- **"Only when your block is selected":** also marked to confirm on the WordPress version you record on.
- **Doc links:** I didn't check that the developer.wordpress.org links in Resources still work.
- **`‹TODO›` placeholders:** episode number, publish date, tier, keyword numbers, viDIQ scores, thumbnail references and the end-screen target are left for you to fill in.

**Not done:** the format template asks for a matching teleprompter file with every script. You only asked for `script.md`, so I didn't write one. I can generate it from these lines if you want it.