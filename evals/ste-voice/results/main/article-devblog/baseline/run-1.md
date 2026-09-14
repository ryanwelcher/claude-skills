I wrote the full tutorial and saved it to `draft.md`. I haven't run any of the code, so build it and try it in the editor before publishing.

The structure:
1. **Intro:** why this action belongs in the toolbar and not the Settings Sidebar, and what each of the three components does.
2. **Starting block:** a `block.json` that stores `mediaId` and `mediaUrl`, and an `edit.js` that shows a `MediaPlaceholder`.
3. **Adding the button:** `BlockControls` → `ToolbarGroup` → `ToolbarButton` with a trash icon, clearing both attributes to `undefined`.
4. **Progressive variants:**
   - keeping the button visible and using `disabled` when there's no image
   - a text button instead of an icon
   - the `group` prop (`default`, `block`, `inline`, `other`)
   - several buttons pulled into their own toolbar component
5. **Gotchas:**
   - a button without a `ToolbarGroup` loses arrow-key navigation
   - an icon button with no `label` has no accessible name
   - leaving a stale `mediaId` behind
   - `undefined` isn't the same as `''`
   - the toolbar only shows when the block is selected
   - removing the image from the block doesn't delete the file

It ends at the last gotcha, with no conclusion.

Check these before publishing:
- **Multi-block selection:** I wrote that custom block controls are hidden when several blocks are selected. I'm not confident that's true in current Gutenberg, so confirm it or cut that sentence.
- **Open-in-new-tab button:** that example passes `href` and `target` to `ToolbarButton`, which should forward them to `Button`. Make sure it still looks and behaves right when the button is disabled.
- **`@wordpress/icons`:** the draft tells readers to install it with npm. If you'd rather keep dependencies down, you could use Dashicon strings instead.