All dependencies were present. Here's the draft:

**Title:** Meta Query Autocomplete & Rethinking the Advanced Query Loop Modal - Live Stream

```
Advanced Query Loop can do nested and grouped queries now, so the modal has officially run out of room. I finally admitted it and had Claude move the dynamic placeholders list behind an info toggle and drop its search. That bought us some space back.

Then I showed off meta key and meta value autocomplete. It's fed by a custom hook that merges meta across post types, and you can still type in anything free-form for meta that isn't registered with the REST API. After that I went shopping for a searchable chip-select to replace FormTokenField. It has a "creatable" option, which is great, but I couldn't find a single-selection mode. So that one's still unsolved. Stay tuned.

00:00 Rethinking the modal layout for grouped queries
02:00 Meta key and value autocomplete walkthrough
04:00 Free-form meta input and trying a searchable select
06:00 Creatable items vs. single-selection limits

Connect:

https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

Projects:

👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/

#wordpress #wordpresstutorial #coding #customblocks #javascript #php #gutenberg #livestream
```

- **Plugin name is a guess:** The transcript only calls it "a query/filtering block." I named it Advanced Query Loop because your last stream (Sept 3) planned exactly this meta query modal and dynamic placeholders. If this clip is from something else, change the name in the hook and the title.
- **No links:** As you asked, I left out the two things mentioned in the recording: FormTokenField, which was named with no URL, and the chip-select component, whose name wasn't clear.
- **Date:** Add the stream date to the end of the title to match your usual format.
- **It's a clip:** The recording is only about 8 minutes, so the chapters cover just that segment. If you upload the full stream, the timestamps won't line up.