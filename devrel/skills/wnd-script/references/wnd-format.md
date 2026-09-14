# WND Teleprompter Format (structure only)

The **shape** of a *What's New for Developers* teleprompter. Use it for STRUCTURE ONLY. All
spoken content comes from the voice — the shared style card + this series' delta card
(`wnd-series-card.md`) + the anti-AI pass. Format here, voice there.

This series is **teleprompter only** — clean spoken **read copy** Ryan reads to camera. No
director script, no `[SCREEN]` cues, no `VO:` labels, no `> ✅ / ⚠️` notes, no packaging,
description, metadata, or thumbnails. **Only the words he reads out loud.** (Fact-checking and
pre-record confirmations still happen — they go in the hand-off message to Ryan, not in the file.)

**Read-copy conventions:**
- **Short blocks, one thought each,** separated by blank lines — so it's easy to read off a
  prompter. Break where he'd pause.
- **`* * *` on its own line** marks a section break (he doesn't read it).
- **Spell things out for reading aloud:** URLs as "developer dot wordpress dot org slash news";
  soften code identifiers so they read naturally ("use-resize-canvas", "gutenberg-react-19",
  "current-color" rather than `fill="currentColor"`).
- **Name the article's sections in the spoken copy** as he moves through them ("Okay, into the
  plugins and tools section…", "Alright, themes.").
- **No timestamps.** Sections are ordered, never timed.

---

```
# What's New for Developers — ‹Month Year› (Teleprompter)

> Read copy only — spoken words, no stage directions. `* * *` marks a section break (don't read it). Pause at the line breaks.

---

‹seasonal line if it fits› Hey everybody, Ryan Welcher here again with another edition of What's New for Developers.

‹what the series is — an article that comes out monthly on the Developer Blog, at developer dot wordpress dot org slash news, covering everything that landed across WordPress and Gutenberg in the past month.›

‹optional subscribe/like nudge — lead straight in, e.g. "Before we get into it, if you haven't already, hit subscribe and give the video a thumbs up."›

So, ‹Month Year› — ‹scope disclaimer: way more in here than I can get to, so I'm gonna hit the big stuff and send you to the article for the rest.›

* * *

‹First section — name it, then walk its items. Per item: what it is, quick previously-X-now-Y, why it matters / who it's for, go look at it. Send people to the article often.›

* * *

‹… more sections, in the article's own order: Highlights → Plugins & Tools → Themes → Playground → (Performance) → Resources/News. Name each section as you get to it. Pace fast on small items; give the marquee ones a little more room.›

* * *

‹CLOSE — "that's it for [Month Year]" + thanks for hanging out / ramble aside + (developer advocate at Automattic) + thumbs-up & subscribe nudge + see you next month + "Thanks a lot, and have a good one."›
```

---

## Notes for filling this in
- **Everything here is voice-governed.** Every spoken block goes through the shared style card +
  `wnd-series-card.md` + the anti-AI pass. There are no stage-direction lanes to keep neutral —
  the whole file is read copy.
- **⛔ Follow the article's order exactly — sections AND items, top to bottom.** The video mirrors
  the post: same sections in the same order, same items in the same order inside each section.
  Never reorder for pacing, emphasis, or narrative. **Skipping is the only allowed deviation** —
  drop items in place when covering only the top stuff, and keep the rest in article order.
  Name the sections as he moves; the on-screen article scrolls to match (that scrolling is the
  editor's job, not something the teleprompter states).
- **NO timestamps. Ever.** Sections are named and ordered, never timed. **Episode length** is
  still worth aiming at — WND runs ~3.5–9.5 min depending on how much of the post is covered —
  but that's a target for the whole thing, and it belongs in the hand-off message if a section
  runs long, not in the file.
- **No packaging / description / metadata. No `[SCREEN]` cues or `> ✅ / ⚠️` notes.** Teleprompter
  only — just the words he reads.
