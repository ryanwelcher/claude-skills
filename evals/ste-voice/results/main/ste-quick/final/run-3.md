**STE pass: Block Developer Cookbook setup passage.** Hybrid mode (the default for Cookbook recipes), quick path (pasted passage). I made no edits, and the commands stay as they are.

## Zone map

| # | Text | Zone |
|---|---|---|
| A | "You can choose to either use the repository…" | Action (prerequisite: pick a setup option) |
| B | "Run the following command…" + `npx` block | Action (setup command) |
| C | "Once the scaffold has completed completed…" + `cd` block | Action (setup command) |
| D | "Finally, make sure to activate the plugin." | Action (step) |

The whole passage is action zone, so nothing is left for your voice.

## Findings

**1. Setup options (A)**
- **Offending text:** "You can choose to either use the repository which provides a development environment or to just download the standalone plugin."
- **Card rules:** Word swap choose → select; Rule 13 (no "just"); Rule 3 (imperative, not "You can"); Rule 1 (21 words, over the 20-word limit).
- **Rewrite:**
  > Select one of these options:
  > - Use the repository. The repository gives you a development environment.
  > - Download the standalone plugin.

**2. Terminal location (B)**
- **Offending text:** "Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation."
- **Card rules:** Rule 1 (21 words); Rule 2 (two actions: open a terminal in a directory, then run a command); Rule 13 ("of your choice" is filler).
- **Rewrite:**
  > Open a terminal in the `plugins` directory of your local WordPress installation.
  >
  > Run this command:

**3. Build step (C)**
- **Offending text:** "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
- **Card rules:**
  - "completed" appears twice.
  - Word swap once → after.
  - Word swap create → make. "newly created" becomes "new".
  - The sentence has no colon before the code block.
  - Rule 2: the step has two actions, and the command can't change, so the prose should say what the command does.
- **Rewrite:**
  > After the scaffold is complete, run this command. The command opens the new `meme-generator` directory and starts the build process:

**4. Activation (D)**
- **Offending text:** "Finally, make sure to activate the plugin."
- **Card rules:**
  - Rule 3: this is an instruction. "Make sure" is for checks, so the step should be a plain imperative.
  - Rule 15: the step needs a full UI path.
  - Rule 7: the procedure has no closing check.
- **Rewrite:**
  > Go to **Plugins > Installed Plugins** and activate the plugin.
  >
  > Make sure that the plugin shows as active.

## Borderline

- **A could be a voice zone.** Sentence A explains a choice rather than giving a step. If you treat it as your voice, drop Finding 1 but still remove "just".
- **Plugin name in Finding 4.** The rewrite doesn't name the plugin, because its label on the **Installed Plugins** screen isn't in the passage. Use the exact label if you want it named (for example, **Meme Generator**).
- **No links for the two options in A.** "the repository" and "the standalone plugin" don't point anywhere. This isn't an STE rule, but readers can't act on sentence A without the links.