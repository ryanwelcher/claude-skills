**Mode:** hybrid (Block Developer Cookbook default). **Path:** quick, because the passage is short and pasted in chat.

## Zone map

| # | Text | Zone |
|---|---|---|
| A | "You can choose to either use the repository…" | Action (setup choice) |
| B | "Run the following command in a terminal…" + `npx` command | Action (setup command) |
| C | "Once the scaffold has completed completed…" + `cd` command | Action (setup command) |
| D | "Finally, make sure to activate the plugin." | Action (step) |

There are no voice zones. I left both code blocks exactly as they are.

## Findings

**1. Zone A**
- **Text:** "You can choose to either use the repository which provides a development environment or to just download the standalone plugin."
- **Rules broken:** Rule 3 (use commands, not "You can…"), Rule 13 (no "just"), Rule 14 (show choices as a list), and the word swap "choose" → "select".
- **Rewrite:**
  > Select one option:
  > - Use the repository. The repository gives you a development environment.
  > - Download the standalone plugin.

**2. Zone B**
- **Text:** "Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation."
- **Rules broken:** Rule 1 (21 words, and the limit for steps is 20), Rule 2 (one sentence gives two actions: go to the folder, then run the command), and Rule 13 ("of your choice" adds nothing).
- **Rewrite:**
  > In a terminal, go to the `plugins` directory of your local WordPress installation.
  >
  > Run this command:

**3. Zone C**
- **Text:** "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
- **Rules broken:** It has a typo ("completed" appears twice) and no end punctuation. It also breaks the word swaps "once" → "when" and "created" → "made" (here "new" is enough). The prose asks for two actions, but a single command does both. Because I can't change the command, the rewrite describes what the command does.
- **Rewrite:**
  > When the scaffold is complete, run this command. The command opens the `meme-generator` directory and starts the build process:

**4. Zone D**
- **Text:** "Finally, make sure to activate the plugin."
- **Rules broken:** Rule 15 (give the full path in the admin screens), Rule 3 ("make sure" is for checks, not for steps), and Rule 7 (end the steps with a check).
- **Rewrite:**
  > Go to **Plugins > Installed Plugins** and activate the meme generator plugin.
  >
  > Make sure that the plugin shows as active.

## Borderline

- **B1, Zone A:** You could treat this sentence as an intro (voice zone) and keep it. Even so, "just" and "choose" should go, because readers act on this choice.
- **B2, Finding 4:** The rewrite uses **Plugins > Installed Plugins**, the standard WordPress admin path. I didn't use the plugin's name as it appears in that list, because I don't know it. Check that name before you add it to the rewrite.
- **B3, Finding 3:** The `cd … && npm run start` command still does two actions in one step. If you can change the recipe's commands, split it into two blocks (`cd meme-generator` and `npm run start`) so that each step has one instruction.