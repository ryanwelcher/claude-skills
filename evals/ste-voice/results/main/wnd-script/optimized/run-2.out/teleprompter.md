# What's New for Developers — September 2026 (Teleprompter)

> Read copy only — spoken words, no stage directions. `* * *` marks a section break (don't read it). Pause at the line breaks.

---

Hey everybody, Ryan Welcher here again with another edition of What's New for Developers.

If you're not familiar with What's New for Developers, it's an article that comes out monthly on the Developer Blog.

It outlines all the work that's been done in the past month across the WordPress and Gutenberg projects, and you can find it at developer dot wordpress dot org slash news.

Before we get into it, if you haven't already, hit subscribe and give the video a thumbs up.

So let's take a look at what's new for developers, September 2026.

Last month was a fun one, because WordPress 7.1, "Mary Lou," went out the door.

Responsive style states, icon registration, all that good stuff. And if you haven't updated yet, well, it's time. It's past time, actually.

If you want the full rundown of what landed in 7.1, go back and check out last month's roundup.

Since then we've had two Gutenberg releases, 23.8 and 23.9.

A lot of this month is fine-tuning and building on earlier work, so it's maybe not as flashy as a pile of brand new APIs. But things are going to pick up during the 7.2 cycle.

Speaking of which, WordPress 7.2 Beta 1 is scheduled for October 20th to 22nd, and the final release is slated for somewhere between December 8th and 10th. The full schedule is on the 7.2 dev cycle page.

And as always, you can test all of this by running WordPress trunk with the latest Gutenberg, or by spinning up a Playground instance with no setup at all.

I'm going to try and cover everything this month, but there's a lot of code and a lot of links in here, so I'd still encourage you to go read the article and check out the table of contents.

* * *

All right, starting with the highlights.

First up, runnable code examples have landed in the Code Reference.

So you can go to a page like the one for class-list on the HTML Processor, hit Run, and the example actually executes against a real WordPress install, powered by Playground.

The examples are written right in the DocBlock, using a code fence called "php interactive."

So the example and the function it documents live in the same file, which is really nice.

This has been sitting as a proposal in the documentation issue tracker for a while, so it's great to see it go live. This is a really cool one. Go and try it.

Next, block variations and transforms can now declare their own keyboard shortcuts.

So, Alt Shift 2 has turned a paragraph into a Heading 2 since 2022. But that was hardcoded in a private component, and every editor package had to render it for itself.

Gutenberg 23.9 added a declarable API for this.

There are two places you can declare a shortcut, and the key names are different between them, so pay attention here.

Variations take a single "shortcut" object. Transforms take a plural "shortcuts" array, with an optional variation name, so one transform can carry six shortcuts without showing up six times in the block switcher.

There's sample code for both in the article, so go and have a look.

The last highlight is the extensible Site Editor, and the headline is that this is where features have to land now.

Gutenberg 23.9 had roughly twenty PRs for the Boot package for Site Editor v2.

An Identity route, a theme preview page with Global Styles editing, mounting for registered plugins, canvas navigation between entity records, unsaved changes warnings, and theme screens gated on theme support.

And the contributing guidelines now require Site Editor features to land in the extensible Site Editor too.

Keep in mind it's still experimental. But if you extend the Site Editor at all, keep an eye on this one. There's an iteration issue linked in the article you can follow along with.

* * *

All right, moving on to the plugins and tools section.

DataViews is dropping private APIs.

If you've bundled the DataViews package into a plugin, you may have run into the error "Cannot unlock an object that was not locked before."

Which is a pretty confusing error to get. What's going on is DataViews ships as a bundled package, but it reaches for private APIs. And two copies of the private-apis package in the same runtime can't unlock each other's objects.

There's an issue tracking the fix, and it ends with dropping private-apis from DataViews entirely.

The nice side effect is that the components DataViews was depending on are getting public homes.

Calendar and Range Calendar moved into the WordPress UI package, with-ignore-IME-events landed in keycodes, and Validated Input Control is public now too.

Eight other validated controls got vendored into DataViews as internal code. But if you've been eyeing one of these components from behind the private API wall, a few of them are now just imports.

Next, inner block templates are moving into block settings.

Gutenberg 23.8 added "template" and "template-insert-updates-selection" as block type settings. Those replace the InnerBlocks props with the same names.

And the reason is real-time collaboration.

The prop-based approach applied the template after the block mounted, on every connected client. So if you inserted a List block with three collaborators in the document, you got three list items.

Moving it into the block type settings means the block and its template land in a single store operation.

Roughly twenty core blocks have already been migrated. The props still work, but they're deprecated, so if your block ships an inner block template, make the change before 7.2 comes out.

Next up, schema support for PHP-only blocks.

The auto-register flag is now in the block dot json schema, so you get autocomplete and validation in your code editor.

This has technically worked since WordPress 7.0. If you want the full picture, the PHP-only block registration dev note from March is still the best place to start.

This next one's a bit in the weeds, but it's consistent kebab case slug generation.

Core's PHP kebab case function handles things differently than a lot of off-the-shelf libraries, especially around numbers.

That logic is now available on the JavaScript side as the kebab-case package, instead of a private utility. So you get the same output in JS as you do in PHP.

"white2white" becomes "white-2-white," for example. There are a few more examples in the article.

Next, the editors now use the admin color scheme.

The post editor, the widgets editor, and the customizer widgets editor are now wrapped in a Theme Provider that's seeded from the active admin color scheme.

The useful part for extenders is that get-admin-theme-colors is a public export of the admin-ui package.

It reads the admin color body class and gives you back the primary and background values. So you can do the same little wrap on your own admin screens, and your design system components pick up the user's color scheme automatically.

And the last one in this section is a time field for DataViews.

Gutenberg 23.8 added a time field type and control. So think business hours, event start times, booking slots, anything where the value is a time of day.

There's no date on it, and that's on purpose.

Values are stored as hours and minutes, or hours, minutes, and seconds, so 9 a.m. reads as 9 a.m. for every visitor, no matter what timezone they're in.

If you need a specific moment in time, datetime is still the right type.

* * *

Alright, themes.

First, some fixes to the theme dot json schema for states.

Responsive style states and pseudo-class states shipped in 7.1, but the schema that validates them wasn't quite complete.

Gutenberg 23.8 fixed that. Responsive states now work for style variations, they're scoped to blocks and not elements, and some errors with pseudo-class styling got corrected.

So your theme dot json won't light up as invalid in your code editor anymore when you use states.

Next, there are more options for curating the styles UI.

Gutenberg 23.8 added an opt-out for the block style state controls, with two settings, block-states-editing-enabled and responsive-editing-enabled.

You can filter both of them through block editor settings all, and both default to true.

Any styles you've already defined in theme dot json, Global Styles, or a block's style attribute keep rendering either way.

So this is really handy if you're locking down a client build and you don't want to break the design you shipped with it.

Next, the label element is now customizable in Global Styles.

Gutenberg 23.9 added label as an element you can style in theme dot json, under styles, elements, label, just like the other elements.

It applies to any markup that renders a label. In Core that's the Search, Form Input, Post Comments Form, Archives, and Categories blocks, and it'll apply to third-party blocks too.

Along the same lines, cite, text input, and select are now editable in Global Styles.

Those were already supported in theme dot json, but now you can edit them in the Styles interface, under the Typography and Colors panels.

Next, the Group block now has vertical and horizontal block gap.

So the block gap property in theme dot json accepts either a plain string, or an object with top and left keys.

The editor UI still only shows the separate axis controls for flex and grid layouts, which makes sense, because that's where you'd actually use them.

Then there are some updated block supports.

The List block gets wide and full alignment. Query No Results gets border and spacing.

And the Query Loop gets block gap, which a lot of people have been waiting on for a long time.

And the last item under themes is a batch of Global Styles and other fixes.

The Accordion Heading block now sends theme dot json spacing to the toggle button instead of the wrapper.

Duotone palettes are editable in Global Styles.

Global Styles also shows you which blocks have custom styles, and lets you filter by them.

Shadow presets keep storing as CSS variables when custom presets exist, which changes what ends up in a user's saved styles.

Block gap values get normalized more consistently. There's one caveat you should know about, which is that the sanitizer rejects parentheses, so literal calc or var values get dropped. If you're using those, go and test your stuff accordingly.

And the Table of Contents block stopped saving its output to post content.

* * *

Alright, the Playground section.

Playground now supports WebMCP. That's a draft browser API for exposing actions as tools that an AI agent can call.

Because Playground runs WordPress inside a nested iframe, there's a new proxy that advertises the embedded site's tools on the outer page and forwards the calls back down.

Now keep in mind, registering a WordPress ability isn't enough on its own. A plugin has to wrap it in a WebMCP tool.

There's a full post about this on the Playground blog, so go and check it out.

And Playground can also run WordPress releases all the way back to version 0.7.

You tick "include older versions" in the settings panel, and PHP gets paired up for you automatically.

So when you're trying to figure out when something broke, you don't have to rebuild some ancient stack by hand. And I've been around long enough to remember a few of those versions the first time around.

* * *

And finally, the resources section.

There was just one post on the Developer Blog since the last roundup, Hands-on with the WordPress 7.1 Icon Registration API. If you missed it, go and read it.

And there's a bunch of other stuff from the past month worth a read.

The What's New in Gutenberg posts for 23.8 and 23.9, the proposal for a Secrets API for WordPress 7.2, and a post on replacing Dashicons in the admin bar and menu.

There's the Playground and WebMCP post I mentioned, the WordCamp US 2026 PHP conversation, the WordPress 7.1 release retrospective, and the Core Security Initiative.

All the links are in the article.

* * *

Well, that's it. That's the end of What's New for Developers for September 2026.

Thanks for hanging out with me while I nerd out over all these WordPress updates.

My name's Ryan Welcher, developer advocate at Automattic.

If you haven't already, please give this video a thumbs up and subscribe to the channel, so we know we're doing stuff you actually want to see.

I'm looking forward to seeing you all next month for October 2026.

Thanks a lot, and have a good one.
