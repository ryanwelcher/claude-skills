# Production-Document Format (structure only)

This is the **shape** of Ryan's video docs (from his Obsidian "YouTube Growth" folder).
Use it for STRUCTURE ONLY. All spoken **VO** content comes from the skill's voice —
`style-card.md` + the anti-AI pass — never copied from any example. Format here, voice there.

**Legend used in the doc:** `[SCREEN]` = what's on screen · `[OST]` = on-screen text ·
**VO** = spoken voiceover (write these in Ryan's voice).

Produce the full document with these sections in order. Leave `‹TODO: …›` placeholders for
anything only Ryan or his tools supply (keyword metrics, viDIQ scores, thumbnail refs,
publish date, tier, vault links).

---

```
# 🎬 W‹n› — ‹Title› (‹for who, e.g. for Developers›)

Part of ‹TODO: [[Block …]]› · rules: ‹TODO: [[Operating Rules]]›

| | |
|---|---|
| **Publish** | ‹TODO: date + record/schedule note› |
| **Type / Tier** | ‹TODO: NATIVE/… · Tier …› |
| **Length** | ~‹n›–‹n› min edited |
| **Target keyword** | *‹keyword›* (‹TODO: vol/mo · comp›) |
| **Scope** | ‹what's in / what's deferred to a later video› |
| **Audience** | ‹e.g. WordPress developers using Claude Code› |
| **Voice** | warm, dev-to-dev, "Hey friends" — tighter than a stream |

**Stack (the real thing):** ‹only for technical builds — the actual tools/packages/links›

**Legend:** `[SCREEN]` = on screen · `[OST]` = on-screen text · **VO** = spoken

---

## 🎥 SCRIPT

### COLD OPEN (the hook — do NOT slow-roll)
`[SCREEN: …]`
**VO:** "‹hook, in Ryan's voice — see style-card. Edited videos usually cold-open.›"
`[OST: "‹title-ish overlay›"]`
> 🎯 ‹director note: why this works / the retention logic for this beat›

### ‹BEAT NAME› (‹intent›)
`[SCREEN: …]`
**VO:** "‹spoken line(s) in voice›"
`[OST bullets: …]`            ← when listing what's coming
```bash
‹commands when relevant›
```
> ✅ ‹confirmed fact + source URL›        ← when stating something checkable
> ⚠️ CONFIRM: ‹thing to verify before recording›
> 🎯 ‹director note›

### … more beats …
‹Each beat: an ALL-CAPS name + (intent), [SCREEN] direction(s), **VO** spoken lines
in voice, optional code, and a `>` note where it earns its place. Build an escalating
spine; end beats on the strongest moment. NO timestamps — see the note below.›

### CTA + END SCREEN
**VO:** "‹comment ask + subscribe + sign-off in voice — e.g. 'See you then, friends.'›"
`[SCREEN: end screen — subscribe + next-video thumbnail]`
`[OST: pinned-comment reminder]`

---

## 📦 PACKAGING

**Title (‹TODO: viDIQ-scored — use winner, A/B with #2›):**
- ✅ **‹winning title›** — *‹TODO: viDIQ score + why›*
- ‹A/B alternate› — *‹TODO: score›*
- ‹more options ranked›

**Thumbnail concept:** ‹composition — split/face/contrast/3–4 bold words›. ‹TODO: template ref›
**viDIQ reference images:** ‹TODO: Ryan's scored image URLs›
**Pinned comment:** ‹the key command/link + a question that drives comments›

---

## 📝 YOUTUBE DESCRIPTION (paste-ready)

> ‹2–3 sentence summary, keyword-forward, in plain voice›

**Chapters:** ‹TODO: time these off the FINAL edit — labels track the SCRIPT beats in order.
First chapter must stay 0:00 (YouTube requires it); you need 3+ chapters, each 10s or longer.›
```
0:00 ‹first beat label›
‹M:SS› ‹next beat label›
‹…one per SCRIPT beat, in order›
```

**Resources:**
- ‹real links referenced in the video›

**My Stuff:** (standing footer — reuse as-is)
👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/
👉 WordPress Snippets VSCode extension: https://marketplace.visualstudio.com/items?itemName=ryanwelcher.modern-wordpress-development-snippets
👉 WordPress Playground markdown editor: https://marketplace.visualstudio.com/items?itemName=ryanwelcher.playground-readme-editor

**Connect:** (standing footer — reuse as-is)
https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

‹#hashtags relevant to the video›

---

## ✅ Pre-record checklist
- [ ] ‹facts to CONFIRM before recording›
- [ ] ‹environment/setup ready›
- [ ] ‹clean cold-open take›
- [ ] Thumbnail from template
- [ ] ‹schedule note›

## 🔀 Alt hooks (A/B in your head)
1. "‹alternate cold-open hook in voice›"
2. "‹another›"
```

---

## Notes for filling this in
- **VO is the only voice-governed part** — every `**VO:**` line goes through `style-card.md`
  and the anti-AI pass. Director notes, `[SCREEN]`, `[OST]`, and packaging are crisp and
  functional, not "in character."
- **NO timestamps on beats. Ever.** Beats are named and ordered, never timed. Any number you'd
  write is a guess that survives neither the recording nor the edit — and once it's wrong it
  actively lies about pacing (a beat marked as a 70-second slot ran 108). Order is real
  information; a made-up clock isn't. If a beat feels too long, say so in a `> 🎯` note in
  words ("this runs long — the version-by-version stretch is the place to cut"), which stays
  true no matter how the edit lands.
- **Chapters** reuse the SCRIPT beat labels **in order**, but the times get filled in from the
  FINAL edit — leave them as `‹M:SS›` placeholders. The first chapter must be `0:00` (YouTube
  requires it) and YouTube needs 3+ chapters, each at least 10 seconds.
- **Standing footers** (My Stuff, Connect) are reused verbatim every time.
- Mark anything Ryan must supply as `‹TODO: …›` so it's obvious what's left to fill.

---

## Teleprompter version (read copy) — REQUIRED companion artifact

Ryan keeps each video in its own folder with two files: `‹Wn - Title› - Script.md` (the full
production doc above) **and** `‹Wn - Title› - Teleprompter.md` (read copy). Whenever you create
or update a script, produce/update the matching teleprompter.

The teleprompter is the **VO lines only**, cleaned for reading aloud:
- **Header note (use verbatim, every teleprompter):**
  > Read copy only — spoken words, no stage directions. Each block is tagged: **🎥 ON CAMERA** = talking head, look at the lens and perform; **🎙️ VOICEOVER** = read over screen-capture, you're not on screen. `* * *` marks a beat break (don't read it). Pause at the line breaks. Spoken code/symbols are spelled out the way you'd say them.
- **Camera indicator on EVERY block (non-negotiable):** tag each read chunk with **🎥 ON CAMERA**
  (talking head — what Ryan calls an "on-screen" section) or **🎙️ VOICEOVER** (over screen-capture),
  derived from that beat's `[SCREEN]` cue in the script. When the camera state changes *within* a
  beat (e.g. cold open: face → demo → face), split the chunk and re-tag — don't leave a block
  ambiguous. Rule of thumb from the on-camera style: framing / opinion / transition / recap =
  🎥 ON CAMERA; type-and-narrate demos, terminal, code, OST checklists = 🎙️ VOICEOVER.
- **Strip** all `[SCREEN]`/`[OST]`/director notes/code blocks/timestamps — read words only.
- **Spell out** code/symbols/URLs the way they're said: `block.json` → "block dot json",
  `--scope` → "dash-dash scope", `/mcp` → "slash-mcp", `developer.wordpress.org/news` →
  "developer dot wordpress dot org slash news".
- `* * *` between beats (matches the SCRIPT's beat breaks); blank lines between spoken paragraphs.
- VO wording must match the Script's VO exactly (same voice/anti-AI pass) — the teleprompter is a
  reformat, not a rewrite.
