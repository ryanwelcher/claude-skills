# What's New for Developers — September 2026 (Teleprompter)

> Read copy only — spoken words, no stage directions. `* * *` marks a section break (don't read it). Pause at the line breaks.

---

Hey everybody, Ryan Welcher here again with another edition of What's New for Developers.

If you're not familiar with What's New for Developers, it's an article that comes out monthly on the Developer Blog.

It outlines all the work that's been done in the past month across the WordPress and Gutenberg projects, and you can find it at developer dot wordpress dot org slash news.

Before we get into it, if you haven't already, go ahead and subscribe to this channel and give this video a thumbs up.

So let's take a look at what's new for developers, September 2026.

There's a lot in this one, and I'm going to try to get through all of it. But the article has way more detail and a ton of links, so definitely go and read it and check out the table of contents.

* * *

So last month was a pretty fun one, because WordPress 7.1, "Mary Lou," shipped.

That brought us responsive style states, icon registration, and all sorts of great stuff. If you haven't updated yet, it's well past time. Go do that. I'll wait.

And if you missed all the developer goodies in that release, last month's roundup is linked in the article.

Since then we've had two Gutenberg releases, 23.8 and 23.9.

A lot of this month is building on and fine-tuning previous work, so some of it's a little less flashy than a brand new API. But the WordPress 7.2 cycle is coming up, and there should be a lot of big changes in the next couple of months.

Speaking of 7.2, Beta 1 is scheduled for October 20th to 22nd, and the final release is planned for somewhere between December 8th and 10th. The full schedule is on the 7.2 dev cycle page, and that's linked in the article too.

And as always, you can test all of this by running WordPress trunk with the latest Gutenberg, or you can spin up a Playground instance with no setup at all.

* * *

All right, the highlights.

First up, runnable code examples have landed in the Code Reference.

So you can open a page like the class-list method on the WP HTML Processor, hit Run, and that snippet actually runs against a real WordPress install, right there in your browser. It's powered by Playground.

The examples are written right in the DocBlock, using a code fence called "php interactive." So the runnable example and the function it documents live in the same file.

This has been sitting as a documentation proposal in the issue tracker for a while, so it's really cool to see it land. Go and try it out.

Next, block variations and transforms can now declare their own keyboard shortcuts.

So, Alt-Shift-2 has turned a paragraph into a Heading 2 since 2022. But that behavior was hardcoded in a private component, and every editor package had to render it for itself.

Gutenberg 23.9 adds a declarable API for this. There are two places you can declare a shortcut, and the key names are different between them, so pay attention.

A variation takes a singular "shortcut" object. A transform takes a plural "shortcuts" array, with an optional variation name, so one transform can carry six shortcuts without showing up six times in the block switcher.

There's sample code in the article, so go and have a look.

And the last highlight, the extensible Site Editor is where features have to land now.

Gutenberg 23.9 had roughly twenty PRs for the Boot package for Site Editor v2. That's things like an Identity route, a theme preview page with Global Styles editing, registered plugin mounting, unsaved-changes warnings, and a bunch more.

And the contributing guidelines now require Site Editor features to land in the extensible Site Editor too.

Keep in mind it's still experimental. But if you extend the Site Editor, this is one to keep an eye on. There's an iteration issue linked in the article if you want to follow along.

* * *

Moving on to the plugins and tools section.

DataViews is dropping private APIs.

So if you've bundled the DataViews package into a plugin, you may have hit an error that says "Cannot unlock an object that was not locked before." Which is a very fun error message to get.

What's happening is DataViews ships as a bundled package, but it reaches for private APIs. And two copies of the private-apis package in the same runtime can't unlock each other's objects.

There's an issue tracking the fix, and it ends with private-apis getting dropped from the package entirely.

The nice side effect is that the components DataViews depended on are getting public homes. Calendar and RangeCalendar moved into the WordPress UI package, with-ignore-IME-events landed in keycodes, and ValidatedInputControl is public now too.

So if you've been eyeing one of those Core components from behind the private API wall, a few of them are now just imports.

Next, inner block templates are moving into block settings.

Gutenberg 23.8 added "template" and "template-insert-updates-selection" as block type settings. Those replace the InnerBlocks props with the same names.

And the reason for this is real-time collaboration. The old prop-based approach applied the template after mount, on every connected client. So if you inserted a List block with three collaborators in the document, you got three list items.

Moving it into the block type settings means the block and its template land in a single store operation.

Roughly twenty core blocks have already been migrated. The props still work, but they're deprecated. So if your block ships an inner block template, you'll want to make the change before 7.2 comes out.

Next up, schema support for PHP-only blocks.

The auto-register flag is now in the block.json schema. So you get autocomplete and validation in your code editor for something that's technically worked since WordPress 7.0.

If you want the full picture, the PHP-only block registration dev note from March is still the best overview. It's linked in the article.

Then there's consistent kebab-case slug generation.

The kebab-case function in WordPress Core does things a little differently than a lot of off-the-shelf libraries, especially around numbers. On the JavaScript side, that used to be a private utility, and now it's its own package, wordpress slash kebab-case.

So you get the same output in JavaScript as you do in PHP. There are some examples in the article showing how it handles numbers, so go and have a look.

Next, the editors now use the admin color scheme.

The post editor, the widgets editor, and the customizer widgets editor are now wrapped in a ThemeProvider that's seeded from your active admin color scheme.

And the useful part for extenders is that get-admin-theme-colors is a public export from the admin-ui package. It reads the admin color body class and gives you back the primary and background values.

So you can do the same little two-line wrap on your own admin screens, and the design system components will pick up whatever color scheme the user chose. That's pretty handy.

And the last one in this section, there's a new time field for DataViews.

Gutenberg 23.8 added a time field type and control. So think business hours, event start times, booking slots, anything where the value is a time of day. There's no date attached to it.

Values are stored as hours and minutes, or hours, minutes, and seconds. So 9 AM reads as 9 AM for every visitor, no matter what timezone they're in. If you need a specific moment in time, datetime is still the right type.

* * *

Alright, the themes section.

First, some schema fixes for states in theme.json.

Responsive style and pseudo-class states shipped in 7.1, but the schema that validates them wasn't quite complete. So Gutenberg 23.8 has a few fixes, and states won't show up as invalid anymore when you're looking at theme.json in your code editor.

That covers responsive states for style variations, making responsive states specific to blocks and not elements, and fixing some errors with pseudo-class styling.

Next, more options for curating the styles UI.

Gutenberg 23.8 added an opt-out for the block style state controls. There's block-states-editing-enabled and responsive-editing-enabled, and you can filter both of them through block editor settings all.

They both default to true. And any styles you've already defined in theme.json, Global Styles, or a block's style attribute keep rendering either way.

So this is really useful if you're locking down a client build and you don't want to break the design you shipped with it.

Next, the label element is now customizable in Global Styles.

Gutenberg 23.9 added label as a new element you can style in theme.json, under styles, elements, label, just like the other elements.

It applies to any markup that renders a label. In Core that's the Search, Form Input, Post Comments Form, Archives, and Categories blocks, and it'll apply to third-party blocks too.

Along the same lines, cite, text input, and select are now editable in Global Styles.

Those were already supported in theme.json, but now you can edit them right in the Styles interface, under the Typography and Colors panels.

Next, the Group block gets vertical and horizontal block gap.

Group now declares its block gap support as both horizontal and vertical. So the block gap property in theme.json takes either a plain string or an object with top and left keys.

The editor UI still only shows the separate axis controls for flex and grid layouts, which makes sense, because that's where they're actually useful.

Then we've got some updated block supports.

List gets wide and full alignment. Query No Results gets border and spacing. And Query Loop gets block gap, which is going to make a lot of layouts easier.

And to wrap up themes, a batch of Global Styles and other fixes.

The Accordion Heading block now sends theme.json spacing to the toggle button instead of the wrapper.

Duotone palettes are editable in Global Styles.

Global Styles also shows you which blocks have custom styles, and you can filter by them. That's a nice one.

Shadow presets keep storing as CSS variables when custom presets exist, and that affects what ends up in a user's saved styles.

Block gap values are normalized more consistently. There's one caveat you should know about, which is that the sanitizer rejects parentheses, so literal calc or var values get dropped. If you're doing that, go test your stuff accordingly.

And the Table of Contents block no longer saves its output to post content.

* * *

Alright, the Playground section.

Playground now supports WebMCP. That's a draft browser API for exposing actions as tools an AI agent can call.

Because Playground runs WordPress inside a nested iframe, there's a new proxy that advertises the embedded site's tools on the outer page and passes the calls back down.

One thing to keep in mind is that registering a WordPress ability isn't enough on its own. A plugin has to wrap it in a WebMCP tool. This one's pretty exciting, and there's a full post about it on the Playground blog.

And Playground can now run WordPress releases all the way back to version 0.7.

You tick "Include older versions" in the settings panel, and the version picker covers everything up through 6.2, with PHP paired up automatically.

Zero point seven. I'm old, but I'm not that old.

This is super handy for figuring out "when did this break?" without having to build some ancient stack by hand. Go and play around with it.

* * *

And finally, the resources section.

On the Developer Blog, there's been one post since the last roundup, "Hands-on with the WordPress 7.1 Icon Registration API." If you missed it, go and read it.

And there's a list of other things worth reading from the past month.

That includes the What's New posts for Gutenberg 23.8 and 23.9, a proposal for a Secrets API for WordPress 7.2, and a post about replacing Dashicons in the admin bar and menu.

There's also the Playground and WebMCP post I just mentioned, the WordCamp US 2026 PHP conversation, the WordPress 7.1 release retrospective, and the Core Security Initiative.

All the links are in the article.

* * *

Well, that's it. That's the end of What's New for Developers for September 2026.

Thanks again for hanging out with me while I nerd out over all the latest WordPress updates.

My name's Ryan Welcher, developer advocate at Automattic.

If you haven't already, please give this video a thumbs up and subscribe to the channel, so we know we're doing stuff you actually want to see.

I'm looking forward to seeing you all next month for October 2026.

Thanks a lot, and have a good one.
