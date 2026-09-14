I derived the title from what the recording covers: **Reworking the Advanced Query Loop Query Modal: Meta Autocomplete & Chip Selects**. Add the stream date at the end if you use the usual "- Live Stream <date>" format.

```
Space in the query builder modal is getting tight now that Advanced Query Loop supports nested and grouped queries, so this one is me rearranging the furniture. First job: get Claude to swap the always-visible dynamic placeholders list (and its search box) for an info toggle so it stops eating the whole modal.

Meta keys and values now autocomplete, so I walked through the custom hook that merges post-type meta, and explained why you still need free-form input for meta that isn't registered with the REST API. Then I tried swapping FormTokenField for a searchable chip-select with a "createable" option. It looked great, right up until I couldn't figure out how to limit it to one selection. So, jury's still out on that one.

00:00 Rethinking the query modal layout and placeholders list
01:45 Autocomplete for meta keys and values
03:10 Walking through the post-type meta hook and hard-coded values
04:00 Why free-form meta input is still needed
05:00 Trying a searchable chip-select component
06:35 Exploring the "createable" option and the single-selection problem

Connect:

https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

Projects:

👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/

#wordpress #wordpresstutorial #coding #customblocks #javascript #php #gutenberg #livestream
```

- **Dependencies:** all were already installed, so nothing was installed.
- **Links:** none are in the description, as you asked. The recording mentioned FormTokenField and the chip-select component, both without URLs.
- **Chapters:** these come straight from the on-device transcript. If you want to check one, the timestamped transcript is at `/var/folders/b5/0n0753r97jj7wvpmccw8phr40000gn/T/tmp.P0RCxNgHh3/audio.srt`.