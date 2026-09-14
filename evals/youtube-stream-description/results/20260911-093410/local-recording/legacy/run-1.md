The recording is an 8-minute clip from a stream. In it, you work through the UI for the meta query modal in Advanced Query Loop, go through the new placeholder and meta key features, and try out a searchable chip-select component live. Both dependencies were already installed, so I didn't install anything. The transcript also mentioned no links, so there was nothing to leave out.

**Suggested title:** Designing the Meta Query Modal for Advanced Query Loop – Live Stream

```
This one's all about the meta query modal for Advanced Query Loop and figuring out where everything actually fits. Nested query groups mean that modal needs every bit of room it can get, so I spent a good chunk of time moving the dynamic placeholders list behind an info toggle and showing off the new auto-listed meta keys and values. No more having to know your meta key names by heart.

Then chat pointed me to a searchable chip-select component and I went down the rabbit hole trying to make it do single selection *and* free-form input at the same time. Why do I need both? Because sometimes your meta isn't registered with the REST API and you just have to type it in. Did I figure it out? We ended up reading the source code, so... you tell me.

00:00 Nested query groups & the modal real estate problem
00:54 Moving the placeholders list behind an info toggle
02:00 Meta keys & values now show up automatically
03:00 Under the hood: the custom hook that merges post meta
04:00 Why unregistered meta still needs free-form input
04:48 Trying out a searchable chip-select with details
06:20 Createable items vs. my single-selection problem
07:45 Digging into the component source

Connect:

https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

Projects:

👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/

#wordpress #wordpresstutorial #coding #customblocks #javascript #php #gutenberg #livestream
```

Transcription accuracy may have affected a few spots:
- **Component name:** Whisper transcribed the chip-select component's name poorly, so I described it rather than naming it.
- **Chapter times:** these follow the transcript and all meet YouTube's chapter rules. The ones at 02:00 and 03:00 are approximate, so check them against the video before you publish.