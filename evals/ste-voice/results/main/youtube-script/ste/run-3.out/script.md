# 🎬 W‹TODO: n› — Add a Toolbar Button to Your Custom Block with BlockControls (for Developers)

Part of ‹TODO: [[Block …]]› · rules: ‹TODO: [[Operating Rules]]›

| | |
|---|---|
| **Publish** | ‹TODO: date + record/schedule note› |
| **Type / Tier** | ‹TODO: NATIVE/… · Tier …› |
| **Length** | ~4–5 min edited (quick tip) |
| **Target keyword** | *BlockControls toolbar button* (‹TODO: vol/mo · comp›) |
| **Scope** | IN: `BlockControls` + `ToolbarGroup` + `ToolbarButton`, conditional rendering, clearing attributes, the Slot/Fill mechanism, the `group` prop. DEFERRED: dropdown menus (`ToolbarDropdownMenu`), `MediaReplaceFlow`, `InspectorControls` |
| **Audience** | WordPress block developers who already have a custom block and want to add editor UI to it |
| **Voice** | warm, dev-to-dev — tighter than a stream |

**Stack (the real thing):**
- `@wordpress/block-editor` → `BlockControls`, `useBlockProps`
- `@wordpress/components` → `ToolbarGroup`, `ToolbarButton`
- `@wordpress/icons` → `trash`
- `@wordpress/i18n` → `__`
- Demo block: meme generator block (image + top text + bottom text), built with `@wordpress/scripts`

**Legend:** `[SCREEN]` = on screen · `[OST]` = on-screen text · **VO** = spoken

---

## 🎥 SCRIPT

### COLD OPEN (the hook — do NOT slow-roll)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So I built a meme generator block. You pick an image, you add your top text and your bottom text, and you've got a meme. Very important work. But I picked the wrong image, and there was no way to get rid of it without deleting the entire block and starting over."

`[SCREEN: screen-capture — meme block selected in the editor, block toolbar visible, no remove option. Ryan hovers around the toolbar looking for it.]`
**VO:** "Which is kind of a terrible experience, right? And it's my block, so I only have myself to blame."

