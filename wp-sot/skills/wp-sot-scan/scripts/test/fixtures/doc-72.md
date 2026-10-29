# **WordPress 7.2 Source of Truth: Draft**

Running draft, in post order. Research and links for each item live in the Notes. Punted items stay in the notes doc and never go into the draft. HTML comments (`<!-- -->`) hold working notes and come out before publishing.

**Emoji key**

* ✏️ To be edited  
* 🙏 Blessed feature: will be developed during the Beta cycle  
* 🔍 To-do or double-check  
* 🎨 Visuals being edited or created  
* 🏈 Confirmed punted to the next release

---

# WordPress 7.2 Source of Truth

Welcome to the Source of Truth for WordPress 7.2\!

Before you dive headfirst into all the big and small changes and pick your favorites, make sure to read these preliminary thoughts about this post and how to use it. If you have any questions, leave a comment. 

A huge "Thank you" to everyone who helped review this post.  It still takes a village. Also, huge respect to the whole release squad for getting WordPress 7.2 over the finish line.

\<\!-- ✏️ Add collaborator credits and contact line.  \--\>

## Changelog

Any changes are cataloged here as the release goes on.

**✏️ Month Day, 2026**: First edition.

## Important note/guidelines

Try not to just copy and paste what's in this post since it's going to be shared with plenty of folks. Use this as inspiration for your own stuff and to get the best info about this release. If you do copy and paste, just remember that others might do the same, and it could lead to some awkward moments with duplicate content floating around online.

* Each item has been tagged using best guesses with different high-level labels so that you can more readily see at a glance who is likely to be most impacted.  
* Each item has a high-level description, visuals (if relevant), and key resources if you would like to learn more.

## Overview 🔍 🎨

*Note: As always, what's shared here is being actively pursued but doesn't necessarily mean each will make it into the final release of WordPress 7.2.*

WordPress 7.2 brings a fresh starting point with Ipsum, a minimal new default theme and the first since Twenty Ten that isn't named after the year. It's designed as a blank canvas for blogging, with nearly all of its design editable in Global Styles.

Much of this release fills in gaps. Dozens of Core blocks pick up design tools they were missing, from backgrounds and shadows to minimum widths and duotone. Responsive styles and interactive states from 7.1 reach more controls, and Global Styles can now style form elements, custom duotone palettes, and Navigation Link states.

Collaboration inside the editor keeps improving, too. Notes move into a margin beside the canvas, where they stay visible while you work, and people you mention get an email.

Beyond the headliners, writing in the editor gets smoother with a long list of small fixes, and developers get public APIs for responsive controls, Interactivity API additions, and new components.

WordPress 7.2 is scheduled for release on December 8, 2026\.

\<\!-- 🎨 Highlight grid image \+ caption linking the grid's GitHub comment. 🔍 Revisit the narrative after Beta 1 and again at RC 1\. \--\>

### Resources

