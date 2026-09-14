I applied all 15 findings to `fixtures/meme-generator.md` in hybrid mode. The file is long (about 60 lines of prose), so the `ste-audit` helper ran the audit. I didn't touch code blocks, commands, technical names, the Overview or the closing.

## Zone map
- **Voice (left alone):** the title and metadata (L1–5), the Overview (L7–9) and the closing (L670–676).
- **Action:** Setup, Standalone, Repository, Step 1, Step 3, Step 8 and Step 9.

## Findings (all applied)
| # | Where | Card rule | What changed |
|---|---|---|---|
| 1 | Setup / Standalone | Numbered steps, check at the end, "choose" → "select" | Two setup options as a list; 4 numbered steps; closing check "Make sure that the plugin shows as active" |
| 2 | Repository | Numbered steps, NOTE up front, check at the end | Docker NOTE moved to the start; 5 numbered steps; a build check at the end |
| 3 | Step 1 (L69–71) | 25-word limit, one action per step, table, "update" → "change" | Attributes table; "Open `block.json`." and "Change the contents…" as separate steps |
| 4 | L128 | "retrieve" → "get", no "we can" | Two short imperative sentences |
| 5 | L200 | Caution goes before the step, "A LOT of" → "many", no humor | **CAUTION** moved before "Add the following to `edit.js`"; save/refresh/console as steps with a check |
| 6 | L204 | One action per step, "update" → "change" | Split into 2 steps |
| 7 | L265–267 | 25-word limit, table, "trigger" | Steps with a check; dependency-array table |
| 8 | L328, L398 | No "let's", check at the end | Imperative sentence; check at the end; `addImages` typo fixed to `allImages` |
| 9 | L402 | 39-word sentence, "choose"/"update" | Two short sentences |
| 10 | L406, L452 | Phrasal verb "open up", one action per step | "Open `block.json`." / "Add…"; "Change `block.json` to the following:" |
| 11 | L444–446 | 34-word sentence, "allows"/"pick", table | "lets the user select"; settings table; sidebar check; "provded" typo fixed |
| 12 | L555 | "open up", one action per step | Split into 2 steps |
| 13 | L664–666 | "a lot of", "allows", idiom "deeper dive" | Plain description; "For more information…" |
| 14 | L668 | Full UI path, 25-word limit | "Go to **Appearance > Editor > Styles > Typography**." plus a check |
| 15 | L24, L59 | Typo "completed completed" | "After the scaffold completes…" |

Where the helper's rewrite broke the card, I adjusted it:
- **#1:** "Select" instead of "Choose", for the word-swap rule.
- **#5:** the caution sits before the step that causes the problem, not after it.
- **#2 and #10:** I kept the `##` headings and didn't repeat "Open `block.json`" when the file is already open.

**Check before publishing:** in #14, the helper guessed the Site Editor path. I used **Appearance > Editor > Styles > Typography**, but it hasn't been checked in the editor.

## Borderline (still open, not applied)
- **L498:** "Do do this…" typo and a "we're going to" sentence. It reads like a transition, but it introduces a code change.
- **L547:** "Great work! Now this block is really starting to take shape!" is a voice line sitting inside an action section. That section still has no check.
- **L676:** "Stick a fork in it…" is the card's own example of a banned idiom. It's in the closing, a voice zone, so hybrid mode leaves it. "bon appetite" is also misspelled.
- **Code blocks:** every code block uses curly quotes, and the `npx` command has `–template` (a dash that should be `--template`). They'll break if someone copies them. The card says never to change code, so these need a separate fix.
- **Step numbering:** the headings go Step 1 → 3 → 8 → 9. That's a structure problem, not an STE one.
- **L404:** "Let's start with choosing the font color." still uses "let's" and "choosing". The audit didn't flag it, so I left it.

No refinement-log entries: none of the fixes added a new rule.