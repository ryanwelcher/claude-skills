# What's New for Developers — September 2026 (Teleprompter)

> Read copy only — spoken words, no stage directions. `* * *` marks a section break (don't read it). Pause at the line breaks.

---

Hey everybody, Ryan Welcher here again with another edition of What's New for Developers.

If you're not familiar with What's New for Developers, it's an article that comes out monthly on the Developer Blog.

You can find it at developer dot wordpress dot org slash news, and it covers all the work that's been done in the past month across the WordPress and Gutenberg projects.

Before we get into it, if you haven't already, hit subscribe and give the video a thumbs up.

So, let's take a look at what's new for developers, September 2026.

Last month was a fun one, because WordPress 7.1, "Mary Lou," shipped.

That brought us responsive style states, icon registration, and a bunch more.

And if you haven't updated yet… it's well past time. Go do that. I'll wait.

If you missed all the developer stuff that came with it, last month's roundup has you covered, so go back and have a look.

Since then we've had two Gutenberg releases, 23.8 and 23.9.

A lot of this month is building on and fine-tuning earlier work, so some of it is maybe a little less flashy than a brand new API.

But the 7.2 cycle is coming up fast, and the article expects a lot of big changes over the next couple of months.

Beta 1 for 7.2 is scheduled for October 20th to 22nd, and the final release is planned for somewhere between December 8th and 10th.

The full schedule is on the 7.2 dev cycle page, and that's linked in the article.

And as always, you can test all of this by running WordPress trunk with the latest Gutenberg, or just spin up a Playground instance with no setup at all.

I'm going to try to get through everything this month, but there's a lot of code in this one, so go read the article and use the table of contents to jump around.

* * *

Okay, starting with the highlights.

First up, runnable code examples in the Code Reference.

This one's really cool.

You can now open a page in the Code Reference, like the one for the HTML Processor's class-list method, hit Run, and the example actually runs in your browser against a real WordPress install, powered by Playground.

And the examples are written right in the DocBlock, using a code fence called php interactive.

So the runnable example lives in the same file as the function it documents, which is kind of the ideal place for it.

This idea has been sitting in the documentation issue tracker as a proposal for a while, so it's great to see it land.

Next, block variations and transforms can now declare their own keyboard shortcuts.

Gutenberg 23.9 added a declarable API for this.

So, Alt-Shift-2 has turned a paragraph into a Heading 2 since 2022, but that was hardcoded in a private component that every editor package had to render for itself.

Now you declare it, and there are two places you can do that.

The key names are different between them, so pay attention here.

Variations take a singular shortcut object.

Transforms take a plural shortcuts array, plus an optional variation-name, so one transform can carry six shortcuts without showing up six times in the block switcher.

The code for both is in the article, so go and have a look.

And the last highlight is the extensible Site Editor.

Gutenberg 23.9 had roughly twenty PRs for the Boot package for Site Editor v2.

We've got an Identity route, a theme preview page with Global Styles editing, registered plugin mounting, canvas navigation between entity records, unsaved-changes warnings, and theme screens that are gated on theme support.

And this one's a pretty big deal, because the contributing guidelines now require Site Editor features to land in the extensible Site Editor too.

Keep in mind it's still experimental.

But if you extend the Site Editor at all, keep an eye on that one. There's an iteration issue linked in the article you can follow along with.

* * *

All right, moving on to the plugins and tools section.

First, DataViews is dropping private APIs.

If you've bundled the DataViews package into your plugin, you may have hit an error that says "Cannot unlock an object that was not locked before."

And yeah, that's a fun one to run into.

What's happening is DataViews ships as a bundled package, but it reaches for private APIs, and when you've got two copies of the private-apis package in one runtime, they can't unlock each other's objects.

There's an issue tracking the fix, and it ends with the private-apis package being removed from DataViews completely.

The nice side effect is that the components DataViews depended on are getting public homes.

Calendar and RangeCalendar moved into the wordpress-ui package, with-ignore-IME-events landed in keycodes, and ValidatedInputControl is public now too.

Eight other Validated controls got pulled into DataViews as internal code, so those aren't public.

But if you've been eyeing a Core component that was stuck behind the private API wall, a few more of them are now just imports.

Next, inner block templates are moving into block settings.

Gutenberg 23.8 added template and template-insert-updates-selection as block type settings, and those replace the InnerBlocks props with the same names.

The reason for this is real-time collaboration.

The old prop-based way applied the template after mount, on each connected client.

So if you inserted a List block with three collaborators in the document, you got three list items.

Which is not what anybody wanted.

Moving it into the block type settings means the block and its template land in a single store operation.

Roughly twenty core blocks have already been migrated.

The props still work, but they're deprecated, so if your block ships an inner block template, you'll want to make that change before 7.2 comes out.

Next up, schema support for PHP-only blocks.

The auto-register flag is now in the block.json schema.

So you get autocomplete and validation in your code editor for something that's technically worked since WordPress 7.0.

If you want the full picture on PHP-only block registration, the dev note from March 2026 is still the best overview, and it's linked in the article.

Then we have consistent kebab case slug generation.

WordPress Core's PHP function for turning things into kebab case handles things a bit differently than a lot of off-the-shelf libraries, especially around numbers.

That behavior is now available on the JavaScript side as the wordpress kebab-case package, instead of being a private utility.

So you get the same output in JS as you do in PHP. There are a few examples in the article showing how it handles numbers.

Next, the editors now use the admin color scheme.

The post editor, the widgets editor, and the customizer widgets editor are all wrapped in a ThemeProvider that's seeded from the active admin color scheme.

The useful bit for extenders is that get-admin-theme-colors is a public export of the admin-ui package.

It reads the admin color body class and gives you back primary and background values.

So you can do the same two-line wrap on your own admin screens, and the design system components will pick up the user's color scheme automatically.

And the last one in this section is a time field for DataViews.

Gutenberg 23.8 added a time field type and control.

This is handy for things like business hours, event start times, booking slots, anything where the value is a time of day.

There's no date, though, so keep that in mind.

Values are stored as hours and minutes, or hours, minutes, and seconds, so 9 a.m. reads as 9 a.m. for every visitor no matter what timezone they're in.

If you need a specific moment in time, datetime is still the right type.

* * *

Alright, themes.

First, some theme.json schema fixes for states.

Responsive style states and pseudo-class states shipped in 7.1, but the schema that validates them wasn't complete.

A few fixes landed in Gutenberg 23.8 for that.

Responsive states now work for style variations, responsive states are specific to blocks and not elements, and some errors with pseudo-class styling were corrected.

So states shouldn't show up as invalid anymore when you're looking at theme.json in your editor.

Next, more options for curating the styles UI.

Gutenberg 23.8 added an opt-out for the block style state controls, with two settings, block-states-editing-enabled and responsive-editing-enabled.

You can filter both of them through block-editor-settings-all.

They both default to true.

And any styles already defined in theme.json, Global Styles, or a block's style attribute keep rendering either way.

So this is really useful if you're locking down a client build and you don't want to break the design you shipped with it.

Next, the label element is now customizable through Global Styles.

Gutenberg 23.9 added label as a new element you can style in theme.json, under styles, elements, label, just like the other element styles.

It applies to any markup that renders a label.

In Core that's the Search, Form Input, Post Comments Form, Archives, and Categories blocks, and it'll apply to third-party blocks as well.

Then we have cite, text input, and select, which are now editable in Global Styles.

These were already supported in theme.json, but now you can edit them in the Styles interface in the editor, under the Typography and Colors panels.

Next, the Group block gets vertical and horizontal block gap.

Group now declares its block gap support as both horizontal and vertical.

That means block gap in theme.json accepts either a plain string or an object with top and left keys.

The editor UI still only shows the separate controls for flex and grid layouts, which is where having two axes actually makes sense.

Then there are some updated block supports.

The List block gets wide and full alignment.

Query No Results gets border and spacing.

And the Query Loop gets block gap, which the article calls out as a long-time wishlist item. It's nice to see that one finally land.

And to wrap up themes, a bunch of smaller Global Styles items and fixes.

The Accordion Heading block now sends theme.json spacing to the toggle button instead of the wrapper.

Duotone palettes are editable in Global Styles.

Global Styles also shows you which blocks have custom styles, and you can filter by them.

Shadow presets keep storing as CSS variables when custom presets exist, which changes what ends up in a user's saved styles.

Block gap values are normalized more consistently.

There's one caveat on that one, though. The sanitizer rejects parentheses, so if you're using a literal calc or var value, it gets dropped. So go and test your stuff accordingly.

And the Table of Contents block stopped saving its output to post content.

* * *

Okay, the Playground section.

Playground now supports WebMCP.

That's a draft browser API for exposing actions as tools that an AI agent can call.

And because Playground runs WordPress inside a nested iframe, there's a new proxy that advertises the embedded site's tools on the outer page, then forwards the calls back down.

Now, registering a WordPress ability on its own isn't enough here. A plugin has to wrap it in a WebMCP tool.

I'm pretty excited about this one, so go and play around with it and see what you come up with.

Playground can also run WordPress releases all the way back to version 0.7.

Zero point seven!

If you tick "Include older versions" in the settings panel, the picker covers everything up through 6.2, and it pairs the right PHP version automatically.

This is super handy when you're trying to figure out when something broke, without having to build some ancient stack by hand.

And yes, some of those versions are older than a few of my plugins that are still out there, and I'm choosing not to think about that.

* * *

And finally, the resources section.

On the Developer Blog, we only had one post since the last roundup.

It's a hands-on look at the WordPress 7.1 Icon Registration API, so if you missed it, definitely go and check it out.

The article also has a list of other good stuff from the past month.

There's the What's New posts for Gutenberg 23.8 and 23.9, a proposal for a Secrets API for WordPress 7.2, and a post on replacing Dashicons in the admin bar and menu.

There's the Playground and WebMCP post, the WordCamp US 2026 PHP conversation, the WordPress 7.1 release retrospective, and the Core Security Initiative.

All sorts of great stuff in there, and the links are all in the article.

* * *

Well, that's it. That's the end of What's New for Developers for September 2026.

Thanks for hanging out with me while I nerd out over all this developer stuff.

My name's Ryan Welcher, developer advocate at Automattic.

If you haven't already, please give this video a thumbs up and subscribe to the channel, so we know we're making stuff you actually want to see.

I'm looking forward to seeing you all next month for October 2026.

Thanks a lot, and have a good one.