`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "I'm Ryan Welcher, a developer advocate at Automattic. And I want to show you how to put your own button right up here in the block toolbar, using a component called `BlockControls`. It's a lot less code than you'd think."
`[OST: "Custom toolbar buttons with BlockControls"]`
> 🎯 Relatable self-inflicted problem first, then the payoff promise. The screen-capture cutaway shows the missing button so "up here" lands when he's back on camera — gesture up-left toward where the toolbar would be.

### THE BROKEN BLOCK (show the problem)
`[SCREEN: screen-capture — editor. Insert meme block, select an image, type top/bottom text. Click through the toolbar: block switcher, drag handle, move arrows, alignment, options menu.]`
**VO:** "Okay, so here's the block. I've got an image in here, I've got my text, and if I click on the block, I get the toolbar. There's the block switcher, the movers, the three-dot menu. All the stuff WordPress gives you for free. What there isn't is anything that says 'take this image out.'"
`[SCREEN: code — src/edit.js, current Edit component]`
**VO:** "And in the code, the image is just two attributes, an `imageId` and an `imageUrl`. So really all this button has to do is clear those two out. That's it."
> 🎯 Keep this beat short. Its only job is to show the toolbar and the two attributes so the fix makes sense.

### WHAT BLOCKCONTROLS ACTUALLY IS (the mechanism)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So before we write anything, let's talk about what `BlockControls` is doing under the hood, because it's kind of clever. It's a Slot/Fill. If you've used `InspectorControls` for the sidebar, it's the exact same idea."

`[SCREEN: simple diagram — block toolbar with a dashed "slot" region; an arrow from `<BlockControls>` inside `edit.js` pointing up into it]`
**VO:** "The idea here is that the block toolbar has a slot in it, like an empty spot that's waiting for stuff. And `BlockControls` is the fill. So you write it right inside your block's `Edit` component, next to all your other markup, but it doesn't render there. React picks it up and puts it into the toolbar instead. It's kind of like leaving a package at the front desk. You drop it off in one place, and it shows up somewhere else."

**VO:** "And because it's tied to your block, it only shows up when your block is the one that's selected. You don't have to manage any of that yourself."
`[OST: "BlockControls = Fill · Block toolbar = Slot"]`
> ✅ `BlockControls` renders its children into the block toolbar via Slot/Fill, and only for the selected block — https://developer.wordpress.org/block-editor/getting-started/fundamentals/block-in-the-editor/ and https://developer.wordpress.org/block-editor/reference-guides/components/toolbar/
> ⚠️ CONFIRM: the "only when selected" behavior is still handled by the block edit context (`isSelected` gate inside `BlockControls`) in the Gutenberg version you record on.
> 🎯 Analogy frames it, then the real detail follows. Don't let the diagram linger.

### ADD THE BUTTON (type-it-and-narrate)
`[SCREEN: code — src/edit.js, typing live]`
**VO:** "All right, let's build it. So up top, we need a few imports. `BlockControls` comes from the block editor package, `ToolbarGroup` and `ToolbarButton` come from components, and I'm grabbing the `trash` icon from the icons package, because I'm not a designer and I'm not going to pretend to be one."

```js
import { __ } from '@wordpress/i18n';
import { BlockControls, useBlockProps } from '@wordpress/block-editor';
import { ToolbarGroup, ToolbarButton } from '@wordpress/components';
import { trash } from '@wordpress/icons';
```

**VO:** "Now down in the return, I'm going to wrap everything in a fragment, and then drop in `BlockControls`. Inside that, a `ToolbarGroup`, and inside that, our `ToolbarButton`."

```jsx
export default function Edit( { attributes, setAttributes } ) {
	const { imageId, imageUrl, topText, bottomText } = attributes;

	return (
		<>
			{ imageUrl && (
				<BlockControls>
					<ToolbarGroup>
						<ToolbarButton
							icon={ trash }
							label={ __( 'Remove image', 'meme-generator' ) }
							onClick={ () =>
								setAttributes( {
									imageId: undefined,
									imageUrl: undefined,
								} )
							}
						/>
					</ToolbarGroup>
				</BlockControls>
			) }
			<div { ...useBlockProps() }>
				{ /* existing meme markup */ }
			</div>
		</>
	);
}
```

**VO:** "So the button gets an icon, and it gets a label. The label matters. That's the tooltip when you hover, and it's what a screen reader announces, since there's no visible text on this thing. Then `onClick` just calls `setAttributes` and sets both image attributes back to `undefined`."

**VO:** "And I've wrapped the whole thing in a check for `imageUrl`, because if there's no image, a 'remove image' button is pretty pointless. I've shipped buttons like that before. Let's not do that."
> ✅ `ToolbarButton` accepts `icon`, `label`, `onClick`; `label` is used for the tooltip/accessible name when there's no visible text — https://developer.wordpress.org/block-editor/reference-guides/components/toolbar-button/
> ⚠️ CONFIRM: setting an attribute to `undefined` via `setAttributes` falls back to its `block.json` default (or removes it) on the WP version being recorded. Match attribute names to the actual demo block.
> 🎯 Pre-type the imports in a snippet if the live typing drags. The `ToolbarButton` block is the part to type on camera.

### WHY NOT JUST A BUTTON? (the gotcha)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "Now, you might be wondering why I didn't just throw a regular `Button` in there. You can, and it'll show up. But the block toolbar is a proper ARIA toolbar, so you move through it with the arrow keys, not Tab. `ToolbarButton` hooks into that for you. A plain `Button` doesn't, and keyboard users end up tabbing into a toolbar that doesn't behave like the rest of it."
> ✅ `Toolbar` implements roving tabindex / arrow-key navigation; items should be `ToolbarButton` or `ToolbarItem` — https://developer.wordpress.org/block-editor/reference-guides/components/toolbar/
> 🎯 This is the developer-grade detail most tutorials skip. Keep it to camera, and keep it short.

### TRY IT OUT (the payoff)
`[SCREEN: screen-capture — editor refresh, select meme block. Trash icon now in the toolbar. Hover for tooltip, click it. Image clears, placeholder/MediaPlaceholder returns. Undo with Cmd+Z, image comes back.]`
**VO:** "Okay, let's see what this does. Refresh, click the block, and there's our trash can. Hover it, and we get 'Remove image.' Click it, and the image is gone. My top and bottom text are still there, which is what we want."

**VO:** "And because this is just `setAttributes`, undo works for free. Command-Z, and the image comes back."

`[SCREEN: screen-capture — deselect block, select a paragraph; toolbar has no trash button. Reselect meme block with no image: no trash button either.]`
**VO:** "And if I click off onto a paragraph, the button's not there. Pick an empty meme block, and it's not there either. Cool."
> ⚠️ CONFIRM: undo restores both attributes in one step during the dry run.
> 🎯 Strongest moment of the demo is the click-and-it's-gone. Let the undo beat breathe for a second.

### BONUS: THE GROUP PROP (where it lands)
`[SCREEN: code — change `<BlockControls>` to `<BlockControls group="other">`, remove the `ToolbarGroup` wrapper]`
**VO:** "One more thing before I let you go. `BlockControls` takes a `group` prop, and that lets you pick which section of the toolbar your button goes into. So if I set it to `other`, the button moves over next to the other secondary stuff. And when you use `group`, WordPress wraps it in a toolbar group for you, so you can drop the `ToolbarGroup`."

```jsx
<BlockControls group="other">
	<ToolbarButton
		icon={ trash }
		label={ __( 'Remove image', 'meme-generator' ) }
		onClick={ () =>
			setAttributes( { imageId: undefined, imageUrl: undefined } )
		}
	/>
