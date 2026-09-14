I used the analyze-stream-recording helper to transcribe the recording. The dependency check passed, so nothing was installed. I left out mentioned links as you asked, though the helper didn't find any anyway.

**Suggested title:** Building a Meta Query Builder Modal for Advanced Query Loop – Live Stream

```
Today's stream was all about the meta query builder for Advanced Query Loop. It lives in a modal now, handles nested queries, and supports dynamic placeholders for things like the current post ID, author ID and date/time. It mostly behaved. Naturally I hit an AQL block rendering bug along the way, then spent a good chunk of time arguing with myself about modal layout and digging through Storybook for the right components.

The list of placeholders had turned into a wall of text, so I split it into collapsible groups (Date/Time, IDs/Content/Users, Relative Dates) that only open one at a time. Next up is moving the info icon into a footer popover and shipping the whole thing, hopefully Friday. No promises.

00:00 Meta query builder UI overview
02:00 Dynamic placeholders and code architecture
04:00 AQL block rendering bug and modal layout benefits
06:00 Meta key/value autocomplete and component complexity
08:00 Reviewing Storybook component options
10:00 Full modal demo with nested query support
12:00 Reorganizing placeholders into grouped sections
14:00 Moving info icon to footer popover
16:00 Toggling groups one at a time and positioning
18:00 Final design review and wrap-up

Connect:

https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

Projects:

👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/

#wordpress #wordpresstutorial #coding #customblocks #javascript #php #gutenberg #livestream
```