# 🎬 W‹TODO: n› — Add a Toolbar Button to Your Custom Block with BlockControls (for Developers)

Part of ‹TODO: [[Block …]]› · rules: ‹TODO: [[Operating Rules]]›

| | |
|---|---|
| **Publish** | ‹TODO: date + record/schedule note› |
| **Type / Tier** | ‹TODO: NATIVE/… · Tier …› · quick tip |
| **Length** | ~4–5 min edited |
| **Target keyword** | *BlockControls* (‹TODO: vol/mo · comp›) |
| **Scope** | IN: `BlockControls` as a Slot/Fill, `ToolbarGroup` + `ToolbarButton`, wiring `onClick` to `setAttributes`, conditional rendering so the button only exists when it's useful. OUT: `group` prop placement, dropdowns/`ToolbarDropdownMenu`, `MediaReplaceFlow`, `InspectorControls` |
| **Audience** | WordPress block developers who already have a custom block and want editor UI in the block toolbar |
| **Voice** | warm, dev-to-dev — tighter than a stream |

**Stack (the real thing):** Meme Generator block from the Block Developer Cookbook (`block-developers-cookbook/meme-generator`, Step 7) · `@wordpress/block-editor` (`BlockControls`) · `@wordpress/components` (`ToolbarGroup`, `ToolbarButton`) · Imgflip API for the meme images · repo: https://github.com/ryanwelcher/block-developer-cookbook

**Legend:** `[SCREEN]` = on screen · `[OST]` = on-screen text · **VO** = spoken

---

## 🎥 SCRIPT

### COLD OPEN (the hook — stuck with a bad meme)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So you pick an image in your block, and you immediately regret it. And there's no way to get rid of it. You can delete the whole block and start over, or you can open the code editor and hand-edit the block comment like an animal. I've done both. I'm not proud of it."

`[SCREEN: editor — Meme Generator block selected, cursor circles the empty space in the block toolbar]`
**VO:** "So we're going to put a button right up here in the block toolbar that fixes it."

`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "I'm Ryan Welcher, a developer advocate at Automattic. And I want to show you how to add your own buttons to the block toolbar with BlockControls, because it's a lot less code than you'd think."
`[OST: "BlockControls → your own toolbar buttons"]`
> 🎯 Hook is the pain (stuck with an image), not the API name. Keep the face → screen → face bookend tight; the screen flash is just one cursor move to show *where* the button goes.

### THE PROBLEM (why the block needs this)
`[SCREEN: editor — insert Meme Generator block, placeholder grid of Imgflip memes, pick one, type top + bottom text]`
**VO:** "Okay, so this is the meme generator block from the Block Developer Cookbook. When there's no image, we show a placeholder with a bunch of memes from the Imgflip API. I pick one, it drops in, I add my setup, my punchline… and yeah, that's not funny. I want a different one."

`[SCREEN: click around the selected block — toolbar has only the core controls]`
**VO:** "And there's nothing here. The placeholder only shows up when the image attribute is empty, and right now nothing in the UI ever empties it. So once you pick, you're stuck with it."
> 🎯 Let the bad meme land as the joke. Pick something genuinely mediocre on camera.

### HOW BLOCKCONTROLS WORKS (the mechanism)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So the thing we want is BlockControls. And the easiest way to think about it is kind of like a mail slot. Your block's sitting over here in the canvas, the toolbar's sitting up there, and BlockControls lets you drop stuff through the slot so it shows up in the toolbar."

`[SCREEN: simple diagram — Edit component JSX on the left with <BlockControls> highlighted, arrow to the block toolbar on the right]`
`[OST: "BlockControls = Fill · block toolbar = Slot"]`
**VO:** "Under the hood, it's a Slot/Fill. The block toolbar renders a slot, and BlockControls is the fill. So in your JSX it sits right next to your block markup, but whatever you put inside it gets rendered up in the toolbar. And the editor only renders those controls for the block that's selected, so you don't have to check isSelected yourself."
> ✅ `BlockControls` is a Fill rendered into the block toolbar's Slot — https://github.com/WordPress/gutenberg/tree/trunk/packages/block-editor/src/components/block-controls
> ⚠️ CONFIRM: controls only render for the selected block without an `isSelected` check (gated inside `useBlockControlsFill`). Verify on the current Gutenberg trunk before saying it on camera.
> 🎯 Analogy frames it, then the Slot/Fill line gives the real detail. Keep the diagram on screen through the whole second VO paragraph.

### WRITING THE BUTTON (type-and-narrate)
`[SCREEN: VS Code — edit.js, imports at top]`
**VO:** "All right, so in edit.js. BlockControls comes from block-editor, and ToolbarGroup and ToolbarButton come from components. Two different packages, which gets me every single time."
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

`[SCREEN: VS Code — scroll to the return that renders the image; type the BlockControls block after </section>]`
**VO:** "Now down in the return, right after the section, we add BlockControls. Inside that goes a ToolbarGroup, which gives us that little divider so our button isn't jammed up against the core ones. And then the ToolbarButton."
```jsx
<>
	<section { ...blockProps }>
		{ /* meme wrapper, RichText, img… */ }
	</section>
	<BlockControls>
		<ToolbarGroup>
			<ToolbarButton
				icon="remove"
				label={ __( 'Remove Meme Image', 'meme-generator' ) }
				onClick={ () => setAttributes( { image: false } ) }
			/>
		</ToolbarGroup>
	</BlockControls>
