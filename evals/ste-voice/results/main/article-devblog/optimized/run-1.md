I wrote the full tutorial and saved it to `draft.md`. It's written in your voice, and the steps use Simplified Technical English, which is the default for the Developer Blog. I haven't built or run the code, so please test it before publishing.

**Structure:**
- **Intro:** explains what `BlockControls`, `ToolbarGroup` and `ToolbarButton` each do, with no "In this article…" opener.
- **Prerequisites and scaffold:** sets up the block with `@wordpress/create-block`.
- **Basic image block:** full `block.json` attributes, `edit.js` and `save.js`.
- **Add the toolbar button:** a `trash` icon button whose `onClick` clears `mediaId`, `mediaUrl` and `mediaAlt`.
- **Disable when empty:** uses `disabled={ ! mediaUrl }` plus `accessibleWhenDisabled`, and explains how keyboard users lose focus without it.
- **Toolbar placement:** a table of the `group` values, then moves the button to `group="other"`.
- **Gotchas:** always pass a `label`; clear to `undefined` instead of `''`; changing `save` breaks existing content without a deprecation; don't nest `ToolbarGroup`; `BlockControls` only works in the editor.
- **Troubleshooting table,** then a one-line close with no wrap-up section.

**STE in the steps:** each numbered step is one imperative action of 20 words or fewer. The warning comes before its step, and every procedure ends with a "Make sure that…" check. Code changes show only the changed lines and say where they go. The intro, reasoning and gotchas stay in your normal voice.

**Check these before publishing:**
- **`group` descriptions:** I wrote short explanations of where each `group` value shows in the toolbar. Check them against the current Gutenberg source.
- **Wrong import:** I say that importing `ToolbarButton` from `@wordpress/block-editor` makes the block crash in the editor. I believe that's right, but I haven't tested it.
- **Minimum version:** I listed WordPress 6.6 or later. I picked that as a safe floor for `accessibleWhenDisabled`, not from checking when it was added.