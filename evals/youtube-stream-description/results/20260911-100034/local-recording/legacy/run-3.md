I've drafted the description, but most of the middle of the recording has no usable transcript, so the chapter list has a hole in it.

**The problem:** from about 04:30 to 40:30, the transcription just repeats "I'm going to add a couple more things" over and over. That's a known Whisper failure (it gets stuck in a loop, often on quiet or music-only audio), not what was actually said. That's roughly 36 of the 58 minutes. The only hint about that stretch comes later: Antonio says "we changed and improved the menu before and the buttons" and that he "should have saved the agentic UI for this moment". So there was a live Studio Code demo in there, but I don't know what happened when. I covered that span with one broad chapter (`06:00`) instead of making up detail. The skill says to run transcription only once, so I didn't re-run it.

A few other things to know:
- **Guest:** the transcript only gives "Antonio" from the Studio team, so the description uses his first name only.
- **Title:** I'd suggest *"WordPress Studio Code, Annotate & Liberate with Antonio - Live Stream"*. Add the date yourself, because the recording doesn't say it.
- **Links:** the Studio repo and the Studio download page both came up on the stream. I left them out as you asked.

```
Antonio from the WordPress Studio team joined me to show off Studio Code, the WordPress-centric AI agent that lives right inside your local dev environment. We started by clearing up a big one from chat (no, this is never going into core — it's a desktop tool, like MAMP is), and then, despite my setup falling apart on me audio-wise, we got Studio Code building stuff.

The highlight for me was Annotate: click a thing on your site, say what's wrong, send it back to the agent. We had it animate some boxes and drop in an image block, and since there was no image handy, Sonnet just drew an SVG sunset. Also covered: the skills and MCP settings, the fact that there's a Linux build now (please tell everyone), the agentic UI landing next month, and /liberate, a new slash command that turns a non-WordPress site into a WordPress one. Jamie Marsland, I'm coming for your speed build challenge.

00:00 Chat Q&A: is Studio Code coming to WordPress core?
02:00 One agent for every site vs. AI inside each site
04:00 Audio gremlins & the Studio Code elevator pitch
06:00 Studio Code demo with Antonio
40:00 What's the craziest thing it's done?
42:00 Annotate demo: animating boxes & adding an image block
48:00 Skills, MCP settings & the SVG Sonnet made
50:00 Windows, WSL & the new Linux build
52:00 Agentic UI & /liberate are coming next month
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

Before you publish, scrub 06:00–40:00 and split that one chapter into proper ones. If you'd like, I can re-transcribe just that segment with a different Whisper model or prompt to try to recover it.