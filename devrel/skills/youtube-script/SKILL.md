---
name: youtube-script
description: |
  Write or audit a YouTube video script in Ryan's voice (conversational, funny,
  developer-to-developer, not AI-sounding). Use to draft a video script or turn an outline
  into one, or to audit or rework an existing script so it sounds like him.
---

# YouTube Script (in Ryan's voice)

Produce a complete, ready-to-record **production document** whose spoken lines sound like
Ryan actually talking. Two concerns, kept separate: the **format** comes from
`references/format-template.md`; the **voice** of the spoken (**VO**) lines comes from
`references/style-card.md`. The goal that overrides all others: the VO **must sound like
him, not like AI.**

## Step 0 — Load voice + format (REQUIRED, every time)

Before writing a single line:
1. Read `references/style-card.md` in full (the voice).
2. Read `references/format-template.md` (the document structure) — for write mode, and for
   audit mode if the script needs reshaping into the production format.
3. Read `references/voice-samples/excerpts.md` — curated verbatim excerpts (opens,
   type-and-narrate explanations, reactions, humor, closes) — to re-anchor on his rhythm.
   These are real, so mirror them. Do not read the full `.txt` transcripts in that folder to
   write a script (each is 15–20k tokens); they are source material for curating more excerpts.
   If the excerpts feel thin for a topic, say so in your hand-off so Ryan can add some.

Do not skip this even if the request seems small. The voice lives in the examples.

## Step 0.5 — Pick the mode

- **Write mode** — Ryan gives a topic/outline and wants a new script → follow Steps 1–4.
- **Audit mode** — Ryan pastes/points at an existing script (his from another tool, or one
  he was handed) and wants it checked/reworked for his voice → jump to **Audit mode** below.

If it's ambiguous which he wants, ask one quick question before proceeding.

## Step 1 — Get what you need

Confirm (ask only for what's missing — don't interrogate):
- **Topic / what the video teaches or announces.**
- **Key points or rough outline**, if Ryan has one. If not, propose a beat list first and
  get a thumbs-up before writing the full script.
- **Approx length / depth** (e.g. "quick 4-min tip" vs "15-min deep dive").
- **Open style**: standard "Hey everybody, how's it going?" or a cold open into the problem.
- **Any demos / code** he'll be showing, so the script can narrate them.
- **Series / content plan (standard intake — always ask):** before writing the CTA, end
  screen, or factual header fields, ask Ryan to **point you at the relevant cadence/plan
  entry or paste the row** (next video, target keyword, tier/type, footage source). His plan
  lives in his Obsidian "YouTube Growth" folder, which this skill can't read on its own — so
  ask every time rather than assume. If he says there's no plan or to keep it generic, use a
  generic CTA ("more coming — subscribe"). **Never invent a "next week we'll cover X" tease,
  an end-screen target, or metadata** — a fabricated next-video promise is a correctness bug,
  not a style choice.

## Step 2 — Write the full production document

Two separate concerns — keep them straight:
- **FORMAT / STRUCTURE → `references/format-template.md`.** Produce the full document in
  that shape: metadata header, `## 🎥 SCRIPT` with named (never timed) beats carrying
  `[SCREEN]`/`[OST]`/**VO**
  lanes and `> 🎯 / ✅ / ⚠️` notes, then `📦 PACKAGING`, `📝 YOUTUBE DESCRIPTION`,
  `✅ Pre-record checklist`, `🔀 Alt hooks`.
- **VOICE → `style-card.md`.** Only the **VO** (spoken) lines are written in Ryan's voice.
  Director notes, `[SCREEN]`, `[OST]`, and packaging are crisp and functional, not "in character."

Default output = the **full document** with `‹TODO: …›` placeholders for anything only
Ryan/his tools supply (keyword volume + competition, viDIQ scores, thumbnail reference
images, publish date, tier, vault `[[links]]`). Reuse the standing **My Stuff** / **Connect**
footers from the template verbatim.

Writing the **VO** lines (this is the voice-governed part):
- **Open** — usually a **cold open** straight into the hook/problem for an edited video
  (the "Hey everybody, how's it going?" greeting is the stream style; edited videos run
  tighter). Hook fast; never "in this video we're going to…".
- **Body** — teach/announce in his voice: **analogies**, **type-it-and-narrate**
  ("so the way this works…", "let's see what this does…"), short punchy sentences,
  fragments, rhetorical questions, woven-in humor and the odd self-deprecating aside.
- **Close** — quick recap then his standard sign-off: "Thanks for watching and I'll see you
  in the next one." (Older variants "See you then, friends." / "Hope it helps. See you next
  time." still read as him, but default to the "next one" sign-off.)

Housekeeping:
- **NEVER put timestamps on beats.** Name and order them; don't time them. Any number is a
  guess that won't survive the recording or the edit, and a wrong one lies about pacing. If a
  beat runs long, say that in words in a `> 🎯` note instead of implying a budget with a clock.
- **Chapters** in the description reuse the SCRIPT beat labels in order, with `‹M:SS›`
  placeholders — Ryan times them off the FINAL edit. First chapter stays `0:00`.
- Put any checkable claim in a `> ✅ fact + source` note and anything to verify in `> ⚠️ CONFIRM:`.

## Step 3 — Anti-AI pass (REQUIRED before showing him)

Re-read every **VO** line against the **"Anti-AI tells"** and **"Hard bans"** sections of
the style card and rewrite anything that trips them. Specifically hunt for and kill:
- "dive in / delve / unleash / supercharge / without further ado / let's get started"
- "real talk", "let's get real"
- press-release sentences, forced enthusiasm, over-signposting, relentless parallelism,
  tidy symmetrical lists.
If a line wouldn't survive him reading it out loud, fix it.

## Step 4 — Deliver + refine

- Hand over the script. Briefly note any spots you're unsure about or that need his demo.
- When he corrects a line because it doesn't sound like him, **add the rule to the relevant
  section of `references/style-card.md` and append a dated bullet to
  `references/refinement-log.md`** so the voice sharpens over time. This feedback loop is the
  point — use it.

## Audit mode (review an existing script)

**REQUIRED SUB-SKILL: use `sounds-like-me`** — it owns the audit workflow (findings →
approval → fix in place → script/teleprompter sync → refinement-log routing). Do not run a
separate audit process here; invoke that skill and follow it.

The only youtube-script-specific addition: if the doc isn't already in the production
format, note that it could be reshaped per `references/format-template.md`, and offer to do
so after the voice pass.

## Quick reference (the non-negotiables)
- Format from `format-template.md`; voice (VO lines only) from `style-card.md`. Keep them separate.
- Audience = developers, treated as friends. Warm, informal, never talks down.
- Funny, heavily self-deprecating, sarcastic only in good fun and never at the viewer.
- Edited videos usually **cold-open**; default sign-off is "Thanks for watching and I'll see
  you in the next one." The "Hey everybody, how's it going?" greeting is the stream style.
- Strip AI tells and the cringe phrases (esp. "real talk"). When unsure, sound MORE like the excerpts.
