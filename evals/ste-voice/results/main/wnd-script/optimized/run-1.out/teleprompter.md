# What's New for Developers — September 2026 (Teleprompter)

> Read copy only — spoken words, no stage directions. `* * *` marks a section break (don't read it). Pause at the line breaks.

---

Hey everybody, Ryan Welcher here again with another edition of What's New for Developers.

If you're not familiar with What's New for Developers, it's an article that comes out monthly on the Developer Blog.

It covers all the work that's been done in the past month across the WordPress and Gutenberg projects, and you can find it at developer dot wordpress dot org slash news.

Before we get into it, if you haven't already, hit subscribe and give the video a thumbs up.

So let's take a look at what's new for developers, September 2026.

As always, I may not have time to go deep on everything, so I'd encourage you to go read the article and check out the table of contents. There's a lot of good stuff in here this month.

* * *

So, last month WordPress 7.1, "Mary Lou," came out.

That release brought us responsive style states, icon registration, and a bunch more.

And if you haven't updated yet, it's well past time. Go do that. I'll wait.

If you want to catch up on all the developer stuff that shipped in 7.1, last month's roundup has you covered.

Since then we've had two Gutenberg releases, 23.8 and 23.9.

These are mostly building on and fine-tuning earlier work, so they might feel a little less flashy than a pile of new APIs.

But the article expects a lot of big changes during the WordPress 7.2 cycle over the next couple of months, so keep an eye on that.

And speaking of 7.2, Beta 1 is scheduled for October 20th to 22nd, with the final release landing somewhere between December 8th and 10th.

The full schedule is on the 7.2 dev cycle page, and that's linked in the article.

And as always, you can test all of this by running WordPress trunk with the latest Gutenberg, or by spinning up a Playground instance with no setup at all.

* * *

Alright, let's start with the highlights.

First up, the Code Reference can now run its code examples right in the browser.

So you open up a page, like the one for the class-list method on the WP HTML Processor, you hit Run, and that snippet actually executes against a real WordPress install powered by Playground.

That's really cool.

The way it works is the examples are written right in the DocBlock, using a code fence called "php interactive."

So the runnable example and the function it documents live in the same file, which is exactly where you want them.

This one's been sitting as a proposal in the documentation issue tracker for a while, so it's great to see it land. Go and play around with it.

Next, block variations and transforms can now declare their own keyboard shortcuts.

Gutenberg 23.9 added a declarable API for this.

So, Alt Shift 2 has turned a paragraph into a Heading 2 since 2022, but that was hardcoded in a private component that every editor package had to render for itself.

Now you can declare shortcuts yourself, and there are two places to do it.

Variations take a single shortcut object, and transforms take a shortcuts array, plural, along with an optional variation name.

That way one transform can carry six shortcuts without showing up six times in the block switcher.

The key names are different between the two, so keep an eye on that. There's sample code for both in the article.

And the last highlight is the extensible Site Editor.

Gutenberg 23.9 had roughly twenty PRs for the Boot package that powers Site Editor v2.

We're talking an Identity route, a theme preview page with Global Styles editing, registered plugin mounting, canvas navigation between entity records, unsaved-changes warnings, and theme screens that check for theme support.

And the contributing guidelines now require Site Editor features to land in the extensible Site Editor too.

Keep in mind it's still experimental, but if you extend the Site Editor at all, this is one to watch. There's an iteration issue you can follow along with, and it's linked in the article.

* * *

All right, moving on to the plugins and tools section.

First, DataViews is dropping private APIs.

If you've bundled the DataViews package into a plugin, you may have run into an error that says "Cannot unlock an object that was not locked before."

That happens because DataViews ships as a bundled package but reaches for private APIs, and when you've got two copies of the private-apis package in the same runtime, they can't unlock each other's objects.

There's an issue tracking the fix, and it ends with DataViews dropping the private-apis package entirely.

And there's a nice side effect here.

Components that DataViews depended on are getting public homes.

Calendar and RangeCalendar moved into the WordPress UI package, with-ignore-IME-events landed in the keycodes package, and ValidatedInputControl is public now too.

Eight of the other Validated controls were pulled into DataViews as internal code, so those aren't public.

But if you've been eyeing a Core component sitting behind the private API wall, a few of them are now just an import away. Go have a look.

Next, inner block templates are moving into block settings.

Gutenberg 23.8 added template and template-insert-updates-selection as block type settings, and those replace the InnerBlocks props with the same names.

The reason for this is real-time collaboration.

With the old prop-based approach, the template got applied after mount, on every connected client.

So if you inserted a List block with three collaborators in the document, you got three list items. Which, you know, is not what anybody wanted.

Moving it into the block type settings means the block and its template land in a single store operation.

About twenty core blocks have already been migrated.

The props still work, but they're deprecated. So if your block ships an inner block template, you'll want to make that change before 7.2 comes out.

After that, schema support for PHP-only blocks.

The auto-register flag is now in the block JSON schema, so you get autocomplete and validation in your code editor for a feature that's technically worked since WordPress 7.0.

If you want the full picture, the PHP-only block registration dev note from March is still the best overview, and it's linked in the article.

Next up is consistent kebab-case slug generation.

The underscore-wp-to-kebab-case function in Core handles things a little differently than a lot of off-the-shelf libraries, especially around numbers.

That logic is now available on the JavaScript side as the WordPress kebab-case package, instead of a private utility.

So you'll get the same output in JS that you get in PHP. The article has a few examples, like "font2xl" becoming "font-2-xl."

Then, the editors now use the admin color scheme.

The post editor, the widgets editor, and the customizer widgets editor are all wrapped in a ThemeProvider that's seeded from the user's admin color scheme.

The useful part for extenders is that get-admin-theme-colors is a public export of the admin-ui package.

It reads the admin color class on the body and gives you back the primary and background values.

So you can do that same little two-line wrap on your own admin screens, and the design system components will pick up whatever scheme the user chose. Pretty handy.

And the last one in this section is a time field for Data Views.

Gutenberg 23.8 added a time field type and control.

This is useful for things like business hours, event start times, booking slots, anything where the value is a time of day. Note there's no date with it.

Values are stored as hours and minutes, or hours, minutes, and seconds, so 9 a.m. reads as 9 a.m. for every visitor no matter what timezone they're in.

If you need a specific moment in time, datetime is still the one you want.

* * *

Alright, the themes section.

First, some fixes to the theme JSON schema for states.

Responsive style states and pseudo-class states shipped with WordPress 7.1, but the schema that validates them wasn't quite complete.

Several fixes landed in Gutenberg 23.8, covering responsive states for style variations, making responsive states specific to blocks and not elements, and correcting some errors with pseudo-class styling.

So if your code editor has been telling you your states are invalid, this should clear that up.

Next, there are more options for curating the styles UI.

Gutenberg 23.8 added an opt-out for the block style state controls, with block-states-editing-enabled and responsive-editing-enabled.

You can filter both of those through block-editor-settings-all, and they both default to true.

And any styles already defined in theme JSON, Global Styles, or a block's style attribute keep rendering either way.

So this is really useful for locking down a client build without breaking the design you shipped with it.

Then, the label element is now customizable through Global Styles.

Gutenberg 23.9 added label as a new element you can style in theme JSON, under styles, elements, label, just like the other elements.

It applies to any markup that renders a label.

In Core that's the Search, Form Input, Post Comments Form, Archives, and Categories blocks, and it'll apply to third-party blocks too.

Next, cite, text input, and select are now editable in Global Styles.

Those were already supported in theme JSON, but a recent PR made them editable in the Styles interface, under the Typography and Colors panels.

After that, the Group block gets vertical and horizontal block gap.

Group now declares its block gap support as both horizontal and vertical.

So the block gap property in theme JSON takes either a plain string or an object with top and left keys.

The editor UI still only shows the separate axis controls for flex and grid layouts, which is where having two axes actually makes sense.

Then there are some updated block supports.

The List block gets wide and full alignment, Query No Results gets border and spacing, and the Query Loop gets block gap.

The article mentions that last one's been on a wishlist for a long time, and yeah, I get it. This one's a lot of fun for layout work.

And to wrap up the themes section, there's a batch of Global Styles and other fixes.

The Accordion Heading block now sends theme JSON spacing to the toggle button instead of the wrapper.

Duotone palettes are editable in Global Styles.

Global Styles also shows you which blocks have custom styles, and you can filter by them.

Shadow presets keep storing as CSS variables when custom presets exist, which changes what ends up in a user's saved styles.

Block gap values are normalized more consistently. There's one caveat here, though. The sanitizer rejects parentheses, so literal calc or var values get dropped. Test your stuff accordingly.

And the Table of Contents block stopped saving its output to post content.

* * *

Alright, the Playground section.

Playground now supports WebMCP, which is a draft browser API for exposing actions as tools an AI agent can call.

Because Playground runs WordPress inside a nested iframe, there's a new proxy that advertises the embedded site's tools on the outer page and forwards the calls back down.

One thing to know is that registering a WordPress ability isn't enough on its own. A plugin has to wrap it in a WebMCP tool.

This one's pretty exciting, and there's a full post on the Playground blog if you want to dig in.

And Playground can now run WordPress releases all the way back to version 0.7.

You tick "Include older versions" in the settings panel, and the version picker covers everything up through 6.2, with PHP pairing automatically.

This is really handy for figuring out when something broke, without rebuilding some ancient stack by hand. And yeah, I've done that by hand before, and I don't recommend it.

* * *

And finally, the resources section.

On the Developer Blog, we've only had one post since the last roundup, and it's Hands-on with the WordPress 7.1 Icon Registration API. If you missed it, go and read that one.

There's also a bunch of other stuff worth a read from the past month.

There's the What's New posts for Gutenberg 23.8 and 23.9.

There's a proposal for a Secrets API for WordPress 7.2, and a post on replacing Dashicons in the admin bar and menu.

There's the WordPress Playground and WebMCP post I mentioned a minute ago.

There's a post on the PHP conversation from WordCamp US 2026, the WordPress 7.1 release retrospective, and the Core Security Initiative.

All sorts of great stuff, and all of it's linked in the article.

* * *

Well, that's it. That's the end of What's New for Developers for September 2026.

Thanks again for hanging out with me while I nerd out over the latest WordPress updates.

My name's Ryan Welcher, developer advocate at Automattic.

If you haven't already, please give this video a thumbs up and subscribe to the channel, so we know we're doing stuff you actually want to see.

I look forward to seeing you all next month for October 2026.

Thanks a lot, and have a good one.
