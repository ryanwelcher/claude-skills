I checked the dependencies (all present) and drafted the description. The helper's chapter times were wrong, so I fixed them before using them, and a big chunk of the transcript turned out to be empty.

- **Chapter times fixed:** The helper wrote minutes as seconds (`00:42` meant 42 minutes, not 42 seconds), so its list broke YouTube's 10-second minimum between chapters. The transcript confirmed the real start points, and I rewrote them as minutes. I also shortened a few of the labels.
- **Missing 4:00–41:00 content:** From about 5:00 to 41:00 the transcription just repeats "I'm going to add a couple more things" over and over. That's a known failure where the speech-to-text model loops on one phrase. So I can't tell what happened in that stretch, and the "Studio Code walkthrough" chapter at 4:00 is a vague label covering it. It's worth scrubbing through that part of the video and adding a chapter or two by hand.
- **Links and hashtags:** I left out the links mentioned in the recording (the Studio repo and developer.wordpress.com/studio), as you asked. I added `#ai` to the hashtags because the stream was about AI tools.

**Suggested title:** WordPress Studio Code with Antonio: Annotate, Skills & a Linux Build - Live Stream

```
Had Antonio from the WordPress Studio team on the stream to show off what Studio Code can actually do, and it was a blast, even with my setup falling apart for the first few minutes. We cleared up what it is (not a plugin, not headed for core, it's a WordPress-centric AI agent that lives inside your local dev environment), then took the annotate feature for a spin: click a thing on your site, tell it what you want, and watch it add animations and an image block. It had no image, so Sonnet just drew an SVG sunset. Sure, why not.

We also got into skills and MCP in Studio, the fact that there's finally a Linux build (please shout this from the rooftops), and what's coming next: the agentic UI and a new /liberate command that turns a non-WordPress site into a WordPress one. I'm already planning a stream around liberate, and probably a speed build rematch with Jamie Marsland, since the last time I went up against AI as the non-AI guy I got destroyed.

00:00 WordPress Studio: AI-powered local development tool
02:00 Two approaches to AI in the WordPress ecosystem
04:00 Studio Code walkthrough and development workflow
42:00 Annotate demo: visual AI-driven editing
48:00 Skills, MCP integration & the new Linux build
52:00 Coming soon: agentic UI & the liberate command
54:00 Chat Q&A, wrap-up & future stream plans

Connect:

https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

Projects:

👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/

#wordpress #wordpresstutorial #coding #customblocks #javascript #php #gutenberg #livestream #ai
```