**Mode:** Hybrid. That's the card's default for the Block Developer Cookbook. I didn't run the linter because the passage is short and there's no file on disk, so I checked it against the card by hand.

## Zone map

| # | Text | Zone |
|---|---|---|
| A | "You can choose to either use the repository…" | Action (borderline: it reads like an intro, but it's a setup choice the reader has to make) |
| B | "Run the following command…" + `npx` command | Action (setup command) |
| C | "Once the scaffold has completed…" + `cd` command | Action (setup command) |
| D | "Finally, make sure to activate the plugin." | Action (step and check) |

## Findings

**A: Choosing a setup option**

1. **Text:** "You can choose to either use the repository which provides a development environment or to just download the standalone plugin."
   **Rules broken:** 3 (not imperative), 13 ("just"), 14 (a comparison written as prose), Word swaps (choose → select)
   **Rewrite:**
   > Select one of these options:
   >
   > | Option | What you get |
   > |---|---|
   > | Repository | The plugin and a development environment |
   > | Standalone plugin | The plugin only |

2. **Text:** Section A, compared with the steps in B–D
   **Problem:** The steps don't say which option they're for. The `create-block --template` command only gives the reader the standalone plugin, so someone who picks "Repository" has no steps to follow.
   **Rule broken:** 2 (one instruction per step; here the step doesn't match the option)
   **Rewrite:** Put a heading or lead-in above step 1: "To use the standalone plugin, do these steps:". Then either add steps for the repository option or link to them.

**B: Scaffolding the plugin**

3. **Text:** "Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation."
   **Rules broken:** 2 (two actions: go to the directory, then run the command), 13 ("of your choice" is filler)
   **Rewrite:**
   > 1. In a terminal, go to the `wp-content/plugins` directory of your local WordPress installation.
   > 2. Run this command:

**C: Starting the build**

4. **Text:** "Once the scaffold has completed completed, start the build process from inside the newly created plugin"
   **Rules broken:** Word swaps (once → after; created → made), 10 ("the scaffold" and "the newly created plugin" are two names for one thing)
   **Other problems:** "completed" appears twice, and the sentence has no final punctuation.
   **Rewrite:**
   > 3. After the command completes, start the build from the new `meme-generator` plugin directory:

**D: Activating the plugin**

5. **Text:** "Finally, make sure to activate the plugin."
   **Rules broken:** 15 (no UI click path), 10 ("make sure" is used for an action here, but the card keeps it for checks)
   **Rewrite:**
   > 4. In the WordPress admin, go to **Plugins > Installed Plugins**.
   > 5. Under **Meme Generator**, click **Activate**.

6. **Text:** The procedure as a whole
   **Rule broken:** 7 (the procedure doesn't end with a check)
   **Rewrite:**
   > 6. Make sure that the **Meme Generator** block shows in the block inserter.

## Borderline

- **B1: Zone for sentence A.** It could be read as intro text in Ryan's voice. I classed it as action because the reader has to make a choice before step 1.
- **B2: Splitting `cd meme-generator && npm run start`.** Rule 2 would make this two steps, one per command. But splitting the line changes a command, which the card says never to do, so I left the code block as it is.
- **B3: Things I assumed.** The rewrites assume the `wp-content/plugins` path, the **Meme Generator** plugin label, and the block name. Check these against the real plugin and admin screens before you use the rewrites.
- **B4: A missing NOTE.** Readers may not know that `npm run start` keeps running in the terminal. A NOTE before step 3 would help: "**NOTE:** The build keeps running. Do not close the terminal." That's new content, not a fix to existing text, so I've left it here rather than in the findings.