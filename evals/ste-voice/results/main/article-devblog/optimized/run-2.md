The full draft is saved to `draft.md`. I haven't built or run the code, so the steps haven't been tested in an editor.

**Structure:**
- **Intro:** says why this kind of action belongs in the toolbar rather than the sidebar, then introduces `BlockControls`, `ToolbarGroup` and `ToolbarButton`.
- **Prerequisites** and **the starting block:** complete `block.json`, `edit.js` and `save.js` for a block that stores `mediaId`, `mediaUrl` and `mediaAlt`.
- **Add the toolbar button:** 11 numbered steps. Each code step shows only the lines that change, with a clear anchor. The steps end with "make sure that" checks, followed by the complete `edit.js`.
- **Pick the right toolbar group:** a table of the `group` values. I used `other` because that's where the core Image block puts **Replace**.
- **Disable instead of hide:** a version that uses the `disabled` prop.
- **Gotchas:**
  - A `ToolbarButton` needs a `ToolbarGroup` around it for keyboard navigation to work.
  - Icon-only buttons need a `label`.
  - Clearing attributes to `undefined` instead of `''` keeps leftover values out of the saved block.
  - Removing the image can be undone.
  - The toolbar only shows for the selected block.
- **Troubleshooting table:** ends with a short pointer to `ToolbarDropdownMenu` for a menu of related actions, with no summary section.

**Simplified English:** it's used only where readers act: the prerequisites, numbered steps, checks and troubleshooting table. The intro, explanations and gotchas are in your voice.

**Things to check before publishing:**
- **Setup:** the steps have readers install `@wordpress/icons` with npm. WordPress doesn't load that package for you, so it gets bundled into the build.
- **Version:** "WordPress 6.6 or later" is a safe floor I picked, not a tested minimum.
- **Cut claims:** I removed two I couldn't confirm. One said disabled toolbar buttons stay focusable; the other was about how the button behaves in **Top toolbar** mode.