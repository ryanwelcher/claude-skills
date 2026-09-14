Transcription and the reference pull both worked. No dependencies were missing and nothing was installed.

**Suggested title:** Building a Meta Query Builder with Dynamic Placeholders for Advanced Query Loop

```
Short one today, and it was all about the new meta query builder I've been working on for Advanced Query Loop. No more needing to know the name of your meta key: keys and values are suggested automatically, you can still type your own, and there's a new set of dynamic placeholders like the current post ID, the logged-in user and a pile of date formats (yes, including the ACF default). It also does nested, grouped meta queries now, which WP_Query has always supported and AQL never did.

Chat sent me down a rabbit hole with the design system's searchable select component, which led to me spiraling about letting people create their own placeholders. Then we spent the rest of the stream going back and forth with Claude on how to make the placeholder list take up less space. We ended with grouped sections and an info popover in the footer. Friday deploy? YOLO.

00:00 Tour of the new meta query builder modal
02:00 Dynamic placeholders & how they resolve on the PHP side
04:00 Is the modal worth the real estate? Turning the list into an info toggle
08:00 Why free-form meta keys still matter (meta not in the REST API)
10:00 Chat shows me the searchable select component
14:00 Spiraling: could you create your own placeholders?
16:00 Full demo: nested queries & the ACF date placeholder
18:00 Grouping the placeholders so they're readable
20:00 Moving the info popover into the footer & wrap-up

Connect:

https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

Projects:

👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/

#wordpress #wordpresstutorial #coding #customblocks #javascript #php #gutenberg #ai #livestream
```

- **Chapters:** the transcript comes in 2-minute chunks, so the chapter times are rounded to those chunks rather than exact topic changes. It's worth checking them against the video before you publish.
- **`#ai` hashtag:** I added it to the standard set because most of the stream was working with Claude, and your recent streams use it too.
- **Links:** as you asked, the description has no links from the recording. Only the Connect and Projects links from your template are in it.