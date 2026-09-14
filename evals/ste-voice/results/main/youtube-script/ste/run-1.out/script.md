# 🎬 W‹TODO: n› — Add a Toolbar Button to Your Custom Block with BlockControls (for Developers)

Part of ‹TODO: [[Block …]]› · rules: ‹TODO: [[Operating Rules]]›

| | |
|---|---|
| **Publish** | ‹TODO: date + record/schedule note› |
| **Type / Tier** | ‹TODO: NATIVE/… · Tier …› |
| **Length** | ~5 min edited |
| **Target keyword** | *wordpress block toolbar button* (‹TODO: vol/mo · comp›) |
| **Scope** | IN: `BlockControls` as a Slot/Fill, `ToolbarGroup` + `ToolbarButton`, wiring `onClick` to `setAttributes`, a "remove image" button on the Meme Generator block. DEFERRED: `group` prop placement, dropdown menus (`ToolbarDropdownMenu`), `InspectorControls`, the rest of the meme block build |
| **Audience** | WordPress developers building custom blocks who want editor UI in the block toolbar |
| **Voice** | warm, dev-to-dev — tighter than a stream |

**Stack (the real thing):** `@wordpress/block-editor` (`BlockControls`), `@wordpress/components` (`ToolbarGroup`, `ToolbarButton`), `@wordpress/i18n`, Meme Generator block from the Block Developer Cookbook (`npx @wordpress/create-block@latest meme-generator --template @block-developer-cookbook/meme-generator`)

**Legend:** `[SCREEN]` = on screen · `[OST]` = on-screen text · **VO** = spoken

---

## 🎥 SCRIPT

### COLD OPEN (the hook — do NOT slow-roll)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So I built a meme generator block. You pick an image, you add your setup and your punchline, it's great. And then I picked the wrong image, and there was no way to change it. The only way out was to delete the whole block and start over, which is a pretty bad experience for something I built on purpose."

`[SCREEN: editor — Meme Generator block selected, toolbar visible, no custom button. Ryan hovers the toolbar looking for something that isn't there.]`
**VO:** "What I want is a button right up here in the block toolbar that says 'get rid of this image.' And that's about ten lines of code."