</>
```

`[SCREEN: highlight the label prop]`
**VO:** "Give it an icon and give it a label. Don't skip the label. It's the tooltip, and it's what a screen reader announces, because an icon button with no label is just a mystery square."

`[SCREEN: highlight the onClick, then scroll up to the `if ( ! image )` placeholder check]`
**VO:** "And the onClick is one line. We set image to false. The edit function already checks if there's no image to decide whether to show the placeholder, so the second that attribute goes falsy, the block re-renders and we're back at the picker."

`[SCREEN: collapse to show the two return branches side by side — placeholder branch vs. image branch]`
**VO:** "And notice where this lives. It's only in the branch that renders the image. So when there's no image, there's no button, which makes sense, right? There's nothing to remove."
> ✅ Code matches Cookbook Step 7 (`fixtures/meme-generator-full.md`) — `icon="remove"`, label `Remove Meme Image`, `setAttributes( { image: false } )`.
> 🎯 This is the longest beat. If the edit runs long, the imports line is the one to trim — the JSX and the conditional-branch point are the lesson.

### DOES IT WORK? (demo)
`[SCREEN: editor — refresh, select the meme block, hover the new toolbar button to show tooltip]`
**VO:** "Let's see what this does. Refresh, click the block, and there's our button. Hover over it and there's the label."

`[SCREEN: click the button — image disappears, placeholder grid returns; pick a new meme]`
**VO:** "Click it, and the image is gone and the placeholder's back. So now I can pick a better one. Much better. Arguably."

`[SCREEN: new image shows with the original top/bottom text still in place]`
**VO:** "And the text stuck around, because we only cleared the image attribute. Which is actually what I want here, since it's the picture that was bad, not my joke. Okay, maybe also my joke."
> ⚠️ CONFIRM: top/bottom text persists after removing and re-picking (attributes untouched, RichText just isn't rendered in the placeholder branch). Check on record.

### THE CAVEAT (false vs. undefined)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "There's one caveat here, and then I'll let you go. The image attribute is typed as an object in block.json, and we're setting it to false. It works, because the check is just 'is this falsy.' But if you want to keep your types honest, set it to undefined instead, and the attribute just gets left out when the block saves."
```js
onClick={ () => setAttributes( { image: undefined } ) }
```
> ⚠️ CONFIRM: attributes set to `undefined` are omitted from the serialized block comment delimiter, and `false` on an `object`-typed attribute doesn't throw a validation notice. Test both in the editor + code editor view.
> 🎯 Optional cut. If the video's already at time, drop this beat and move the `undefined` tip into the pinned comment.

### RECAP + CTA
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So that's the whole trick. Wrap your button in BlockControls, put it in a ToolbarGroup, give it a label, and have the onClick update your attributes. The editor handles getting it into the toolbar for you."

**VO:** "Let me know in the comments what button you're adding to your own block toolbar. And if you haven't already, hit subscribe, because there's more block development stuff coming. Thanks for watching and I'll see you in the next one."
`[SCREEN: end screen — subscribe + ‹TODO: end-screen target (no content plan entry; use a generic/latest-upload element)›]`
`[OST: pinned-comment reminder]`

---

## 📦 PACKAGING

**Title (‹TODO: viDIQ-scored — use winner, A/B with #2›):**
- ✅ **Add a Toolbar Button to Your Custom Block (BlockControls)** — *‹TODO: viDIQ score + why›*
- BlockControls in 5 Minutes: Custom Block Toolbar Buttons — *‹TODO: score›*
- How to Add Block Toolbar Controls in WordPress — *‹TODO: score›*
- Your Block Needs a Remove Button — *‹TODO: score›*

**Thumbnail concept:** Split frame — left: Ryan's face, mildly disgusted; right: zoomed block toolbar with the new remove button circled, a bad meme behind it. 3–4 bold words: "ADD TOOLBAR BUTTONS". ‹TODO: template ref›
**viDIQ reference images:** ‹TODO: Ryan's scored image URLs›
**Pinned comment:** `<BlockControls><ToolbarGroup><ToolbarButton … /></ToolbarGroup></BlockControls>` — full code is in the Block Developer Cookbook (link in description). Tip: `setAttributes( { image: undefined } )` keeps the attribute type clean. What button are you adding to your block toolbar?

---

## 📝 YOUTUBE DESCRIPTION (paste-ready)

> Want your custom WordPress block to have its own button in the block toolbar? BlockControls makes it a few lines of code. In this quick tip, I add a "remove image" button to a meme generator block using BlockControls, ToolbarGroup, and ToolbarButton, and explain how the Slot/Fill behind it gets your button into the toolbar.

**Chapters:** ‹TODO: time these off the FINAL edit — labels track the SCRIPT beats in order. First chapter must stay 0:00 (YouTube requires it); you need 3+ chapters, each 10s or longer.›
```
0:00 Stuck with a bad meme
‹M:SS› The problem
‹M:SS› How BlockControls works
‹M:SS› Writing the button
‹M:SS› Does it work?
‹M:SS› The caveat: false vs. undefined
‹M:SS› Recap
```

**Resources:**
- Block Developer Cookbook (Meme Generator recipe): https://github.com/ryanwelcher/block-developer-cookbook
- BlockControls source + README: https://github.com/WordPress/gutenberg/tree/trunk/packages/block-editor/src/components/block-controls
- ToolbarButton reference: https://developer.wordpress.org/block-editor/reference-guides/components/toolbar-button/ ‹TODO: confirm URL›
- Imgflip API: https://imgflip.com/api

**My Stuff:** (standing footer — reuse as-is)
👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/
👉 WordPress Snippets VSCode extension: https://marketplace.visualstudio.com/items?itemName=ryanwelcher.modern-wordpress-development-snippets
👉 WordPress Playground markdown editor: https://marketplace.visualstudio.com/items?itemName=ryanwelcher.playground-readme-editor

**Connect:** (standing footer — reuse as-is)
https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

#WordPress #Gutenberg #BlockDevelopment #BlockEditor #WordPressDeveloper

---

## ✅ Pre-record checklist
- [ ] CONFIRM: BlockControls only renders for the selected block with no `isSelected` check
- [ ] CONFIRM: `image: undefined` is omitted from the block comment; `false` on an object attribute raises no notice
- [ ] CONFIRM: top/bottom text survives remove → re-pick
- [ ] CONFIRM: ToolbarButton docs URL resolves
- [ ] Meme Generator block at the pre-Step-7 state (no toolbar button) in a clean local site, `npm run start` running
- [ ] A deliberately bad first meme picked and ready, a better one lined up
- [ ] Slot/Fill diagram graphic made
- [ ] Clean cold-open take
- [ ] Thumbnail from template
- [ ] ‹TODO: schedule note›

## 🔀 Alt hooks (A/B in your head)
1. "Your block has a toolbar. It's right there. And you're not putting anything in it? Come on. Let's fix that."
2. "Every block I've built that has an image, I've forgotten to add a way to remove the image. Every single one. So let's add the button I keep forgetting."
