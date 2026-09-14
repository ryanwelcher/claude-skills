# Ryan's YouTube Voice — Style Card

This is a distilled profile of how Ryan actually talks, derived from transcripts of his
livestreams/videos (see `voice-samples/`) plus his own description of his style. When
writing a script, match THIS — not generic "engaging YouTuber" voice. When in doubt,
re-read `voice-samples/excerpts.md` and mirror its rhythm.

> Note on the samples: the transcripts are livestreams, so they're looser and more
> banter-heavy than an edited tutorial. Mine them for **sentence-level voice** (rhythm,
> word choice, humor, how he explains things). Use the **open/close** patterns below for
> the macro structure of an edited video, NOT the rambly stream sign-offs.

## Who he's talking to
WordPress **developers** — competent engineers (comfortable with JS and PHP). Treated as
friends: warm, direct, second person, never talked down to. Each video's own `Audience:`
header line refines this (e.g. "block developers adding frontend interactivity",
"developers using Claude Code") — honor it for that video.

**Pitch developer-grade.** Per the channel strategy, the moat is the *credible,
real-architecture* version of these topics no one else is making. Go to mechanism level —
how it works under the hood (e.g. `InspectorControls` is a Slot/Fill that renders into the
sidebar slot; how block attributes serialize into the delimiter comment; what a function
actually applies) — not beginner hand-holding. Assume language fundamentals; explain
WordPress/block internals properly. An analogy can *frame* a concept, but always follow it
with the correct technical detail. When unsure if something's too basic, go deeper.

## Energy & register
- Conversational baseline with **bursts of high energy**. Off-the-cuff, not polished.
- Talks in short, punchy units. Fragments are good. Self-interrupts and course-corrects
  out loud ("So, what is this thing? This might be a good — maybe I shouldn't look at this").
- Rhetorical questions to himself and the viewer ("What is this thing? What do we got here?").
- Direct address and check-ins ("right?", "you know?").

## Open
- **Every video cold-opens** straight into the hook/problem (not "usually" — always), then a
  quick identity line — he's a **developer advocate at Automattic**. Don't append "and I
  build WordPress" / "I build WordPress for a living." Tighter than a stream.
- **The cold open opens on TALKING HEAD (his face, to camera)** — the first `[SCREEN]` cue is
  always `TALKING HEAD — Ryan to camera`. Deliver the hook to camera first; cut to
  screen-capture/b-roll only after the hook lands. Returning to face for the self-intro is a
  good bookend.
- **The self-intro is its own clean sentence** — "I'm Ryan Welcher, a developer advocate at
  Automattic." Never glue a lead-in onto the name ("So, I'm Ryan Welcher…" / "And I'm Ryan
  Welcher…"). And don't strand it as a lone dramatic beat — follow it immediately with a
  value-prop sentence (a NEW sentence) saying what you're about to show them: "I'm Ryan
  Welcher, a developer advocate at Automattic. And I want to show you my favorite little
  trick for…"
- **No reveal-pivot tags after a hook** — "That's a real thing now." / "And it's real." read
  as infomercial. After an imagined-scenario hook, just NAME the product and let that signal
  it's real. If a pivot is truly needed, keep it understated and self-aware.
- **Subscribe nudge (when used) leads straight in**: "Before we get into it, if you haven't
  already, hit subscribe and give the video a thumbs up." No "Quick one before we start:" /
  "Quick one:" dress-up.
- The **"Hey everybody, how's it going?"** greeting is his stream/live style — use it for
  livestream-flavored content, not tight edited tutorials.
- No throat-clearing, no "in today's video we're going to be taking a look at…".

## On-camera presence (talking head is the HOME BASE, not just bookends)
Ryan wants **a lot more on-camera** across every script. Treat **talking head as the default
lane** the video keeps returning to — model it on the WordPress.com videos (WND), where the
format is "talking head + the thing on screen" and his face is the through-line.
- **Open** on `TALKING HEAD — Ryan to camera` + the hook (always — see Open above).
- **Cut to screen-capture/code only for the demo itself**, then **cut back to TALKING HEAD**
  for: transitions between major beats, the "here's why this matters" framing, opinions/
  reactions, gotchas, and the recap/close. Don't leave long stretches that are screen-only.
- Practically: most beats should have a face moment. When laning a beat, ask "would he say
  this to camera or over the screen?" — framing/opinion/transition = to camera; type-and-
  narrate demo = over the screen. Put an explicit `[SCREEN: TALKING HEAD — Ryan to camera]`
  cue wherever he returns to face, so the edit is unambiguous.

## Close
- Quick recap, then his **standard sign-off**: **"Thanks for watching and I'll see you in
  the next one."** Keep it short; don't pad it.
- Older variants ("See you then, friends." / "Hope it helps. See you next time.") still
  read as him, but default to the "next one" sign-off above unless he says otherwise.
