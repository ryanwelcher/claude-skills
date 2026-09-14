I drafted this from the 8-minute clip. It's a slice of the Advanced Query Loop work: redesigning the meta query modal, making dynamic placeholders less cluttered, and arguing with chat over which select component to use. Nothing needed installing; `ffmpeg` and `mlx_whisper` were both already there.

**Suggested title:** Designing the Meta Query Modal for Advanced Query Loop - Live Stream Clip

```
Today I was poking at the new meta query modal for Advanced Query Loop, and trying to figure out how to fit grouped, nested queries into it without it turning into a wall of UI. Chat had opinions. Good ones, annoyingly. We moved the dynamic placeholders list out of the way behind an info button and showed off meta keys and values that now just show up for you, so you don't need to know what they're called.

Then it turned into a hunt for a searchable select that takes exactly one value AND lets you type your own. That matters because some meta isn't registered with the REST API and you still need to be able to type it in. I was pretty sure I'd get sent a link to the answer two seconds after I asked. You can tell Claude wrote a lot of this code.

00:00 Modal or fly-out? Making room for grouped & nested meta queries
00:54 Moving the dynamic placeholders list behind an info button
02:00 Meta keys & values show up for you, and you can still type your own
03:10 Under the hood: the custom hook that merges post type meta
04:00 Why free-form input matters: meta not registered with the REST API
05:00 Trying chat's pick: a searchable chip select
06:00 One value only plus free input, and the "creatable" option

Connect:

https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

Projects:

👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/

#wordpress #wordpresstutorial #coding #customblocks #javascript #php #gutenberg #livestream
```

- **Chapter times:** these are rough. I matched them to the transcript's cue times, but they could be a few seconds off, so check them against the video before you publish.
- **Clip start:** the recording starts partway through the stream. If you upload the full stream instead, the chapters will need new times.
- **Script error:** the fetch script for recent descriptions finished with a zsh error (`(eval):1: == not found`), but all five reference descriptions still came back.