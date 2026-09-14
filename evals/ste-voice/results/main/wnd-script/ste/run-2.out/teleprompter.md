# What's New for Developers — September 2026 (Teleprompter)

> Read copy only — spoken words, no stage directions. `* * *` marks a section break (don't read it). Pause at the line breaks.

---

Hey everybody, Ryan Welcher here again with another edition of What's New for Developers.

If you're not familiar with What's New for Developers, it's an article that comes out monthly on the Developer Blog.

It outlines all the work that's been done in the past month across the WordPress and Gutenberg projects, and you can find it at developer dot wordpress dot org slash news.

Before we get into it, if you haven't already, hit subscribe and give the video a thumbs up.

So, last month was a fun one, because WordPress 7.1, "Mary Lou," went out the door.

Responsive style states, icon registration, all that good stuff.

And if you haven't updated yet, it's well past time, so go do that.

If you want to catch up on all the developer goodies in 7.1, go check out last month's roundup.

Since then, we've had two Gutenberg releases, 23.8 and 23.9.

A lot of this is building on and fine-tuning earlier work, so it's maybe a little less flashy than a bunch of brand new APIs.

But WordPress 7.2 development is ramping up, and I think we're going to see some big changes over the next couple of months.

Beta 1 is scheduled for October 20th to 22nd, and the final release is planned for somewhere between December 8th and 10th.

The full schedule is on the WordPress 7.2 dev cycle page, and that's linked in the article.

And as always, you can test the latest stuff by running WordPress trunk with the newest Gutenberg release, or by spinning up a Playground instance with no setup at all.

So let's take a look at what's new for developers, September 2026.

I'm going to try to get through everything this month, but there's a lot of detail and code in here I won't read out, so I'd really encourage you to go read the article and check out the table of contents.

* * *

Okay, we're starting with the highlights.

First up, runnable code examples have landed in the Code Reference.

So you can open up a page, like the one for the class-list method on the WP HTML Processor, hit Run, and that snippet actually executes against a real WordPress install.

And that's powered by Playground.

The examples are written right in the DocBlock, using a code fence called "php interactive."

So the example you can run and the function it documents live in the same file, which is pretty great.

This has been sitting as a proposal in the documentation issue tracker for a while, so it's really cool to see it go live.

Next, block variations and transforms can now declare their own keyboard shortcuts.

Gutenberg 23.9 added a declarable API for this.

Alt-Shift-2 has turned a paragraph into a Heading 2 since 2022, but that was hardcoded in a private component that every editor package had to render for itself.

Now you declare it. And there are two places you can do that, and the key names are a little different between them.

Variations take a single "shortcut" object.

Transforms take a plural "shortcuts" array, plus an optional variation name, so one transform can carry six shortcuts without showing up six times in the block switcher.

The code for both is in the article, so go and have a look.

And the last highlight is about the extensible Site Editor.

Gutenberg 23.9 had roughly twenty PRs for the Boot package for Site Editor v2.

We're talking an Identity route, a theme preview page with Global Styles editing, registered plugin mounting, canvas navigation between entity records, unsaved-changes warnings, and theme screens gated on theme support.

And the contributing guidelines now say that Site Editor features have to land in the extensible Site Editor too.

It's still experimental, but if you extend the Site Editor, keep an eye on this one.

There's an iteration issue on GitHub you can follow along with, and it's linked in the article.

* * *

All right, moving on to the plugins and tools section.

First up, DataViews is dropping private APIs.

So if you've bundled the DataViews package into a plugin, you may have hit an error that says "Cannot unlock an object that was not locked before."

And that's a fun one to run into.

What's happening is DataViews ships as a bundled package, but it reaches for private APIs, and two copies of the private-apis package in one runtime can't unlock each other's objects.

There's an issue tracking the fix, and it ends with dropping private-apis from the package completely.

The nice side effect is that the components DataViews depended on are getting public homes.

Calendar and Range Calendar moved into the WordPress UI package, with-ignore-IME-events landed in keycodes, and Validated Input Control is public now too.

The other Validated controls were copied into DataViews as internal code.

But if you've been eyeing a Core component that was stuck behind the private API wall, a few more of them are now just imports.

Next, inner block templates are moving into block settings.

Gutenberg 23.8 added "template" and "template insert updates selection" as block type settings, and those replace the InnerBlocks props with the same names.

And the reason for this is real-time collaboration.

The prop-based approach applied the template after the block mounted, on every connected client.

So if you inserted a List block with three collaborators in the document, you got three list items.

Moving it into the block type settings means the block and its template land in a single store operation.

About twenty core blocks have already been migrated.

The props still work, but they're deprecated, so if your block ships an inner block template, you'll want to make this change before 7.2 comes out.

Then we've got schema support for PHP-only blocks.

The auto-register flag is now in the block dot json schema.

So you get autocomplete and validation in your code editor for something that's technically worked since WordPress 7.0.

If you want the full picture, the PHP-only block registration dev note from March is still the best overview, and it's linked in the article.

Next is consistent kebab case slug generation.

Core's to-kebab-case function in PHP handles things a little differently than a lot of off-the-shelf libraries, especially around numbers.

That logic is now available as the WordPress kebab-case package, instead of a private utility on the JavaScript side.

So your JavaScript and your PHP produce the same slugs, and there are some examples in the article.

Next up, the editors now use the admin color scheme.

The post editor, the widgets editor, and the customizer widgets editor are all wrapped in a Theme Provider that's seeded from whatever admin color scheme is active.

The useful part for extenders is that get-admin-theme-colors is a public export of the admin-ui package.

It reads the admin color body class and gives you back the primary and background values.

So you can do the same two-line wrap on your own admin screens, and the design system components will pick up the user's color scheme automatically.

And the last one in this section is a time field for DataViews.

Gutenberg 23.8 added a time field type and control.

This is handy for business hours, event start times, booking slots, anything where the value is a time of day.

And just to be clear, there's no date in it.

Values are stored as hours and minutes, or hours, minutes, and seconds, so 9 a.m. reads as 9 a.m. for every visitor, no matter what timezone they're in.

If you need a specific moment in time, datetime is still the one you want.

* * *

Alright, themes.

First, some fixes to the theme dot json schema for states.

Responsive style states and pseudo-class states shipped in WordPress 7.1, but the schema that validates them wasn't quite complete.

Gutenberg 23.8 has several fixes, so those states won't show up as invalid when you're looking at theme dot json in your code editor.

That covers responsive states for style variations, making responsive states specific to blocks and not elements, and some errors with pseudo-class styling.

Next, there are more options for curating the styles UI.

Gutenberg 23.8 added an opt-out for the block style state controls, with two settings, block-states-editing-enabled and responsive-editing-enabled.

You can filter both of them through block-editor-settings-all.

They both default to true, and any styles you've already defined in theme dot json, Global Styles, or a block's style attribute keep rendering either way.

So this is really useful for locking down a client build without breaking the design you shipped.

Next, the label element is now customizable in Global Styles.

Gutenberg 23.9 added label as an element you can style in theme dot json, under styles, elements, label, just like the other elements.

It applies to any markup that renders a label.

In Core, that's the Search, Form Input, Post Comments Form, Archives, and Categories blocks, and it'll apply to third-party blocks too.

Then cite, text input, and select are now editable in Global Styles.

Those were already supported in theme dot json, but now you can edit them in the Styles interface in the editor, under the Typography and Colors panels.

Next, the Group block gets vertical and horizontal block gap.

It now declares block gap support for both axes, so the block gap property in theme dot json accepts either a plain string or an object with top and left keys.

The editor UI still only shows the separate controls for flex and grid layouts, which is where having two axes actually makes sense.

We've also got some updated block supports.

The List block gets wide and full alignment, Query No Results gets border and spacing, and the Query Loop gets block gap.

That Query Loop one is a nice one to see.

And finally for themes, a bunch of smaller Global Styles and other fixes.

The Accordion Heading block now sends theme dot json spacing to the toggle button instead of the wrapper.

Duotone palettes are editable in Global Styles.

Global Styles also shows you which blocks have custom styles, and lets you filter by them.

Shadow presets keep storing as CSS variables when custom presets exist, which affects what ends up in a user's saved styles.

Block gap values get normalized more consistently.

But there's a caveat there, because the sanitizer rejects parentheses, so literal calc or var values get dropped. So keep an eye on that one and test your stuff accordingly.

And the Table of Contents block stopped saving its output to post content.

* * *

Okay, the Playground section.

Playground now supports WebMCP, which is a draft browser API for exposing actions as tools that an AI agent can call.

Because Playground runs WordPress in a nested iframe, there's a new proxy that advertises the embedded site's tools on the outer page and forwards the calls back down.

Now, registering a WordPress ability isn't enough on its own. A plugin has to wrap it in a WebMCP tool.

There's a full post about it on the Playground blog, so definitely go and check that out.

And Playground can also run WordPress releases all the way back to version 0.7.

You tick "Include older versions" in the settings panel, and the version picker covers everything through 6.2, and it pairs up the PHP version for you.

This is great when you're trying to figure out "when did this break?" and you don't want to rebuild an old stack by hand.

Go and play around with it and see how far back you can go.

* * *

And finally, the resources section.

On the Developer Blog, we only had one post since the last roundup, and that's "Hands-on with the WordPress 7.1 Icon Registration API."

If you missed it, go and give it a read.

There's also a bunch of other stuff from the past month that's worth your time.

You've got the "What's new in Gutenberg" posts for 23.8 and 23.9, and there's a proposal for a Secrets API for WordPress 7.2.

There's a post on replacing Dashicons in the admin bar and menu, and the Playground and WebMCP post I mentioned earlier.

And then there's the WordCamp US 2026 PHP conversation, the WordPress 7.1 release retrospective, and the Core Security Initiative.

All the links are in the article, so go and have a look.

* * *

Well, that's it. That's the end of What's New for Developers for September 2026.

Thanks again for hanging out with me while I nerd out over the latest WordPress updates.

My name's Ryan Welcher, developer advocate at Automattic.

If you haven't already, please give this video a thumbs up and subscribe to the channel, so we know we're doing stuff you actually want to see.

I'm looking forward to seeing you all next month for October 2026.

Thanks a lot, and have a good one.
