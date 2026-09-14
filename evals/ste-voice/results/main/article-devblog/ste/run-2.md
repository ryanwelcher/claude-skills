I saved the full draft to `draft.md`. It's written for the Developer Blog: your voice for the intro, reasoning and transitions, and Simplified Technical English for the parts readers act on. I haven't built or run the example code, and I haven't checked the API details against a live WordPress install.

**Structure**
- **Intro:** Starts with why toolbar actions matter, then shows how `BlockControls`, `ToolbarGroup` and `ToolbarButton` fit together.
- **Prerequisites:** A short STE list.
- **Basic image block:** Full `block.json`, `edit.js` and `save.js`, with attachment ID, URL and alt text attributes and a `MediaPlaceholder`. A 6-step test procedure follows.
- **Add the toolbar button:** A table of the three components, then numbered steps that end with a "Make sure that…" check. The clear handler sets the values to `undefined` in a single `setAttributes` call, and the article explains why (clean saved markup, one undo step).
- **Disable when empty:** Uses `disabled={ ! mediaUrl }`, with a brief case for disabling rather than hiding.
- **Toolbar placement:** A table of `group` prop values, then moving the button to `group="other"`, next to where core puts **Replace**. The finished `edit.js` comes after.
- **Gotchas:** A missing `label`, the toolbar only showing when the block is selected, `undefined` versus an empty string, attributes read from markup, one `setAttributes` call per action, and pointing to `MediaReplaceFlow`.
- **Troubleshooting:** A table of problem, cause and fix. The article ends there, with no conclusion.

**STE rules applied**
- Each step is one imperative action.
- Code changes show only the changed lines, anchored to a location in `src/edit.js`.
- The caution about `ToolbarButton` outside a `ToolbarGroup` comes before its steps.
- Every procedure ends with a check.

**Two things to check before publishing:**
- Prerequisites say WordPress 6.5+ and Node 20+. Change these to whatever versions you want to require.
- The table of `group` values and where each one shows reflects my understanding of the current editor. Confirm it in a recent Gutenberg build.