- Usually paired with a comment ask + subscribe nudge in the CTA beat.
- **Comment ask: keep it real and answerable.** Prompt something the viewer can actually
  answer from having watched, and **name the comments explicitly** ("let me know **in the
  comments** what you built and if you ran into any issues") — don't rely on an implied
  channel. DON'T invent unverifiable host claims to juice engagement — **never "I read every
  one"**, "I reply to all of them", etc. A plain "I want to see what you build" is fine.
  And make sure the ask matches the video — don't prompt for a detail the build wouldn't
  produce.

## Verbal tics (use naturally, do NOT stuff)
Frequencies from ~53k words of transcript, highest first:
`so` · `like` · `okay` · `going to` · `right` · `cool` · `actually` · `you know` ·
`kind of` · `basically` · `anyways` / `anyway` · `all right` · `let's`.

- Keep the **connective/cadence** tics: "So,…", "Okay, so…", "All right,…", "right?",
  "anyways", "cool", "the idea here is…", "the way I built this…".
- **Disfluencies (`um`, `uh`)**: these are huge in the spoken transcripts but are SPOKEN
  filler. In a word-for-word script, mostly leave them OUT. A rare "uh" or a trailing
  "…so, yeah" is fine for authenticity — don't litter them.
- **Watch any single emphasis word repeating across beats** — e.g. "whole" leaned on 5× in
  one draft. "That's the whole point, really." is approved and stays; vary the rest — trim
  to ~2–3 uses of any one emphasis word per script.
- **No sincerity-signalling adverbs** — "and honestly,…", "genuinely", "truly", "I'll be
  honest,…", "to be fair,…". Writing "honestly" in front of a claim is a written device for
  faking spoken candour; he just says the thing. Same family as the banned `genuinely`
  intensifier. If the sentence needs softening, use a real hedge — `kind of`, `sort of`,
  `pretty`, trailing `really` — or state the opinion flat: "I'm pretty happy to see this land."
- **North American spelling and idiom** — he's Canadian, not British. Write `color`, not
  `colour`; "figure out why", not "work out why". Watch for this drifting in on rewrites,
  and keep spelling consistent with the code being shown on screen.

## How he explains tech
- **Analogies to everyday things** ("it's like Saturday Night Live", "basically like a human").
- **Type-it-and-narrate**: describes what he's doing as he does it ("So the way I built
  this…", "what we have to do is basically kill…", "let's see what this does").
- Shows the thing, pokes at it, reacts in real time. Comfortable saying "I don't know what
  this is, let's find out."
- "under the hood" for what's happening internally. "the idea here is" to frame a concept.
- **Tool-neutral instructions.** When telling viewers to search their own code, don't assume
  their workflow ("grep for…", "every hit") — say "take a look through your editor code
  for…", "check your editor CSS for…", "every one you find." The audience is developers,
  but terminal vs editor search is their call.

## Humor (a core part of the voice — don't sand it off)
- Jokes **a lot**. Light, quick, woven in — not stand-up bits.
- **Heavy self-deprecation**: happy to call his own code crap ("that my code is crap.
  Basically…"), play up getting old, etc. Punch UP or at HIMSELF, never down.
- **Sarcasm** is welcome but only ever aimed at people he knows personally and clearly in
  good fun — NEVER mean, never at the audience's or a stranger's expense.
- Playful asides and bits ("there's jokes there, Terrence, there's jokes — but I'm too
  mature as an adult to make those jokes").
- **NO meme-y / elliptical internet quips or slang** — "free real estate", "who among us",
  "here's the receipts". If a joke needs the viewer to fill in a missing half or reads as
  trying-to-sound-hip, say it plainly and in first person instead: "and yeah, I've shipped
  a few of those."
- **NO whimsical bit-motifs for bugs** — personifying a bug as haunted/possessed/cursed is a
  writer's bit, not his reaction. He reacts with plain confusion/deadpan: "That makes no
  sense." / "What? Nothing about the block changed." / "The diff is two lines. That's it —
  two lines."

## Hard bans (makes him cringe — never write these)
- **"real talk"**, **"let's get real"**, and that entire family. He finds them stupid.
- Anything that sounds like a LinkedIn influencer or forced hype.
- **"near and dear (to my heart)"** for ANY item. Use **neutral enthusiasm** instead:
  "this one's a lot of fun", "I'm pretty excited about this one". Also don't over-tag an
  item's importance with a presenter cue ("one I really wanna slow down on") — just
  introduce it and talk about it.
- **Announce-the-feeling constructions** — "here's the part I love", "the bit I actually
  care about", "my favorite kind of X". He reacts to things; he doesn't pre-label his
  feelings about them. State the thing plainly and let a short blunt fragment or pointer
  carry the reaction: "Now watch this." / "And look —" / "And the fix? You delete code." /
  "that's the whole point, really".
- **"asterisk" as the word for a qualifier** — he says **"caveat."** And say it in a
  sentence with a verb ("There's one caveat here, and then I'll drop it."), never as a bare
  counted fragment ("One caveat.") or colon label ("Caveat:"). Same test for cousins like
  "one wrinkle" / "one gotcha".
- **Cost/price framing for effort** — "what it costs you", "what each one costs you". Reads
  salesy. Say plainly how much you have to write/do yourself, or just let the enumeration
  make the effort point on its own.
- **Corporate/PM framing** — "action item", "the status changed from X to Y", "the
  recommendation is now…". Say it conversationally as advice to the viewer: "this is the
  month it goes from 'keep an eye on this' to 'okay, actually go test your plugins.'"
- **Deadline-drama abstractions** — "ending on a schedule", "the clock is ticking", "the
  window is closing", "on a countdown". Press-release framing for a timeline. Say what's
  actually happening, plainly, and let the dates/releases carry the urgency: "And the last
  few releases have been closing that gap."
- **Audience-tag clichés** — "this one's for you", "you're in the right place". Pay off a
  "if you're a developer…" setup with a casual "stick around," or state who it's for as a
  flat sentence.
- **Unverifiable host claims** as engagement bait — "I read every one", "I reply to all of
  them" (see Close).
- **Fabricated next-video teases or metadata** — never invent "next week we'll cover X", an
  end-screen target, or factual header fields. Pull from the content plan or keep the CTA
  generic.

## Anti-AI tells (strip these every time — this is what makes it sound written-by-a-bot)
- ❌ "dive in", "delve", "unleash", "unlock", "supercharge", "game-changer", "robust",
  "seamless", "in this video we're going to explore", "without further ado",
  "let's get started", "buckle up".
- ❌ Over-signposting: "Firstly… Secondly… In conclusion…".
- ❌ **Label/colon openers and dangling counted-noun fragments** that announce a category
  instead of just saying the thing: "Assumption: you know JS and PHP", "Two honest ones.",
  "A couple of caveats:", "One important note:", "Three takeaways:". The family also includes
  **"X version:" lead-ins** ("Practical version —", "Short version:") and "here's the one
  thing to do right now:". You don't say a colon out loud, and you don't open with a count
  that points at nothing. Fold the label into a spoken sentence: "I'm assuming you know JS
  and PHP…", "And what that means in practice is…", "the one thing to do right now is…".
  A natural lead-in to a single point is fine; what's banned is the slide-label /
  announce-then-restate construction.
- ❌ **Telegraphic colon-speak** — VO lines that dropped their verbs/articles into shot-list
  shorthand: "Watch: tablet preview.", "Fixed block: updates. Broken block: doesn't
  flinch.", "Two blocks, one job: how wide is the canvas?". Restore the
  subject/verb/article: "Watch this — tablet preview. The canvas shrinks. The fixed block
  updates…", "Two blocks, and they've got one job — tell me how wide the canvas is."
  Deliberate punchy fragments stay ("No error. Just wrong."); what's out is the colon-label
  rhythm where a sentence lost its verb. Enumerations speak as "One — …" with a full
  clause, not "One: noun." And write setup-reversals as ONE complete conditional sentence
  ("If that sounds like a reason to wait, it's actually the opposite —"), not two clipped
  beats.
- ❌ **Stacked punch fragments (stutter-stop narration)** — three-plus clipped fragments in
  a row, especially in demo beats: "Status 200. Doing absolutely nothing." / "Iframed? Gone.
  Both of them." / "Masonry. Sliders. Lightboxes. Maps." One punch fragment per moment;
  everything around it keeps its verbs and connectors ("so", "and", "which", "right?") the
  way the transcripts flow. Spoken lists ride on commas ("Masonry, sliders, lightboxes,
  maps — a whole generation…"), not periods.
- ❌ Perfectly balanced, symmetrical sentences and tidy three-item lists everywhere.
- ❌ Em-dash-heavy "not only X but also Y" construction; relentless parallelism; stacked
  em-dash hooks and colon-lists ("an agentic expert: a senior dev at your disposal") — break
  them into short spoken sentences.
- ❌ Forced enthusiasm ("This is absolutely amazing!") and corporate hedging.
- ✅ Instead: uneven rhythm, fragments, a tangent, a self-deprecating aside, a real
  reaction. If a sentence sounds like a press release, rewrite it the way he'd say it out loud.

## Editing traps (process rules — when revising, not just writing)
- **Chat-edit drift**: after several rounds of iterating lines in chat, re-read the full VO
  out loud against this card — incremental tweaks accumulate toward press-release rhythm
  even when each single edit seemed fine.
- **Compression creates tells**: cutting a line for TIME can strip the verb and turn a
  spoken sentence into a banned slide-label ("One asterisk, and then I'll drop it." →
  "One asterisk."). When trimming, cut whole clauses or whole sentences — never the
  verb/predicate that makes a fragment speakable — then re-check the trimmed line against
  Anti-AI tells before calling it done.

## Refinement log
Corrections are recorded in `refinement-log.md` next to this card. **Do not read it to apply the rules**: every entry is already distilled into the sections above. To capture a new correction, update the relevant section above, then append a dated bullet to `refinement-log.md`.
