# 🎬 W‹TODO: n› — Add a Toolbar Button to Your Custom Block with BlockControls (for Block Developers)

Part of ‹TODO: [[Block …]]› · rules: ‹TODO: [[Operating Rules]]›

| | |
|---|---|
| **Publish** | ‹TODO: date + record/schedule note› |
| **Type / Tier** | ‹TODO: NATIVE/… · Tier …› |
| **Length** | ~4–5 min edited |
| **Target keyword** | *‹TODO: e.g. "wordpress BlockControls" / "add button to block toolbar"›* (‹TODO: vol/mo · comp›) |
| **Scope** | IN: `BlockControls` as a Slot/Fill, `ToolbarButton`, the `group` prop, wiring an `onClick` to `setAttributes`, showing the button only when it applies. DEFERRED: `ToolbarDropdownMenu`, `MediaReplaceFlow`, block-level toolbar controls for multi-select. |
| **Audience** | WordPress block developers who already have a custom block and want editor UI in the toolbar |
| **Voice** | warm, dev-to-dev, "Hey friends" — tighter than a stream |

**Stack (the real thing):** a custom "meme generator" block (image + top text + bottom text) built with `@wordpress/scripts` · `@wordpress/block-editor` (`BlockControls`, `useBlockProps`) · `@wordpress/components` (`ToolbarButton`) · `@wordpress/icons` (`trash`) · ‹TODO: repo link for the meme block›

**Legend:** `[SCREEN]` = on screen · `[OST]` = on-screen text · **VO** = spoken

---

## 🎥 SCRIPT

### COLD OPEN (the hook — do NOT slow-roll)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So I built a meme generator block. You pick an image, you type some top text and some bottom text, and boom, you've got a meme. Great. Now try to get rid of the image. You can't. There's no button for it, so you delete the block and start over, which is a pretty embarrassing thing to find in a block I wrote myself."
`[SCREEN: screen-capture — select the meme block, hover around the toolbar looking for a remove option, open the three-dot menu, close it, delete the block]`
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "I'm Ryan Welcher, a developer advocate at Automattic. And I want to show you how to put your own button right in the block toolbar with BlockControls, so you never have to ship a block like this one."
`[OST: "BlockControls → your own toolbar button"]`
> 🎯 The broken UX is the hook — show the dead end on screen before explaining anything. Keep the screen-capture insert short; the three-dot menu open/close is the visual punchline.

### THE BLOCK AS-IS (what the toolbar gives you for free)
`[SCREEN: editor — meme block with an image selected, zoom on the block toolbar]`
**VO:** "Okay, so here's the block. Image, top text, bottom text. When I select it, we get the block toolbar up here, and it's got the stuff WordPress gives every block. The block switcher, the drag handle, the up and down movers, and then the three-dot menu, which is kind of where features go to hide. What I want is a little trash can right in this toolbar that clears out the image and puts the placeholder back."
`[OST: "Goal: a 'Remove image' button in the toolbar"]`
> 🎯 Keep this beat brief — it's orientation, not teaching. Pointer-highlight each toolbar item as it's named.

### WHAT BLOCKCONTROLS ACTUALLY IS (Slot/Fill, under the hood)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So what is BlockControls? If you've used InspectorControls to put settings in the sidebar, you already know this one. It's a Slot/Fill. The toolbar has a slot sitting in it, and anything you wrap in BlockControls inside your block's edit component gets rendered into that slot."
`[SCREEN: simple diagram — block Edit component → <BlockControls> (Fill) → arrow → block toolbar (Slot)]`
**VO:** "It's kind of like the mail slot in your front door. You don't walk into the house to drop off a letter, you just push it through the slot and it shows up on the other side. Your edit component lives in the block canvas, but the button ends up in the toolbar, which is a totally different part of the React tree. And BlockControls only renders its fill when your block is selected, so you don't have to wrap anything in an isSelected check yourself."
`[OST: "BlockControls = Fill · block toolbar = Slot"]`
> ✅ `BlockControls` and `InspectorControls` are both Slot/Fill-based components exported from `@wordpress/block-editor`. Source: https://github.com/WordPress/gutenberg/tree/trunk/packages/block-editor/src/components/block-controls
> ⚠️ CONFIRM: the fill is only displayed for the selected block (via the block edit context), so no manual `isSelected` guard is needed. Check `use-block-controls-fill.js` in the source above against the WP version you record on.
> 🎯 This is the developer-grade beat. The mail slot frames it; the "different part of the React tree" line is the real detail — don't cut it.

