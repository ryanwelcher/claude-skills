I saved the full tutorial to `draft.md`. I didn't show you an outline first, as you asked.

**How it's laid out:**
- **Intro:** says what the block toolbar is for, then covers the three pieces: `BlockControls`, `ToolbarGroup` and `ToolbarButton`.
- **The starting block:** an Image Card block, with its `block.json`, an `edit` function using `MediaPlaceholder`, and a `save` function.
- **Adding the button:** the full `edit` code with a trash button that clears the image, plus notes on the fragment, `label` and `onClick`.
- **Only showing the button when it's useful:** two options, hiding the button when there's no image or disabling it.
- **Placing the button:** the `group` prop, using `group="other"` so it sits next to core's **Replace** control.
- **Using text instead of an icon:** `ToolbarButton` with a text label.
- **Gotchas:**
  - Don't use a plain `Button`, because it breaks arrow-key navigation in the toolbar.
  - Clear attributes with `undefined`, and reset any attribute that has a default back to that default.
  - Clear every related attribute, not just the URL.
  - You don't need to check `isSelected`.
  - The button can disappear in content-only mode.

**Check before publishing:** I wrote the content-only gotcha from memory and didn't check it against Gutenberg's code. It claims that `templateLock: 'contentOnly'` hides the `default` toolbar group but keeps `other` visible. That detail has changed between releases, so test it or look at `block-controls/hook.js` before this goes out.

It ends on that last gotcha, with no conclusion section.