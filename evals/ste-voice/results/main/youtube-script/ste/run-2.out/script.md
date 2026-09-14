# 🎬 W‹TODO: n› — Add a Toolbar Button to Your Custom Block with BlockControls (for Developers)

Part of ‹TODO: [[Block …]]› · rules: ‹TODO: [[Operating Rules]]›

| | |
|---|---|
| **Publish** | ‹TODO: date + record/schedule note› |
| **Type / Tier** | ‹TODO: NATIVE/… · Tier …› · quick tip |
| **Length** | ~4–5 min edited |
| **Target keyword** | *BlockControls toolbar button* (‹TODO: vol/mo · comp›) |
| **Scope** | IN: `BlockControls` → `ToolbarGroup` → `ToolbarButton` in a custom block's `edit.js`, wired to `setAttributes`, plus how the Slot/Fill puts it in the toolbar. DEFERRED: dropdowns (`ToolbarDropdownMenu`), the `group` prop, `InspectorControls`, the rest of the meme generator build. |
| **Audience** | WordPress block developers who already have a custom block and want editor UI in the block toolbar |
| **Voice** | warm, dev-to-dev — tighter than a stream |

**Stack (the real thing):** `@wordpress/block-editor` (`BlockControls`, `useBlockProps`, `RichText`) · `@wordpress/components` (`ToolbarGroup`, `ToolbarButton`, `Placeholder`) · Meme Generator block from the Block Developer Cookbook (`npx @wordpress/create-block@latest meme-generator --template @block-developer-cookbook/meme-generator`) · image data from the Imgflip API

**Legend:** `[SCREEN]` = on screen · `[OST]` = on-screen text · **VO** = spoken

---

## 🎥 SCRIPT

### COLD OPEN (the hook — do NOT slow-roll)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So I built a meme generator block. You pick an image, you type your top text, your bottom text, and it's great. And then I picked the wrong image, and there was no way to change it. The only fix was to delete the whole block and start over, which is not a great experience. I built it, and even I was annoyed."

`[SCREEN: screen-capture — meme block selected in the editor, cursor hunting around the toolbar for a way to swap the image; nothing there]`
**VO:** "What I wanted was one little button, right up here in the toolbar, that gets rid of the image so I can pick another one."

