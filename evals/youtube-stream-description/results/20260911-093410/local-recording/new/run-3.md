Here's the description for the recording. I derived the title from what it covers: **Reworking the Advanced Query Loop Meta Query Modal with Claude Code - Live Stream**

```
The query builder modal in Advanced Query Loop now handles grouped, nested queries, so it needed a lot more room. So I had Claude turn the dynamic placeholders list into an info panel you can toggle, and dropped the search while we were in there. Then came autocomplete for meta keys and values, pulling existing keys in with a custom hook. That part actually worked.

The rest was me hunting for a component that does a fixed list AND lets you type your own value. You need that when your meta isn't registered with the REST API. That landed me on a searchable chip-select with a "createable" option, and I still hadn't figured out how to limit it to a single selection when the clip ended. Classic.

00:00 Reworking the query modal for nested query groups
01:30 Moving dynamic placeholders into an info toggle
02:00 Meta key and value autocomplete
02:50 Walking through the post meta hook and hard-coded values
04:00 Why free-form meta input is still needed
04:45 Trying a searchable chip-select component
06:00 Createable items and the single-selection problem

Connect:

https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

Projects:

👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/

#wordpress #wordpresstutorial #coding #customblocks #javascript #php #gutenberg #livestream
```

- **Plugin name:** the recording doesn't say "Advanced Query Loop" out loud. I named it because your Sept 3 stream was already planning this meta query modal for that plugin. If this is a different project, change the title and the first sentence.
- **Links left out:** as you asked, I didn't add the two things mentioned in the recording, the FormTokenField component and an unnamed chip-select package.
- **No date in the title:** your recent titles end with the stream date, but I couldn't get it from the file. Add it before you upload.
- **Transcript to check chapters against:** `/var/folders/b5/0n0753r97jj7wvpmccw8phr40000gn/T/tmp.tlzabKIRL1/audio.srt`

All dependencies were already installed, so nothing was installed.