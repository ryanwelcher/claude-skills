---
name: wnd-script
description: |
  Write the teleprompter read copy for an episode of Ryan's monthly "What's New for Developers"
  (WND) video, walking through that month's Developer Blog post in his voice. Use to write or
  script a WND episode, a What's New for Developers video, or a monthly developer-news roundup.
---

# What's New for Developers — Teleprompter (in Ryan's voice)

Produce a **teleprompter only** — clean, spoken **read copy** Ryan reads to camera — for an
episode of the monthly *What's New for Developers* series on WordPress.com. The episode is a
**talking-head walkthrough of that month's Developer Blog post** — Ryan on camera, the article
on screen, no overlays and no demos. The goal that overrides all others: every line **must
sound like him, not like AI** — and like the *WND series specifically*, which opens and closes
differently from his personal channel.

> **Teleprompter only — one file.** This series used to ship a director "script" (with `[SCREEN]`
> cues, `**VO:**` labels, and `> ✅ / ⚠️` notes) alongside the read copy. It no longer does. The
> only deliverable is the teleprompter: spoken words, nothing he doesn't read out loud. No
> `[SCREEN]` directions, no fact/confirm notes in the file. Fact-checking and pre-record
> confirmations still happen — they live in your hand-off **message** to Ryan, not in the file.

Two concerns, kept separate:
- **VOICE** = the shared style card **+** the WND series delta card.
- **FORMAT** = `references/wnd-format.md` (teleprompter read copy; talking head + article on screen).

## ⛔ Hard requirement — the source article (do this before anything else)

The month's "What's new for developers" Developer Blog post is the **source of truth and is
absolutely required.** The entire teleprompter is a walkthrough of that specific article.

- **If Ryan did not provide the post URL, STOP and ask for it.** Do not start writing, do not
  load voice, do not propose an outline — ask for the link first.
- **Fetch and read the actual post.** Build the read copy only from what's in it.
- **Never invent, infer, or remember content.** No items, features, version numbers, function
  names, contributor names, links, or "what's new" claims that aren't in the fetched article.
  If you can't verify it against the post, it doesn't go in the teleprompter — raise it in your
  hand-off message instead. Writing WND content without the article in hand is a correctness
  bug, not a style choice.

## Step 0 — Load voice + format (REQUIRED, every time)

Before writing a single line, read **all** of these:
1. **`../youtube-script/references/style-card.md`** — the shared core voice. This is the single
   source of truth for "this is Ryan" and is intentionally shared with the `youtube-script`
   skill so the voice never drifts between them. Read it in full.
2. **`references/wnd-series-card.md`** — the WND **delta**: the series-specific open, close,
   identity, register, and signature phrases that differ from the personal channel. Read in full.
3. **`references/wnd-format.md`** — the teleprompter document structure.
4. **`references/wnd-voice-samples/excerpts.md`** — curated verbatim lines from real WND episodes
   (greeting, scope disclaimer, section transitions, report-and-point items, reactions, close).
   Mirror their rhythm, especially the open and close.

Do not skip the excerpts. The series voice lives in them. The full `.txt` transcripts in that
folder are source material for curating excerpts — do not read them to write an episode.

## Step 1 — Get what you need

Confirm (ask only for what's missing — don't interrogate):
- **The source post (REQUIRED — see the hard requirement above)** — the URL of the month's
  "What's new for developers" article. If it's missing, **ask for it and wait** before doing
  anything else. Once you have it, fetch/read it and pull every main item. Everything in the
  read copy comes from this article and nothing else.
