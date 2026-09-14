# STE Card — Simplified Technical English for action zones

A working subset of ASD-STE100 Simplified Technical English. This is **STE-informed**, not
certified STE: the full controlled dictionary is licensed and too large to load. Apply these
rules where readers *act*. Everywhere else, Ryan's voice cards win.

This card is the single source of truth. Skills read it live by path — never copy its rules
into a SKILL.md.

## Zones

Split every piece of content into two kinds of zone before writing or auditing.

| Zone | Rules | Contains |
|---|---|---|
| **Action zone** | This card wins | Numbered steps, prerequisites/requirements, warnings and cautions, UI click paths, troubleshooting tables, "make sure that…" checks, setup commands |
| **Voice zone** | Voice card wins (`write-article/references/writing-style.md` or `youtube-script/references/style-card.md`) | Intros, "why this matters", reasoning asides, transitions between sections, closings, credits |

**Strict mode** applies this card to the whole piece (both zones). Use it only when asked.

## Never change

- Code blocks, commands, file paths, and code identifiers.
- UI labels exactly as they appear on screen (**Appearance > Editor**), even if a label uses an unapproved word.
- Technical names (`useEffect`, `block.json`, SlotFill) — STE allows technical names and technical verbs from the domain.
- Strings inside code (placeholders, translated labels).

## Writing rules (action zones)

1. **Procedural sentences: 20 words max.** Descriptive sentences: 25 words max.
2. **One instruction per step.** Two actions → two steps. Exception: an action and its direct object location ("Open `src/edit.js`.").
3. **Imperative mood for instructions.** "Open the file." Not "You should open the file" or "Let's open the file."
4. **Active voice.** Name who or what does the action.
5. **Put the condition first.** "If the block has no image, the block shows a placeholder."
6. **Warnings and cautions come before the step they apply to**, never after.
   - `**WARNING:**` — risk of injury or data loss.
   - `**CAUTION:**` — risk of damage: broken code, a crashed browser, a failed build.
   - `**NOTE:**` — useful data that is not a risk.
   A warning or caution starts with the instruction ("Do not…"), then gives the reason.
7. **End a procedure with a check.** "Make sure that the placeholder shows again."
8. **No idioms, humor, metaphors, or emoji.** "Stick a fork in it" → "The procedure is complete."
9. **No phrasal verbs.** "set up" → "configure", "spin up" → "start", "find out" → "find", "go back" → "return".
10. **One word, one meaning.** Pick one term for a thing and keep it ("select", not "select" then "choose" then "pick").
11. **No -ing words as nouns or sentence openers.** "Filtering the images" → "Filter the images".
12. **Keep articles** ("the", "a"). Do not drop them to shorten a sentence.
13. **No hedging in instructions** ("you might want to", "feel free to", "just"). If a step is optional, say "Optional:" at the start.
14. **Tables for comparisons and parameter lists** instead of prose.
15. **Full paths for UI navigation.** "Go to **Appearance > Editor > Styles**." Not "look in the Style section".
16. **Show only changed code, with an unambiguous anchor** ("In `src/edit.js`, below `useBlockProps()`, add:"). New files get full contents.

## Word swaps

Use the word on the right. These cover the most common misses in developer content.

| Avoid | Use |
|---|---|
| choose, pick | select |
| display, render (in prose) | show |
| ensure, verify | make sure |
| allow, enable (someone to) | let |
| update, modify | change |
| retrieve, fetch (in prose) | get |
| utilize, leverage | use |
| create, generate | make |
| execute, trigger | run, start |
| numerous, a lot of | many |
| in order to | to |
| prior to | before |
| once (meaning "after") | after, when |
| via | through, with |
| e.g., i.e. | for example, that is |

## Destination defaults

Skills pick a mode from the destination unless the user says "STE full", "strict", or "no STE".

| Destination | Mode |
|---|---|
| WordPress Developer Blog, Block Developer Cookbook, developer.wordpress.org | Hybrid (action zones) |
| ryanwelcher.com tutorials | Hybrid |
| Workshop section files | Hybrid, with every coding step in STE |
| P2 posts, opinion/essay posts, social posts | Off |
| YouTube and WND scripts/teleprompters | Off — spoken read copy |

## Refinement log
Corrections are recorded in `refinement-log.md` next to this card. **Do not read it to apply the rules**: every entry is already distilled into the sections above. To capture a new correction, update the relevant section above, then append a dated bullet to `refinement-log.md`.
