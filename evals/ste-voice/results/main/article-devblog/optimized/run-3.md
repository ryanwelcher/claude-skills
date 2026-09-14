I wrote the full tutorial and saved it to `draft.md`. I skipped the outline step, as you asked. I haven't run the code in a real editor, so it hasn't been tested.

**What it covers:**
- **Starting point:** an image card block with the full `block.json`, `edit.js` and `save.js`, where `MediaPlaceholder` picks the image. Right now the only way to remove the image is to delete the block.
- **The three components:** a short table of what `BlockControls`, `ToolbarGroup` and `ToolbarButton` each do.
- **First version:** a button that clears the image by setting `mediaId` and `mediaUrl` to `undefined`. The post explains why `undefined` beats an empty string: it keeps the attribute out of the saved markup.
- **Showing it only when useful:** the button appears only when the block has an image. This step switches to `BlockControls group="other"` and adds a table of the `group` values.
- **Visible label:** "Remove" text next to the trash icon, followed by the complete final `edit.js`.
- **Gotchas:**
  - Use `ToolbarButton` rather than a plain `Button`, because a plain `Button` breaks arrow-key navigation.
  - Always pass a `label`.
  - The controls only show when the block is selected.
  - Removing the image doesn't delete the file from the Media Library.
  - Undo already works, so you don't need a confirmation step.
  - A troubleshooting table for common problems.

**Style:** The Developer Blog calls for the hybrid mode. The intro, explanations and transitions are in your voice. The prerequisites, numbered steps, caution and troubleshooting table use Simplified Technical English (STE). Each step is one action of 20 words or fewer, and each set of steps ends with a "Make sure that…" check. Code edits show only the changed code, with a clear note on where it goes. The post ends on one line pointing to other toolbar controls, not a summary section.

**Worth checking before publishing:**
- The "WordPress 6.5 or later" requirement is a guess. The code should work on older versions too, so adjust it if you like.
- Replacing the `ToolbarButton` in the last step drops the `mediaUrl &&` check around it. The final `edit.js` has the check, so the finished code is right.