</BlockControls>
```
`[SCREEN: screen-capture — editor, button now in the "other" section of the toolbar]`
> ⚠️ CONFIRM: current valid `group` values (`default`, `block`, `inline`, `other`, `parent`) and that `group` auto-wraps children in a `ToolbarGroup` — check `packages/block-editor/src/components/block-controls/` in Gutenberg trunk.
> 🎯 This beat is the first cut if the video runs long. The tip stands on its own without it.

### RECAP (wrap to camera)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So that's kind of it. `BlockControls` is a fill that drops your UI into the block toolbar, you put a `ToolbarButton` inside it so keyboard navigation keeps working, and the button itself just calls `setAttributes`. My meme block now lets you fix your mistakes, which is more than I can say for most of my code."
`[OST bullets: BlockControls → ToolbarGroup → ToolbarButton · label = tooltip + accessible name · render it conditionally]`

### CTA + END SCREEN
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "Let me know in the comments what button you're adding to your block toolbar, and if you ran into anything weird along the way. If this helped, give it a thumbs up and hit subscribe, because there's more block development stuff coming. Thanks for watching and I'll see you in the next one."
`[SCREEN: end screen — subscribe + ‹TODO: end-screen video target›]`
`[OST: pinned-comment reminder]`
> 🎯 No content plan entry. CTA stays generic on purpose. Don't tease a specific next video.

---

## 📦 PACKAGING

**Title (‹TODO: viDIQ-scored — use winner, A/B with #2›):**
- ✅ **Add a Custom Toolbar Button to Your WordPress Block (BlockControls)** — *‹TODO: viDIQ score + why›*
- How to Use BlockControls in a Custom WordPress Block — *‹TODO: score›*
- My Block Had No Remove Button, So I Added One — *‹TODO: score›*
- WordPress Block Toolbar Buttons in 5 Minutes — *‹TODO: score›*

**Thumbnail concept:** Split frame. Left: zoomed-in block toolbar with a big highlighted trash icon. Right: Ryan's face reacting to a silly meme image. 3–4 bold words: "ADD TOOLBAR BUTTONS". ‹TODO: template ref›
**viDIQ reference images:** ‹TODO: Ryan's scored image URLs›
**Pinned comment:** The code: `<BlockControls><ToolbarGroup><ToolbarButton icon={ trash } label="Remove image" onClick={ … } /></ToolbarGroup></BlockControls>`. What button are you adding to your block toolbar?

---

## 📝 YOUTUBE DESCRIPTION (paste-ready)

> Need a custom button in your WordPress block toolbar? In this quick tip, I use BlockControls, ToolbarGroup, and ToolbarButton to add a "remove image" button to a meme generator block. We also look at how BlockControls works as a Slot/Fill, why ToolbarButton matters for keyboard users, and how the group prop controls where your button lands.

**Chapters:** ‹TODO: time these off the FINAL edit — labels track the SCRIPT beats in order. First chapter must stay 0:00 (YouTube requires it); you need 3+ chapters, each 10s or longer.›
```
0:00 Cold open
‹M:SS› The broken block
‹M:SS› What BlockControls actually is
‹M:SS› Add the button
‹M:SS› Why not just a Button?
‹M:SS› Try it out
‹M:SS› Bonus: the group prop
‹M:SS› Recap
```

**Resources:**
- Block Editor Handbook — Toolbars and block controls: https://developer.wordpress.org/block-editor/getting-started/fundamentals/block-in-the-editor/
- ToolbarButton component: https://developer.wordpress.org/block-editor/reference-guides/components/toolbar-button/
- Toolbar component: https://developer.wordpress.org/block-editor/reference-guides/components/toolbar/
- ‹TODO: link to meme generator block repo/gist, if public›

**My Stuff:**
👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/
👉 WordPress Snippets VSCode extension: https://marketplace.visualstudio.com/items?itemName=ryanwelcher.modern-wordpress-development-snippets
👉 WordPress Playground markdown editor: https://marketplace.visualstudio.com/items?itemName=ryanwelcher.playground-readme-editor

**Connect:**
https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

#WordPress #Gutenberg #BlockEditor #WordPressDevelopment #React

---

## ✅ Pre-record checklist
- [ ] CONFIRM `BlockControls` `group` values and that `group` auto-wraps in a `ToolbarGroup`
- [ ] CONFIRM `setAttributes( { imageId: undefined, imageUrl: undefined } )` clears cleanly and undo restores both in one step
- [ ] CONFIRM Handbook/component URLs in Resources still resolve
- [ ] Match attribute names in the script to the real meme block (`imageId` / `imageUrl`)
- [ ] Meme block builds, has an image + text loaded, and `npm start` is running
- [ ] Slot/Fill diagram graphic ready for the mechanism beat
- [ ] Imports snippet ready in case live typing drags
- [ ] Clean cold-open take (talking head)
- [ ] Thumbnail from template
- [ ] ‹TODO: schedule note›

## 🔀 Alt hooks (A/B in your head)
1. "I picked the wrong image for my meme, and my own block wouldn't let me take it out. So let's fix that, and add a button right in the block toolbar."
2. "Every core block has little buttons up in the toolbar. Your custom block can have them too, and it's about fifteen lines of code."
