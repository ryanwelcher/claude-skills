I wrote the full tutorial and saved it to `draft.md`. I didn't run any of the code, so test the snippets in a block before you publish.

**Structure:**
1. **Intro:** says why frequent actions belong in the block toolbar rather than the settings sidebar.
2. **Starting block:** a `block.json` and `edit.js` for an "Image Card" block with `mediaId`, `mediaUrl` and `mediaAlt` attributes, using `MediaPlaceholder`.
3. **Adding the toolbar button:** the smallest working version with `BlockControls`, `ToolbarGroup` and `ToolbarButton` plus the `trash` icon. Notes cover where the button renders, why `label` matters for accessibility, and where the icon comes from.
4. **Only show the button when it's useful:** hiding the button versus disabling it, with a recommendation to hide it.
5. **Using a text label instead of an icon:** a "Clear" text button, and the `group="other"` prop on `BlockControls`.
6. **The complete `edit.js`**
7. **Gotchas:**
   - Reset every image attribute, not just the URL.
   - `undefined` and an empty string save differently.
   - The three components come from two different packages.
   - `BlockControls` only renders when the block is selected.
   - Clearing can be undone, so there's no need for a confirm dialog.

It ends on the last gotcha, with no conclusion section.

Two claims to check against the current Gutenberg source before publishing:
- Passing `group` to `BlockControls` makes a wrapping `ToolbarGroup` unnecessary.
- Core puts actions like **Replace** in the `other` group.