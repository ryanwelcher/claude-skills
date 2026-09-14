I checked the dependencies, pulled your 5 most recent descriptions to match the voice, and ran the transcription helper on the recording.

**Suggested title:** Building a Meta Query Builder Modal for Advanced Query Loop - Live Stream

```
Today was all about the new meta query builder modal I've been working on for Advanced Query Loop, and yes, full disclosure, Claude wrote a good chunk of it. You don't have to remember your meta key names anymore because it gives you a list. There are dynamic placeholders for things like the current post ID, the current user and a pile of date formats. And it now supports nested meta queries, which WP_Query has always handled and AQL just... didn't.

Then chat started throwing component suggestions at me and I spent a while digging through Storybook looking for a searchable single-select field that doesn't exist yet. I also found out about a dumb empty-render bug in the AQL block (thanks Justin). By the end we'd reorganized the placeholder list into groups and moved the info icon into the bottom bar, so it stops eating all the space in the modal. Good enough for an MVP? Let me know.

00:00 Introducing the Meta Builder Modal
02:00 Dynamic Placeholders and Advanced Options
04:00 Modal Design and User Experience Refinements
06:00 Meta Field Discovery and Searchability
10:00 Implementing Creatable Component Inputs
14:00 Custom Dynamic Values?
16:00 Building Complex Nested Queries
18:00 Organizing Placeholders Into Logical Groups
20:00 Demo Wrap-Up and Future Plans

Connect:

https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

Projects:

👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/

#wordpress #wordpresstutorial #coding #customblocks #javascript #php #gutenberg #livestream
```

I didn't use the helper's chapter list as-is:

- **Broken timestamps:** The helper wrote `00:02`, `00:04` and so on, which YouTube reads as seconds, and it rejects chapters less than 10 seconds apart. The transcript is split into 2-minute blocks, so I converted them to `02:00`, `04:00` and so on.
- **Nested queries chapter:** The helper put this at 14:00, but that part of the transcript is you thinking out loud about letting people create their own dynamic values. The nested query demo starts around 16:00, so I split it into two chapters.
- **Spelling:** I fixed "Createable" to "Creatable".

The helper's recap also called AQL "Advanced Query Language," so I wrote the opening paragraph from the transcript itself. As you asked, no links from the recording are included and the Stream Together line is left out. There's no date in the title because the recording doesn't say when it was streamed.