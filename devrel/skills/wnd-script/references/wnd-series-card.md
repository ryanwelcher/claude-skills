# What's New for Developers — Series Voice Card (DELTA on top of the shared style card)

This is a **delta**, not a replacement. The core voice — who he's talking to, energy, humor,
hard bans, anti-AI tells — lives in the shared style card. **Read that first.** It is the single source of
truth for "this is Ryan," and any correction made there flows to this series too (that's the
whole point — no drift). *(Path from this file: `../../youtube-script/references/style-card.md`.)*

This file only captures what's **different** about the *What's New for Developers* (WND) series:
a monthly WordPress.com video where Ryan walks through that month's "What's new for developers"
post on the WordPress Developer Blog. Format is **talking head + the article on screen** — no
overlays, no on-screen text, no demos. Just Ryan talking through the post.

Derived from real episodes in `wnd-voice-samples/` (Oct 2025 – Jan 2026). When in doubt,
re-read `wnd-voice-samples/excerpts.md` and mirror it.

---

## The big structural differences vs. the personal channel

| | Personal channel (style-card default) | **WND series (use THIS)** |
|---|---|---|
| **Open** | Cold open straight into the hook | **Branded greeting open** (see below) — NOT a cold open |
| **Identity** | "I'm a developer advocate and I build WordPress" | "developer advocate at **Automattic**" |
| **Close** | "See you then, friends." | **"That's it for [month]… thanks for hanging out… have a good one."** — NOT the "friends" sign-off |
| **Register** | Mechanism-deep, type-it-and-narrate | **Report-and-point-to-the-article** roundup; lighter on internals |
| **CTA** | Comment-driven ("tell me in the comments") | Standard **thumbs-up + subscribe** nudge (often at open AND close) |
| **Scope** | Covers its topic fully | **Explicitly can't cover everything** — repeatedly sends viewers to read the full post |

Everything else (humor, self-deprecation, "go check it out / play around with it," fragments,
"so / okay / right," the dev-to-dev warmth) is the **same** — pull it from the shared style card.

---

## Open (this is a fixed convention — don't cold-open this series)

The WND open has a consistent shape. Hit these beats, in his voice:

1. *(optional)* a quick **seasonal/topical line** if it fits the month — e.g. "Happy New Year!
   It's 2026 and I'm really excited to see what WordPress has in store for us…", or a holidays
   nod in December. Skip if nothing fits; don't force it.
2. **The branded greeting** — some variant of:
   *"Hey everybody, Ryan Welcher here again with another edition of What's New for Developers."*
3. **What the series is** (he assumes new viewers every month):
   *"If you're not familiar with What's New for Developers, it's an article that comes out
   monthly on the Developer Blog — you can find it at developer.wordpress.org/news — and it
   outlines all the work that's been done in the past month across the WordPress and Gutenberg
   projects."*
4. *(optional, common)* an **early subscribe/like nudge**:
   *"Before we get started, if you haven't already, go ahead and subscribe to this channel and
   like this video for more content like this."*
5. **Into it** — name the month and go:
   *"So let's take a look at what's new for developers, [Month, Year]."*
6. *(common)* a **scope disclaimer** — set the expectation that it's a roundup, not exhaustive:
   *"As always, I may not have time to cover everything, so I encourage you to go read the
   article and check out the table of contents — there's a lot of great stuff in here."* Some
   months he flips this into "I'm going to do things a little differently and only call out a
   few top-level items and leave the rest for you to read."

> Vary the wording each month — these are patterns, not a script to paste. But the *beats* are
> stable: greeting → what it is → (sub nudge) → name the month → (scope disclaimer).

---

## Body — register & how he moves through it

- **It's a guided walkthrough of the article — in the article's exact order.** Sections *and*
  items, top to bottom, no reordering ever (skipping items is fine; moving them is not). He
  **names the sections as he moves**: "Moving on to the plugins and tools section…",
  "Under themes…", "The Playground section…", "And finally, the resources section." The
  on-screen article scrolls to match.
- **Report-and-point, lighter on mechanism.** Per item, the beat is usually:
  *what it is → what changed (often a quick "previously X, now Y") → why it matters / who it's
  for → go look at it.* He'll give real context ("previously you had to pick one or the other…
  now you can combine both"), but this is a roundup — it does **not** go as deep into internals
  as a dedicated personal-channel video. Don't over-engineer the mechanism here.
- **Constantly sends people to the source.** "Go and read the article," "the links are in the
  article," "there's documentation and sample code in the article," "check out the table of
  contents." This is a defining habit of the series — keep it.
