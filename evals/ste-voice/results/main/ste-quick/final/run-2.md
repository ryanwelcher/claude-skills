**Mode:** Hybrid (Block Developer Cookbook default). **Path:** Quick (short pasted passage, so no linter or helper). As you asked, this is findings only. I haven't made any edits.

## Zone map

| Passage | Zone |
|---|---|
| "You can choose to either use the repository…" | Action (a setup choice the reader must make) |
| "Run the following command…" and its code block | Action (setup command) |
| "Once the scaffold has completed completed…" and its code block | Action (setup command) |
| "Finally, make sure to activate the plugin." | Action (setup step) |

The passage has no voice zones. Both code blocks stay as they are.

## Findings

**1.** "You can choose to either use the repository which provides a development environment or to just download the standalone plugin."
- **Rules broken:** Rule 1 (24 words, over the 20-word limit for steps), Rule 3 (not a command), Rule 13 ("just"), Rule 14 (a comparison belongs in a list or table). "choose" should be **select**.
- **Rewrite:**
  > Select one of these options:
  > - **Repository:** use the repository. It includes a development environment.
  > - **Standalone plugin:** download only the plugin.

**2.** "Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation."
- **Rules broken:** Rule 1 (20 words, right at the limit), Rule 2 (two actions: go to the folder, then run the command), Rule 13 ("of your choice" adds nothing).
- **Rewrite:**
  > 1. In a terminal, go to the `wp-content/plugins` directory of your local WordPress installation.
  > 2. Run this command:

**3.** "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
- **Rules broken:** "completed" appears twice (a typo), and the sentence has no period. "once" should be **after**. Rule 10: "the newly created plugin" is a new name for the `meme-generator` directory.
- **Rewrite:**
  > After the scaffold is complete, start the build process from the `meme-generator` directory:

**4.** "Finally, make sure to activate the plugin."
- **Rules broken:**
  - Rule 3: "make sure to" is the phrase for checks, not for commands.
  - Rule 15: the step has no UI path.
  - Rule 7: the steps don't end with a check.
- **Rewrite:**
  > 5. In the WordPress admin, go to **Plugins > Installed Plugins**.
  > 6. Activate the plugin.
  > 7. Make sure that the plugin shows as active.

**5.** The passage as a whole
- **Rule broken:** Rule 2. These are steps done in order, but they're written as prose paragraphs.
- **Rewrite:** Put the steps from findings 2–4 in a numbered list, with each code block under its step.

## Borderline

- **B1. The command in finding 3 does two things.** `cd meme-generator && npm run start` breaks Rule 2, but the card says never to change commands. One option is two code blocks (`cd meme-generator`, then `npm run start`), each under its own step. That changes the code, so it's your call.
- **B2. `wp-content/plugins` in finding 2 is new text.** It's the standard path, but the original only says "plugins directory." If you'd rather not name a path, keep "the plugins directory."
- **B3. Which repository?** Finding 1 mentions "the repository" but doesn't say which one. A non-native reader may not know it. Consider linking to it or naming it.
- **B4. A clearer check.** The check in finding 4 could name the block instead: "Make sure that the Meme Generator block shows in the block inserter." Only use this if that is the block's real name on screen.