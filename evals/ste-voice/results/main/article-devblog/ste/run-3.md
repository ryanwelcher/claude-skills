I wrote the full tutorial and saved it to `draft.md`. It uses the hybrid style set for the Developer Blog: your voice in the intro, the explanations and the gotchas, and Simplified Technical English in the parts readers act on. That covers the prerequisites, numbered steps, test checks, the caution and the troubleshooting table. I haven't built or run any of the code.

**How it's laid out:**
1. **Intro:** the toolbar is where users already look, but most custom blocks put everything in the sidebar instead.
2. **Prerequisites.**
3. **How the three pieces fit together:** a table showing that `BlockControls` is the slot, `ToolbarGroup` is the container and `ToolbarButton` is the control.
4. **A basic image block:** `block.json` attributes, `edit.js` with `MediaPlaceholder`, and `save.js`. It ends on the problem: once an image is picked, you can't pick a different one.
5. **Adding the button:** numbered steps (install `@wordpress/icons`, imports, `onClearImage`, the `BlockControls group="other"` markup), a test procedure ending in a "make sure that…" check, and the complete `edit.js`. Three notes cover `group`, only showing the button when there's an image, and `label` as the accessible name.
6. **A second example:** a rounded-corners on/off button using `isPressed`, as numbered steps with a check at the end.
7. **Gotchas:**
   - Clear attributes with `undefined`, not `''`.
   - Changing `save` breaks blocks already in posts, so the caution comes before the step.
   - Install `@wordpress/icons` directly rather than relying on it arriving through another package.
   - A troubleshooting table for when the button doesn't show.
   - Don't put important actions only in the toolbar.

It ends on the last gotcha, with no conclusion section.

**Check these before publishing:**
- **`cornerAll` icon:** I believe it's in `@wordpress/icons`, but I didn't confirm it.
- **Empty `imageId` claim:** the gotcha says an `imageId` of `''` gets ignored the next time the post loads. That's how I understand attribute parsing to work, and it would be worth a quick test.
- **Plugin text domain:** the code uses `toolbar-demo` as a placeholder. Change it to match your plugin.
- **No CSS for rounded corners:** the example doesn't include a stylesheet for the `is-rounded` class. That's why its check only confirms the button shows as pressed.