### ADD THE BUTTON (type-and-narrate)
`[SCREEN: VS Code — src/edit.js of the meme block]`
**VO:** "All right, let's go write it. Up top, I'm pulling BlockControls in from the block-editor package, ToolbarButton from components, and the trash icon from the icons package."
```js
import { BlockControls, useBlockProps } from '@wordpress/block-editor';
import { ToolbarButton } from '@wordpress/components';
import { __ } from '@wordpress/i18n';
import { trash } from '@wordpress/icons';
```
**VO:** "Then down in the return, I drop in BlockControls, and I'm giving it a group of 'other'. The group prop tells it which section of the toolbar to land in, and because the slot wraps each group in its own toolbar group for you, I can put a ToolbarButton straight inside. Icon is trash, and the label is 'Remove image'. That label isn't just for looks, by the way. It's the tooltip, and it's what a screen reader announces, since the button has no visible text."
```jsx
<BlockControls group="other">
	<ToolbarButton
		icon={ trash }
		label={ __( 'Remove image', 'meme-generator' ) }
		onClick={ removeImage }
	/>
</BlockControls>
```
`[SCREEN: editor — refresh, select block, trash icon now in the toolbar; hover to show tooltip]`
**VO:** "Let's see what this does. Refresh, select the block, and there it is. We've got a trash can. It doesn't do anything yet, because I haven't written removeImage, but it's in there."
> ⚠️ CONFIRM: `@wordpress/icons` is bundled, not a WP-provided global, so it must be in the block's `package.json` (`npm install @wordpress/icons`). Make sure it's installed before recording so the build doesn't fail on camera.
> ⚠️ CONFIRM: `group="other"` renders children inside a toolbar group without an explicit `<ToolbarGroup>` wrapper on your WP version. If not, wrap the button in `<ToolbarGroup>` and adjust the VO line.
> 🎯 If the build does fail on camera, keep it. A real reaction here fits the voice better than a clean take.

### WIRE UP REMOVE (setAttributes does the work)
`[SCREEN: VS Code — above the return in edit.js]`
**VO:** "So the way this block stores the image is two attributes, the image ID and the image URL. Removing the image is just setting both of those back to undefined."
```js
const removeImage = () =>
	setAttributes( { imageId: undefined, imageUrl: undefined } );
```
**VO:** "And under the hood, when an attribute is undefined, it just gets left out when the block serializes. It's not stored as an empty string or anything like that, it's gone. So the edit component sees no URL and renders the placeholder again, the same way it did when you first inserted the block."
`[SCREEN: editor — click the trash button, image disappears, MediaPlaceholder returns; hit undo, image comes back]`
**VO:** "Click it, and the image is gone, and we're back to the placeholder. And because this all goes through setAttributes, undo just works. Look at that. I didn't write anything for undo."
> ⚠️ CONFIRM: attribute names (`imageId`, `imageUrl`) match the meme block's `block.json`. If the URL attribute is sourced from markup (e.g. `source: "attribute"` on the `img` `src`) rather than the comment delimiter, adjust the serialization line to say the `img` just isn't rendered.
> 🎯 The undo moment is the payoff of this beat — give it a beat of silence on screen before the VO line.

### ONLY SHOW IT WHEN IT MAKES SENSE (conditional render)
`[SCREEN: editor — select a meme block with no image yet; the trash button is still there]`
**VO:** "Now there's one problem left. If I insert a fresh meme block with no image, the trash button is still sitting there, and clicking it removes nothing. That's a button that lies to you, and I've shipped a few of those."
`[SCREEN: VS Code — wrap BlockControls in a condition]`
**VO:** "The fix is small. I only render BlockControls when there's actually an image URL."
```jsx
{ imageUrl && (
	<BlockControls group="other">
		<ToolbarButton
			icon={ trash }
			label={ __( 'Remove image', 'meme-generator' ) }
			onClick={ removeImage }
		/>
	</BlockControls>
) }
```
`[SCREEN: editor — empty block: no trash button · pick an image: trash button appears · remove: it disappears again]`
**VO:** "Empty block, no button. Pick an image, and the button shows up. Remove it, and the button goes away with it. Cool."
> 🎯 Strongest demo moment is the button appearing and disappearing — end the screen-capture here and cut straight to face.