`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "I'm Ryan Welcher, a developer advocate at Automattic. And I want to show you how to add your own button to the block toolbar with `BlockControls`, and what's actually going on under the hood when you do."
`[OST: "BlockControls → your own toolbar button"]`
> 🎯 Problem first, on face. The quick cut to the empty toolbar makes the missing button visible before he names the fix. Back to camera for the self-intro so it bookends the hook.

### WHERE WE'RE STARTING (the block as it is)
`[SCREEN: VS Code — src/edit.js, scrolled to the `if ( ! image )` placeholder branch, then the main return]`
**VO:** "Okay, so here's the block. If there's no image, we return a `Placeholder` with an image picker in it. Once you pick one, it gets saved to the `image` attribute and we render the meme with the two `RichText` fields on top."

`[SCREEN: highlight `if ( ! image )`]`
**VO:** "And that `if` is the important bit. If `image` goes back to being empty, the block drops right back into the picker. So the button doesn't need to do anything clever. It just has to clear that attribute."
> 🎯 Keep this short. The viewer only needs to see that clearing `image` puts the placeholder back.

### WHAT BLOCKCONTROLS ACTUALLY IS (the mechanism)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So before we write it, let's talk about what `BlockControls` is, because it's kind of a weird component the first time you see it. It's a Slot/Fill. The block toolbar has a slot in it, which is basically an empty spot waiting for content. `BlockControls` is the fill. Whatever you put inside it doesn't render where you wrote it in your JSX. It gets teleported up into the toolbar."

`[SCREEN: simple diagram overlay — `<BlockControls>` in edit.js with an arrow up to the block toolbar]`
**VO:** "It's kind of like forwarding your mail. You write the address in your component, and the editor delivers it to the toolbar. And because it's tied to your block's edit context, it only shows up when your block is the one that's selected."
`[OST: "Slot = the toolbar · Fill = <BlockControls>"]`
> ✅ `BlockControls` is a Fill that renders into the block toolbar slot for the selected block — https://developer.wordpress.org/block-editor/reference-guides/components/block-controls/ (also https://developer.wordpress.org/block-editor/reference-guides/slotfills/)
> ⚠️ CONFIRM: "only shows when your block is selected" matches current Gutenberg behavior for the recorded WP version.
> 🎯 This is the developer-grade moment. The mail analogy frames it, and the "only when selected" detail is the real mechanism. Don't cut it for time.

### ADDING THE BUTTON (type-and-narrate)
`[SCREEN: VS Code — imports at top of src/edit.js]`
**VO:** "All right, so imports first. `BlockControls` comes from `@wordpress/block-editor`, and `ToolbarGroup` and `ToolbarButton` come from `@wordpress/components`."

```js
import {
	useBlockProps,
	RichText,
	BlockControls,
} from '@wordpress/block-editor';
import {
	Placeholder,
	ToolbarGroup,
	ToolbarButton,
} from '@wordpress/components';
```

`[SCREEN: scroll to the main return — add `<BlockControls>` after the closing `</section>`, inside the fragment]`
**VO:** "Now down in the return, right after the section, we drop in `BlockControls`. And notice I'm putting it inside the fragment next to the block markup, not inside the section. It doesn't matter where it lives in the tree, because it's not rendering here anyway. That's the Slot/Fill thing again."

`[SCREEN: type `<ToolbarGroup>` then `<ToolbarButton />` with props, one at a time]`
**VO:** "Inside that we add a `ToolbarGroup`, which gives our button its own little section of the toolbar with a divider. And then the `ToolbarButton` itself. We give it an `icon`, and I'm just using the `remove` dashicon. Then a `label`, which is what shows up in the tooltip and what screen readers announce, so don't skip it. And then `onClick`, where we call `setAttributes` and set `image` to `false`."

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
> ✅ `ToolbarButton` props (`icon`, `label`, `onClick`) — https://developer.wordpress.org/block-editor/reference-guides/components/toolbar-button/
> 🎯 Type it live. Code matches Step 7 of the Block Developer Cookbook Meme Generator recipe.

### LET'S SEE WHAT THIS DOES (the payoff)
`[SCREEN: editor — refresh, select the meme block, new remove icon visible in toolbar. Hover to show the "Remove Meme Image" tooltip.]`
**VO:** "Okay, save, refresh, and let's see what this does. Select the block, and there's our button. Hover it and you get the label."

`[SCREEN: click the button — block snaps back to the Placeholder image picker. Pick a different image.]`
**VO:** "Click it, and we're right back in the picker. Pick a new image, and the text we already typed is still there, because we only cleared the one attribute. So nobody has to delete the block anymore, which is the thing I should have built in the first place."
> 🎯 End the demo on the text surviving the image swap. That's the strongest moment in the video.

### ONE THING I'D CHANGE (gotcha, to camera)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "There's one caveat here, and then I'll drop it. Our `image` attribute is typed as an object in block dot json, and we're setting it to `false`. It works, because that `if ( ! image )` check doesn't care. But `false` isn't an object, so when the post gets parsed again it fails validation and gets thrown out. If you want it tidier, set it to `undefined` instead and it's just gone. I wrote `false` and I'm leaving it in the demo, so you can go ahead and judge me for that."
> ⚠️ CONFIRM before recording: (1) `setAttributes( { image: false } )` on an `object`-typed attribute serializes `"image":false` into the block comment and is dropped on re-parse; (2) `setAttributes( { image: undefined } )` removes it from the serialized attributes. Test both in the editor (Code editor view) and cut this beat if either doesn't hold.
> 🎯 Self-deprecating closer on the gotcha. If the confirm fails, drop the beat entirely — it's not load-bearing.

### RECAP (to camera)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So that's kind of it. `BlockControls` is a fill for the block toolbar slot, you put a `ToolbarGroup` in it, and a `ToolbarButton` inside that. Wire `onClick` up to `setAttributes`, and your block can change its own state right from the toolbar. And once you've got that pattern, you can add pretty much any button you want up there."
`[OST bullets: BlockControls (fill) → ToolbarGroup → ToolbarButton → setAttributes]`

### CTA + END SCREEN
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "Let me know in the comments what button you added to your block's toolbar, and if you ran into anything weird along the way. If this helped, give it a thumbs up and hit subscribe, because there's more block stuff coming. Thanks for watching and I'll see you in the next one."
`[SCREEN: end screen — subscribe + ‹TODO: end-screen target (no content plan entry; use "best for viewer" or a playlist)›]`
`[OST: pinned-comment reminder]`

---

## 📦 PACKAGING

**Title (‹TODO: viDIQ-scored — use winner, A/B with #2›):**
- ✅ **Add a Custom Toolbar Button to Your WordPress Block (BlockControls)** — *‹TODO: viDIQ score + why›*
- How to Use BlockControls in a Custom WordPress Block — *‹TODO: score›*
- Your Block Needs a Toolbar Button (Here's How) — *‹TODO: score›*
- WordPress Block Toolbar Buttons in 5 Minutes — *‹TODO: score›*

**Thumbnail concept:** Split frame. Left: the block toolbar zoomed in with the new remove icon circled. Right: Ryan pointing at it, mildly smug. 3 bold words: "ADD YOUR BUTTON". ‹TODO: template ref›
**viDIQ reference images:** ‹TODO: Ryan's scored image URLs›
**Pinned comment:** "The whole button is `<BlockControls><ToolbarGroup><ToolbarButton icon label onClick /></ToolbarGroup></BlockControls>`. What button are you adding to your block's toolbar?"

---

## 📝 YOUTUBE DESCRIPTION (paste-ready)

> Learn how to add a custom toolbar button to your WordPress block with BlockControls. We add a "remove image" button to a meme generator block using ToolbarGroup and ToolbarButton, and look at how BlockControls works as a Slot/Fill for the block toolbar.

**Chapters:** ‹TODO: time these off the FINAL edit — labels track the SCRIPT beats in order. First chapter must stay 0:00 (YouTube requires it); you need 3+ chapters, each 10s or longer.›
```
0:00 Cold open
‹M:SS› Where we're starting
‹M:SS› What BlockControls actually is
‹M:SS› Adding the button
‹M:SS› Let's see what this does
‹M:SS› One thing I'd change
‹M:SS› Recap
```

**Resources:**
- BlockControls: https://developer.wordpress.org/block-editor/reference-guides/components/block-controls/
- ToolbarButton: https://developer.wordpress.org/block-editor/reference-guides/components/toolbar-button/
- SlotFills reference: https://developer.wordpress.org/block-editor/reference-guides/slotfills/
- Block Developer Cookbook: https://github.com/ryanwelcher/block-developer-cookbook

**My Stuff:** (standing footer — reuse as-is)
👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/
👉 WordPress Snippets VSCode extension: https://marketplace.visualstudio.com/items?itemName=ryanwelcher.modern-wordpress-development-snippets
👉 WordPress Playground markdown editor: https://marketplace.visualstudio.com/items?itemName=ryanwelcher.playground-readme-editor

**Connect:** (standing footer — reuse as-is)
https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

#WordPress #Gutenberg #BlockDevelopment #WordPressDeveloper #React

---

## ✅ Pre-record checklist
- [ ] CONFIRM `BlockControls` only renders for the selected block on the recorded WP version
- [ ] CONFIRM the `image: false` vs `image: undefined` serialization behavior (Code editor view) — cut the gotcha beat if it doesn't hold
- [ ] CONFIRM the reference URLs above resolve (SlotFills + component docs)
- [ ] Meme Generator block scaffolded, `npm run start` running, edit.js at the pre-Step-7 state (no BlockControls, imports trimmed)
- [ ] A meme block already inserted with an image and both text fields filled in, so the text-survives-the-swap payoff reads
- [ ] Diagram overlay for the Slot/Fill beat
- [ ] Clean cold-open take on talking head
- [ ] Thumbnail from template
- [ ] ‹TODO: schedule note›

## 🔀 Alt hooks (A/B in your head)
1. "This block has a bug, and the bug is me. I built a meme generator where you can pick an image and then never, ever change it. So let's fix that with a toolbar button."
2. "See this toolbar on top of your block? You can put your own buttons in there. It's one component, and it's kind of a weird one, so let's look at how it works."
