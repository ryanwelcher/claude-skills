# 🎬 W‹TODO: n› — Add a Toolbar Button to Your Custom Block with BlockControls (for Developers)

Part of ‹TODO: [[Block …]]› · rules: ‹TODO: [[Operating Rules]]›

| | |
|---|---|
| **Publish** | ‹TODO: date + record/schedule note› |
| **Type / Tier** | ‹TODO: NATIVE/… · Tier …› |
| **Length** | ~4–5 min edited |
| **Target keyword** | *BlockControls toolbar button* (‹TODO: vol/mo · comp›) |
| **Scope** | IN: `BlockControls` as a Slot/Fill, `ToolbarGroup` + `ToolbarButton`, wiring `onClick` to `setAttributes`, where the fill lives in `Edit`. DEFERRED: dropdown menus (`ToolbarDropdownMenu`), the `group` prop in depth, sidebar controls (`InspectorControls`). |
| **Audience** | WordPress block developers who already have a custom block and want editor UI in the block toolbar |
| **Voice** | warm, dev-to-dev — tighter than a stream |

**Stack (the real thing):** Meme Generator block from the Block Developer Cookbook (`@block-developer-cookbook/meme-generator` create-block template) · `@wordpress/block-editor` (`BlockControls`) · `@wordpress/components` (`ToolbarGroup`, `ToolbarButton`) · `@wordpress/scripts` (`npm run start`)

**Legend:** `[SCREEN]` = on screen · `[OST]` = on-screen text · **VO** = spoken

---

## 🎥 SCRIPT

### COLD OPEN (the hook — do NOT slow-roll)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So I built a meme generator block. You pick an image, you type your setup, you type your punchline. Great. And then you realize you picked the wrong image, and there's no way to change it. You have to delete the whole block and start over, which is a pretty bad experience, and yeah, I shipped it like that for a while."
`[SCREEN: screen capture — meme block selected in the editor, cursor hunting around the toolbar for a way to swap the image, finds nothing]`
**VO:** "So let's fix it by putting a button right up here in the block toolbar."
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "I'm Ryan Welcher, a developer advocate at Automattic. And I want to show you how to add your own button to a block's toolbar with `BlockControls`. It's a lot less code than you'd think."
`[OST: "Custom toolbar buttons with BlockControls"]`
> 🎯 The pain is visible in a few seconds: wrong image, no way out. Land the hook on camera, show the missing button, then come back to face for the intro.

### THE SETUP (where we're starting)
`[SCREEN: screen capture — edit.js open in VS Code, scrolled to the two returns in Edit]`
**VO:** "Okay, so here's the block. If there's no image, we return a `Placeholder` with the image picker in it. Once you pick one, we save it to the `image` attribute and render the meme with the two `RichText` fields on top of it. So that `if ( ! image )` check is doing all the work here. If we can get `image` back to empty, the placeholder comes back and you can pick again."
`[OST: "No image → Placeholder · Image → meme"]`
> 🎯 Keep this fast. The one thing viewers need to hold onto is that clearing the attribute brings the picker back. Everything after this depends on it.
> ⚠️ CONFIRM: on-screen code matches the Cookbook's Step 7 starting point (imports already include `BlockControls`, `ToolbarGroup`, `ToolbarButton` in the template — decide whether to show adding them or point out they're already there).

### WHAT BLOCKCONTROLS ACTUALLY IS (the mechanism)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So before we write anything, what is `BlockControls` actually doing? The toolbar isn't part of your block's markup. It lives somewhere else entirely in the editor. `BlockControls` is a Slot/Fill. The editor puts a slot up in the toolbar, and anything you put inside `BlockControls` gets rendered into that slot, even though you wrote it right in the middle of your `Edit` component."
`[SCREEN: simple diagram — Edit component on the left with <BlockControls> highlighted, arrow up to the block toolbar slot]`
**VO:** "It's kind of like forwarding your mail. You write the address in one place and it shows up somewhere else. And because the editor only shows those controls for the selected block, you don't have to worry about your button showing up on every block on the page."
`[OST: "BlockControls = Slot/Fill → block toolbar"]`
> 🎯 This is the developer-grade beat. Analogy frames it, then the real detail (fill renders into the toolbar slot, only for the selected block).
> ⚠️ CONFIRM: `BlockControls` fills only render while the block is selected (check `useBlockControlsFill` / `useBlockEditContext` in the Gutenberg source before recording).

### ADDING THE BUTTON (type-and-narrate)
`[SCREEN: screen capture — edit.js, typing below the closing </section> in the second return]`
**VO:** "All right, so down in the second return, the one that renders the actual meme, right after the closing `section`, I'm going to add `BlockControls`. Inside that we want a `ToolbarGroup`. The group is what gives you that little divider, so your button gets its own section instead of being jammed up against the core controls."
```jsx
<BlockControls>
	<ToolbarGroup>
		<ToolbarButton
			icon="remove"
			label={ __( 'Remove Meme Image', 'meme-generator' ) }
			onClick={ () => setAttributes( { image: false } ) }
		/>
	</ToolbarGroup>
</BlockControls>
```
**VO:** "And then the button itself. `ToolbarButton`. For the icon I'm just passing the string `remove`, which is a dashicon, because I'm a developer and not a designer and nobody wants to see me draw an SVG. The label is what shows up in the tooltip, and it's what a screen reader announces, so don't skip it. And then `onClick` just calls `setAttributes` and sets `image` to `false`. That's it."
`[OST: "BlockControls → ToolbarGroup → ToolbarButton"]`
**VO:** "And notice where this lives. It's only in the return that has an image. So when there's no image, there's no button, which makes sense, right? There's nothing to remove."
> 🎯 The "only in the image branch" point is a nice design detail that falls right out of the code. Keep it, it's short.
> ⚠️ CONFIRM: `image: false` on an attribute typed `object`. It works in the editor, but on reload a value that doesn't match the type gets dropped and falls back to undefined. Decide whether to say that out loud or switch the demo to `image: undefined` and mention why.