- **Calls action items honestly.** When something's experimental: "keep in mind it's still
  experimental, so you have to enable it in the Gutenberg experiments screen." When a release
  affects people: "go and test your stuff accordingly," "keep an eye on that one."
- **Credits people by name.** Contributors and Developer Blog authors get named — Nick Diego,
  Justin Tadlock, Troy Chaplin, etc. Keep this when the article names them.
- **Playground enthusiasm — but the "voodoo magic" payoff is RETIRED (2026-07-20).** Playground
  still gets genuine excitement when it comes up. But **do NOT use "if you haven't played with
  Playground yet, you have to — it's voodoo magic, there's no other way to explain it."** Ryan
  said it every single episode and retired it. React to whatever the specific Playground item
  actually is instead — and don't just swap in a NEW fixed catchphrase to repeat. ("Playground
  is one of my favorite things" is fine used sparingly and varied.)

## WND signature phrases (use naturally — these are his, mine the samples for more)
- "This is a really cool one." / "This one's pretty exciting (for block developers)." /
  "This one's a pretty big deal." / "This is huge — a huge deal for…"
- "Go and check it out." / "Go and have a look." / "Play around with it (and see what you
  think / come up with)." / "I'd highly recommend going and having a look."
- "All that good stuff." / "All sorts of great stuff." / "All kinds of really great things."
- "This one's a bit in the weeds, but…"
- "Keep an eye on that one." / "Test your stuff accordingly."
- "This is going to remove a lot of the need for [custom CSS / custom blocks]."
- "Definitely go and check this out." / "Now's a good time to go and have a look."
- Self-deprecating framing of the whole video — **VARY it, don't reuse verbatim (2026-07-20).**
  The *sentiment* (thanking people for hanging out while he geeks out) is core; the exact wording
  should change episode to episode. "watch me ramble on about all this great developer stuff" is
  ONE option, not the default — rotate it: "geek out about all this developer stuff," "nerd out
  over the latest WordPress updates," "dig into all this with me." Ryan flagged the same line
  every video as too repetitive.
- Occasional personal aside tied to an item (the Flash/ActionScript nostalgia, "the other day
  I connected the details block to a piece of post meta"). Keep these light and real; one or two
  an episode. **Do NOT use "near and dear" / "near and dear to my heart"** — Ryan banned it for
  any item (2026-07-20); reach for neutral enthusiasm instead ("this one's a lot of fun", "I'm
  pretty excited about this one"). See the shared style card's Hard bans.

---

## Close (fixed convention — NOT the "friends" sign-off)

Hit these beats:
1. **"That's it" for the month:** *"Well, that's it. That's the end of What's New for
   Developers for [Month, Year]."*
2. **Thanks + self-deprecation (VARY the wording each episode — 2026-07-20):** thank people for
   hanging out — *"Thanks again for hanging out with me"* — plus a self-deprecating nod to the
   format. **Rotate the self-deprecating phrase; don't reuse "ramble on about all this great
   developer stuff" every time** (Ryan flagged it as the same line every video). Keep the
   sentiment, change the words: "…for letting me geek out about all this developer stuff,"
   "…for hanging out while I nerd out over the latest WordPress updates," etc.
3. *(sometimes)* **identity restated:** *"My name's Ryan Welcher, developer advocate at
   Automattic."*
4. **Subscribe/thumbs-up nudge:** *"If you haven't already, please give this video a thumbs up
   and subscribe to the channel — so we know we're doing stuff you actually want to see"* /
   *"…'cause we'll be doing more content like this on a regular basis."*
5. **Forward-looking:** *"I look forward to seeing you all next month for [Next Month, Year]."*
6. **Sign-off:** *"Thanks a lot. Have a good one."* (or "Thanks again for watching.")
   Seasonal warmth when it fits (holidays, New Year). **Never** "see you then, friends" — that's
   the other channel.

---

## Quick reference (WND non-negotiables)
- **Greeting open**, not a cold open. **"Have a good one"**, not "friends."
- Identity = **developer advocate at Automattic**.
- It's a **roundup that points at the article** — name the sections, send people to read it,
  don't pretend to cover everything.
- Same humor, same warmth, same anti-AI/hard-ban rules as the shared style card.
- Talking head + article on screen. No overlays, no OST, no demos.

## Refinement log (WND-specific)
Corrections are recorded in `refinement-log.md` next to this card. **Do not read it to apply the rules**: every entry is already distilled into the sections above. To capture a new correction, update the relevant section above, then append a dated bullet to `refinement-log.md`.
