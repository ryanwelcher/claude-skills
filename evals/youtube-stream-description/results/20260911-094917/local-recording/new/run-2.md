I ran the dependency check (it passed), then transcribed the recording on-device, pulled your 5 most recent descriptions for voice, and read the template.

**Suggested title:** Building a Meta Query Builder for Advanced Query Loop - Live Stream

I left out the links mentioned in the recording, as you asked: AQL, two unnumbered PRs, and the Storybook combobox. The recording has no date, so the title doesn't have one either.

```
Short one today, but a fun one. I showed off the new meta query builder I've been working on for Advanced Query Loop. It lives in a modal now, which gives it room for nested and grouped meta queries. It autocompletes your meta keys and values, lets you type in keys that aren't registered with the REST API, and supports dynamic placeholders (current post ID, the ACF compact date format and more) that get resolved in PHP. I also found a bug where the default AQL block renders an empty element, so that's on the list.

Chat sent me to the searchable/creatable combobox in the WordPress design system Storybook, which got me thinking about letting you create your own placeholders. Then Claude and I regrouped the placeholder list into three sections and moved it into a footer popover that only opens one section at a time. It ships soon, possibly as a Friday deploy, because apparently I like to live dangerously.

00:00 Demo: new meta query builder modal with nested queries
02:00 Dynamic placeholders and the PHP placeholder resolver
03:40 Empty default-block bug and why the modal needs the space
05:40 Meta key/value autocomplete and free-form input
08:00 Behind the scenes: post meta hook and hardcoded values
10:00 Exploring the searchable/creatable combobox in Storybook
13:50 Idea: user-created custom placeholders
15:50 Walkthrough: building a date query with placeholders
18:20 Grouping the placeholder list into sections
20:00 Moving placeholder info into a footer popover and wrap-up

Connect:

https://www.twitch.tv/ryanwelchercodes
https://twitter.com/ryanwelcher
https://www.linkedin.com/in/ryanwelcher/
https://bsky.app/profile/ryanwelcher.com

Projects:

👉 Advanced Query Loop plugin: https://wordpress.org/plugins/advanced-query-loop/

#wordpress #wordpresstutorial #coding #customblocks #javascript #php #gutenberg #livestream
```