- **Which month/year** the episode covers (usually obvious from the post).
- **Length / coverage depth** — WND episodes run ~3.5–9.5 min. Does he want to cover everything
  or call out only the top items and send the rest to the article? (Both are normal for the
  series; the open's scope disclaimer should match the choice.)
- **Any seasonal hook** for the open (New Year, holidays, a major release like a new WP version).

## Step 2 — Write the teleprompter

- Produce the document in the shape of `references/wnd-format.md`: a title line, the standing
  "read copy only" header note, then spoken **read copy** in short blocks separated by blank
  lines, with `* * *` on its own line marking each section break. **No `[SCREEN]` directions, no
  `VO:` labels, no `> ✅ / ⚠️` notes, no packaging/metadata — only what he reads aloud.**
- **⛔ ORDER IS NON-NEGOTIABLE. The teleprompter follows the article top to bottom — always.**
  Same section order, and **same item order inside each section**, exactly as the post has it.
  He's reading the article on screen while he talks; if the copy jumps around, the recording
  and the edit fall apart. So:
  - Never reorder sections or items, for any reason — not to "lead with the strongest item,"
    not to group related things, not for pacing, not for a better narrative arc.
  - Never merge two sections, and never split one item's coverage across two places.
  - Cutting is the *only* allowed deviation: if he's covering just the top items, **skip**
    items in place and keep everything you do cover in the article's order. Say so in the
    open's scope disclaimer and send the rest to the article.
  - If the article's order genuinely reads badly out loud, keep the order anyway and flag it
    in your hand-off message — it's his call, not yours.
- **Name the sections in the spoken copy** as he moves ("Okay, into the plugins and tools
  section…", "Alright, themes.") — Highlights → Plugins & Tools → Themes → Playground →
  Performance → Resources/News, or whatever sections and order the post actually uses.
- **Open** with the branded greeting beats (NOT a cold open) and **close** with the WND
  sign-off ("that's it for [month]… have a good one") — both per `wnd-series-card.md`.
- Write in his voice: report-and-point register, real context per item, send people to the
  article, the WND signature phrases, woven-in humor and self-deprecation. Credit contributors
  the post names.
- **Break lines the way he'd pause** — short blocks, one thought each — so it reads easily off a
  prompter. **Spell things out for reading aloud:** URLs as "developer dot wordpress dot org
  slash news"; soften code identifiers so they read naturally ("use-resize-canvas",
  "gutenberg-react-19", "current-color" instead of `fill="currentColor"`).
- **NEVER put timestamps on beats.** Name and order the sections; don't time them. Any number is
  a guess that won't survive the recording or the edit. Aim at the episode length as a whole
  (~3.5–9.5 min); if a section runs long, that's a note for your hand-off message, not the file.

## Step 3 — Anti-AI + voice pass (REQUIRED before showing him)

Re-read every spoken line against the **"Anti-AI tells"** and **"Hard bans"** sections of the
shared style card AND the rules in the WND delta card — those cards are the source of truth for
the criteria; don't work from memory or from a summary. (Their refinement logs are already
distilled into those sections; don't read the logs.) In particular:
- Kill the AI tells, the hard bans, and the label/colon openers the style card lists (you don't
  say a slide label out loud).
- Confirm the **open is the branded greeting** (not a cold open) and the **close is the WND
  sign-off** (not "friends") — getting these wrong is the #1 way a WND teleprompter reads as
  off-series.
- Confirm the **article's order** survived — sections and items, top to bottom (see Step 2).
- Confirm the identity line says **developer advocate at Automattic**.
If a line wouldn't survive him reading it out loud, rewrite it.

## Step 4 — Deliver + refine

- Hand over the teleprompter. In your **message** (not the file), briefly flag anything to verify
  before recording — version numbers, dates, anything state-dependent — and any line you're
  unsure reads as him. (These used to live in `> ⚠️ CONFIRM:` notes in the old script file; now
  they go in the hand-off so the read copy stays clean.)
- When he corrects a line: if it's **series-specific**, add the rule to the relevant section of
  `references/wnd-series-card.md` and append a dated bullet to `references/refinement-log.md`.
  If it's a **core-voice** correction (true on any channel), do the same in the shared
  `../youtube-script/references/style-card.md` and its `refinement-log.md` instead, so both
  skills benefit. This routing keeps the voices from drifting.

## Audit mode (review or rework an existing WND teleprompter)

If he hands you a teleprompter that already exists — his own draft, an older episode, or one
you wrote in a previous session — and asks for a voice pass, a review, or a rework:

**REQUIRED SUB-SKILL: use `sounds-like-me`** — it owns the audit workflow (findings →
approval → fix in place → refinement-log routing). Do not run a separate audit process here;
invoke that skill and follow it. It already knows to read the shared `style-card.md` plus this
series' `wnd-series-card.md` for WND files.

The only wnd-script-specific additions to flag while auditing:
- **Article order.** If you have the source post, check the teleprompter still follows it top to
  bottom — sections *and* items. Out-of-order copy is a finding, same as an off-voice line.
- **Format drift.** If the file still carries the retired director-script furniture (`[SCREEN]`
  cues, `**VO:**` labels, `> ✅ / ⚠️` notes, packaging/metadata), note that it should be reshaped
  to clean read copy per `references/wnd-format.md`, and offer to do it after the voice pass.

## Quick reference (the non-negotiables)
- **The source post URL is REQUIRED.** No link → ask for it and stop. Build the read copy only
  from the fetched article; never invent items, versions, names, or links that aren't in it.
- **Teleprompter only — one file.** Clean spoken read copy: no `[SCREEN]` directions, no `VO:`
  labels, no fact/confirm notes, no packaging/description/metadata. Verifications go in the
  hand-off message.
- Voice = shared `style-card.md` (core) **+** `wnd-series-card.md` (series delta). Format =
  `wnd-format.md`. Keep them separate.
- **Branded greeting open**, **WND sign-off close** ("have a good one"), identity = **developer
  advocate at Automattic**.
- It's a roundup that **points at the article** — name the sections, send people to read it.
- **Follow the article's order exactly** — sections *and* items, top to bottom. Skipping is
  allowed; reordering never is.
- Strip AI tells, hard bans, and label/colon openers. When unsure, sound MORE like the WND excerpts.
- **Auditing an existing teleprompter → use `sounds-like-me`**, not a hand-rolled review.
