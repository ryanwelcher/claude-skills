Here's the draft description. All dependencies were already installed, so I didn't install anything. The recording is an 8-minute clip rather than a full stream, and no links were mentioned in it.

**Suggested title:** Advanced Query Loop: Reworking the Meta Query Modal & Autocomplete - Live Stream

```
Ran out of room in the Advanced Query Loop meta query modal, especially now that nested query groups are a thing. So I had Claude swap the always-visible dynamic placeholders list (and its search box) for a simple info toggle. Then I showed off the meta key and meta value fields, which now autocomplete from your existing values but still let you type whatever you want. I also walked through the custom hook that pulls meta in from across post types, because unregistered meta is a thing and you still need to be able to type it in.

The rest was me and chat trying out a searchable chip select component. Its "createable" option looked really promising, right up until I couldn't get it to stop at one item. FormTokenField with max length set to 1 is still the fallback, and yes, we did not settle it.

00:00 Rethinking modal space for nested query groups
01:58 Meta key and value autocomplete with free-form input
03:00 Walking through the custom post type meta hook
04:16 Why unregistered meta needs free-form entry
04:55 Trying a searchable chip select component
05:50 FormTokenField max length vs. single selection
06:30 Exploring the "createable" option

Connect:

https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

Projects:

👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/

#wordpress #wordpresstutorial #coding #customblocks #javascript #php #gutenberg #livestream
```