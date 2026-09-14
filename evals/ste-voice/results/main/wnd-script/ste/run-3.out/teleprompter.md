# What's New for Developers — September 2026 (Teleprompter)

> Read copy only — spoken words, no stage directions. `* * *` marks a section break (don't read it). Pause at the line breaks.

---

Hey everybody, Ryan Welcher here again with another edition of What's New for Developers.

If you're not familiar with What's New for Developers, it's an article that comes out monthly on the Developer Blog.

It outlines all the work that's been done in the past month across the WordPress and Gutenberg projects, and you can find it at developer dot wordpress dot org slash news.

Before we get into it, if you haven't already, go ahead and subscribe to the channel and give this video a thumbs up.

So let's take a look at what's new for developers, September 2026.

Last month was a fun one, because WordPress 7.1, "Mary Lou," shipped.

That release brought us responsive style states, icon registration, and a bunch more.

If you haven't updated yet, it's time. Like, well past time.

And if you missed all the developer goodies in that release, last month's roundup is linked in the article, so go catch up.

Since then we've had two Gutenberg releases, 23.8 and 23.9.

A lot of this is building on and fine-tuning earlier work, so it's maybe not the flashiest month.

But there's a lot of useful stuff in here, and the article expects some pretty big changes during the 7.2 cycle over the next couple of months.

Speaking of 7.2, Beta 1 is scheduled for October 20th to the 22nd, with the final release sometime between December 8th and 10th.

The full schedule is on the WordPress 7.2 dev cycle page, and that's linked in the article.

And as always, you can test the latest changes by running WordPress trunk with the newest Gutenberg release, or just spin up a Playground instance with no setup at all.

I'm going to try and get through everything this month, but there's code samples and a ton of links in the article, so definitely go read it and check out the table of contents.

* * *

Okay, starting with the highlights.

First up, the Code Reference now runs its examples right in the browser.

So you open up a page, like the one for class-list on the HTML Processor, you hit Run, and the snippet actually executes against a real WordPress install. And that's powered by Playground.

The examples are written directly in the DocBlock, using a code fence called "php interactive."

Which means the runnable example lives in the same file as the function it's documenting.

This has been sitting as a proposal in the documentation issue tracker for a while, so it's really cool to see it land. Go and try a few of them out.

Next, block variations and transforms can now declare their own keyboard shortcuts.

Gutenberg 23.9 added a declarable API for this.

So, Alt-Shift-2 has turned a paragraph into a Heading 2 since 2022, but that was hardcoded in a private component that every editor package had to render for itself.

Now you declare it. And there are two places you can do that, and the key names are different between them, so pay attention to this part.

Variations take a single shortcut object.

Transforms take a plural shortcuts array, on a block-type transform, plus an optional variation-name.

That way one transform can carry six shortcuts without showing up six times in the block switcher.

The code for both is in the article, so go and have a look.

And the last highlight is the extensible Site Editor.

Gutenberg 23.9 had roughly twenty PRs for the Boot package for Site Editor v2.

We're talking an Identity route, a theme preview page with Global Styles editing, registered plugin mounting, canvas navigation between entity records, unsaved-changes warnings, and theme screens gated on theme support.

And this one's a pretty big deal, because the contributing guidelines now require Site Editor features to land in the extensible Site Editor too.

It's still experimental, but if you extend the Site Editor, keep an eye on this one. There's an iteration issue linked in the article you can follow along with.

* * *

All right, moving on to the plugins and tools section.

DataViews is dropping its private APIs.

If you've bundled the DataViews package into a plugin, you may have hit an error that says "Cannot unlock an object that was not locked before."

What's happening is DataViews ships as a bundled package, but it reaches for private APIs, and two copies of the private-apis package in the same runtime can't unlock each other's objects.

There's an issue tracking the fix, and it ends with private-apis getting dropped from the package entirely.

And there's a nice side effect here.

The components DataViews depended on are getting public homes.

Calendar and RangeCalendar moved into the WordPress UI package, with-ignore-IME-events landed in keycodes, and ValidatedInputControl is public now too.

Eight other Validated controls got vendored into DataViews as internal code, so not everything came out.

But if you've been eyeing a Core component from behind the private API wall, a few more of them are now just imports.

Next up, inner block templates are moving into block settings.

Gutenberg 23.8 added template and template-insert-updates-selection as block type settings, replacing the InnerBlocks props with the same names.

The reason for this is real-time collaboration.

The prop-based approach applied the template after mount, on each connected client.

So if you inserted a List block with three collaborators in the document, you got three list items. Which is not what anybody wants.

Moving it into the block type settings means the block and its template land in a single store operation.

Roughly twenty core blocks have already been migrated.

The props still work, but they're deprecated, so if your block ships an inner block template, you'll want to make that change before 7.2 comes out. Test your stuff accordingly.

Then we have schema support for PHP-only blocks.

The auto-register flag is now in the block dot json schema.

So you get autocomplete and validation in your code editor for something that's technically worked since WordPress 7.0.

If you want the full picture, the PHP-only block registration dev note from March is still the best overview, and it's linked in the article.

Next, consistent kebab case slug generation.

Core's to-kebab-case function in PHP handles things a bit differently than a lot of off-the-shelf libraries, especially around numbers.

That's now available on the JavaScript side as the WordPress kebab-case package, instead of a private utility.

So in JavaScript you get the same output as PHP. "white2white" becomes "white-2-white", for example. There are a few more examples in the article.

This one's a bit in the weeds, but if you've ever had slugs not match between PHP and JS, you know why it matters.

Next, the editors now use the admin color scheme.

The post editor, the widgets editor, and the customizer widgets editor are all wrapped in a ThemeProvider that's seeded from whatever admin color scheme is active.

The useful part for extenders is that get-admin-theme-colors is a public export of the admin-ui package.

It reads the admin color body class and gives you back primary and background values.

So you can do the same two-line wrap on your own admin screens, and the design system components will pick up the user's chosen scheme automatically. That's a really nice one.

And the last item in this section is a time field for DataViews.

Gutenberg 23.8 added a time field type and control.

So this is handy for things like business hours, event start times, booking slots, anything where the value is a time of day.

And note that there's no date with it.

Values are stored as hours and minutes, or hours, minutes, and seconds, so 9 a.m. reads as 9 a.m. for every visitor, no matter their timezone.

If you need a specific moment in time, datetime is still the type you want.

* * *

Alright, themes.

First, some theme dot json schema fixes for states.

Responsive style and pseudo-class states shipped with WordPress 7.1, but the schema that validates them wasn't quite complete.

So several fixes landed in Gutenberg 23.8, covering responsive states for style variations, making responsive states specific to blocks and not elements, and correcting some errors with pseudo-class styling.

What that means for you is states won't show up as invalid when you're looking at theme dot json in your code editor anymore.

Next, there are more options for curating the styles UI.

Gutenberg 23.8 added an opt-out for the block style state controls, with block-states-editing-enabled and responsive-editing-enabled.

Both of them are filterable through the block editor settings all filter, and both default to true.

Styles that are already defined in theme dot json, Global Styles, or a block's style attribute keep rendering either way.

So this is really useful for locking down a client build without breaking the design you shipped with it. The filter code is in the article.

Then, the label element is now customizable in Global Styles.

Gutenberg 23.9 added label as a new element you can style through theme dot json, under styles, elements, label, just like the other element styles.

It applies to any markup that renders a label.

In Core that's the Search, Form Input, Post Comments Form, Archives, and Categories blocks, and it'll apply to third-party blocks as well.

Next, cite, text input, and select are now editable in Global Styles.

These were already supported in theme dot json, but a recent PR made them editable in the Styles interface in the editor, under the Typography and Colors panels.

Then we've got vertical and horizontal block gap for the Group block.

Group now declares its block gap support as both horizontal and vertical.

So the block gap property in theme dot json takes either a plain string, or an object with top and left keys.

The editor UI still limits the separate axis controls to flex and grid layouts, which is where you'd actually use them.

Next, some updated block supports.

List gets wide and full alignment, Query No Results gets border and spacing, and Query Loop gets block gap.

And the article calls out that last one as being on the wishlist for a long time, so, nice to see it land.

And to round out the themes section, a handful of smaller fixes worth a look.

The Accordion Heading block now routes theme dot json spacing to the toggle button instead of the wrapper.

Duotone palettes are editable in Global Styles.

Global Styles also shows you which blocks have custom styles, and lets you filter by them.

Shadow presets keep storing as CSS variables when custom presets exist, and that affects what ends up in a user's saved styles.

Block gap values are normalized more consistently. But there's one caveat here, the sanitizer rejects parentheses, so literal calc or var values get dropped. Keep an eye on that one.

And the Table of Contents block stopped saving its output to post content.

* * *

Okay, the Playground section.

Playground now supports WebMCP, which is a draft browser API for exposing actions as tools that an AI agent can call.

Because Playground runs WordPress inside a nested iframe, there's a new proxy that advertises the embedded site's tools on the outer page and forwards the calls back down.

Now, registering a WordPress ability isn't enough on its own. A plugin has to wrap it in a WebMCP tool.

So if you're playing around with abilities and AI agents, go and read the Playground post on this one.

And this next one's a lot of fun. Playground can now run WordPress releases all the way back to version 0.7.

You tick "Include older versions" in the settings panel, and the version picker covers everything through 6.2, with PHP paired up automatically.

This is super handy for figuring out "when did this break?" without having to rebuild some ancient stack by hand.

And I'll admit I'm old enough to remember some of those versions the first time around.

* * *

And finally, the resources section.

On the Developer Blog, we've only had one post since the last roundup, and it's Hands-on with the WordPress 7.1 Icon Registration API. So if you missed it, go and check it out.

There's also a bunch of other stuff worth reading from the past month.

The What's New in Gutenberg posts for 23.8 and 23.9, a proposal for a Secrets API for WordPress 7.2, and a post on replacing Dashicons in the admin bar and menu.

There's the Playground and WebMCP post I mentioned, the WordCamp US 2026 PHP conversation, the WordPress 7.1 release retrospective, and the Core Security Initiative.

All sorts of great stuff. The links are all in the article.

* * *

Well, that's it. That's the end of What's New for Developers for September 2026.

Thanks again for hanging out with me while I nerd out over the latest WordPress updates.

My name's Ryan Welcher, developer advocate at Automattic.

If you haven't already, please give this video a thumbs up and subscribe to the channel, so we know we're making stuff you actually want to see.

I look forward to seeing you all next month for October 2026.

Thanks a lot, and have a good one.