### TRY IT (the payoff)
`[SCREEN: screen capture — save, refresh editor, select the meme block, hover the new button to show the tooltip, click it]`
**VO:** "Okay, let's save and see what this does. Select the block, and there's our button, with its own little group. Hover it, and you get the tooltip. And if I click it…"
`[SCREEN: meme disappears, Placeholder with the image picker comes back, pick a different meme]`
**VO:** "…the image is gone and we're right back at the picker. Pick a better meme, and the text is still there, because we only cleared the image. We never touched `topText` or `bottomText`."
> 🎯 Strongest moment in the video. Let the click breathe in the edit before the VO picks back up.
> ⚠️ CONFIRM: the setup/punchline text actually persists after swapping the image on the recording build.

### RECAP (why this matters)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So that's all there is to it. `BlockControls` is a fill that drops whatever you give it into the toolbar slot. You group your buttons with `ToolbarGroup`, and each `ToolbarButton` is just an icon, a label, and an `onClick` that updates your attributes. And that same pattern works for anything you want one click away. Toggles, resets, whatever your block needs."
> 🎯 Keep the recap to what they just watched. Don't introduce dropdowns here, that's scope creep for a quick tip.

### CTA + END SCREEN
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "If you add a toolbar button to one of your own blocks, let me know in the comments what it does. I want to see what you build. There's a lot more block development stuff coming, so if you haven't already, hit subscribe. Thanks for watching and I'll see you in the next one."
`[SCREEN: end screen — subscribe + ‹TODO: end-screen video (no content plan entry — pick from existing uploads)›]`
`[OST: pinned-comment reminder]`

---

## 📦 PACKAGING

**Title (‹TODO: viDIQ-scored — use winner, A/B with #2›):**
- ✅ **Add a Custom Toolbar Button to Your WordPress Block (BlockControls)** — *‹TODO: viDIQ score + why›*
- How to Use BlockControls in a Custom WordPress Block — *‹TODO: score›*
- Your Block Needs a Toolbar Button. Here's How. — *‹TODO: score›*

**Thumbnail concept:** Split frame. Left, the block toolbar zoomed in with the new remove button circled in a bright color. Right, Ryan's face looking at it. 3–4 bold words: "ADD YOUR OWN BUTTON". ‹TODO: template ref›
**viDIQ reference images:** ‹TODO: Ryan's scored image URLs›
**Pinned comment:** "Here's the snippet: `<BlockControls><ToolbarGroup><ToolbarButton icon="remove" label="…" onClick={ … } /></ToolbarGroup></BlockControls>`. What button are you adding to your block's toolbar?"

---

## 📝 YOUTUBE DESCRIPTION (paste-ready)

> Add your own button to a custom WordPress block's toolbar with BlockControls. We add a "remove image" button to a meme generator block, look at how BlockControls works as a Slot/Fill, and wire a ToolbarButton up to setAttributes.

**Chapters:** ‹TODO: time these off the FINAL edit — labels track the SCRIPT beats in order. First chapter must stay 0:00 (YouTube requires it); you need 3+ chapters, each 10s or longer.›
```
0:00 Cold open
‹M:SS› The setup
‹M:SS› What BlockControls actually is
‹M:SS› Adding the button
‹M:SS› Try it
‹M:SS› Recap
```

**Resources:**
- Block Developer Cookbook (Meme Generator recipe): https://github.com/ryanwelcher/block-developer-cookbook
- ‹TODO: BlockControls docs link — confirm URL (Block Editor Handbook, block toolbar and settings sidebar)›
- ‹TODO: ToolbarButton component reference — confirm URL (WordPress Storybook / Gutenberg components README)›

**My Stuff:** (standing footer — reuse as-is)
👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/
👉 WordPress Snippets VSCode extension: https://marketplace.visualstudio.com/items?itemName=ryanwelcher.modern-wordpress-development-snippets
👉 WordPress Playground markdown editor: https://marketplace.visualstudio.com/items?itemName=ryanwelcher.playground-readme-editor

**Connect:** (standing footer — reuse as-is)
https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

#WordPress #Gutenberg #BlockDevelopment #BlockControls #React

---

## ✅ Pre-record checklist
- [ ] CONFIRM `BlockControls` only renders for the selected block (Gutenberg source)
- [ ] Decide `image: false` vs `image: undefined` for the demo (attribute type is `object`)
- [ ] CONFIRM text persists after removing and re-picking the image
- [ ] CONFIRM resource URLs for BlockControls / ToolbarButton docs
- [ ] Meme Generator block scaffolded from the Cookbook template, at the Step 7 starting point, `npm run start` running
- [ ] A meme already picked in the editor (the "wrong" one) for the cold open
- [ ] Slot/Fill diagram graphic ready for the mechanism beat
- [ ] Clean cold-open take
- [ ] Thumbnail from template
- [ ] ‹TODO: schedule note›

## 🔀 Alt hooks (A/B in your head)
1. "You picked the wrong meme. It happens to the best of us. And right now the only way to fix it is to delete the whole block. So let's add a button."
2. "That toolbar that shows up when you select a block? You can put your own buttons in it, and it takes about ten lines of code."