* Help Test WordPress 7.2 🔍  
* Follow along with [Dev Notes published](https://make.wordpress.org/core/tag/dev-notes+7-2/).  
* WordPress 7.2 Field Guide (expected at RC 1\) 🔍  
* [Roadmap to 7.2](https://make.wordpress.org/core/2026/09/18/roadmap-to-7-2/)  
* [WordPress 7.2 Development Cycle](https://make.wordpress.org/core/7-2/)  
* **What's new for developers:** [September](https://developer.wordpress.org/news/2026/09/whats-new-for-developers-september-2026/), [October](https://developer.wordpress.org/news/2026/10/whats-new-for-developers-october-2026/)

This release consists of features from the Gutenberg plugin versions 23.7 – 24.2 🔍. Here are the release posts of those plugin releases: [23.7](https://make.wordpress.org/core/2026/08/06/whats-new-in-gutenberg-23-7-05-august/) \| [23.8](https://make.wordpress.org/core/2026/08/19/whats-new-in-gutenberg-23-8-19-august/) \| [23.9](https://make.wordpress.org/core/2026/09/02/whats-new-in-gutenberg-23-9-2-september/) \| [24.0](https://make.wordpress.org/core/2026/09/16/whats-new-in-gutenberg-24-0-16-september/) \| [24.1](https://make.wordpress.org/core/2026/09/30/whats-new-in-gutenberg-24-1-30-september/) \| [24.2](https://make.wordpress.org/core/2026/10/14/whats-new-in-gutenberg-24-2-14-october/). Later Gutenberg releases contain bug fixes, backported to the WordPress 7.2 release branch.

### Assets ✏️

In this Google Drive folder you can view all assets in this document.

### Tags

To make this document easier to navigate based on specific audiences, the following tags are used liberally:

* **\[end user\]**: end user focus.  
* **\[theme builder\]**: block or classic theme author.  
* **\[plugin author\]**: plugin author, whether block or otherwise.  
* **\[developer\]**: catch-all term for more technical folks.  
* **\[site admin\]**: this includes a "builder" type.  
* **\[enterprise\]**: specific items that would be of interest to or particularly impact enterprise-level folks.  
* **\[all\]**: broad impact to every kind of WordPress user.

How can you use these? Use your browser's **Find** capability and search for the string including the brackets. Then use the arrows to navigate through the post from one result to the next.

\<\!-- 🎨 Reuse the short video on navigating by tags from past editions. \--\>

## Priority Items for WordPress 7.2

### Ipsum, the new default theme 🔍 🎨

\==\[all\] \[theme builder\]==

WordPress 7.2 ships with Ipsum, a new default theme and the first since Twenty Ten that isn't named after the year. It's an intentionally minimal blog theme built as a blank canvas: headers, heroes, and sidebars are there when you need them and stay out of the way when you just want to write. Style variations restyle the whole page, images included, and every color combination meets WCAG AA contrast.

Ipsum ships with very little CSS. Most of its design lives in `theme.json`, so nearly everything is editable in Global Styles, which also makes it a good reference for anyone building block themes.

The theme is still in development, so expect changes during the beta period. You can [try Ipsum in Playground](https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/WordPress/ipsum/trunk/.github/blueprint.json) or download it from the [Ipsum GitHub repository](https://github.com/WordPress/ipsum) and [report issues](https://github.com/WordPress/ipsum/issues) there.

Read the announcement: [Introducing Ipsum, the new default theme](https://make.wordpress.org/core/2026/09/16/introducing-ipsum-the-new-default-theme/)

\<\!-- 🔍 Confirm Ipsum is committed to Core for Beta 1, and that the Playground link loads. 🎨 Screenshot plus style variation grid. \--\>

### Notes move into the canvas margin 🔍 🎨

\==\[end user\] \[site admin\] \[enterprise\]==

Notes now sit in a margin beside the editor canvas instead of floating over it, so you can keep a conversation open while you change block or post settings ([\#83786](https://github.com/WordPress/gutenberg/pull/83786), [\#83852](https://github.com/WordPress/gutenberg/pull/83852)). On narrower screens, threads collapse to the author's avatar. A new **Notes** submenu in the **Options** menu lets you expand, minimize, or hide them ([\#83768](https://github.com/WordPress/gutenberg/pull/83768)).

A few smaller changes protect your work: deleting a note offers **Undo** ([\#83988](https://github.com/WordPress/gutenberg/pull/83988)), unsent notes and replies are kept when you select another block ([\#84110](https://github.com/WordPress/gutenberg/pull/84110)), and people you @mention now get an email linking to the post ([\#79606](https://github.com/WordPress/gutenberg/pull/79606)).

Notes also get emoji reactions, so you can acknowledge feedback without adding another reply ([\#76767](https://github.com/WordPress/gutenberg/pull/76767)). The **Add note** button in the block toolbar now only adds notes ([\#84635](https://github.com/WordPress/gutenberg/pull/84635)), and highlights connect more clearly to the text they're attached to ([\#80578](https://github.com/WordPress/gutenberg/pull/80578)). \<\!-- 🔍 Merged after Gutenberg 24.2 (Oct 16–19); confirm it's in Beta 1\. \--\>

Tracking: [Notes iteration for WordPress 7.2](https://github.com/WordPress/gutenberg/issues/80015) (\#80015)

\<\!-- 🔍 Mention emails: Core changeset 63012 (Aug 4, @since 7.1.0) may have shipped in 7.1. Remove if so. 🎨 Short video of the margin, avatars, and Notes submenu. \--\>

### Design tools for nearly every Core block 🔍 🎨

\==\[theme builder\] \[site admin\] \[end user\]==

Across Gutenberg 24.1 and 24.2, contributors switched on existing design tools for dozens of Core blocks that didn't have them yet. There are no new controls to learn, just fewer cases where you need a wrapper Group block or custom CSS to get the look you want. Highlights include:

* **Background image, size, and gradient:** Buttons, Columns, Heading, List, Media & Text, Gallery, Tabs, and more ([\#83203](https://github.com/WordPress/gutenberg/pull/83203), [\#83226](https://github.com/WordPress/gutenberg/pull/83226)).  
* **Shadow:** Paragraph, Heading, List, Buttons, Gallery, Quote, Video, and more ([\#83926](https://github.com/WordPress/gutenberg/pull/83926), [\#83045](https://github.com/WordPress/gutenberg/pull/83045)).  
* **Minimum width and height:** Heading, Columns, Buttons, Embed, Gallery, and more ([\#83580](https://github.com/WordPress/gutenberg/pull/83580), [\#83895](https://github.com/WordPress/gutenberg/pull/83895)).  
* **Link, heading, and button colors:** Accordion, Tabs, Quote, Details, Post Template ([\#83390](https://github.com/WordPress/gutenberg/pull/83390), [\#83371](https://github.com/WordPress/gutenberg/pull/83371)).  
* **Duotone:** Gallery, Video, and Media & Text ([\#83978](https://github.com/WordPress/gutenberg/pull/83978), [\#83979](https://github.com/WordPress/gutenberg/pull/83979), [\#83981](https://github.com/WordPress/gutenberg/pull/83981)).  
* **Fit text:** Post Title, Site Title, Site Tagline, and Poetry ([\#83036](https://github.com/WordPress/gutenberg/pull/83036), [\#82074](https://github.com/WordPress/gutenberg/pull/82074), [\#83980](https://github.com/WordPress/gutenberg/pull/83980)). \<\!-- 🔍 Post Title (\#83036) merged Oct 19; confirm it's in Beta 1\. \--\>

The Group block can also set separate horizontal and vertical gaps in flex and grid layouts ([\#81476](https://github.com/WordPress/gutenberg/pull/81476)).

Theme builders can set all of these in `theme.json` under `styles.blocks`. If your theme styles links inside Accordion, Tabs, or Post Template with custom CSS, check for specificity conflicts with the new `has-link-color` classes. The full list is in the [Gutenberg 24.1](https://github.com/WordPress/gutenberg/releases/tag/v24.1.0) and [Gutenberg 24.2](https://make.wordpress.org/core/2026/10/14/whats-new-in-gutenberg-24-2-14-october/) changelogs.

Tracking: [Block supports and design tools](https://github.com/WordPress/gutenberg/issues/76525) (\#76525)

\<\!-- 🔍 \#76525 is still titled for 7.1; look for a 7.2 tracking issue. 🎨 Before/after of the Styles panel on a block that gained background and shadow. \--\>

### Responsive styles and states, round two 🔍 🎨

\==\[theme builder\] \[plugin author\] \[site admin\]==

Responsive styles and interactive states arrived in WordPress 7.1, and 7.2 extends them. You can now set a block's position per viewport ([\#83094](https://github.com/WordPress/gutenberg/pull/83094)) and add custom CSS for a specific state ([\#83539](https://github.com/WordPress/gutenberg/pull/83539)). The Gallery block's columns, crop, and aspect ratio can change by screen size, too ([\#82003](https://github.com/WordPress/gutenberg/pull/82003), [\#82233](https://github.com/WordPress/gutenberg/pull/82233)).

Navigation Link blocks get hover, focus, and active controls in Global Styles ([\#83451](https://github.com/WordPress/gutenberg/pull/83451)), so you can style menu states across your site without editing `theme.json`.

For block developers, the viewport API is now public. Custom blocks can use `getStyleForState()` and `setStyleForState()` from `@wordpress/block-editor` to make their own controls work per viewport ([\#82741](https://github.com/WordPress/gutenberg/pull/82741)).

Tracking: [Responsive style states for blocks, 7.2 tasks](https://github.com/WordPress/gutenberg/issues/80388) (\#80388)

\<\!-- 🔍 Confirm \#83539 covers both viewport and pseudo states; check for a 7.2 dev note on the public viewport API. 🎨 Screenshot of Navigation Link state controls in Global Styles. \--\>

### Global Styles: form elements, duotone palettes, and more 🔍 🎨

\==\[site admin\] \[theme builder\] \[end user\]==

Global Styles can now style more of the elements that make up your site. Citations, text inputs, and select dropdowns get typography and color controls ([\#80852](https://github.com/WordPress/gutenberg/pull/80852)), and themes can style `<label>` elements through `theme.json` ([\#81160](https://github.com/WordPress/gutenberg/pull/81160)). Search, comment, and plugin forms can now match the rest of your design without custom CSS.

You can also create your own duotone palettes in a new **Duotone** tab instead of relying only on the theme's ([\#81605](https://github.com/WordPress/gutenberg/pull/81605)). Elements like links, buttons, and headings are now listed alongside blocks in Global Styles ([\#81645](https://github.com/WordPress/gutenberg/pull/81645)), and element screens preview the state you're styling, such as hover ([\#83787](https://github.com/WordPress/gutenberg/pull/83787)). \<\!-- 🔍 Merged after Gutenberg 24.2 (Oct 16–19); confirm it's in Beta 1\. \--\>

When you're tracking down a stray style, Global Styles also marks blocks that have custom styles with a dot and lets you filter the list to show only those blocks ([\#81373](https://github.com/WordPress/gutenberg/pull/81373)).

In the block inspector, controls now show the values a block inherits from Global Styles instead of appearing empty, so you can see what you're overriding before you change anything ([\#82840](https://github.com/WordPress/gutenberg/pull/82840)).

Tracking: [Form elements in Global Styles](https://github.com/WordPress/gutenberg/issues/34198) (\#34198) and [Display inherited Global Styles and local overrides](https://github.com/WordPress/gutenberg/issues/82520) (\#82520)

\<\!-- 🔍 Confirm \#34198 is the right tracking link (the fetched page looked like a separate 7.2 iteration issue citing it). Confirm inherited values show by default in 7.2 (indicators stay behind the experiment). 🎨 Screenshot of the custom-styles filter and the Duotone tab. \--\>

## New Blocks

### Description List block 🔍

\==\[end user\] \[site admin\]==

The new Description List block is for content built from terms and their descriptions, such as glossaries, specifications, event details, or FAQs. It outputs proper `<dl>`, `<dt>`, and `<dd>` markup, so browsers and assistive technologies understand how each term relates to its description. Inside the block, you add Term and Detail blocks in whatever order you need. Press \<kbd\>Tab\</kbd\> to turn a term into a detail, or \<kbd\>Shift\</kbd\>+\<kbd\>Tab\</kbd\> to turn it back ([\#81728](https://github.com/WordPress/gutenberg/pull/81728)).

Tracking: [Block for description list](https://github.com/WordPress/gutenberg/issues/4880) (\#4880)

\<\!-- 🔍 At risk: \#81728 was not merged as of Oct 16, and review questions (dt/dd content model, side-by-side layout, Enter behavior, block naming) were still open. Remove if it misses Beta 1 and isn't blessed. 🎨 Screenshot once merged. \--\>

### Table of Contents block 🔍

\==\[end user\] \[theme builder\]==

After several years as an experiment, the Table of Contents block is set to become available to everyone. It now builds its list from the post's headings on the server instead of saving a static copy, so it stays up to date whenever headings change ([\#80318](https://github.com/WordPress/gutenberg/pull/80318), [\#80404](https://github.com/WordPress/gutenberg/pull/80404)). Turning it into a static list is now a confirmed **Detach** action ([\#80844](https://github.com/WordPress/gutenberg/pull/80844)), and the block gained background, shadow, and text alignment support.

Tracking: [Stabilize the Table of Contents Block](https://github.com/WordPress/gutenberg/issues/42229) (\#42229)

\<\!-- 🔍 At risk: no stabilization PR found on trunk as of Oct 16\. The editor preview of unsaved headings (\#84642) is an open draft, and 7 of 17 tracking tasks were checked. Remove if it stays experimental. 🎨 Screenshot once stabilized. \--\>

## Improved Blocks and Block handling

Core blocks pick up a long list of refinements in 7.2, from sorting galleries to finding links and icons faster.

### Gallery: sort, shuffle, and a Grid variation 🔍 🎨

\==\[end user\] \[site admin\]==

The Gallery block's **Order by** control now works on images you've picked by hand, not just dynamic galleries, and a **Random** option shuffles the images on every page load ([\#83438](https://github.com/WordPress/gutenberg/pull/83438)). A new Grid variation gives you a quick way to start with a grid layout ([\#81909](https://github.com/WordPress/gutenberg/pull/81909)).

Dynamic galleries from 7.1 get some polish, too. The toolbar button that converts one into a regular gallery is now called **Detach**, with a modal explaining what happens, and the change is a single undo step ([\#80727](https://github.com/WordPress/gutenberg/pull/80727), [\#80665](https://github.com/WordPress/gutenberg/pull/80665)). In the lightbox, clicking an image no longer closes it when navigation is turned on ([\#78898](https://github.com/WordPress/gutenberg/pull/78898)).

Tracking: [WordPress 7.2: Dynamic galleries and media inserter](https://github.com/WordPress/gutenberg/issues/81370) (\#81370)

\<\!-- 🎨 Short video of Order by and Random. \--\>

### Navigation: one search for every link 🔍

\==\[site admin\] \[end user\]==

When you add a link to a Navigation block, a single search now covers every kind of content at once and shows each result's type. Posts and pages are ranked ahead of categories, tags, and media, so the link you most likely want is near the top ([\#83408](https://github.com/WordPress/gutenberg/pull/83408), [\#83652](https://github.com/WordPress/gutenberg/pull/83652), [\#83407](https://github.com/WordPress/gutenberg/pull/83407)). The Navigation Link block also has a new name in the editor, with Custom Link as its default variation ([\#82375](https://github.com/WordPress/gutenberg/pull/82375)).

In the Site Editor sidebar, you can now edit menu links in a popover straight from List View ([\#84005](https://github.com/WordPress/gutenberg/pull/84005)), and an empty menu shows an inserter so you can start adding links ([\#84003](https://github.com/WordPress/gutenberg/pull/84003)). The link popover can also set **Open in new tab** directly ([\#83506](https://github.com/WordPress/gutenberg/pull/83506)).

Tracking: [Improve Navigation Editing in the Extensible Site Editor Sidebar](https://github.com/WordPress/gutenberg/issues/77069) (\#77069)

\<\!-- 🔍 Confirm the Navigation Link block's new display name. Sidebar editing and Open in new tab merged Oct 16–19, after Gutenberg 24.2; confirm they're in Beta 1\. \--\>

### Icon block: search by keyword 🔍

\==\[end user\] \[site admin\]==

Searching in the Icon block now matches keywords, not just icon names, so typing "hamburger" finds the Menu icon ([\#82367](https://github.com/WordPress/gutenberg/pull/82367), [\#83884](https://github.com/WordPress/gutenberg/pull/83884)). The block's `icon` attribute also supports Block Bindings, so the icon can come from a custom field or other source ([\#80730](https://github.com/WordPress/gutenberg/pull/80730)).

### General quality of life improvements ✏️

\==\[end user\] \[site admin\]==

* **Columns:** The column count slider is gone. Add columns with a plus button instead ([\#83262](https://github.com/WordPress/gutenberg/pull/83262)), and transform Columns into a Row ([\#81802](https://github.com/WordPress/gutenberg/pull/81802)).  
* **Button:** The link popover opens only when you ask for it, not every time you select the block ([\#30166](https://github.com/WordPress/gutenberg/pull/30166)).  
* **Cover and Media & Text:** A new Media section in the block inspector ([\#82751](https://github.com/WordPress/gutenberg/pull/82751), [\#82593](https://github.com/WordPress/gutenberg/pull/82593)), plus an **Add Media** button in the Media & Text toolbar ([\#82420](https://github.com/WordPress/gutenberg/pull/82420)).  
* **Video and Cover:** Autoplay respects the visitor's reduced-motion preference ([\#83337](https://github.com/WordPress/gutenberg/pull/83337), [\#83452](https://github.com/WordPress/gutenberg/pull/83452)).  
* **List:** \<kbd\>Tab\</kbd\> indents and \<kbd\>Shift\</kbd\>+\<kbd\>Tab\</kbd\> outdents selected list items, including multiple at once ([\#82411](https://github.com/WordPress/gutenberg/pull/82411), [\#82460](https://github.com/WordPress/gutenberg/pull/82460)). The block also supports alignment ([\#68002](https://github.com/WordPress/gutenberg/pull/68002)).  
* **Tabs:** Content in inactive tabs can be found with your browser's Find feature ([\#81743](https://github.com/WordPress/gutenberg/pull/81743)).  
* **Query Loop:** The "Keyword" filter is now "Search terms," with help text ([\#82387](https://github.com/WordPress/gutenberg/pull/82387)).  
* **Playlist:** Edit metadata for several tracks at once ([\#81441](https://github.com/WordPress/gutenberg/pull/81441)).  
* **Math:** Improved inline math UI ([\#77743](https://github.com/WordPress/gutenberg/pull/77743)), and LaTeX errors appear when you leave the field instead of on every keystroke ([\#80500](https://github.com/WordPress/gutenberg/pull/80500)).  
* **Page List:** Converting to a static list is now a confirmed **Detach** action ([\#80847](https://github.com/WordPress/gutenberg/pull/80847)).  
* **Backgrounds:** Set a background image from a URL ([\#82230](https://github.com/WordPress/gutenberg/pull/82230)).  
* **Alignments:** Wide and full alignment options show as unavailable instead of disappearing when a theme doesn't support them ([\#82600](https://github.com/WordPress/gutenberg/pull/82600)).

## Editor enhancements

Beyond blocks, the editing experience itself gets smoother, with fewer paper cuts and better ways to work with media and revisions.

### Fewer paper cuts while writing 🔍 🎨

\==\[end user\]==

A long-running effort to fix everyday editing annoyances continues. You can now insert a block straight from the parent selector in the block toolbar ([\#81532](https://github.com/WordPress/gutenberg/pull/81532)), press \<kbd\>Enter\</kbd\> to select the next block ([\#63484](https://github.com/WordPress/gutenberg/pull/63484)), and apply formatting across several blocks at once ([\#58913](https://github.com/WordPress/gutenberg/pull/58913)). Multi-selection works on mobile browsers ([\#81542](https://github.com/WordPress/gutenberg/pull/81542)), and the in-between inserter shows up on wrapped lines ([\#83276](https://github.com/WordPress/gutenberg/pull/83276)).

Keyboard users can press \<kbd\>Escape\</kbd\> to leave the editor canvas and \<kbd\>Enter\</kbd\> to go back in ([\#82314](https://github.com/WordPress/gutenberg/pull/82314)), and non-breaking spaces are now marked while you edit, with a button to replace them ([\#74040](https://github.com/WordPress/gutenberg/pull/74040), [\#84737](https://github.com/WordPress/gutenberg/pull/84737)). You can also drag a multi-selection by grabbing anywhere inside it ([\#81602](https://github.com/WordPress/gutenberg/pull/81602)). \<\!-- 🔍 \#84737 and \#81602 merged Oct 18; confirm they're in Beta 1\. \--\>

Tracking: [Block Editor Paper Cuts](https://github.com/WordPress/gutenberg/issues/81453) (\#81453)

### Media editor: restore the original image 🔍 🎨

\==\[end user\] \[site admin\]==

The media editor modal from 7.1 can now restore an image to its original, uncropped version from the **More options** menu ([\#81805](https://github.com/WordPress/gutenberg/pull/81805)). WordPress keeps track of which original an edited image came from to make this possible ([\#81803](https://github.com/WordPress/gutenberg/pull/81803)).

Images are also attached to the post when you save it. Unattached images in Image and Gallery blocks get the current post as their parent, which makes the **Uploaded to this post** filter and dynamic galleries more useful ([\#81977](https://github.com/WordPress/gutenberg/pull/81977)). This is skipped on sites with attachment pages turned on, and on published posts only newly added images are attached ([\#84851](https://github.com/WordPress/gutenberg/pull/84851), [\#84890](https://github.com/WordPress/gutenberg/pull/84890)).

Animated images now get animated sub-sizes when you upload them, instead of only a still first frame ([\#80385](https://github.com/WordPress/gutenberg/pull/80385)). \<\!-- 🔍 \#80385 merged Oct 16; confirm it's in Beta 1 and whether it applies only to client-side processing. \--\>

Tracking: [WordPress 7.2 Iteration: Media Editor Modal](https://github.com/WordPress/gutenberg/issues/80389) (\#80389)

\<\!-- 🔍 Confirm how to turn off auto-attaching (\`autoAttachMediaEnabled\` editor setting). \--\>

### Visual revisions polish 🔍

\==\[end user\] \[site admin\]==

Visual revisions now show changes to the post title ([\#82586](https://github.com/WordPress/gutenberg/pull/82586)), and adjacent inline changes are merged so the differences are easier to read ([\#80579](https://github.com/WordPress/gutenberg/pull/80579)). The Global Styles revisions screen also moved to the same DataViews layout used elsewhere in the editor ([\#80856](https://github.com/WordPress/gutenberg/pull/80856)).

Tracking: [Visual Revisions: post-7.0 polish](https://github.com/WordPress/gutenberg/issues/79120) (\#79120)

You can also share a link to a specific revision ([\#79934](https://github.com/WordPress/gutenberg/pull/79934)) and compare revisions in a code diff view from the **Options** menu ([\#80314](https://github.com/WordPress/gutenberg/pull/80314)).

\<\!-- 🔍 On hold: shareable URLs (\#79934) and the code diff view (\#80314) merged Aug 3 in Gutenberg 23.8. Check whether they shipped in 7.1; remove this paragraph if so. \--\>

### Clearer error screens 🔍

\==\[all\]==

When something breaks in the editor, the error screen now explains what happened in plainer language and includes a button to copy the error details, so it's easier to report the problem or share it with your developer ([\#76470](https://github.com/WordPress/gutenberg/pull/76470), [\#82496](https://github.com/WordPress/gutenberg/pull/82496)). Debugging details are available right in the error screen ([\#81642](https://github.com/WordPress/gutenberg/pull/81642)), and the Site Editor no longer falls back to a blank screen when one part fails ([\#82486](https://github.com/WordPress/gutenberg/pull/82486)).

Background: [Defensive data design](https://make.wordpress.org/core/2026/08/04/defensive-data-design/)

\<\!-- 🔍 \#82496 (merged Oct 16\) adds a copy option and a show/hide details button for save failures; confirm what \#76470 changes. 🎨 Screenshot of the new error screen. \--\>

### Smaller editor improvements ✏️

* The **Options** menu groups its view settings into **Appearance**, **Notes**, and **Panels** submenus ([\#82976](https://github.com/WordPress/gutenberg/pull/82976)).  
* The post author field is searchable and finds users on the server, which helps on sites with many authors ([\#83323](https://github.com/WordPress/gutenberg/pull/83323)).  
* New posts no longer get published with an `auto-draft` slug ([\#83518](https://github.com/WordPress/gutenberg/pull/83518)).  
* The starter patterns modal can filter patterns by category ([\#81396](https://github.com/WordPress/gutenberg/pull/81396)).  
* The Command Palette has a **View post** command ([\#66720](https://github.com/WordPress/gutenberg/pull/66720)).  
* In the inserter, "My patterns" is now "Site patterns," with a filter by author ([\#84680](https://github.com/WordPress/gutenberg/pull/84680)). \<\!-- 🔍 Merged after Gutenberg 24.2 (Oct 16–19); confirm it's in Beta 1\. \--\>  
* Restoring a revision first saves any unsaved changes as their own revision, so nothing is lost ([\#84590](https://github.com/WordPress/gutenberg/pull/84590)), and the browser backup notice shows the backup's date before you restore it ([\#84735](https://github.com/WordPress/gutenberg/pull/84735)). \<\!-- 🔍 Merged after Gutenberg 24.2 (Oct 16–19); confirm it's in Beta 1\. \--\>  
* Snackbar notices with an action, like **Undo**, stay on screen longer ([\#84842](https://github.com/WordPress/gutenberg/pull/84842)). \<\!-- 🔍 Merged after Gutenberg 24.2 (Oct 16–19); confirm it's in Beta 1\. \--\>  
* The inserter opens faster and doesn't re-render every item when the selection changes ([\#83437](https://github.com/WordPress/gutenberg/pull/83437), [\#83284](https://github.com/WordPress/gutenberg/pull/83284)).  
* **Select all** in List View is much faster on long posts: on a post with 1,000 blocks, it dropped from 16.8 seconds to 0.4 seconds ([\#81210](https://github.com/WordPress/gutenberg/pull/81210)).  
* The post editor and widgets editors now use your admin color scheme ([\#81112](https://github.com/WordPress/gutenberg/pull/81112)). \<\!-- 🔍 On hold: 23.8 straddled 7.1 and 7.2; confirm this wasn't already in 7.1. \--\>

## Admin / Workflow updates

### SVG icons replace Dashicons in the admin 🔍 🎨

\==\[all\]==

The admin bar and admin menu are switching from the Dashicons icon font to SVG icons rendered with `wp_get_icon()`, the icon API added in 7.1. SVG icons are announced more reliably by screen readers, work with forced-colors modes, and don't break when an icon font is blocked. If your plugin styles its admin menu icon, check it against the new markup.

Read more: [Replacing Dashicons in the admin bar and menu](https://make.wordpress.org/core/2026/09/04/replacing-dashicons-in-the-admin-bar-and-menu/) ([\#65089](https://core.trac.wordpress.org/ticket/65089))

Tracking: [Omnibar: WP 7.2 Iteration Issue](https://github.com/WordPress/gutenberg/issues/82723) (\#82723)

\<\!-- 🔍 Patch (wordpress-develop \#12270) was still in review; confirm it's committed. Icon choices were still being settled. \--\>

### Admin accessibility improvements 🔍

\==\[all\]==

Several long-standing accessibility tickets are on the 7.2 roadmap: admin notices that are easier to hear and dismiss ([\#50486](https://core.trac.wordpress.org/ticket/50486)), an option to turn off metabox rearranging ([\#50699](https://core.trac.wordpress.org/ticket/50699)), and removing the separate accessibility mode for widgets ([\#52399](https://core.trac.wordpress.org/ticket/52399)). Core also adds automated axe-core checks to catch regressions ([\#66015](https://core.trac.wordpress.org/ticket/66015)).

\<\!-- 🔍 Confirm which of these tickets are committed for 7.2. \--\>

### Application password improvements 🔍

\==\[site admin\] \[enterprise\]==

Application passwords get security hardening and UX refinements: an email notification when a new one is created ([\#63927](https://core.trac.wordpress.org/ticket/63927)), safer handling of `default_role` values ([\#46744](https://core.trac.wordpress.org/ticket/46744)), and better environment detection on sites without HTTPS ([\#57388](https://core.trac.wordpress.org/ticket/57388)).

\<\!-- 🔍 Confirm which tickets land; \#66009 (UX) couldn't be read. \--\>

## Developer Goodies

\==\[developer\] \[theme builder\] \[plugin author\] \[enterprise\]==

WordPress 7.2 gives developers public APIs for responsive controls, Interactivity API additions, a growing component library, and a handful of changes worth testing before the release.

### Global Styles and theme.json

#### Text shadow block support and presets 🔍

Text shadow, added to Global Styles in 7.1, is now a block support with a UI. Paragraph and Heading opt in through `supports.typography.textShadow`, and themes can define presets in `theme.json` under `settings.typography.textShadowPresets`. Core ships two defaults, Light and Strong ([\#79584](https://github.com/WordPress/gutenberg/pull/79584)).

#### Preset slug references fixed 🔍

Since WordPress 5.8, `var:preset|…` references used the raw slug while the generated CSS custom property used a kebab-cased version, so a slug like `n27` silently pointed to the wrong variable. References are now kebab-cased to match ([\#80583](https://github.com/WordPress/gutenberg/pull/80583)). Slugs that already worked are unaffected.

#### Override background-color padding 🔍

Themes can now override the padding WordPress adds to blocks that have a background color ([\#82024](https://github.com/WordPress/gutenberg/pull/82024)).

#### Background-clip block support 🔍

A new background-clip block support controls how far a block's background extends, including clipping it to the block's text ([\#77141](https://github.com/WordPress/gutenberg/pull/77141), [\#77142](https://github.com/WordPress/gutenberg/pull/77142)).

\<\!-- 🔍 On hold: confirm what the UI exposes (gradient text?), which blocks opt in, and that it's in 7.2. Rewrite or remove. \--\>

#### Turn off the responsive and state editing UI 🔍

Two editor settings let you hide the new styling UI from users: `responsiveEditingEnabled` hides the **Responsive styles** option, and `blockStatesEditingEnabled` hides the hover, focus, and active state controls ([\#80814](https://github.com/WordPress/gutenberg/pull/80814), [\#80956](https://github.com/WordPress/gutenberg/pull/80956), [\#81058](https://github.com/WordPress/gutenberg/pull/81058)). Both only affect the UI. Styles that are already saved keep rendering.

\<\!-- 🔍 On hold: the 7.1 Source of Truth already covers \`responsiveEditingEnabled\`. Check whether \`blockStatesEditingEnabled\` shipped in 7.1 too; keep only what's new in 7.2. \--\>

### Post editor sidebar moves to DataForm 🔍

The post and page settings sidebar is now built on DataForm, the same form system used for Quick Edit ([\#85081](https://github.com/WordPress/gutenberg/pull/85081)). `PluginDocumentSettingPanel`, `PluginSidebar`, `PluginPostStatusInfo`, the publish panels, and `removeEditorPanel` keep working, but `PluginPostExcerpt` hasn't been ported and may be removed. If your plugin extends the sidebar, test it now.

Read more: [Call for testing: DataForm editor inspector](https://make.wordpress.org/core/2026/09/17/call-for-testing-dataform-editor-inspector/)

\<\!-- 🔍 Stabilized on Oct 19 (\#85081), after Gutenberg 24.2. Confirm it's in Beta 1, and check what happened to \`PluginPostExcerpt\` and the \`editor.PostFeaturedImage\` filter (\#83133). \--\>

### DataViews, DataForm, and the Fields API 🔍

The Fields API gains a server-side registry and REST route ([\#84078](https://github.com/WordPress/gutenberg/pull/84078)). DataViews adds a `time` field type ([\#80830](https://github.com/WordPress/gutenberg/pull/80830)), `aspectRatio` and `mediaFit` options for grid previews ([\#79329](https://github.com/WordPress/gutenberg/pull/79329), [\#81604](https://github.com/WordPress/gutenberg/pull/81604)), and `isAny` and `isNone` filters for numeric fields ([\#77942](https://github.com/WordPress/gutenberg/pull/77942)). Core actions, like setting the homepage or posts page, are now registered on the server and live in a new `@wordpress/core-actions` package ([\#84660](https://github.com/WordPress/gutenberg/pull/84660), [\#84643](https://github.com/WordPress/gutenberg/pull/84643)). \<\!-- 🔍 Core actions PRs merged Oct 16; confirm they're in Beta 1\. \--\>

Tracking: [DataViews, DataViewsPicker, DataForm, Fields in WordPress 7.2](https://github.com/WordPress/gutenberg/issues/81228) (\#81228)

### Interactivity API 🔍

A new `data-wp-html` directive renders trusted HTML from the store ([\#83092](https://github.com/WordPress/gutenberg/pull/83092)). The router also exposes `state.navigating` and `state.initiator` so you can react to client-side navigations, replacing the deprecated `state.navigation.hasStarted` and `hasFinished` ([\#83280](https://github.com/WordPress/gutenberg/pull/83280)).

Tracking: [Interactivity API for WordPress 7.2](https://github.com/WordPress/gutenberg/issues/83078) (\#83078)

### Block API changes 🔍

* Inner block templates move into `registerBlockType()` settings. The `template` and `templateInsertUpdatesSelection` props on `<InnerBlocks>` are deprecated ([\#80027](https://github.com/WordPress/gutenberg/pull/80027)).  
* PHP-only blocks: an attribute with `items.enum` now gets a token field in the inspector ([\#83394](https://github.com/WordPress/gutenberg/pull/83394)).  
* `InspectorControls`' `__experimentalGroup` prop is removed; use `group` ([\#83171](https://github.com/WordPress/gutenberg/pull/83171)).  
* The empty-state block appender is now a real "ghost" block. CSS or tests that target `.block-editor-default-block-appender` need updating ([\#81231](https://github.com/WordPress/gutenberg/pull/81231)).

### Plugin menu items and apiFetch 🔍

`PluginMoreMenuItem`, `PluginSidebarMoreMenuItem`, and `PluginPreviewMenuItem` now render with the new `Menu` component. The `as` prop is deprecated and ignored ([\#81564](https://github.com/WordPress/gutenberg/pull/81564), [\#82321](https://github.com/WordPress/gutenberg/pull/82321)).

`apiFetch` now resolves an empty `200` response to `null` instead of rejecting with `invalid_json` ([\#79325](https://github.com/WordPress/gutenberg/pull/79325)). It also adds `apiFetch.unregister()` for removing middleware ([\#82408](https://github.com/WordPress/gutenberg/pull/82408)) and exposes `defaultFetchHandler` ([\#82553](https://github.com/WordPress/gutenberg/pull/82553)).

### Components and icons 🔍

`@wordpress/ui` adds a large set of components, including Menu, CheckboxControl, RadioGroupControl, SwitchControl, SearchableSelectControl, Calendar, Spinner, Meter, and Progress ([\#79560](https://github.com/WordPress/gutenberg/pull/79560), [\#82213](https://github.com/WordPress/gutenberg/pull/82213), [\#83143](https://github.com/WordPress/gutenberg/pull/83143), [\#83146](https://github.com/WordPress/gutenberg/pull/83146), [\#80979](https://github.com/WordPress/gutenberg/pull/80979), [\#81337](https://github.com/WordPress/gutenberg/pull/81337)).

A few utilities that used to be private are now public: `withIgnoreIMEEvents` in `@wordpress/keycodes`, for keyboard handlers that shouldn't fire while someone is typing with an input method editor ([\#81343](https://github.com/WordPress/gutenberg/pull/81343)), and a new `@wordpress/kebab-case` package that matches how PHP generates slugs ([\#81294](https://github.com/WordPress/gutenberg/pull/81294)).

### Icon collections: private icons and core-admin 🔍

Icon collections can now be marked as not public, so icons can ship with WordPress for use in the admin without showing up in the Icon block ([\#82634](https://github.com/WordPress/gutenberg/pull/82634), [\#83277](https://github.com/WordPress/gutenberg/pull/83277)). A new `core-admin` collection holds the icons used by the admin interface, including a set of popular icons ([\#83261](https://github.com/WordPress/gutenberg/pull/83261), [\#85072](https://github.com/WordPress/gutenberg/pull/85072)), and the Icon block won't render non-public icons on the front end ([\#82774](https://github.com/WordPress/gutenberg/pull/82774)).

### Deprecations and breaking changes 🔍

Test your plugins and themes against these before 7.2 is released:

* **Icons are stroke-based.** Core icons were redrawn as strokes, so setting `fill` no longer recolors them. Use CSS `color` instead ([\#78812](https://github.com/WordPress/gutenberg/pull/78812), [\#82754](https://github.com/WordPress/gutenberg/pull/82754)).  
* **Deprecated components:** Badge ([\#82379](https://github.com/WordPress/gutenberg/pull/82379)), Divider ([\#83040](https://github.com/WordPress/gutenberg/pull/83040)), ResponsiveWrapper ([\#83347](https://github.com/WordPress/gutenberg/pull/83347)), Scrollable ([\#83273](https://github.com/WordPress/gutenberg/pull/83273)), ZStack ([\#83344](https://github.com/WordPress/gutenberg/pull/83344)), Elevation ([\#83269](https://github.com/WordPress/gutenberg/pull/83269)), Animate ([\#80931](https://github.com/WordPress/gutenberg/pull/80931)), and `__experimentalSurface` ([\#80943](https://github.com/WordPress/gutenberg/pull/80943)). The private Menu API is also deprecated in favor of the `@wordpress/ui` Menu ([\#82947](https://github.com/WordPress/gutenberg/pull/82947)).  
* **Interactivity API:** Deprecated behaviors that reached their removal date are gone ([\#84098](https://github.com/WordPress/gutenberg/pull/84098)).  
* **`@wordpress/reusable-blocks`** is now a no-op package ([\#79186](https://github.com/WordPress/gutenberg/pull/79186)).  
* **DataViews:** The RichText control moved from DataViews' private exports to the editor package ([\#81430](https://github.com/WordPress/gutenberg/pull/81430)).  
* **Footnotes:** Footnote IDs now start with an `fn-` prefix. Update any CSS or links that target the old IDs ([\#82398](https://github.com/WordPress/gutenberg/pull/82398)).  
* **Block gap:** A block that doesn't declare `blockGap` support is now treated as not supporting it ([\#82401](https://github.com/WordPress/gutenberg/pull/82401)).

\<\!-- 🔍 Confirm each item is in the 7.2 package update and check for dev notes to link. \--\>

### Secrets API 🔍

A proposed Secrets API gives plugins a standard, encrypted place to store credentials like API keys, with `wp_set_secret()`, `wp_get_secret()`, and `wp_delete_secret()`. WP-CLI support is in scope, and an admin UI is planned for a later release.

Read more: [Proposal: A Secrets API for WordPress 7.2](https://make.wordpress.org/core/2026/08/25/proposal-a-secrets-api-for-wordpress-7-2/) ([\#66187](https://core.trac.wordpress.org/ticket/66187))

\<\!-- 🔍 The 7.2 vs 7.3 decision was due before Beta 1\. Remove if punted. \--\>

### wp\_kses() rebuilt on the HTML API 🔍

`wp_kses()` is being rebuilt on the HTML API instead of regular expressions. Output is normalized, `<script>` and `<style>` contents are stripped, and some malformed SVG, MathML, and comments are rejected. The `wp_kses_force_legacy_parser` filter restores the old behavior if you need it.

Read more: [Progress Report: wp\_kses()](https://make.wordpress.org/core/2026/10/07/progress-report-wp_kses/) ([\#66208](https://core.trac.wordpress.org/ticket/66208))

\<\!-- 🔍 Targeting "7.2 or 7.3 depending on testing." Remove if it moves to 7.3. \--\>

### AI: embeddings in the PHP AI Client 🔍

The bundled PHP AI Client updates to 1.4.0, adding embedding generation through a new `wp_ai_client_embedding()` function that follows the same pattern as AI prompts. It's infrastructure only: there's no indexing or search built in ([\#65638](https://core.trac.wordpress.org/ticket/65638)).

\<\!-- 🔍 Trac \#65638 is milestoned 7.2 but was still open. Remove if it doesn't land. \--\>

### NO\_BACKSLASH\_ESCAPES SQL mode turned off

WordPress 7.2 turns off the `NO_BACKSLASH_ESCAPES` SQL mode by default, since it can break WordPress's escaped queries. Sites that need it can turn it back on with a filter in a `db.php` drop-in.

Read more: [NO\_BACKSLASH\_ESCAPES SQL mode is now turned off by default in WordPress 7.2](https://make.wordpress.org/core/2026/10/09/no_backslash_escapes-sql-mode-is-now-turned-off-by-default-in-wordpress-7-2/)

---

A list of [all the dev notes can be reviewed from the Make Core blog](https://make.wordpress.org/core/tag/dev-notes+7-2/).

# **Notes**

**Emoji key**

* ✏️ To be edited  
* 🙏 Blessed feature: will be developed during the Beta cycle  
* 🔍 To-do or double-check  
* 🎨 Visuals being edited or created  
* 🏈 Confirmed punted to the next release

---

## **Release basics**

| Milestone | Date |
| :---- | :---- |
| Beta 1 | October 20, 15:00 UTC |
| Beta 2 | October 27 |
| Beta 3 | November 3 |
| Beta 4 | November 10 |
| RC 1 (Field Guide, hard string freeze, branch) | November 17 |
| RC 2 | November 24 |
| RC 3 | December 1 |
| Final | December 8 (State of the Word) |

* **Gutenberg range (likely, confirm at Beta 1\) 🔍:** 7.1 shipped 22.7–23.6. 7.2 should cover 23.7–24.2, with 24.2 (October 14\) the last plugin release before Beta 1\. 23.8 straddled both cycles: some PRs were backported to 7.1, others target 7.2.  
* **Release squad:** Matt Mullenweg (lead), David Baumwald (coordination), George Mamadashvili and Peter Wilson (tech), Henrique Iamarino (theme design), Maggie Cabrera and Carolina Nymark (theme dev), Jb Audras and Eshaan Dabasiya (triage), Md Noruzzaman, Jina Parekh, Erick Wambua (test).  
* **Release parties** move to livestreamed webinars starting with 7.2.

**Official planning sources**

* [WordPress 7.2 development cycle page](https://make.wordpress.org/core/7-2/)  
* [Roadmap to 7.2](https://make.wordpress.org/core/2026/09/18/roadmap-to-7-2/) (Anne McCarthy, Sep 18, updated Sep 28\)  
* [7.2 GitHub project board](https://github.com/orgs/WordPress/projects/300)  
* [Open Gutenberg iteration issues](https://github.com/WordPress/gutenberg/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22%5BType%5D%20Iteration%22)  
* [Announcing the 7.2 release squad](https://make.wordpress.org/core/2026/09/09/announcing-the-wordpress-7-2-release-squad/)  
* [7.2 Call for Volunteers (schedule)](https://make.wordpress.org/core/2026/08/12/wordpress-7-2-call-for-volunteers/)  
* [7.2 release party schedule](https://make.wordpress.org/core/2026/10/06/wordpress-7-2-release-party-schedule/)  
* [Iterating from live events to livestreamed releases](https://make.wordpress.org/core/2026/09/23/iterating-from-live-events-to-livestreamed-releases/)  
* [Bug scrub schedule for 7.2](https://make.wordpress.org/core/2026/09/09/bug-scrub-schedule-for-wordpress-7-2/)  
* [Test scrub schedule for 7.2](https://make.wordpress.org/test/2026/10/01/test-scrub-schedule-for-wordpress-7-2/)  
* [All posts tagged 7.2](https://make.wordpress.org/core/tag/7-2/)  
* [Dev notes tagged 7.2](https://make.wordpress.org/core/tag/dev-notes+7-2/) (one so far)  
* [Dev Chat Agenda, October 14](https://make.wordpress.org/core/2026/10/14/dev-chat-agenda-oct-14-2026/)  
* [Trac: tickets for the next major release](https://core.trac.wordpress.org/report/6)

**Gutenberg release posts in range**

* [What's new in Gutenberg 23.7 (Aug 5\)](https://make.wordpress.org/core/2026/08/06/whats-new-in-gutenberg-23-7-05-august/)  
* [What's new in Gutenberg 23.8 (Aug 19\)](https://make.wordpress.org/core/2026/08/19/whats-new-in-gutenberg-23-8-19-august/) · [v23.8.0 notes](https://github.com/WordPress/gutenberg/releases/tag/v23.8.0)  
* [What's new in Gutenberg 23.9 (Sep 2\)](https://make.wordpress.org/core/2026/09/02/whats-new-in-gutenberg-23-9-2-september/)  
* [What's new in Gutenberg 24.0 (Sep 16\)](https://make.wordpress.org/core/2026/09/16/whats-new-in-gutenberg-24-0-16-september/)  
* [What's new in Gutenberg 24.1 (Sep 30\)](https://make.wordpress.org/core/2026/09/30/whats-new-in-gutenberg-24-1-30-september/) · [v24.1.0 notes](https://github.com/WordPress/gutenberg/releases/tag/v24.1.0)  
* [What's new in Gutenberg 24.2 (Oct 14\)](https://make.wordpress.org/core/2026/10/14/whats-new-in-gutenberg-24-2-14-october/)

**Project docs to cross-check:** `wp-7-1-sot-backlog.md`, `wp-7-1-punted-items.md`, `gutenberg-23-8-developer-roundup.md`, `gutenberg-24-0-24-1-features.md`, `whats-new-for-developers-october-2026-notes.md`.

---

## **Priority item candidates (first pass) ✏️**

My opinionated short list, based on the roadmap, the highlight-worthy work that has actually merged, and breadth of impact. The release's highlight grid issue doesn't exist yet (or I haven't found it); check for it after Beta 1\. 🔍

1. **Ipsum, the new default theme**: ships with the release and ends year-based theme names. Highest visibility.  
2. **Notes in the canvas margin**: the biggest visible editor change merged this cycle, building on 6.9 and 7.1.  
3. **Design tools everywhere**: hundreds of PRs turning on background, shadow, min width/height, color, and border supports across most Core blocks. Big for themes.  
4. **Responsive and state styling, round two**: public viewport API for custom blocks, per-viewport position and custom CSS, Navigation Link hover/focus/active in Global Styles.  
5. **Global Styles grows up**: form elements (labels, inputs, selects, citations), custom duotone palettes, "show only customized blocks," inherited values in the inspector.  
6. **Security foundations**: Secrets API (if it lands), application password hardening, `wp_kses()` on the HTML API (7.2 or 7.3).

---

## **Default theme**

### **Ipsum 🔍 🎨**

\==\[all\] \[theme builder\]==

* Minimal blank-canvas blog theme with style variations, typesets, and dotted-underline accents. The post says all color combinations meet WCAG AA.  
* Ends the year-based "Twenty\*" naming. Replaces the earlier Mētis direction (the squad post still calls it Twenty Twenty-Seven).  
* Leads: Henrique Iamarino (design); Carolina Nymark, Maggie Cabrera, Juanfra Aldasoro (development).  
* Links:  
  * [Introducing Ipsum, the new default theme](https://make.wordpress.org/core/2026/09/16/introducing-ipsum-the-new-default-theme/)  
  * [GitHub: WordPress/ipsum](https://github.com/WordPress/ipsum)  
  * [Playground blueprint](https://playground.wordpress.net/?blueprint-url=https://raw.githubusercontent.com/WordPress/ipsum/trunk/.github/blueprint.json) (one commenter reported it failed to load 🔍)  
  * [Twenty Twenty-Seven team announcement (Mētis)](https://make.wordpress.org/core/2026/04/08/tt7-team/)  
* 🔍 Confirm when Ipsum is committed to Core and which Gutenberg features it showcases.

---

## **Collaboration**

### **Notes: canvas margin, drafts, undo 🔍 🎨**

\==\[end user\] \[site admin\] \[enterprise\]==

* **Merged (Gutenberg 24.2):** floating notes move into a margin beside the canvas and stay visible while editing; threads collapse to avatars in narrow views; a Notes submenu controls visibility; deleting a note offers Undo; unsent drafts are kept; child notes restore with their parent.  
* **Carried from 7.1, not confirmed:** emoji reactions ([\#75144](https://github.com/WordPress/gutenberg/issues/75144)), in progress. No merged reactions PR found.  
* **Exploring only:** suggestion mode ([\#73411](https://github.com/WordPress/gutenberg/issues/73411)). Likely not 7.2. 🔍  
* **Mentions send email** (merged in 23.8, not behind a flag): [\#79606](https://github.com/WordPress/gutenberg/pull/79606). Confirm it's in 7.2, not 7.1. 🔍  
* Links:  
  * Tracking: [Notes iteration for WordPress 7.2 (\#80015)](https://github.com/WordPress/gutenberg/issues/80015)  
  * Canvas margin: [\#79970 (issue)](https://github.com/WordPress/gutenberg/issues/79970), [\#83786](https://github.com/WordPress/gutenberg/pull/83786), [\#83768](https://github.com/WordPress/gutenberg/pull/83768), [\#83852](https://github.com/WordPress/gutenberg/pull/83852)  
  * Undo and drafts: [\#83988](https://github.com/WordPress/gutenberg/pull/83988), [\#84110](https://github.com/WordPress/gutenberg/pull/84110), [\#84100](https://github.com/WordPress/gutenberg/pull/84100)  
  * Notes action menu uses UI Menu: [\#81930](https://github.com/WordPress/gutenberg/pull/81930)  
  * Anne's proposal post: [Elevating and refining the WordPress Notes feature](https://nomad.blog/2026/09/03/elevating-and-refining-the-wordpress-notes-feature/)

### **Real-time collaboration 🏈**

* Not on the 7.2 roadmap. The direction moved to a server-aware approach, developed as a feature plugin.  
* Links:  
  * [Moving to a server-aware approach for collaboration](https://make.wordpress.org/core/2026/09/18/moving-to-a-server-aware-approach-for-collaboration/)  
  * [Real-time Collaboration: A Guide to Sync Engines (Oct 14\)](https://make.wordpress.org/core/2026/10/14/real-time-collaboration-a-guide-to-sync-engines/)  
  * [Iteration issue \#82146](https://github.com/WordPress/gutenberg/issues/82146)  
  * [Presence API: What's new](https://make.wordpress.org/core/2026/10/02/presence-api-whats-new/)  
  * [RTC removed from 7.0](https://make.wordpress.org/core/2026/05/08/rtc-removed-from-7-0/)  
* **Developer note:** `WP_ALLOW_COLLABORATION` removed and `wp_collaboration_enabled` option deleted on upgrade; RTC is now a single Gutenberg experiment ([\#80658](https://github.com/WordPress/gutenberg/pull/80658)). Plugin-only, but worth a line for anyone who configured it. 🔍

---

## **Design tools and styling**

### **Block supports on nearly every Core block 🔍**

\==\[theme builder\] \[site admin\] \[end user\]==

* Gutenberg 24.1 (\~140 PRs) and 24.2 (\~80 PRs) enabled existing supports on Core blocks that lacked them: background image/size/gradient, shadow, min width/height, link/heading/button colors, border, padding/margin, text columns, text align, text indent, duotone (Gallery, Video, Media & Text), fit text (Site Title, Site Tagline, Poetry).  
* All reachable from `theme.json` `styles.blocks`.  
* **Theme watch-out:** Accordion, Tabs, Tab Panel, and Post Template now output `has-link-color` and similar classes. Possible specificity collisions.  
* Background-clip infrastructure and UI (text gradients).  
* Links:  
  * Tracking: [Block supports and design tools (\#76525)](https://github.com/WordPress/gutenberg/issues/76525) (still titled for 7.1 when fetched)  
  * [24.1 changelog](https://github.com/WordPress/gutenberg/releases/tag/v24.1.0) · [24.2 post](https://make.wordpress.org/core/2026/10/14/whats-new-in-gutenberg-24-2-14-october/)  
  * Background-clip: [\#77141](https://github.com/WordPress/gutenberg/pull/77141), [\#77142](https://github.com/WordPress/gutenberg/pull/77142)  
  * Duotone: [Gallery \#83978](https://github.com/WordPress/gutenberg/pull/83978), [Video \#83979](https://github.com/WordPress/gutenberg/pull/83979), [Media & Text \#83981](https://github.com/WordPress/gutenberg/pull/83981)  
  * Fit text: [Site Title \#82074](https://github.com/WordPress/gutenberg/pull/82074), [Site Tagline \#83034](https://github.com/WordPress/gutenberg/pull/83034), [Poetry \#83980](https://github.com/WordPress/gutenberg/pull/83980)  
  * Text columns: [Group \#83425](https://github.com/WordPress/gutenberg/pull/83425)  
  * Background image from URL: [\#82230](https://github.com/WordPress/gutenberg/pull/82230)  
  * Override background-color padding: [\#82024](https://github.com/WordPress/gutenberg/pull/82024)  
  * Axial block gap for Group (flex/grid): [\#81476](https://github.com/WordPress/gutenberg/pull/81476)

### **Text shadow block support and presets 🔍**

\==\[theme builder\] \[developer\]==

* New `supports.typography.textShadow`; Paragraph and Heading opt in. `theme.json` gains `textShadow`, `textShadowPresets`, `defaultTextShadowPresets` (defaults: Light and Strong). Global Styles text shadow already shipped in 7.1; this is the block support and presets.  
* Link: [\#79584](https://github.com/WordPress/gutenberg/pull/79584)

### **Responsive style states, round two 🔍**

\==\[developer\] \[plugin author\] \[theme builder\]==

* **Merged:** public API for viewport states in custom block controls (`getStyleForState()`, `setStyleForState()`, `getSelectedBlockStyleState()`, `hasSelectedBlockStyleState()`); Gallery columns, crop, and aspect ratio per viewport; position per viewport; state-specific custom CSS; responsive status in the footer.  
* **Still open:** overlay colors, duotone, drop cap and fit text per viewport, plugin-registered viewports. The `group="viewport"` slot is undocumented. `wp_get_viewport_media_queries()` for Core is in review, not merged. 🔍  
* Links:  
  * Tracking: [Responsive style states for blocks, 7.2 tasks (\#80388)](https://github.com/WordPress/gutenberg/issues/80388)  
  * [\#82741 public API](https://github.com/WordPress/gutenberg/pull/82741), [\#82003 Gallery columns/crop](https://github.com/WordPress/gutenberg/pull/82003), [\#82233 Gallery aspect ratio](https://github.com/WordPress/gutenberg/pull/82233), [\#83094 position](https://github.com/WordPress/gutenberg/pull/83094), [\#83539 custom CSS](https://github.com/WordPress/gutenberg/pull/83539), [\#84146 footer status](https://github.com/WordPress/gutenberg/pull/84146)  
  * Core helper: [wordpress-develop \#13561](https://github.com/WordPress/wordpress-develop/pull/13561)  
  * UI gates: `responsiveEditingEnabled` ([\#80814](https://github.com/WordPress/gutenberg/pull/80814)) and `blockStatesEditingEnabled` ([\#80956](https://github.com/WordPress/gutenberg/pull/80956), [\#81058](https://github.com/WordPress/gutenberg/pull/81058)). 🔍 The first may have shipped in 7.1 already (the 7.1 SoT covers it).  
  * 7.1 background: [Responsive block styles dev note](https://make.wordpress.org/core/2026/08/05/responsive-block-styles-and-configurable-viewports-in-wordpress-7-1/)

### **Custom states (`-current`) and Navigation Link states 🔍**

\==\[theme builder\] \[site admin\]==

* **Merged:** Global Styles pseudo-state controls (hover, focus, active) for Navigation Link ([\#83451](https://github.com/WordPress/gutenberg/pull/83451)); per-instance state rules scoped to the block root ([\#83986](https://github.com/WordPress/gutenberg/pull/83986)).  
* **Not found on trunk:** the `-current` state UI for Navigation Link and Tabs, Navigation Link color/border/spacing supports ([\#83454](https://github.com/WordPress/gutenberg/pull/83454), [\#83457](https://github.com/WordPress/gutenberg/pull/83457)). The core of this item may miss 7.2. 🔍  
* Links: Tracking [Custom states for blocks, iteration for WP 7.2 (\#79283)](https://github.com/WordPress/gutenberg/issues/79283) · [7.1 dev note: Pseudo and custom style states](https://make.wordpress.org/core/2026/08/05/pseudo-and-custom-style-states-in-wordpress-7-1/)

### **Global Styles: form elements, duotone, custom-style filter 🔍**

\==\[theme builder\] \[site admin\]==

* Labels register as a `theme.json` element ([\#81160](https://github.com/WordPress/gutenberg/pull/81160)); citations, inputs, and selects exposed in Global Styles typography and color ([\#80852](https://github.com/WordPress/gutenberg/pull/80852)). More design work needed before full Elements API support.  
* Custom duotone palettes in a Duotone tab ([\#81605](https://github.com/WordPress/gutenberg/pull/81605)).  
* A dot marks blocks with custom styles; filter to show only those ([\#81373](https://github.com/WordPress/gutenberg/pull/81373)).  
* Global Styles revisions use the DataViews pickerActivity layout ([\#80856](https://github.com/WordPress/gutenberg/pull/80856)).  
* Links: Tracking [Form elements in Global Styles, iteration for WP 7.2](https://github.com/WordPress/gutenberg/issues/34198) (🔍 the fetched page may be a separate 7.2 issue citing \#34198) · Sub-issues [\#81647](https://github.com/WordPress/gutenberg/issues/81647), [\#81648](https://github.com/WordPress/gutenberg/issues/81648) · 6.9 background: [How WordPress 6.9 gives forms a theme.json makeover](https://developer.wordpress.org/news/2025/11/how-wordpress-6-9-gives-forms-a-theme-json-makeover/)

### **Inherited Global Styles values in the inspector 🔍**

\==\[site admin\] \[theme builder\]==

* Block controls now show values inherited from Global Styles, without an experiment flag ([\#82840](https://github.com/WordPress/gutenberg/pull/82840)). The dot/diamond indicators stay behind the `gutenberg-global-styles-inheritance-ui` experiment and look unlikely for 7.2.  
* Links: Tracking [Display inherited Global Styles and local overrides (7.2) (\#82520)](https://github.com/WordPress/gutenberg/issues/82520) · [\#77894](https://github.com/WordPress/gutenberg/pull/77894) · [\#80815](https://github.com/WordPress/gutenberg/pull/80815) · 7.1 tracking [\#77595](https://github.com/WordPress/gutenberg/issues/77595)  
* Carryover: listed as punted from 7.1 ("decision before Beta 2"). 🔍

### **Preset slug kebab-casing fix 🔍**

\==\[theme builder\] \[developer\]==

* `var:preset|…` references now kebab-case slugs to match emitted custom properties (bug since 5.8). Targets 7.2, not backported to 7.1.  
* Link: [\#80583](https://github.com/WordPress/gutenberg/pull/80583)

---

## **Blocks**

### **New: Description list block 🔍**

\==\[end user\] \[site admin\]==

* Roadmap: three static blocks outputting `<dl>`, `<dt>`, `<dd>`. No implementing PR found yet.  
* Link: [Block for description list (\#4880)](https://github.com/WordPress/gutenberg/issues/4880)

### **Table of Contents block stabilization 🔍**

\==\[end user\] \[theme builder\]==

* Now server-rendered, with saved static markup dropped. Still open: where heading-level detection runs in the editor, template context, third-party heading sources, tests, and edge cases. Tight four days out.  
* "Convert to static list" renamed to a confirmed Detach action ([\#80844](https://github.com/WordPress/gutenberg/pull/80844)). New supports: background, shadow, text align ([\#83251](https://github.com/WordPress/gutenberg/pull/83251), [\#83187](https://github.com/WordPress/gutenberg/pull/83187), [\#83430](https://github.com/WordPress/gutenberg/pull/83430)).  
* Links: Tracking [Stabilize the Table of Contents Block (\#42229)](https://github.com/WordPress/gutenberg/issues/42229) · [\#80318](https://github.com/WordPress/gutenberg/pull/80318) · [\#80404](https://github.com/WordPress/gutenberg/pull/80404) · [\#80786](https://github.com/WordPress/gutenberg/issues/80786) · [\#80199 tests](https://github.com/WordPress/gutenberg/pull/80199)  
* Carryover: punted from 7.1.

### **Gallery: sorting, dynamic mode, Grid variation, lightbox 🔍**

\==\[end user\] \[site admin\]==

* Order by works on hand-picked images; Random shuffles each page load ([\#83438](https://github.com/WordPress/gutenberg/pull/83438)). Duotone ([\#83978](https://github.com/WordPress/gutenberg/pull/83978)).  
* Dynamic mode: toolbar button renamed "Detach" with an explanatory modal ([\#80727](https://github.com/WordPress/gutenberg/pull/80727)); single undo step ([\#80665](https://github.com/WordPress/gutenberg/pull/80665)).  
* Grid block variation of Gallery ([\#81909](https://github.com/WordPress/gutenberg/pull/81909)).  
* Lightbox: clicking an image no longer closes the dialog when navigation is on ([\#78898](https://github.com/WordPress/gutenberg/pull/78898)). Roadmap lists lightbox UX gaps as open to contributors ([\#51132](https://github.com/WordPress/gutenberg/issues/51132)).  
* Media inserter redesign for large libraries is still open ([\#79729](https://github.com/WordPress/gutenberg/issues/79729)).  
* Links: Tracking [WordPress 7.2: Dynamic galleries and media inserter (\#81370)](https://github.com/WordPress/gutenberg/issues/81370) · 7.1 background [\#77117](https://github.com/WordPress/gutenberg/issues/77117)

### **Navigation: one search for every link, Custom Link variation 🔍**

\==\[site admin\] \[end user\]==

* Link search covers all content types at once, with types shown and posts/pages ranked first ([\#83408](https://github.com/WordPress/gutenberg/pull/83408), [\#83652](https://github.com/WordPress/gutenberg/pull/83652), [\#83407](https://github.com/WordPress/gutenberg/pull/83407)).  
* Navigation Link block name changes, with a default Custom Link variation ([\#82375](https://github.com/WordPress/gutenberg/pull/82375)).  
* Sidebar navigation editing in the Site Editor is a 7.2 target with no task list yet: [\#77069](https://github.com/WordPress/gutenberg/issues/77069).  
* Open request from Dev Chat: border/spacing support for Navigation blocks ([\#66392](https://github.com/WordPress/gutenberg/pull/66392), [\#66483](https://github.com/WordPress/gutenberg/pull/66483), [\#68455](https://github.com/WordPress/gutenberg/pull/68455)). 🔍

### **Icons: keyword search, private collections, stroke redraw 🔍**

\==\[end user\] \[plugin author\] \[developer\]==

* Icon block search matches keywords, like "hamburger" for Menu ([\#82367](https://github.com/WordPress/gutenberg/pull/82367), [\#83884](https://github.com/WordPress/gutenberg/pull/83884)).  
* Icons can ship to Core without appearing in the Icon block; new `core-admin` collection; `public` moved to collections ([\#82634](https://github.com/WordPress/gutenberg/pull/82634), [\#83261](https://github.com/WordPress/gutenberg/pull/83261), [\#83277](https://github.com/WordPress/gutenberg/pull/83277), [\#82774](https://github.com/WordPress/gutenberg/pull/82774)).  
* Icon block bindings for the `icon` attribute ([\#80730](https://github.com/WordPress/gutenberg/pull/80730)).  
* **Breaking for icon styling:** \~330 icons redrawn as strokes; `fill` no longer recolors them, use `color` ([\#78812](https://github.com/WordPress/gutenberg/pull/78812), [\#82540](https://github.com/WordPress/gutenberg/pull/82540), [\#82754](https://github.com/WordPress/gutenberg/pull/82754)).

### **Other block changes worth a look ✏️ 🔍**

* Columns: slider removed, add columns with a plus button ([\#83262](https://github.com/WordPress/gutenberg/pull/83262)); transform Columns to Row ([\#81802](https://github.com/WordPress/gutenberg/pull/81802)).  
* Button: link popover opens only on explicit action ([\#30166](https://github.com/WordPress/gutenberg/pull/30166)).  
* Video and Cover respect reduced-motion for autoplay ([\#83337](https://github.com/WordPress/gutenberg/pull/83337), [\#83452](https://github.com/WordPress/gutenberg/pull/83452)). Video block GIF variations removed ([\#82696](https://github.com/WordPress/gutenberg/pull/82696)).  
* Cover and Media & Text get a Media inspector section ([\#82751](https://github.com/WordPress/gutenberg/pull/82751), [\#82593](https://github.com/WordPress/gutenberg/pull/82593)); Media & Text "Add Media" in the toolbar ([\#82420](https://github.com/WordPress/gutenberg/pull/82420)).  
* List: Tab indents/outdents fully selected and multi-selected items ([\#82460](https://github.com/WordPress/gutenberg/pull/82460), [\#82411](https://github.com/WordPress/gutenberg/pull/82411)); align support ([\#68002](https://github.com/WordPress/gutenberg/pull/68002)).  
* Query Loop: "Keyword" filter renamed "Search terms" ([\#82387](https://github.com/WordPress/gutenberg/pull/82387)); reload notice becomes a snackbar ([\#82246](https://github.com/WordPress/gutenberg/pull/82246)).  
* Tabs: inactive panel content findable with browser Find ([\#81743](https://github.com/WordPress/gutenberg/pull/81743)).  
* Playlist: bulk track metadata editing ([\#81441](https://github.com/WordPress/gutenberg/pull/81441)).  
* Math: inline UI improved ([\#77743](https://github.com/WordPress/gutenberg/pull/77743)); LaTeX errors shown on blur ([\#80500](https://github.com/WordPress/gutenberg/pull/80500)).  
* Page List and TOC: one-way conversions become a confirmed "Detach" ([\#80847](https://github.com/WordPress/gutenberg/pull/80847), [\#80844](https://github.com/WordPress/gutenberg/pull/80844)).  
* Footnote IDs get an `fn-` prefix ([\#82398](https://github.com/WordPress/gutenberg/pull/82398)).  
* Alignment options shown as unavailable instead of hidden ([\#82600](https://github.com/WordPress/gutenberg/pull/82600)).

---

## **Editor enhancements**

### **Block editor paper cuts 🔍**

\==\[end user\]==

* Insert blocks from the parent selector in the toolbar ([\#81532](https://github.com/WordPress/gutenberg/pull/81532)); parent selector shows for blocks inside patterns ([\#82912](https://github.com/WordPress/gutenberg/pull/82912)).  
* Enter selects the next block ([\#63484](https://github.com/WordPress/gutenberg/pull/63484)); rich text formatting across blocks ([\#58913](https://github.com/WordPress/gutenberg/pull/58913)).  
* Mobile: multi-selection via editableRoot ([\#81542](https://github.com/WordPress/gutenberg/pull/81542), [\#82816](https://github.com/WordPress/gutenberg/pull/82816)); iOS double-tap selection fix ([\#81042](https://github.com/WordPress/gutenberg/pull/81042)).  
* In-between inserter on wrapped lines ([\#83276](https://github.com/WordPress/gutenberg/pull/83276)) and sized to adjacent blocks ([\#68074](https://github.com/WordPress/gutenberg/pull/68074)).  
* Escape/Enter to leave or enter the canvas ([\#82314](https://github.com/WordPress/gutenberg/pull/82314)).  
* Visualize non-breaking spaces ([\#74040](https://github.com/WordPress/gutenberg/pull/74040)).  
* **The empty-state appender is now a real "ghost" block** ([\#81231](https://github.com/WordPress/gutenberg/pull/81231)). Breaks CSS and e2e selectors targeting `.block-editor-default-block-appender`.  
* Links: Tracking [Block Editor Paper Cuts (\#81453)](https://github.com/WordPress/gutenberg/issues/81453) · 7.1 tracking [\#63255](https://github.com/WordPress/gutenberg/issues/63255)

### **Options menu, post author, slugs 🔍**

* Options menu's View group gains Appearance, Notes, and Panels submenus ([\#82976](https://github.com/WordPress/gutenberg/pull/82976)).  
* Post author field is searchable and queries users on the server ([\#83323](https://github.com/WordPress/gutenberg/pull/83323)).  
* New posts no longer publish with the `auto-draft` slug ([\#83518](https://github.com/WordPress/gutenberg/pull/83518)); post slug prefers server sanitization ([\#78135](https://github.com/WordPress/gutenberg/pull/78135)).  
* Starter patterns modal gets category filtering ([\#81396](https://github.com/WordPress/gutenberg/pull/81396)).  
* Command Palette: View post command ([\#66720](https://github.com/WordPress/gutenberg/pull/66720)).

### **Visual revisions polish 🔍**

\==\[end user\] \[site admin\]==

* Merged after 7.1: post title diffs in revisions ([\#82586](https://github.com/WordPress/gutenberg/pull/82586), [\#82536](https://github.com/WordPress/gutenberg/pull/82536)); merged adjacent inline diffs ([\#80579](https://github.com/WordPress/gutenberg/pull/80579)).  
* 🔍 Shareable URLs ([\#79934](https://github.com/WordPress/gutenberg/pull/79934)) and the code diff view ([\#80314](https://github.com/WordPress/gutenberg/pull/80314)) merged August 3, in 23.8. Check whether they shipped in 7.1 or land in 7.2.  
* Links: Tracking [Visual Revisions: post-7.0 polish (\#79120)](https://github.com/WordPress/gutenberg/issues/79120)

### **Media editor modal 🔍**

\==\[end user\] \[site admin\]==

* Restore the original uncropped image from More options ([\#81805](https://github.com/WordPress/gutenberg/pull/81805)); original attachment ID tracked for edited images ([\#81803](https://github.com/WordPress/gutenberg/pull/81803)); panel layout refactor ([\#81840](https://github.com/WordPress/gutenberg/pull/81840)); tools lock while saving ([\#82417](https://github.com/WordPress/gutenberg/pull/82417)).  
* Links: Tracking [WordPress 7.2 Iteration: Media Editor Modal (\#80389)](https://github.com/WordPress/gutenberg/issues/80389)

### **Images attach to the post on save 🔍**

\==\[plugin author\] \[site admin\]==

* Unattached images in Image and Gallery blocks get the current post as `post_parent` after save. Skips synced patterns, template parts, autosaves; stops above 100 images. Opt out with `autoAttachMediaEnabled` (how to set it is unconfirmed).  
* Link: [\#81977](https://github.com/WordPress/gutenberg/pull/81977) · Related issue [\#66663](https://github.com/WordPress/gutenberg/issues/66663)

---

## **Admin and workflow**

### **DataForm editor inspector 🔍**

\==\[plugin author\] \[developer\] \[enterprise\]==

* The post/page sidebar is being rebuilt on DataForm (experiment "Editor Inspector: Use DataForm"). Keeps working: `PluginDocumentSettingPanel`, `PluginSidebar`, `PluginPostStatusInfo`, pre/post-publish panels, `removeEditorPanel`. **`PluginPostExcerpt` is not ported and may be removed.** 🔍 Confirm whether this ships on by default in 7.2.  
* Links:  
  * [Call for testing: DataForm editor inspector](https://make.wordpress.org/core/2026/09/17/call-for-testing-dataform-editor-inspector/)  
  * [Back-compat call for testing (\#82770)](https://github.com/WordPress/gutenberg/issues/82770)  
  * Parent: [Consolidate Quick Edit and Editor Inspector (\#76076)](https://github.com/WordPress/gutenberg/issues/76076)  
  * [\#82678](https://github.com/WordPress/gutenberg/pull/82678) (MediaUpload filter) · [\#83133](https://github.com/WordPress/gutenberg/pull/83133) (`editor.PostFeaturedImage` filter)

### **DataViews, DataForm, Fields API 🔍**

\==\[plugin author\] \[developer\]==

* Fields API: server-side registry and REST route ([\#84078](https://github.com/WordPress/gutenberg/pull/84078)).  
* New `time` field ([\#80830](https://github.com/WordPress/gutenberg/pull/80830)); grid `aspectRatio` and `mediaFit` ([\#79329](https://github.com/WordPress/gutenberg/pull/79329), [\#81604](https://github.com/WordPress/gutenberg/pull/81604)); `isAny`/`isNone` on numeric fields ([\#77942](https://github.com/WordPress/gutenberg/pull/77942)); `showPlaceholderIfEmpty` ([\#82527](https://github.com/WordPress/gutenberg/pull/82527)); timezone in datetime control ([\#82291](https://github.com/WordPress/gutenberg/pull/82291)).  
* DataViews no longer uses private APIs; the RichText private export moved to the editor package (breaking) ([\#81430](https://github.com/WordPress/gutenberg/pull/81430)).  
* View config reference docs ([\#81149](https://github.com/WordPress/gutenberg/pull/81149)) and the layered view-resolution fix ([\#80832](https://github.com/WordPress/gutenberg/pull/80832)). 🔍 Both were backported to 7.1.  
* Links: Tracking [DataViews, DataViewsPicker, DataForm, Fields in WordPress 7.2 (\#81228)](https://github.com/WordPress/gutenberg/issues/81228) · UX: [hierarchy \#80360](https://github.com/WordPress/gutenberg/issues/80360), [bulk actions \#80408](https://github.com/WordPress/gutenberg/issues/80408) · DataViews as npm package decision: [\#67274](https://github.com/WordPress/gutenberg/issues/67274) · 7.1 tracking [\#76045](https://github.com/WordPress/gutenberg/issues/76045)

### **Extensible Site Editor (v2) 🔍**

\==\[plugin author\] \[developer\]==

* Goal: replace Site Editor v1 with v2 (`admin.php?page=site-editor-v2`); 7.2 aims for feature parity. Every v2 screen now takes its view config from the server, including Identity and Navigation. Stabilizing the experiment is still an open question, so v2 may stay experimental in 7.2.  
* Links: Tracking [Extensible Site Editor: 7.2 Iteration Issue (\#79895)](https://github.com/WordPress/gutenberg/issues/79895) · [\#82138](https://github.com/WordPress/gutenberg/pull/82138), [\#82140](https://github.com/WordPress/gutenberg/pull/82140), [\#82456](https://github.com/WordPress/gutenberg/pull/82456), [\#82457](https://github.com/WordPress/gutenberg/pull/82457), [\#82458](https://github.com/WordPress/gutenberg/pull/82458), [\#82692](https://github.com/WordPress/gutenberg/pull/82692) · Quick Edit uses view config form ([\#82962](https://github.com/WordPress/gutenberg/pull/82962)) · Core backport [wordpress-develop \#13296](https://github.com/WordPress/wordpress-develop/pull/13296)

### **Omnibar: SVG icons replace Dashicons in the admin 🔍**

\==\[all\]==

* Admin bar and sidebar Dashicons swapped for SVG icons via `wp_get_icon()`; patch in review. Icon choices still being settled.  
* Open feedback: whether to keep the W and site name in the Toolbar.  
* Links:  
  * [Replacing Dashicons in the admin bar and menu](https://make.wordpress.org/core/2026/09/04/replacing-dashicons-in-the-admin-bar-and-menu/)  
  * [Call for feedback: the W and the site name in the Toolbar](https://make.wordpress.org/core/2026/10/12/call-for-feedback-the-w-and-the-site-name-in-the-toolbar/)  
  * Tracking: [Omnibar: WP 7.2 Iteration Issue (\#82723)](https://github.com/WordPress/gutenberg/issues/82723)  
  * Trac [\#65089](https://core.trac.wordpress.org/ticket/65089), [\#66087](https://core.trac.wordpress.org/ticket/66087) · [wordpress-develop \#12270](https://github.com/WordPress/wordpress-develop/pull/12270), [\#13453](https://github.com/WordPress/wordpress-develop/pull/13453)  
  * Admin color: default admin theme color is Blueberry ([\#83749](https://github.com/WordPress/gutenberg/pull/83749)); editors pick up the admin color scheme ([\#81112](https://github.com/WordPress/gutenberg/pull/81112))

### **Error state overhaul 🔍**

* Clearer errors with a copy button; ErrorBoundary surfaces debugging details; root error boundary in the Site Editor.  
* Links: [Defensive data design](https://make.wordpress.org/core/2026/08/04/defensive-data-design/) · [\#76470](https://github.com/WordPress/gutenberg/pull/76470) · [\#82496](https://github.com/WordPress/gutenberg/pull/82496) · [\#81642](https://github.com/WordPress/gutenberg/pull/81642) · [\#82486](https://github.com/WordPress/gutenberg/pull/82486)

### **Accessibility (Core) 🔍**

\==\[all\]==

* Admin notices easier to announce and dismiss ([\#50486](https://core.trac.wordpress.org/ticket/50486)); axe-core automated testing ([\#66015](https://core.trac.wordpress.org/ticket/66015)); toggle to turn off metabox rearranging ([\#50699](https://core.trac.wordpress.org/ticket/50699), [wordpress-develop \#12627](https://github.com/WordPress/wordpress-develop/pull/12627)); remove widgets accessibility mode ([\#52399](https://core.trac.wordpress.org/ticket/52399)).

### **On This Day dashboard widget 🔍**

* Roadmap retries it, but Trac \#65116 is still open and milestoned 7.1, with unresolved questions (opt-in vs default, merging with Gutenberg \#74936, whether it belongs in Core). Likely punt again.  
* Links: [Trac \#65116](https://core.trac.wordpress.org/ticket/65116) · [wordpress-develop \#11630](https://github.com/WordPress/wordpress-develop/pull/11630) · [Gutenberg \#74936](https://github.com/WordPress/gutenberg/issues/74936)  
* Carryover: punted from 7.1.

---

## **Security**

### **Secrets API 🔍**

\==\[plugin author\] \[developer\] \[enterprise\]==

* First-class encrypted credential store: `wp_set_secret()`, `wp_get_secret()`, `wp_delete_secret()`, `wp_import_option_as_secret()`, `WP_Secret`. WP-CLI in scope; admin UI deferred to 7.3. **7.2 vs 7.3 decision due before Beta 1\.**  
* Links: [Proposal: A Secrets API for WordPress 7.2](https://make.wordpress.org/core/2026/08/25/proposal-a-secrets-api-for-wordpress-7-2/) · [Trac \#66187](https://core.trac.wordpress.org/ticket/66187) · [wordpress-develop \#13759](https://github.com/WordPress/wordpress-develop/pull/13759) · [Feature plugin](https://github.com/ericmann/secrets-api)

### **Application password improvements 🔍**

\==\[site admin\] \[enterprise\]==

* UX improvements, email notification on add, environment detection on non-HTTPS sites, safer `default_role`, SameSite cookies.  
* Links: [\#66009](https://core.trac.wordpress.org/ticket/66009) (couldn't be read 🔍), [\#63927](https://core.trac.wordpress.org/ticket/63927), [\#57388](https://core.trac.wordpress.org/ticket/57388), [\#46744](https://core.trac.wordpress.org/ticket/46744), [\#37000](https://core.trac.wordpress.org/ticket/37000)

### **`wp_kses()` rebuilt on the HTML API 🔍**

\==\[plugin author\] \[developer\]==

* Normalized output; `script`/`style` contents stripped; some malformed SVG, MathML, and comments rejected. `wp_kses_force_legacy_parser` restores old behavior. **"7.2 or 7.3" depending on testing.**  
* Links: [Progress Report: wp\_kses()](https://make.wordpress.org/core/2026/10/07/progress-report-wp_kses/) · [Trac \#66208](https://core.trac.wordpress.org/ticket/66208) · [wordpress-develop \#13271](https://github.com/WordPress/wordpress-develop/pull/13271)

### **Sudo mode 🔍**

* Re-authentication for sensitive actions. Proposal pending; no link yet.

---

## **Developer goodies**

### **Interactivity API 🔍**

\==\[developer\] \[plugin author\]==

* `data-wp-html` directive with `asDangerousHTML()` ([\#83092](https://github.com/WordPress/gutenberg/pull/83092), merged). Router navigation lifecycle: `state.navigating`, `state.initiator`, `initiator` option for `navigate()`; replaces deprecated `state.navigation.hasStarted`/`hasFinished` ([\#83280](https://github.com/WordPress/gutenberg/pull/83280), in 24.2). Expired deprecations removed ([\#84098](https://github.com/WordPress/gutenberg/pull/84098)).  
* Links: Tracking [Interactivity API for WordPress 7.2 (\#83078)](https://github.com/WordPress/gutenberg/issues/83078) · [\#83076](https://github.com/WordPress/gutenberg/issues/83076) · [\#80960](https://github.com/WordPress/gutenberg/issues/80960)

### **Block API changes 🔍**

\==\[developer\] \[plugin author\]==

* Inner block templates move into `registerBlockType()` settings; `<InnerBlocks>` `template` props deprecated ([\#80027](https://github.com/WordPress/gutenberg/pull/80027)).  
* PHP-only blocks: `items.enum` generates a token field ([\#83394](https://github.com/WordPress/gutenberg/pull/83394)); `supports.autoRegister` in the schema ([\#80173](https://github.com/WordPress/gutenberg/pull/80173)).  
* `InspectorControls` `__experimentalGroup` removed ([\#83171](https://github.com/WordPress/gutenberg/pull/83171)).  
* Missing `blockGap` treated as unsupported ([\#82401](https://github.com/WordPress/gutenberg/pull/82401)); `blockGap` normalized ([\#81460](https://github.com/WordPress/gutenberg/pull/81460)).  
* `@wordpress/reusable-blocks` becomes a no-op ([\#79186](https://github.com/WordPress/gutenberg/pull/79186)).

### **Plugin menu items render through `@wordpress/ui` Menu 🔍**

\==\[plugin author\]==

* `PluginMoreMenuItem`, `PluginSidebarMoreMenuItem`, `PluginPreviewMenuItem`: `as` prop deprecated and ignored; links only honor `target="_blank"`.  
* Links: [\#81564](https://github.com/WordPress/gutenberg/pull/81564) · [\#82321](https://github.com/WordPress/gutenberg/pull/82321) · [\#82319](https://github.com/WordPress/gutenberg/pull/82319) · Private Menu API deprecated ([\#82947](https://github.com/WordPress/gutenberg/pull/82947))

### **`apiFetch` changes 🔍**

\==\[developer\] \[plugin author\]==

* Empty 200 responses resolve to `null` (previously rejected `invalid_json`); `apiFetch.unregister()`; `defaultFetchHandler` exposed.  
* Links: [\#79325](https://github.com/WordPress/gutenberg/pull/79325) · [\#82408](https://github.com/WordPress/gutenberg/pull/82408) · [\#82553](https://github.com/WordPress/gutenberg/pull/82553)

### **Components and `@wordpress/ui` 🔍**

\==\[developer\] \[plugin author\]==

* New in `@wordpress/ui`: Menu, CheckboxControl, CheckboxGroup, RadioGroup(Control), Switch(Control), SearchableSelect(Control), SearchableChipSelect(Control), Calendar/RangeCalendar, TextareaControl, Spinner, Meter, Progress, Breadcrumb.  
* Deprecated in `@wordpress/components`: Badge, Divider, ResponsiveWrapper, Scrollable, ZStack, Elevation, Animate, `__experimentalSurface`.  
* Public now: `withIgnoreIMEEvents` in `@wordpress/keycodes`; new `@wordpress/kebab-case` package; `@wordpress/data` `normalizeArgs` and `getResolutionArgs`.  
* Links: [24.0 notes](https://make.wordpress.org/core/2026/09/16/whats-new-in-gutenberg-24-0-16-september/) · [24.1 notes](https://github.com/WordPress/gutenberg/releases/tag/v24.1.0) · [24.2 post](https://make.wordpress.org/core/2026/10/14/whats-new-in-gutenberg-24-2-14-october/) · Deprecations: [Badge \#82379](https://github.com/WordPress/gutenberg/pull/82379), [Divider \#83040](https://github.com/WordPress/gutenberg/pull/83040), [ResponsiveWrapper \#83347](https://github.com/WordPress/gutenberg/pull/83347), [Scrollable \#83273](https://github.com/WordPress/gutenberg/pull/83273), [ZStack \#83344](https://github.com/WordPress/gutenberg/pull/83344), [Elevation \#83269](https://github.com/WordPress/gutenberg/pull/83269), [Animate \#80931](https://github.com/WordPress/gutenberg/pull/80931), [Surface \#80943](https://github.com/WordPress/gutenberg/pull/80943) · [withIgnoreIMEEvents \#81343](https://github.com/WordPress/gutenberg/pull/81343) · [kebab-case \#81294](https://github.com/WordPress/gutenberg/pull/81294) · [Calendar \#81337](https://github.com/WordPress/gutenberg/pull/81337)

### **Database: `NO_BACKSLASH_ESCAPES` off by default ✅ dev note published**

\==\[developer\] \[enterprise\]==

* Link: [NO\_BACKSLASH\_ESCAPES SQL mode is now turned off by default in WordPress 7.2](https://make.wordpress.org/core/2026/10/09/no_backslash_escapes-sql-mode-is-now-turned-off-by-default-in-wordpress-7-2/)

### **Performance 🔍**

* Retire script/style concatenation in favor of prefetching. Trac \#57548 is milestoned **Future Release**, not 7.2. Likely not in 7.2.  
* Enhanced Responsive Images (feature plugin; merge not confirmed).  
* Inserter opens with less main-thread blocking ([\#83437](https://github.com/WordPress/gutenberg/pull/83437), [\#83284](https://github.com/WordPress/gutenberg/pull/83284)); List View "Select all" on 1,000 blocks from 16.8s to 0.4s ([\#81210](https://github.com/WordPress/gutenberg/pull/81210)).  
* Links: [Trac \#57548](https://core.trac.wordpress.org/ticket/57548) · [Enhanced Responsive Images issues](https://github.com/WordPress/performance/issues?q=is%3Aopen+label%3A%22%5BPlugin%5D+Enhanced+Responsive+Images%22) · [Enhanced Responsive Images plugin](https://wordpress.org/plugins/auto-sizes/)

### **Client-side media 🔍**

* 7.2 goals: durable upload queue, server-side fallback, video transcoding and posters, JPEG XL, animated GIF sub-sizes. None confirmed merged. Probably later.  
* Links: Tracking [Client Side Media iteration for WordPress 7.2 and beyond (\#80159)](https://github.com/WordPress/gutenberg/issues/80159) · [7.1 dev note](https://make.wordpress.org/core/2026/07/22/client-side-media-processing-in-wordpress-7-1/)

### **Tooling (not Core, but readers will ask) ✏️**

* Gutenberg tests use Vitest; `@wordpress/scripts` 36 drops Jest ([Make post](https://make.wordpress.org/core/2026/09/23/gutenbergs-javascript-unit-and-integration-tests-now-use-vitest/), [\#82843](https://github.com/WordPress/gutenberg/pull/82843)).  
* [Updating WordPress to Node.js 24 and npm 11](https://make.wordpress.org/core/2026/09/09/updating-wordpress-to-use-node-js-24-and-npm-11/).

---

## **AI (mostly in the AI plugin, not Core) 🔍**

The roadmap says this work happens in the AI plugin and may not land in 7.2.

* **Embeddings in Core:** [Trac \#65638](https://core.trac.wordpress.org/ticket/65638) is open and **milestoned 7.2**. It updates the PHP AI Client to 1.4.0 and adds `wp_ai_client_embedding()` ([wordpress-develop \#12530](https://github.com/WordPress/wordpress-develop/pull/12530)). Moved from 7.1 after Beta 1\. Semantic search itself: [AI \#962](https://github.com/WordPress/ai/issues/962).  
* **Streaming responses:** [php-ai-client \#100](https://github.com/WordPress/php-ai-client/issues/100).  
* **Connectors:** on/off controls, performance, key handling during provider outages: [\#65523](https://core.trac.wordpress.org/ticket/65523), [\#65215](https://core.trac.wordpress.org/ticket/65215), [\#65551](https://core.trac.wordpress.org/ticket/65551).  
* **Abilities and MCP:** [AI \#40](https://github.com/WordPress/ai/issues/40), [AI \#1025](https://github.com/WordPress/ai/pull/1025), [MCP Adapter](https://github.com/WordPress/mcp-adapter), [\#313](https://github.com/WordPress/mcp-adapter/issues/313), [\#178](https://github.com/WordPress/mcp-adapter/issues/178), [AI \#992](https://github.com/WordPress/ai/pull/992), [WebMCP \#448](https://github.com/WordPress/ai/issues/448), [Agent identity \#923](https://github.com/WordPress/ai/issues/923).  
* **Guidelines and Knowledge:** moved to 7.2 after missing 7.1, but still in the experiment and framed as AI-plugin work. Likely not in Core 7.2. [\#77230](https://github.com/WordPress/gutenberg/issues/77230) · [\#75171](https://github.com/WordPress/gutenberg/issues/75171) · [Merge proposal: Guidelines built on Knowledge](https://make.wordpress.org/core/2026/06/22/merge-proposal-guidelines-built-on-knowledge/)  
* [AI plugin](https://wordpress.org/plugins/ai/) · [AI plugin issues](https://github.com/WordPress/ai/issues)

---

## **Not in 7.2 (or very unlikely)**

* 🏈 **Real-time collaboration**: intentionally off the roadmap. Links above.  
* 🏈 **React 19 in Core**: Gutenberg 24.2 turns it on by default in the plugin ([\#83784](https://github.com/WordPress/gutenberg/pull/83784), [incompatible plugins \#84607](https://github.com/WordPress/gutenberg/pull/84607)), but contributors on the tracking issue say it won't be part of 7.2 and will likely be 7.3. [Upgrading to React 19 (\#71336)](https://github.com/WordPress/gutenberg/issues/71336). Worth a heads-up for plugin developers testing with Gutenberg.  
* 🔍 **Script/style concatenation removal**: Future Release on Trac.  
* 🔍 **On This Day widget**: still unresolved.  
* 🔍 **Classic block deprecation**: reverted for 7.1; the follow-up post sets direction but no 7.2 target. [The Classic block stays in the inserter for WordPress 7.1](https://make.wordpress.org/core/2026/07/07/the-classic-block-stays-in-the-inserter-for-wordpress-7-1/)  
* 🔍 **Suggestion mode for Notes**: exploring only.  
* 🔍 **Guidelines/Knowledge in Core**: experiment only.

---

## **7.1 carryover check**

| Item (from `wp-7-1-punted-items.md`) | 7.2 status | Links |
| ----- | ----- | ----- |
| On This Day widget | On roadmap; Trac still milestoned 7.1, open | [\#65116](https://core.trac.wordpress.org/ticket/65116) |
| Display inherited styles | Values shown without a flag; indicators still experimental | [\#82520](https://github.com/WordPress/gutenberg/issues/82520) |
| Writing flow / drag and drop | Continued as paper cuts | [\#81453](https://github.com/WordPress/gutenberg/issues/81453) |
| Real-time collaboration | 🏈 Not on 7.2 roadmap | [Post](https://make.wordpress.org/core/2026/09/18/moving-to-a-server-aware-approach-for-collaboration/) |
| Guidelines | Experiment / AI plugin | [\#77230](https://github.com/WordPress/gutenberg/issues/77230) |
| Table of Contents block | On roadmap; partly done | [\#42229](https://github.com/WordPress/gutenberg/issues/42229) |
| Classic block deprecation | No 7.2 target found | [Post](https://make.wordpress.org/core/2026/07/07/the-classic-block-stays-in-the-inserter-for-wordpress-7-1/) |
| React 19 | 🏈 Plugin only; Core likely 7.3 | [\#71336](https://github.com/WordPress/gutenberg/issues/71336) |
| AI generation streaming | AI roadmap item | [php-ai-client \#100](https://github.com/WordPress/php-ai-client/issues/100) |
| Abilities API expansion | AI plugin work | [AI \#40](https://github.com/WordPress/ai/issues/40) |
| AI embeddings | Trac milestoned 7.2, open | [\#65638](https://core.trac.wordpress.org/ticket/65638) |
| Unicode email addresses | 🔍 Conflict: [changeset 62482](https://core.trac.wordpress.org/changeset/62482/) committed June 10 with `@since 7.1.0` and no revert shown, but your punted list marks it ❌ and [\#31992](https://core.trac.wordpress.org/ticket/31992) is still open. Check whether it shipped in 7.1. | [Call for testing](https://make.wordpress.org/core/2026/06/10/call-for-testing-unicode-email-addresses/) |

---

## **Open questions to resolve after Beta 1 🔍**

1. Confirm the Gutenberg range (expected 23.7–24.2) from the Beta 1 post.  
2. Find the 7.2 highlight grid issue.  
3. Secrets API: 7.2 or 7.3?  
4. `wp_kses()` on the HTML API: 7.2 or 7.3?  
5. DataForm editor inspector: on by default or still an experiment?  
6. Extensible Site Editor v2: does it stay experimental?  
7. Description list block: is there an implementing PR?  
8. `-current` custom states: did they land?  
9. Which 23.8 items shipped in 7.1 vs 7.2 (visual revisions URLs/code view, note mention emails, `responsiveEditingEnabled`).  
10. Unicode email: shipped in 7.1 or not?  
11. Open state and milestones for every GitHub issue here: page fetches didn't show them.  
12. Watch the [dev notes tag](https://make.wordpress.org/core/tag/dev-notes+7-2/) as notes land between Beta 1 and RC 1\.

---

## **Sweep: October 19 (day before Beta 1\)**

**Make Core:** No new 7.2 posts or dev notes since October 14\. The only dev note is still `NO_BACKSLASH_ESCAPES`. New posts were [WP Feature Notifications weekly update](https://make.wordpress.org/core/2026/10/16/wp-feature-notifications-weekly-update-2026-10-16/) and [Call for code review help: Gutenberg wp/x.y branch workflows](https://make.wordpress.org/core/2026/10/16/call-for-code-review-help-repairing-gutenberg-github-actions-workflows-for-wp-x-y-branches/), neither of which affects the draft.

**Unchanged:**

* Secrets API: no decision posted. [wordpress-develop \#13759](https://github.com/WordPress/wordpress-develop/pull/13759) is open, marked "do not merge," with no October activity. Trac \#66187 and \#66208 couldn't be fetched.  
* Description List ([\#81728](https://github.com/WordPress/gutenberg/pull/81728)): still not merged.  
* Table of Contents: no stabilization commit.

**Merged to Gutenberg trunk October 16–19 (after 24.2), now in the draft with 🔍 "confirm in Beta 1":**

* Notes emoji reactions ([\#76767](https://github.com/WordPress/gutenberg/pull/76767)). This was on the "not expected" list; it landed.  
* Notes: Add note toolbar button is add-only ([\#84635](https://github.com/WordPress/gutenberg/pull/84635)); anchor highlights ([\#80578](https://github.com/WordPress/gutenberg/pull/80578)).  
* **DataForm inspector stabilized** ([\#85081](https://github.com/WordPress/gutenberg/pull/85081)).  
* Navigation sidebar editing: edit links in a popover from List View ([\#84005](https://github.com/WordPress/gutenberg/pull/84005)); inserter for empty menus ([\#84003](https://github.com/WordPress/gutenberg/pull/84003)). Navigation Link "Open in new tab" from the popover ([\#83506](https://github.com/WordPress/gutenberg/pull/83506)).  
* Global Styles: elements listed alongside blocks ([\#81645](https://github.com/WordPress/gutenberg/pull/81645)); preview selected state ([\#83787](https://github.com/WordPress/gutenberg/pull/83787)).  
* Post Title fit text ([\#83036](https://github.com/WordPress/gutenberg/pull/83036)).  
* Non-breaking spaces marked with a replace button ([\#84737](https://github.com/WordPress/gutenberg/pull/84737)); drag a multi-selection from anywhere inside it ([\#81602](https://github.com/WordPress/gutenberg/pull/81602)).  
* Animated image sub-sizes ([\#80385](https://github.com/WordPress/gutenberg/pull/80385)), from the client-side media iteration.  
* Auto-attach refinements ([\#84851](https://github.com/WordPress/gutenberg/pull/84851), [\#84890](https://github.com/WordPress/gutenberg/pull/84890)).  
* Save-failure error: copy option and show/hide details ([\#82496](https://github.com/WordPress/gutenberg/pull/82496)).  
* "My patterns" renamed "Site patterns" with author filter ([\#84680](https://github.com/WordPress/gutenberg/pull/84680)); restoring a revision saves unsaved changes first ([\#84590](https://github.com/WordPress/gutenberg/pull/84590)); backup date shown ([\#84735](https://github.com/WordPress/gutenberg/pull/84735)); snackbars with actions stay longer ([\#84842](https://github.com/WordPress/gutenberg/pull/84842)).  
* Core actions registered on the server, new `@wordpress/core-actions` ([\#84660](https://github.com/WordPress/gutenberg/pull/84660), [\#84643](https://github.com/WordPress/gutenberg/pull/84643)).  
* Popular icons shipped to `core-admin` ([\#85072](https://github.com/WordPress/gutenberg/pull/85072)).

**Merged but not added (minor or internal):** Connectors screen preloads REST responses ([\#77353](https://github.com/WordPress/gutenberg/pull/77353)); List View nesting with top-level items ([\#84856](https://github.com/WordPress/gutenberg/pull/84856)); slug preview from the current title ([\#84893](https://github.com/WordPress/gutenberg/pull/84893), [\#84896](https://github.com/WordPress/gutenberg/pull/84896)); avatar fallbacks ([\#84824](https://github.com/WordPress/gutenberg/pull/84824)); Emotion removal and TypeScript conversions.

## **Automated scan results: October 22, 2026**

Changes to linked items

* Reopened: \#66187 Secrets API. https://core.trac.wordpress.org/ticket/66187

New candidates (not in the Doc yet)

* ~~Accordion block attributes. https://github.com/WordPress/gutenberg/pull/81500~~
* Font size presets. https://github.com/WordPress/gutenberg/pull/81777

End of automated scan results: October 22, 2026

A note Justin wrote below the block: see https://github.com/WordPress/gutenberg/pull/81888

## Automated scan results: October 29, 2026

* Tabs block. https://github.com/WordPress/gutenberg/pull/81999

# **Punted from 7.2**

# **Backlog from 7.1**