`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "I'm Ryan Welcher, a developer advocate at Automattic. And I want to show you how to add that button to your own block with `BlockControls`. It's about ten lines of code."
`[OST: "Custom toolbar buttons with BlockControls"]`
> 🎯 Open on the pain (the broken UX of his own block), show the empty toolbar, then promise a small fix. The "ten lines" line sets up a short video, so keep the demo tight to match it.
> ⚠️ CONFIRM: count the final JSX. The `<BlockControls>` block plus the new imports should come to about ten lines. If it's clearly more, change the line to "a handful of lines."

### WHERE WE'RE STARTING (the block as it is)
`[SCREEN: VS Code — `src/edit.js` of the meme generator, scrolled to the `if ( ! image )` early return]`
**VO:** "Okay, so here's the block. The part that matters is this check up here. If there's no `image` attribute, we return a `Placeholder` with the image picker in it. If there *is* an image, we skip that and render the meme, with the two `RichText` fields and the `img` tag."

`[SCREEN: highlight `if ( ! image )`]`
**VO:** "So the picker already exists. The block just needs `image` to be empty again. That means our button only has one job, which is to clear that attribute."
> 🎯 This beat makes the rest of the demo obvious. Once viewers see that "no image = picker," the `onClick` is a one-liner they already expect. Keep it brief.

### WHAT BLOCKCONTROLS ACTUALLY IS (the mechanism)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "Before we write anything, let's talk about what `BlockControls` is doing, because it's kind of neat. It's a Slot/Fill. The block toolbar has a slot in it, and `BlockControls` is the fill. So anything you put inside `BlockControls` in your `edit` function doesn't render where you wrote it. It gets picked up and rendered over in the toolbar instead."

**VO:** "It's kind of like forwarding your mail. You write the address in your component, and the post office delivers it somewhere else."
`[OST: "BlockControls = Fill → block toolbar Slot"]`

**VO:** "And the other nice part is that the editor only shows those controls when your block is selected. You don't write any of that logic yourself."
> ✅ `BlockControls` is a Slot/Fill that renders its children into the block toolbar, and the toolbar shows only for the selected block. Source: https://developer.wordpress.org/block-editor/getting-started/fundamentals/block-in-the-editor/#block-toolbar and the `BlockControls` README in the Gutenberg repo, https://github.com/WordPress/gutenberg/tree/trunk/packages/block-editor/src/components/block-controls
> ⚠️ CONFIRM: check the fundamentals doc anchor still resolves before putting it in the description.

### ADDING THE BUTTON (type-and-narrate)
`[SCREEN: VS Code — imports at top of `src/edit.js`]`
**VO:** "All right, imports first. `BlockControls` comes from `@wordpress/block-editor`, and `ToolbarGroup` and `ToolbarButton` come from `@wordpress/components`."

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

`[SCREEN: VS Code — scroll to the main `return`, cursor after the closing `</section>`]`
**VO:** "Now down in the main return, right after the section, I'm going to drop in `BlockControls`. And yes, I'm putting it *after* the markup, which looks like it should put a button under my meme. It won't, because of that Slot/Fill thing. Where you put it in the JSX doesn't change where it shows up."

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

`[SCREEN: highlight `<ToolbarGroup>`]`
**VO:** "Inside that, a `ToolbarGroup`. That's what gives us the little divider, so our button gets its own section instead of getting mashed up against the core controls."

`[SCREEN: highlight `icon` and `label` props]`
**VO:** "Then the `ToolbarButton`. I'm using the `remove` dashicon, and the `label` is doing more than you'd think. It's the tooltip when you hover, and it's also the accessible name for the button. So an icon-only button with no label is a button nobody using a screen reader can figure out. Don't skip it."

`[SCREEN: highlight `onClick`]`
**VO:** "And `onClick` just calls `setAttributes` and sets `image` to `false`. That's it, really."
> ✅ `ToolbarButton` `label` is used as the tooltip and `aria-label` for icon-only buttons. Source: https://developer.wordpress.org/block-editor/reference-guides/components/toolbar-button/
> ⚠️ CONFIRM: `image` is declared as `"type": "object"` in `block.json`. Setting it to `false` works in the editor, but check that it survives save → reload without a block validation warning. If it doesn't, use `setAttributes( { image: undefined } )` in the recording instead, and update the VO to "sets `image` to `undefined`."
> 🎯 This is the longest beat. If it runs long in the edit, the `ToolbarGroup` divider explanation is the easiest cut. Keep the `label` accessibility point.

### DOES IT WORK? (the payoff)
`[SCREEN: screen-capture — refresh editor, select the meme block]`
**VO:** "Okay, let's save, refresh, and select the block. And look, there's our button in the toolbar. Hover it and you get the tooltip."

`[SCREEN: click the remove button — the meme disappears and the image picker placeholder comes back]`
**VO:** "Click it, and we're back at the picker. So I can go grab a better image, which, let's be clear, is doing a lot of the work in any meme I make."

`[SCREEN: pick a new image, type top/bottom text]`
**VO:** "And my text is still there, because we only cleared `image`. The `topText` and `bottomText` attributes didn't change."
> ⚠️ CONFIRM: on the demo build, the RichText values come back after picking a new image. They should, since only `image` is reset. Check on camera before you say it.
> 🎯 End this beat on the new meme, fully rendered. That's the strongest visual in the video.

### ONE THING TO NOTICE (the gotcha)
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "There's one thing I want to point out. I only put `BlockControls` in the main return, not in the placeholder branch. So when there's no image, the button's gone, which is what we want, since there's nothing to remove. But if you ever add a toolbar button and it just doesn't show up, go check which return you put it in. I've done that more than once."
> 🎯 Short, self-deprecating, and it's a real bug viewers will hit with early returns. If the edit needs time, this beat can be cut without breaking the flow.

### RECAP + CTA + END SCREEN
`[SCREEN: TALKING HEAD — Ryan to camera]`
**VO:** "So, to recap, you wrap your controls in `BlockControls`, group them with `ToolbarGroup`, and use `ToolbarButton` with a real label and an `onClick` that updates your attributes. The Slot/Fill handles putting it in the toolbar and showing it only when the block's selected."

**VO:** "Let me know in the comments what toolbar button you're adding to your own blocks, and if you ran into any issues. And if you want more WordPress dev stuff like this, hit subscribe, there's more coming."

**VO:** "Thanks for watching and I'll see you in the next one."
`[SCREEN: end screen — subscribe + ‹TODO: next-video target — no content plan entry; pick at publish›]`
`[OST: pinned-comment reminder]`

---

## 📦 PACKAGING

**Title (‹TODO: viDIQ-scored — use winner, A/B with #2›):**
- ✅ **Add a Custom Toolbar Button to Your WordPress Block (BlockControls)** — *‹TODO: viDIQ score + why›*
- How to Use BlockControls in a Custom WordPress Block — *‹TODO: score›*
- WordPress Block Toolbar Buttons in 10 Lines of Code — *‹TODO: score; only if the "ten lines" CONFIRM holds›*

**Thumbnail concept:** Split frame. Left: Ryan's face, confused, beside a meme block with the wrong image. Right: the block toolbar zoomed in, with the new remove button circled. Bold text: "ADD A TOOLBAR BUTTON". ‹TODO: template ref›
**viDIQ reference images:** ‹TODO: Ryan's scored image URLs›
**Pinned comment:** "The whole thing is `<BlockControls>` → `<ToolbarGroup>` → `<ToolbarButton label onClick />`. What toolbar button are you adding to your own blocks?"

---

## 📝 YOUTUBE DESCRIPTION (paste-ready)

> Want to add your own button to the block toolbar in WordPress? In this quick tip, I add a "remove image" button to a meme generator block with BlockControls, ToolbarGroup, and ToolbarButton, and explain how the Slot/Fill gets it into the toolbar.

**Chapters:** ‹TODO: time these off the FINAL edit — labels track the SCRIPT beats in order. First chapter must stay 0:00 (YouTube requires it); you need 3+ chapters, each 10s or longer.›
```
0:00 Cold open
‹M:SS› Where we're starting
‹M:SS› What BlockControls actually is
‹M:SS› Adding the button
‹M:SS› Does it work?
‹M:SS› One thing to notice
‹M:SS› Recap
```

**Resources:**
- Block toolbar and BlockControls (Block Editor Handbook): https://developer.wordpress.org/block-editor/getting-started/fundamentals/block-in-the-editor/#block-toolbar
- ToolbarButton component reference: https://developer.wordpress.org/block-editor/reference-guides/components/toolbar-button/
- Block Developer Cookbook (meme generator block): https://github.com/ryanwelcher/block-developer-cookbook
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

#WordPress #Gutenberg #BlockDevelopment #WordPressDeveloper #JavaScript #React

---

## ✅ Pre-record checklist
- [ ] CONFIRM `image: false` vs `image: undefined` survives save → reload with no block validation warning (and match the VO to whichever you use)
- [ ] CONFIRM the "about ten lines" claim against the final diff
- [ ] CONFIRM `topText` / `bottomText` stay put after swapping the image
- [ ] CONFIRM the Handbook anchor link and ToolbarButton reference URL still resolve
- [ ] Meme generator block scaffolded at the "Step 6" state (picker works, no `BlockControls` yet), and a post with the wrong image already inserted for the cold open
- [ ] Editor zoomed so the toolbar button is readable at 1080p
- [ ] Clean cold-open take (talking head → toolbar hunt → talking head)
- [ ] Thumbnail from template
- [ ] ‹TODO: schedule note›

## 🔀 Alt hooks (A/B in your head)
1. "This is the block toolbar. Every core block puts its own buttons up here. And for some reason, it took me way too long to figure out I could put mine up there too."
2. "I made a meme, and I picked the wrong image. And the block I wrote gave me no way to fix it. So let's add one button and fix that."
