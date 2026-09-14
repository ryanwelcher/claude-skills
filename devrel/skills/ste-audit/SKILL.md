---
name: ste-audit
description: Internal forked helper for ste-pass. Maps zones in one file, runs ste-lint.py, and returns Simplified Technical English findings with proposed rewrites. Not for direct use.
context: fork
model: sonnet
user-invocable: false
allowed-tools: Bash(python3 *) Read
---

# STE audit (forked helper)

`ste-pass` calls this helper for files too long to audit inline. You run in a fork, on Sonnet, so the
parent's context and model are untouched. **Do not edit anything and do not ask questions.** Return
the three sections below and nothing else.

Arguments: `$ARGUMENTS` = `<file path> <hybrid|strict> [destination]`

## Steps

1. Read the card: `${CLAUDE_SKILL_DIR}/../ste-pass/references/ste-card.md`.
2. Read the target file. If it does not exist, return one line, `ERROR: <path> not found`, and stop.
3. **Map the zones** per the card's **Zones** table. Record each section's line range and zone.
   Instructions written as prose ("Run the following command…", "Once the scaffold has completed,
   start the build…") are **action zones** even when they are not numbered.
4. **Run the linter** on the action-zone ranges:
   ```
   python3 ${CLAUDE_SKILL_DIR}/../ste-pass/scripts/ste-lint.py <file> --lines <ranges>   # hybrid
   python3 ${CLAUDE_SKILL_DIR}/../ste-pass/scripts/ste-lint.py <file> --strict           # strict
   ```
   Use its hits as the starting list. Do not re-count words by hand. Drop hits that are UI labels,
   technical names, or voice-zone lines the linter misread.
5. **Add the judgment findings** the linter can't see:
   - Prose instructions that should be numbered steps.
   - A warning or caution after the step it applies to.
   - A step with more than one action.
   - A procedure with no final "make sure that…" check.
   - A vague UI location with no click path.
   - A comparison or parameter list in prose that belongs in a table.
   - Typos and doubled words in action zones.
6. **Write complete rewrites, not word swaps.** When an action zone needs restructuring, propose the
   full replacement text for that range: numbered steps, cautions moved before their step, and a
   final check. Keep code blocks, commands, UI labels, and technical names exactly as they are. In
   hybrid mode, never propose changes to voice zones.

## Return exactly this

```
## Zone map
| lines | zone | section |
|---|---|---|

## Findings
1. **L<start>–<end>** · <card rule, e.g. R2 or Word swaps> · "<offending text, max 2 lines>"
   → <proposed replacement text for that range>

## Borderline
- **L<n>** · <why it might not be a real finding> → <proposed rewrite>
```

No preamble, no summary, no copy of the file beyond the quoted offending text and the rewrites.
