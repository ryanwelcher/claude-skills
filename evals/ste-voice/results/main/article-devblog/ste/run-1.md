I saved the full draft to `draft.md`. I skipped the outline and didn't ask any questions. Because it's for the Developer Blog, I used the hybrid style. The intro, explanations and section transitions are in your voice. The numbered steps, prerequisites, the one caution and the troubleshooting table follow the STE card. I didn't build the example block or run the code.

**How it's laid out:**
1. **Intro:** A custom block with an image gives users no way to get back to the empty placeholder without deleting the block. That's why a toolbar button helps.
2. **Prerequisites** and a **starting block** made with `create-block`. It stores the image ID, URL and alt text, and shows a `MediaPlaceholder` when there's no image.
3. **Add the toolbar button:** a table explaining `BlockControls`, `ToolbarGroup` and `ToolbarButton`, the `onRemoveImage` handler, and why the button only shows when the block has an image.
4. **Choosing where the button shows:** a table of the `group` prop's values, using `group="other"`.
5. **Add a replace button** next to the remove button with `MediaReplaceFlow`.
6. **Gotchas:**
   - Clear attributes to `undefined`, not `''`, so they don't get saved in the post.
   - Always give `ToolbarButton` a `label`.
   - Use `ToolbarButton`, not a plain `Button`, or keyboard users can't reach it with the arrow keys.
   - Focus is lost when the button disappears after removal; this section includes a `useRef` fix.
   - The toolbar only shows when the block is selected.
7. **Troubleshooting table.** The article ends there, with no conclusion.

**Check these before publishing:**
- **Prerequisites:** "WordPress 6.6+" and "Node 20+" are my guesses, so change them to whatever you want to require.
- **`group` prop values:** Confirm the names and where each group shows up against the current Gutenberg version.
- **Focus fix:** It moves focus to the block wrapper with `blockRef.current?.focus()`. Test it with a keyboard in the editor.