### RECAP (to camera)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So that's it. BlockControls is a fill for the block toolbar, you put a ToolbarButton inside it, and the onClick is just a regular setAttributes call, so undo comes along for free. And if the button only makes sense sometimes, only render it sometimes. That's really all there is to it, and my meme block is a little less embarrassing now."
`[OST bullets: BlockControls = toolbar Fill · ToolbarButton + label · onClick → setAttributes · render it only when it applies]`

### CTA + END SCREEN
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "Let me know in the comments what button you'd add to your own block's toolbar. And if you haven't already, hit subscribe, because there's more block stuff coming. Thanks for watching and I'll see you in the next one."
`[SCREEN: end screen — subscribe + ‹TODO: next-video / playlist target from content plan›]`
`[OST: pinned-comment reminder]`

---

## 📦 PACKAGING

**Title (‹TODO: viDIQ-scored — use winner, A/B with #2›):**
- ✅ **Add a Custom Toolbar Button to Your WordPress Block (BlockControls)** — *‹TODO: viDIQ score + why›*
- How to Use BlockControls in a Custom Block — *‹TODO: score›*
- My Block Had No Remove Button, So I Added One — *‹TODO: score›*
- WordPress Block Toolbar Buttons in 5 Minutes — *‹TODO: score›*

**Thumbnail concept:** split frame — left, Ryan looking puzzled at a block toolbar with a big red circle around the three-dot menu; right, the same toolbar zoomed with a highlighted trash icon. 3–4 bold words: "ADD YOUR OWN BUTTON". ‹TODO: template ref›
**viDIQ reference images:** ‹TODO: Ryan's scored image URLs›
**Pinned comment:** "The whole thing is `<BlockControls group="other">` + a `ToolbarButton` whose `onClick` calls `setAttributes`. What button would you add to your own block's toolbar?"

---

## 📝 YOUTUBE DESCRIPTION (paste-ready)

> Want your own button in the WordPress block toolbar? In this quick tip I add a "Remove image" button to a custom meme generator block using BlockControls and ToolbarButton, look at how BlockControls works as a Slot/Fill, and only show the button when there's actually an image to remove.

**Chapters:** ‹TODO: time these off the FINAL edit — labels track the SCRIPT beats in order. First chapter must stay 0:00 (YouTube requires it); you need 3+ chapters, each 10s or longer.›
```
0:00 Cold open
‹M:SS› The block as-is
‹M:SS› What BlockControls actually is
‹M:SS› Add the button
‹M:SS› Wire up remove
‹M:SS› Only show it when it makes sense
‹M:SS› Recap
```

**Resources:**
- BlockControls source (block-editor package): https://github.com/WordPress/gutenberg/tree/trunk/packages/block-editor/src/components/block-controls
- Block toolbar and settings sidebar (Block Editor Handbook): ‹TODO: confirm URL — https://developer.wordpress.org/block-editor/getting-started/fundamentals/block-in-the-editor/›
- ToolbarButton component reference: ‹TODO: confirm URL — https://developer.wordpress.org/block-editor/reference-guides/components/toolbar-button/›
- WordPress icons library: ‹TODO: confirm URL — https://wordpress.github.io/gutenberg/?path=/story/icons-icon--library›
- Meme generator block code: ‹TODO: repo link›

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
- [ ] CONFIRM `BlockControls` fill only shows for the selected block (no `isSelected` guard needed) on the recording WP version
- [ ] CONFIRM `group="other"` renders a `ToolbarButton` without an explicit `ToolbarGroup`
- [ ] CONFIRM attribute names + how the image URL is sourced in the meme block's `block.json`; adjust the serialization VO if needed
- [ ] `@wordpress/icons` installed in the block's `package.json`; `npm start` running
- [ ] Two meme blocks ready in the editor: one with an image, one fresh/empty
- [ ] Start state for demo: `edit.js` with no `BlockControls` yet
- [ ] Mail-slot diagram graphic for the Slot/Fill beat
- [ ] Resource URLs checked
- [ ] Clean cold-open take (talking head)
- [ ] Thumbnail from template
- [ ] ‹TODO: schedule note›

## 🔀 Alt hooks (A/B in your head)
1. "The three-dot menu in the block toolbar is kind of where features go to hide. So if your block has one thing people do all the time, it shouldn't live in there. It should be a button, right in the toolbar."
2. "I made a meme generator block, and the only way to change your mind about the image was to delete the block. That's on me. So let's fix it, and it turns out the fix is pretty small."
