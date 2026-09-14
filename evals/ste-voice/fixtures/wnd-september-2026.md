# What’s new for developers? (September 2026)

Source: https://developer.wordpress.org/news/2026/09/whats-new-for-developers-september-2026/

Last month was a fun one in the WordPress world as [version 7.1, “Mary Lou,”](https://wordpress.org/news/2026/08/mary-lou/) launched to the world. The release included responsive style states, icon registration, and more. If you haven’t updated already, it’s well past time. And if you haven’t caught up on all the developer goodies, be sure to catch up in [last month’s roundup](https://developer.wordpress.org/news/2026/08/whats-new-for-developers-august-2026/).

Since then, we’ve had a couple of new Gutenberg releases: [23.8](https://make.wordpress.org/core/2026/08/19/whats-new-in-gutenberg-23-8-19-august/) and [23.9](https://make.wordpress.org/core/2026/09/02/whats-new-in-gutenberg-23-9-2-september/). These continue building upon and fine-tuning previous work. Some of the changes in these releases may feel less glamorous than a lot of new APIs, but I expect a lot of major changes during the WordPress 7.2 development cycle over the next couple of months.

Speaking of WordPress 7.2, Beta 1 is scheduled for October 20-22, 2026, with the final release sometime between December 8-10. For the full release schedule, check out the [WordPress 7.2 dev cycle page](https://make.wordpress.org/core/7-2/).

As always, you can test the latest changes by running WordPress trunk along with the newest Gutenberg release, or by spinning up a [Playground instance](https://playground.wordpress.net/?php=8.0&wp=beta&networking=no&language=&multisite=no&random=y4q1rn88xn) with no setup at all.

Table of Contents

- [Highlights](#highlights)- [Runnable code examples land in the Code Reference](#runnable-code-examples-land-in-the-code-reference)
- [Block variations and transforms can declare their own keyboard shortcuts](#block-variations-and-transforms-can-declare-their-own-keyboard-shortcuts)
- [The extensible Site Editor is where features have to land now](#the-extensible-site-editor-is-where-features-have-to-land-now)

- [Plugins and tools](#plugins-and-tools)- [DataViews drops private APIs](#dataviews-drops-private-apis)
- [Inner block templates move into block settings](#inner-block-templates-move-into-block-settings)
- [Schema support for PHP-only blocks](#schema-support-for-php-only-blocks)
- [Consistent kebab case slug generation](#consistent-kebab-case-slug-generation)
- [Editors now use the admin color scheme](#editors-now-use-the-admin-color-scheme)
- [Time field for Data Views](#time-field-for-data-views)

- [Themes](#themes)- [States theme.json schema fixes](#states-theme-json-schema-fixes)
- [More options for curating the styles UI](#more-options-for-curating-the-styles-ui)
- [<label> now customizable via Global Styles](#label-now-customizable-via-global-styles)
- [Cite, text input, and select dropdown editable in Global Styles](#cite-text-input-and-select-dropdown-editable-in-global-styles)
- [Vertical and horizontal block gap added for Group](#vertical-and-horizontal-block-gap-added-for-group)
- [Updated block supports](#updated-block-supports)
- [Global styles and other fixes](#global-styles-and-other-fixes)

- [Playground](#playground)
- [Resources](#resources)- [Developer Blog](#developer-blog)
- [General](#general)

## Highlights

### Runnable code examples land in the Code Reference

The [Code Reference now runs its examples in the browser](https://make.wordpress.org/core/2026/09/04/runnable-code-examples-are-now-live-in-the-code-reference/). Open a page like [WP_HTML_Processor::class_list()](https://developer.wordpress.org/reference/classes/wp_html_processor/class_list/), hit Run, and the snippet executes against a real WordPress install powered by Playground. 

Examples are written directly in DocBlocks using a code fence named php interactive:

<?php
/**
 * Generator for a foreach loop to step through each class name for the matched tag.
 *
 * ```php interactive
 * $p = new WP_HTML_Tag_Processor( "<div class='free &lt;egg&gt;\tlang-en'>" );
 * $p->next_tag();
 * foreach ( $p->class_list() as $class_name ) {
 *   echo "{$class_name} ";
 * }
 * // Outputs: "free <egg> lang-en "
 * ```
 */
public function class_list() {}

This means the runnable example and the documented function live in the same file. The idea has been open as a [documentation proposal](https://github.com/WordPress/Documentation-Issue-Tracker/issues/730) in the documentation issue tracker for a while.

### Block variations and transforms can declare their own keyboard shortcuts

Gutenberg 23.9 added a [declarable API](https://github.com/WordPress/gutenberg/pull/81588) for block keyboard shortcuts. Alt+Shift+2 has converted a paragraph to a Heading 2 since 2022, but that behavior was hardcoded in a private component that each editor package had to render for itself.

There are two declaration sites, and the key names differ between them. Variations take a singular shortcut object:

wp.blocks.registerBlockVariation( 'core/heading', {
	name: 'h2',
	title: 'Heading 2',
	attributes: { level: 2 },
	isActive: ( blockAttributes ) => blockAttributes.level === 2,
	shortcut: {
		name: 'core/block-editor/transform-to-heading-2',
		description: __( 'Transform the selected block into a heading 2.' ),
		keyCombination: { modifier: 'access', character: '2' },
	},
} );

Transforms take a plural shortcuts array on a type: ‘block’ transform, plus an optional variationName so one transform can carry six shortcuts without appearing six times in the block switcher.

### The extensible Site Editor is where features have to land now

Gutenberg 23.9 carried roughly twenty PRs for the Boot package for Site Editor v2: an Identity route, a theme preview page with Global Styles editing, registered plugin mounting, canvas navigation between entity records, unsaved-changes warnings, and theme screens gated on theme support. You can follow along in the [extensible Site Editor iteration issue](https://github.com/WordPress/gutenberg/issues/79895).

The contributing guidelines now [require site editor features to land in the extensible site editor too](https://github.com/WordPress/gutenberg/pull/81752).

It is currently experimental, but if you extend the Site Editor, it’s worth keeping an eye on this progress.

## Plugins and tools

### DataViews drops private APIs

If you’ve bundled @wordpress/dataviews into a plugin, you may have hit Cannot unlock an object that was not locked before. The cause is that DataViews ships as a bundled package but reaches for private APIs, and two copies of @wordpress/private-apis in one runtime can’t unlock each other’s objects. [DataViews: remove all private API usage](https://github.com/WordPress/gutenberg/issues/81230) tracks the fix, which ends with dropping @wordpress/private-apis from the package entirely.

The happy side effect is that components DataViews depended on are getting public homes instead. Calendar and RangeCalendar [moved into @wordpress/ui](https://github.com/WordPress/gutenberg/pull/81337) rather than being copied, withIgnoreIMEEvents [landed in @wordpress/keycodes](https://github.com/WordPress/gutenberg/pull/81343), and ValidatedInputControl is [now public too](https://github.com/WordPress/gutenberg/pull/81627). Eght other Validated* controls were vendored into DataViews as internal code. But if you’ve been eyeing a Core component from behind the private API wall, a few more of them are now just imports.

### Inner block templates move into block settings

Gutenberg 23.8 added [template and templateInsertUpdatesSelection as block type settings](https://github.com/WordPress/gutenberg/pull/80027), replacing the <InnerBlocks> props of the same names:

registerBlockType( 'core/list', {
	template: [ [ 'core/list-item' ] ],
	templateInsertUpdatesSelection: true,
	// …
} );

The change is because of ongoing work on real-time collaboration. The prop-based path applied the template after mount, on each connected client—so inserting a List block with three collaborators in the document produced three list items. Moving the declaration into block type settings means the block and its template land in a single store operation.

Roughly twenty core blocks have been migrated. The props still work, but they’re deprecated, so if your block ships an inner block template, you’ll want to make the change before 7.2 is released.

### Schema support for PHP-only blocks

The autoRegister flag is now [in the block.json schema](https://github.com/WordPress/gutenberg/pull/80173). This means code editor autocomplete and validation for a feature that has technically worked since WordPress 7.0. For a full reference, the [PHP-only block registration dev note](https://make.wordpress.org/core/2026/03/03/php-only-block-registration/) from March 2026 is still the best overview.

### Consistent kebab case slug generation

WordPress Core’s _wp_to_kebab_case() uses semantics that differ from many off-the-shelf libraries, particularly around numbers. That’s now available as [the @wordpress/kebab-case package](https://github.com/WordPress/gutenberg/pull/81294) instead of a private utility on the JavaScript side of things.

Usage in JS will produce the same output as in PHP:

kebabCase( 'white2white' ); // 'white-2-white'
kebabCase( 'font2xl' );     // 'font-2-xl'
kebabCase( 'white4th' );    // 'white-4th'

### Editors now use the admin color scheme

The post editor, widgets editor, and customizer widgets editor are now wrapped in a ThemeProvider [seeded from the active admin color scheme](https://github.com/WordPress/gutenberg/pull/81112).

The useful part for extenders is that getAdminThemeColors() is a public export of @wordpress/admin-ui. It reads the admin-color-* body class and returns primary and background values, which means you can do the same two-line wrap on your own admin screens and have design-system components pick up the user’s chosen scheme automatically.

### Time field for Data Views

Gutenberg 23.8 added a time [field type and control](https://github.com/WordPress/gutenberg/pull/80830). This can be useful for things like business hours, event start times, booking slots, or anything where the value is a time of day. Note that there is no date.

Values are stored as HH:mm or HH:mm:ss, so 9:00am reads as 9:00am for every visitor regardless of their timezone. For specific moments, datetime is still the right type.

## Themes

### States theme.json schema fixes

Responsive style and pseudo-class states shipped with WordPress 7.1, but the schema that validates them was not complete. Several fixes landed in Gutenberg 23.8.

These changes will ensure that states do not appear as invalid when viewing theme.json in your code editor:

- [Responsive states for style variations](https://github.com/WordPress/gutenberg/pull/81309)

- [Responsive states are specific to blocks](https://github.com/WordPress/gutenberg/pull/81253) (not elements)

- [Corrected errors with pseudo-class styling](https://github.com/WordPress/gutenberg/pull/81209)

### More options for curating the styles UI

Gutenberg 23.8 [added an opt-out](https://github.com/WordPress/gutenberg/pull/80956) for the block style state controls: a blockStatesEditingEnabled and responsiveEditingEnabled. Both are filterable through block_editor_settings_all:

add_filter( 'block_editor_settings_all', function ( $settings ) {
	$settings['blockStatesEditingEnabled'] = false;
	$settings['responsiveEditingEnabled']  = false;
	return $settings;
} );

Both default to true. Styles already defined in theme.json, Global Styles, or a block’s style attribute keep rendering either way. That makes them useful for locking down a client build without breaking the design you shipped with it.

### <label> now customizable via Global Styles

Gutenberg 23.9 added <label> as a new element to style via theme.json. You can customize it via styles.elements.label like other element styles. It applies to any markup rendering a <label>. In Core that covers the Search, Form Input, Post Comments Form, Archives, and Categories blocks. It will also apply to third-party blocks.

### Cite, text input, and select dropdown editable in Global Styles

cite, textInput, and select were already supported via theme.json. But a recent [PR made them editable](https://github.com/WordPress/gutenberg/pull/80852) via the Styles interface in the editor under the Typography and Colors panels.

### Vertical and horizontal block gap added for Group

The Group block now declares its blockGap support as [both horizontal and vertical](https://github.com/WordPress/gutenberg/pull/81476). This means that the blockGap property in theme.json accepts both a plain string or an object with top and left keys.

The editor UI continues to restrict the axial controls to flex and grid layouts, which is where the separate axes would be useful.

### Updated block supports

A few blocks gained new supports, making it easier to use them across a variety of layouts:

- List: [wide and full alignment](https://github.com/WordPress/gutenberg/pull/68002)

- Query No Results: [border and spacing](https://github.com/WordPress/gutenberg/pull/64601)

- Query Loop: [block gap](https://github.com/WordPress/gutenberg/pull/79689) (this one has been on my wishlist for a long time!)

### Global styles and other fixes

Several other smaller items landed that are worth a look:

- The Accordion Heading block now [routes theme.json spacing to the toggle button](https://github.com/WordPress/gutenberg/pull/81976) rather than the wrapper.

- Duotone palettes are [editable in Global Styles](https://github.com/WordPress/gutenberg/pull/81605).

- Global Styles also [indicates which blocks have custom styles](https://github.com/WordPress/gutenberg/pull/81373) and lets you filter by them.

- Shadow presets [keep storing as CSS variables when custom presets exist](https://github.com/WordPress/gutenberg/pull/81346), which affects what lands in a user’s saved styles.

- blockGap values are [normalized more consistently](https://github.com/WordPress/gutenberg/pull/81460). Note that the sanitizer rejects parentheses, so literal calc() or var() values are dropped.

- The Table of Contents block [stopped saving its output](https://github.com/WordPress/gutenberg/pull/80404) to post content.

## Playground

Playground now [supports WebMCP](https://make.wordpress.org/playground/2026/09/05/wordpress-playground-and-webmcp-bringing-ai-agents-into-your-browser-workflow/), a draft browser API for exposing actions as tools an AI agent can call. Because Playground runs WordPress in a nested iframe, a new proxy advertises the embedded site’s tools on the outer page and forwards calls back down. Note that registering a WordPress ability isn’t enough on its own. A plugin has to wrap it in a WebMCP tool.

Playground can also [run releases back to version 0.7](https://make.wordpress.org/playground/2026/08/24/run-any-era-of-wordpress-in-playground/). Tick Include older versions in the settings panel and the picker covers everything through 6.2, with PHP pairing automatically. This is handy for answering “when did this break?” without rebuilding an old stack by hand.

## Resources

### Developer Blog

We’ve only had one post since the last monthly roundup. Check it out if you missed it:

- [Hands-on with the WordPress 7.1 Icon Registration API](https://developer.wordpress.org/news/2026/08/hands-on-with-the-wordpress-7-1-icon-registration-api/)

### General

Also worth a read from the past month:

- [What’s new in Gutenberg 23.8?](https://make.wordpress.org/core/2026/08/19/whats-new-in-gutenberg-23-8-19-august/)

- [What’s new in Gutenberg 23.9?](https://make.wordpress.org/core/2026/09/02/whats-new-in-gutenberg-23-9-2-september/)

- [Proposal: A Secrets API for WordPress 7.2](https://make.wordpress.org/core/2026/08/25/proposal-a-secrets-api-for-wordpress-7-2/)

- [Replacing Dashicons in the Admin Bar and Menu](https://make.wordpress.org/core/2026/09/04/replacing-dashicons-in-the-admin-bar-and-menu/)

- [WordPress Playground and WebMCP: bringing AI agents into your browser workflow](https://make.wordpress.org/playground/2026/09/05/wordpress-playground-and-webmcp-bringing-ai-agents-into-your-browser-workflow/)

- [WordCamp US 2026: PHP Conversation](https://make.wordpress.org/core/2026/09/03/wordcamp-us-2026-php-conversation/)

- [WordPress 7.1 Release Retrospective](https://make.wordpress.org/core/2026/09/07/wordpress-7-1-release-retrospective/)

- [The Core Security Initiative](https://make.wordpress.org/core/2026/08/28/xpost-the-core-security-initiative/)

Props to @welcher for feedback and review on this article.
