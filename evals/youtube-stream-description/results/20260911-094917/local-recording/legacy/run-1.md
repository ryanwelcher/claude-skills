Suggested title: **Building a Meta Query Modal for Advanced Query Loop - Live Stream**

```
Short one today, and it was all about the new meta query builder I'm working on for Advanced Query Loop. It's a modal now, so you pick your meta keys and values from a list instead of having to remember them. You can still type in keys that aren't registered with the REST API, you can nest groups of queries, and there's a set of dynamic placeholders like the current post ID, the logged-in user and a bunch of date formats (including the ACF default, you're welcome).

Full disclosure, Claude wrote a lot of this. Then chat took over the design review. Someone showed me a creatable chip component in Storybook that I didn't know existed, which sent me spiralling about letting people create their own placeholders. After a few rounds we'd sorted the placeholders into collapsible groups and moved the info panel into a popover in the footer. Might even be a Friday deploy. YOLO.

00:00 First look at the new meta query builder modal
02:00 Dynamic placeholders & how they resolve in PHP
04:00 A silly empty-render bug & is the modal worth the space?
06:00 Autocomplete for meta keys & values
08:00 Why free-form meta keys still matter (meta not registered with REST)
10:00 Chat shows me a creatable chip component in Storybook
14:00 Could you create your own placeholders?
16:00 Recap: building a nested query with the ACF date placeholder
18:00 Grouping the placeholders into collapsible sections
20:00 Moving the info panel into a footer popover & wrap-up

Connect:

https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

Projects:

👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/

#wordpress #wordpresstutorial #coding #customblocks #javascript #php #gutenberg #ai #livestream
```

I transcribed the 22-minute recording on this machine. `ffmpeg` and `mlx_whisper` were both already installed, so nothing was installed. The chapters start on the transcript's 2-minute marks, so each one may be off by up to about two minutes. Check them against the video before you publish.

- **`#ai`:** I added this hashtag because Claude built part of the feature on stream. Your recent stream descriptions use it too.
- **Names left out:** I didn't name the chat member who suggested the component, or Justin, who found the bug. Whisper may have misheard those names, so check them before adding either.

The Google Drive connector isn't authorized. I didn't need it for this, but it won't work until you authorize it in your claude.ai connector settings.