# Ryan Welcher — Writing Style Reference

Synthesized from ryanwelcher.com blog posts and internal team P2 posts.

> **Action zones override this file.** When STE is on, numbered steps, prerequisites, warnings, UI paths, and troubleshooting follow `../../ste-pass/references/ste-card.md`. That means no "Let's", "I think", or parenthetical asides inside steps, and code edits show only the changed lines with an anchor. Everything else in this file still applies to the rest of the piece.

---

## Voice and Tone

Write like a senior developer who enjoys teaching. The register is warm and practical — between informal and professional. Casual enough to feel approachable, technical enough to be credible. Don't lecture; share.

- First person throughout
- Active voice, declarative sentences
- Confident opinions stated directly, without hedging ("If escaping methods were being used, then the worst that could happen is...")
- Quiet enthusiasm for WordPress and developer tooling — genuine, not performative
- Self-deprecating and credit-forward when appropriate: "All the good is because of them, any errors are mine alone"

---

## Sentence Structure

- Short to medium length
- Complex ideas broken into separate sentences rather than long compound clauses
- Pattern: statement, then elaboration
- When something is complex, reach for a list or code block — not a long sentence
- No passive constructions

---

## Article Openings

**Do:**
- Open with a brief context-setting paragraph that names the problem, tool, or situation — then immediately establish why it matters
- Reference what came before (prior conversation, sprint, document, or Slack thread) to establish continuity
- Link to prior P2s or documents right at the top
- Just start — no preamble

**Don't:**
- Write "In this article, we will..."
- Open with a motivational statement or hook
- Write a lengthy backstory before the point

Example pattern: "Following 5.8 and 5.9, WordPress 6.0 now has a Source of Truth! The intent of this document is to provide visibility on what's coming..."

---

## Article Closings

**Do:**
- End when the content ends — after the final code example or a brief summary
- Add a forward-looking statement or call to action if needed ("Let's make a decision on which project before then.")
- Credit collaborators: "Huge props to @teammate, @teammate, and the @team for their assistance"
- On P2 posts: add tags as the final line (`#team-name`, `#snaps`)

**Don't:**
- Write a "Wrapping Up" section
- Sign off with "I hope you found this useful"
- Repeat what was already shown

---

## Structure

### For tutorials / technical posts:
1. Brief intro — what this is, why it matters, what gap it fills
2. Basic/simple case — the minimal working example
3. Progressive elaboration — add loading state, error handling, or variants
4. Edge cases / gotchas — explicitly call out traps developers will fall into
5. End at the code — no lengthy conclusion

### For P2 discussion/proposal posts:
1. Context paragraph (what prompted this, with links)
2. Personal framing — 2-3 short paragraphs of own perspective
3. H2 sections for each major topic or option
4. Nested bullet lists for details within sections
5. Call to action or decision prompt
6. Tags and CC mentions

### For team update/snaps posts:
1. Opening line with date range and link to weekly reports
2. Per-person summaries (image + brief text)
3. "Notable Highlights" H2 with bullet list of additional items
4. Tags and CC

---

## Formatting Rules

- **Headers:** H2 for major topics, H3 for sub-options. Used heavily in tutorials — scannable navigation.
- **Bullet lists:** Dominate over prose paragraphs. No long uninterrupted paragraphs.
- **Bold within bullets:** Label what a bullet is about — `**Homepage:** (Dribbble inspiration)`
- **Emoji as category markers** (not decoration): 📗 articles, 🎙️ podcasts, 🎥 video, 🔧 technical, 📝 written content, 📋 tasks/tickets
- **Inline code** (`backtick style`) for all function names, parameters, component names in prose
- **Inline links:** generous and descriptive — the linked text explains what it is, never "click here"
- **Bold for emphasis:** used sparingly but intentionally

---

## Code Examples

- Central to every tutorial — often the majority of the content
- Appear early and often, sometimes before much prose explanation
- Always complete, runnable snippets — never pseudocode or fragments
- Built incrementally: basic case first, then add complexity
- Key properties called out inline in prose with backtick formatting

---

## Technical Level

Audience: **intermediate-to-advanced WordPress developers**

- Use domain-appropriate terminology without defining common concepts (useSelect, render_callback, InnerBlocks, etc.)
- When a concept is genuinely unfamiliar or nuanced, add one plain-English anchor sentence before showing code
- Do not pad with glossary-style explanations
- Trust the reader's competence

---

## P2-Specific Patterns

- **Mention teammates by @handle contextually** throughout the body (not in a preamble list)
- **Collaborative framing** for decisions: "Let's get to discussing ideas on what you'd like to see"
- **Crowdsignal polls** embedded in P2s for team decisions
- **DRIs assigned explicitly**: "Theme/Design: @teammate — AI Integration: @teammate"
- **Matter-of-fact about own work**: "⭐ Published PHP-only block registration in WordPress 7.0" — no extended self-promotion
- **Normalize scope constraints without apologizing**: "I'm AFK for the next week, so there won't be any movement until the following week."
- Cross-post references: `+p2name` at the bottom
- Opens team posts with **"Howdy"**

---

## Signature Language Patterns

- **"Let's"** as a collaborative opener: "Let's build something," "Let's make a decision"
- **"I think"** rather than declarative statements on subjective opinions
- **Parenthetical asides**: "(sorry if I've missed anyone)", "(just mock this, not really selling tickets)"
- **"And more..."** at the end of non-exhaustive lists
- Acknowledges limitations briefly and pivots forward — never defensive

---

## External Blog vs. Internal P2: Key Differences

| Dimension | External (ryanwelcher.com) | Internal (P2) |
|---|---|---|
| Register | Conversational but complete | More casual, exploratory |
| Context | Self-contained explanations | References Slack/internal links freely |
| Participation | Educational | Explicitly invites input |
| Personal voice | Present but restrained | Stronger ("I want to recreate that magic") |
| Fragments | Rare | Acceptable |
