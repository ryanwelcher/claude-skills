I've drafted the description, but the transcript has a big hole. From **~05:00 to ~40:15** Whisper got stuck repeating one line ("I'm going to add a couple more things", 1,050 times). About 35 minutes of the stream, probably the main Studio Code demo with Antonio, came through with no usable content. A second, smaller loop ("yeah, yeah, yeah") covers roughly 44:30–47:50.

The skill says to run transcription only once and not to guess at content, so I didn't make up chapters for that stretch. I put a single broad chapter at `04:00` instead. Its label comes from what the two of them refer back to later, around 41:00–42:00: the menu and button changes, and the agentic UI. Check that label against the actual recording before you publish.

**Suggested title:** WordPress Studio Code with Antonio: Annotate, Agentic UI & Liberate - Live Stream

I only have "Antonio" from the transcript, and his surname never comes up. I also left the date off the title because I can't tell it from the file.

```
Antonio joined me on the stream to show off Studio Code, the AI agent that lives inside WordPress Studio, and to settle once and for all that no, it's never getting merged into core. We poked at Annotate (click the thing, say what you want, the agent does it), watched Sonnet draw its own SVG because we didn't have an image handy, and found out Studio finally has a Linux build. Somebody tell the conference crowd.

Also in here: the agentic UI and the new /liberate command, which turns a non-WordPress site into a WordPress one. I'm already planning a stream around it, and I'm going to harass Jamie Marsland into a speed build rematch. Last time I was the "not AI" side and I got destroyed, so what could go wrong?!

00:00 What Studio Code is (and why it'll never be in core)
02:00 One agent for all your sites vs. AI inside every site
04:00 Studio Code demo with Antonio: menus, buttons & the agentic UI
40:00 The craziest thing it's done & the Studio repo
42:00 Annotate one more time: animations & an image block
48:00 Skills, MCP & a Sonnet-generated SVG
50:00 Studio on Linux (and Windows)
52:00 What's next: agentic UI & /liberate
54:00 Hybrid themes, Shopify to Woo & managing expectations
56:00 Wrap-up

Connect:

https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

Projects:

👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/

#wordpress #wordpresstutorial #coding #customblocks #javascript #php #gutenberg #ai #livestream
```

- **Links:** as you asked, I left out the links mentioned in the recording, including the Studio repo URL shared in chat and the Studio download page.
- **Hashtags:** I added `#ai` to the base set, the same as your recent Studio and AI streams.
- **Chapter times:** the timestamps are from the raw recording. You mentioned on stream that you'll cut out technical glitches before uploading. If those edits shorten the video, the chapter times will shift.
- **Reference-fetch script:** `fetch-recent.sh` printed all five reference descriptions, then exited with `(eval):1: == not found`. That's a zsh error in the script, not a missing dependency. You'll probably want to fix it.