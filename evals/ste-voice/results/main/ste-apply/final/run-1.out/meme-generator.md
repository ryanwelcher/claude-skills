# Meme Generator

Skill Level:

⏲️ 25 minutes

## Overview

In this recipe, we’re whipping up a meme generator block that’s sure to spice up your WordPress site! You’ll learn how to connect to a third-party meme API, let users add their own text, and even register custom fonts to give their creations that perfect punchline. It’s a flavorful mix of fun, functionality, and font finesse—so grab your spatula, and let’s get silly in the editor! 🧂😎🖼️

## Setup

Select one of these setups:

- **Standalone** — download the standalone plugin only.
- **Repository** — use the repository, which includes a development environment.

## Standalone

1. Open a terminal in the plugins directory of your local WordPress installation.
2. Run this command:

```bash
npx @wordpress/create-block@latest meme-generator –template @block-developer-cookbook/meme-generator
```

3. After the scaffold completes, go to the new plugin directory and start the build process:

```bash
cd meme-generator && npm run start
```

4. Activate the plugin.

Make sure that the Meme Generator plugin shows as active on the **Plugins** screen.

## Repository

**NOTE:** This procedure needs Docker. Install Docker before you start.

1. If you have not cloned the repository, clone it:

```bash
git clone git@github.com:ryanwelcher/block-developer-cookbook.git
```

2. Install the dependencies:

```bash
npm install
```

3. Start the development environment:

```bash
npm run env start
```

4. Run this script from the root of the repository:

```bash
npm run prep:meme-generator
```

5. After the scaffold completes, go to the new plugin directory and start the build process:

```bash
cd plugins/meme-generator && npm run start
```

Make sure that the build process starts without errors.

## Step 1 – Setting up the block attributes

A meme consists of an image overlayed with some text. In our case, we’re going to have two text boxes; one at the top of the image and one at the bottom.

The block uses three attributes:

| Attribute | Type | Purpose |
|---|---|---|
| `image` | object | Stores the image details |
| `topText` | string | Stores the top text |
| `bottomText` | string | Stores the bottom text |

1. Open `block.json`.
2. Change the contents to the following attribute definitions:

```json
{
	“$schema”: “https://schemas.wp.org/trunk/block.json”,
	“apiVersion”: 3,
	“name”: “block-developers-cookbook/meme-generator”,
	“version”: “1.0.0”,
	“title”: “Meme Generator”,
	“category”: “block-developer-cookbook”,
	“description”: “Generate and display memes on your site.”,
	“example”: {},
	“attributes”: {
		“topText”: {
			“type”: “string”
		},
		“bottomText”: {
			“type”: “string”
		},
		“image”: {
			“type”: “object”
		}
	},
	“supports”: {},
	“textdomain”: “meme-generator”,
	“editorScript”: “file:./index.js”,
	“editorStyle”: “file:./index.css”,
	“style”: “file:./style-index.css”
}
```

## Step 3 – Getting the images

Now that we have the text fields in place, we need to get the images. For this block, we’re going to use a 3rd party API called https://imgflip.com/api to provide a list of common meme images that we can use.

There is a public endpoint available at https://api.imgflip.com/get_memes which returns JSON data that looks like this:

```json
{
	“success”: true,
	“data”: {
		“memes”: [
			{
				“id”: “181913649”,
				“name”: “Drake Hotline Bling”,
				“url”: “https://i.imgflip.com/30b1gx.jpg”,
				“width”: 1200,
				“height”: 1200,
				“box_count”: 2,
				“captions”: 1426000
			},
			// More memes….
		]
	}
}
```

Use the JavaScript `fetch()` function to get the data. Use the React `useState` hook to store the list of images after they load.

**CAUTION:** Do not leave the editor open for long after this step. This code runs `fetch()` on every render, and the requests can crash the browser.

Add the following to `edit.js`:

```js
/**
 * The edit function describes the structure of your block in the context of the
 * editor. This represents what the editor will render when the block is used.
 *
 * @param  root0
 * @param  root0.attributes
 * @param  root0.setAttributes
 * @see https://developer.wordpress.org/block-editor/developers/block-api/block-edit-save/#edit
 * @return {WPElement} Element to render.
 */
export default function Edit( { attributes, setAttributes } ) {
	const { image, topText, bottomText } = attributes;

	const blockProps = useBlockProps();
	// Store the image in state.
	const [ allImages, setAllImages ] = useState( [] );
	
	// Fetch the image from the API
	fetch( ‘https://api.imgflip.com/get_memes’ )
		.then( ( res ) => res.json() )
		.then( ( { success, data } ) => {
			if ( success ) {
				console.log( data );
				setAllImages( data.memes );
			} else {
				console.log( ‘no data’ );
			}
		} );

	return (
		<>
			<section { …blockProps }>
				<div className=”meme-wrapper”>
					<RichText
						className=”text-overlay text-overlay__top”
						value={ topText }
						placeholder={ __( ‘Setup’, ‘meme-generator’ ) }
						onChange={ ( newTopText ) =>
							setAttributes( { topText: newTopText } )
						}
						allowedFormats={ [] }
						disableLineBreaks
						style={ { color: ‘white’ } }
					/>

					<RichText
						className=”text-overlay text-overlay__bottom”
						value={ bottomText }
						placeholder={ __( ‘Punchline’, ‘meme-generator’ ) }
						onChange={ ( newBottomText ) =>
							setAttributes( { bottomText: newBottomText } )
						}
						allowedFormats={ [] }
						disableLineBreaks
						style={ { color: ‘white’ } }
					/>
					<img
						src=”https://i.imgflip.com/1bh8.jpg”
						alt=”The Most Interesting Man In The World”
					/>
				</div>
			</section>
		</>
	);
}
```

1. Save the file and refresh the page.
2. Open the browser console.

Make sure that the console shows many messages from the fetch call. The next change fixes this problem.

To fix this, we need to control when the request is run and more importantly, how many times it’s run. Luckily for us, React has a built in hook that can do exactly this called useEffect. This hooks entire purpose is to help a component work with external systems. Any function that is passed to the hook will be run when something in the component changes.

1. Remove the fetch call. You add it again later in this step.
2. Change `edit.js` to the following:

```js
/**
 * The edit function describes the structure of your block in the context of the
 * editor. This represents what the editor will render when the block is used.
 *
 * @param  root0
 * @param  root0.attributes
 * @param  root0.setAttributes
 * @see https://developer.wordpress.org/block-editor/developers/block-api/block-edit-save/#edit
 * @return {WPElement} Element to render.
 */
export default function Edit( { attributes, setAttributes } ) {
	const { image, topText, bottomText } = attributes;

	const blockProps = useBlockProps();
	const [ allImages, setAllImages ] = useState( [] );

	useEffect( () => {
		console.log( ‘useEffect is running’ );
	} );
	
	return (
		<>
			<section { …blockProps }>
				<div className=”meme-wrapper”>
					<RichText
						className=”text-overlay text-overlay__top”
						value={ topText }
						placeholder={ __( ‘Setup’, ‘meme-generator’ ) }
						onChange={ ( newTopText ) =>
							setAttributes( { topText: newTopText } )
						}
						allowedFormats={ [] }
						disableLineBreaks
						style={ { color: ‘white’ } }
					/>

					<RichText
						className=”text-overlay text-overlay__bottom”
						value={ bottomText }
						placeholder={ __( ‘Punchline’, ‘meme-generator’ ) }
						onChange={ ( newBottomText ) =>
							setAttributes( { bottomText: newBottomText } )
						}
						allowedFormats={ [] }
						disableLineBreaks
						style={ { color: ‘white’ } }
					/>
					<img
						src=”https://i.imgflip.com/1bh8.jpg”
						alt=”The Most Interesting Man In The World”
					/>
				</div>
			</section>
		</>
	);
}
```

1. Save the file and refresh the page.
2. Select the block in the editor.

Make sure that the console shows a message each time you select the block.

The block needs the `useEffect` hook to run only when the block first mounts in the editor. The dependency array, the second parameter of the hook, controls when the hook runs:

| Dependency array | When the hook runs |
|---|---|
| Not set | Every time the component changes |
| `[]` (empty) | Only when the component first renders |

Change the hook to the following:

```js
/**
 * The edit function describes the structure of your block in the context of the
 * editor. This represents what the editor will render when the block is used.
 *
 * @param  root0
 * @param  root0.attributes
 * @param  root0.setAttributes
 * @see https://developer.wordpress.org/block-editor/developers/block-api/block-edit-save/#edit
 * @return {WPElement} Element to render.
 */
export default function Edit( { attributes, setAttributes } ) {
	const { image, topText, bottomText } = attributes;

	const blockProps = useBlockProps();
	const [ allImages, setAllImages ] = useState( [] );

	useEffect( () => {
		console.log( ‘useEffect is running’ );
	}, [] );

	return (
		<>
			<section { …blockProps }>
				<div className=”meme-wrapper”>
					<RichText
						className=”text-overlay text-overlay__top”
						value={ topText }
						placeholder={ __( ‘Setup’, ‘meme-generator’ ) }
						onChange={ ( newTopText ) =>
							setAttributes( { topText: newTopText } )
						}
						allowedFormats={ [] }
						disableLineBreaks
						style={ { color: ‘white’ } }
					/>

					<RichText
						className=”text-overlay text-overlay__bottom”
						value={ bottomText }
						placeholder={ __( ‘Punchline’, ‘meme-generator’ ) }
						onChange={ ( newBottomText ) =>
							setAttributes( { bottomText: newBottomText } )
						}
						allowedFormats={ [] }
						disableLineBreaks
						style={ { color: ‘white’ } }
					/>
					<img
						src=”https://i.imgflip.com/1bh8.jpg”
						alt=”The Most Interesting Man In The World”
					/>
				</div>
			</section>
		</>
	);
}
```

The hook now runs only once, when the component first renders. Add the fetch call to the hook:

```js
/**
 * The edit function describes the structure of your block in the context of the
 * editor. This represents what the editor will render when the block is used.
 *
 * @param  root0
 * @param  root0.attributes
 * @param  root0.setAttributes
 * @see https://developer.wordpress.org/block-editor/developers/block-api/block-edit-save/#edit
 * @return {WPElement} Element to render.
 */
export default function Edit( { attributes, setAttributes } ) {
	const { image, topText, bottomText } = attributes;

	const blockProps = useBlockProps();
	const [ allImages, setAllImages ] = useState( [] );

	useEffect( () => {
		fetch( ‘https://api.imgflip.com/get_memes’ )
			.then( ( res ) => res.json() )
			.then( ( { success, data } ) => {
				if ( success ) {
					console.log( data.memes );
					setAllImages( data.memes );
				} else {
					console.log( ‘no data’ );
				}
			} );
	}, [] );

	return (
		<>
			<section { …blockProps }>
				<div className=”meme-wrapper”>
					<RichText
						className=”text-overlay text-overlay__top”
						value={ topText }
						placeholder={ __( ‘Setup’, ‘meme-generator’ ) }
						onChange={ ( newTopText ) =>
							setAttributes( { topText: newTopText } )
						}
						allowedFormats={ [] }
						disableLineBreaks
						style={ { color: ‘white’ } }
					/>

					<RichText
						className=”text-overlay text-overlay__bottom”
						value={ bottomText }
						placeholder={ __( ‘Punchline’, ‘meme-generator’ ) }
						onChange={ ( newBottomText ) =>
							setAttributes( { bottomText: newBottomText } )
						}
						allowedFormats={ [] }
						disableLineBreaks
						style={ { color: ‘white’ } }
					/>
					<img
						src=”https://i.imgflip.com/1bh8.jpg”
						alt=”The Most Interesting Man In The World”
					/>
				</div>
			</section>
		</>
	);
}
```

Make sure that the console shows the list of memes only once. The `allImages` state variable now stores the list.

## Step 8 – Formatting the text

Each meme image has different colors and a different layout. The next changes let the user control how the text looks and where it sits on the image.

Let’s start with choosing the font color.

1. Open `block.json`.
2. Add the following to the `supports` property:

```json
{
	“$schema”: “https://schemas.wp.org/trunk/block.json”,
	“apiVersion”: 3,
	“name”: “block-developers-cookbook/meme-generator”,
	“version”: “1.0.0”,
	“title”: “Meme Generator”,
	“category”: “block-developer-cookbook”,
	“description”: “Generate and display memes on your site.”,
	“example”: {},
	“attributes”: {
		“topText”: {
			“type”: “string”
		},
		“bottomText”: {
			“type”: “string”
		},
		“image”: {
			“type”: “object”
		}
	},
	“supports”: {
		“html”: false,
		“color”: {
			“text”: true,
			“background”: false,
			“enableContrastChecker”: false
		}
	},
	“textdomain”: “meme-generator”,
	“editorScript”: “file:./index.js”,
	“editorStyle”: “file:./index.css”,
	“style”: “file:./style-index.css”
}
```

This configuration lets the user select a text color from the colors that the active theme provides.

| Setting | Value | Reason |
|---|---|---|
| `background` | `false` | The block does not use a background color. This option is on by default. |
| `enableContrastChecker` | `false` | The checker compares the text color to the default theme background. It can show a false warning. |

Refresh the block. Make sure that the block sidebar shows the text color option:

![screenshot](image)

Next, let’s add some typography controls for the size and alignment of the text.

Change `block.json` to the following:

```json
{
	“$schema”: “https://schemas.wp.org/trunk/block.json”,
	“apiVersion”: 3,
	“name”: “block-developers-cookbook/meme-generator”,
	“version”: “1.0.0”,
	“title”: “Meme Generator”,
	“category”: “block-developer-cookbook”,
	“description”: “Generate and display memes on your site.”,
	“example”: {},
	“attributes”: {
		“topText”: {
			“type”: “string”
		},
		“bottomText”: {
			“type”: “string”
		},
		“image”: {
			“type”: “object”
		}
	},
	“supports”: {
		“html”: false,
		“color”: {
			“text”: true,
			“background”: false,
			“enableContrastChecker”: false
		},
		“typography”: {
			“fontSize”: true,
			“textAlign”: true
		}
	},
	“textdomain”: “meme-generator”,
	“editorScript”: “file:./index.js”,
	“editorStyle”: “file:./index.css”,
	“style”: “file:./style-index.css”
}
```

Refresh the block again and you can now set the font size and control how text is aligned.

![screenshot](image)

Finally, let’s add some controls to be able to set the font family, style, and weight. Do do this we’re going to use some experimental properties on block.json

```json
{
	“$schema”: “https://schemas.wp.org/trunk/block.json”,
	“apiVersion”: 3,
	“name”: “block-developers-cookbook/meme-generator”,
	“version”: “1.0.0”,
	“title”: “Meme Generator”,
	“category”: “block-developer-cookbook”,
	“description”: “Generate and display memes on your site.”,
	“example”: {},
	“attributes”: {
		“topText”: {
			“type”: “string”
		},
		“bottomText”: {
			“type”: “string”
		},
		“image”: {
			“type”: “object”
		}
	},
	“supports”: {
		“html”: false,
		“color”: {
			“text”: true,
			“background”: false,
			“enableContrastChecker”: false
		},
		“typography”: {
			“fontSize”: true,
			“textAlign”: true
		},
		“__experimentalFontFamily”: true,
		“__experimentalFontStyle”: true,
		“__experimentalFontWeight”: true
	},
	“textdomain”: “meme-generator”,
	“editorScript”: “file:./index.js”,
	“editorStyle”: “file:./index.css”,
	“style”: “file:./style-index.css”
}
```

Refresh and you’ll see some new options for controlling the font in the block sidebar

![screenshot](image)

Great work! Now this block is really starting to take shape!

## Step 9 – Meme fonts

Part of what makes memes great are the fonts they use. At this point, we’re at the mercy of the fonts that have been defined by the active theme or have been installed by the user.

While we can’t automatically install fonts, we can provide some for the user to install. Let’s do that now.

1. Open `meme-generator.php`.
2. Add the following code inside the `init` hook callback:

```php
<?php
/**
 * Plugin Name:       Meme Generator
 * Description:       Generate and display memes on your site.
 * Requires at least: 6.5
 * Requires PHP:      7.0
 * Version:           1.0.0
 * Author:            The Block Developer Cookbook
 * License:           GPL-2.0-or-later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       meme-generator
 *
 * @package           block-developers-cookbook
 */

namespace BlockDevelopersCookbook;

/**
 * Registers the block using the metadata loaded from the `block.json` file.
 * Behind the scenes, it registers also all assets so they can be enqueued
 * through the block editor in the corresponding context.
 *
 * @see https://developer.wordpress.org/reference/functions/register_block_type/
 */
function meme_generator_block_init() {
	// Register the block.
	register_block_type( __DIR__ . ‘/build’ );

	/**
	* Register some Meme fonts
	*/
	wp_register_font_collection( ‘memes’, [
		‘name’          => __( ‘Meme fonts’, ‘meme-generator’ ),
		‘description’   => __( ‘For the LOLZ!.’, ‘meme-generator’ ),
		‘font_families’ => [
			[
				‘font_family_settings’ => [
					‘fontFamily’ => ‘arial, sans-serif’,
					‘slug’       => ‘arial’,
					‘name’       => __( ‘Arial’, ‘meme-generator’ ),
				],
				‘categories’ => [ ‘memes’, ‘sans-serif’ ]
			],
			[
				‘font_family_settings’ => [
					‘fontFamily’ => “Comic Sans MS, cursive, sans-serif”,
					‘slug’       => ‘comic-sans’,
					‘name’       => __( ‘Comic Sans’, ‘meme-generator’ ),
				],
				‘categories’ => [ ‘memes’, ‘serif’ ]
			],
			[
				‘font_family_settings’ => [
					‘fontFamily’ => “‘Impact’, sans-serif”,
					‘slug’       => ‘impact’,
					‘name’       => __( ‘Impact’, ‘meme-generator’ ),
					‘fontFace’   => [
						[
							‘fontFamily’ => ‘Impact’,
							‘src’        => trailingslashit( plugin_dir_url( __FILE__ ) ) . ‘assets/fonts/impact.ttf’,
							‘fontWeight’ => ‘400’,
							‘fontStyle’  => ‘normal’,
						],
					]
				],
				‘categories’ => [ ‘monospace’, ‘serif’ ]
			],
			[
				‘font_family_settings’ => [
					‘fontFamily’ => “‘Montserrat’, sans-serif”,
					‘slug’       => ‘montserrat’,
					‘name’       => __( ‘Montserrat’, ‘meme-generator’ ),
					‘fontFace’   => [
						[
							‘fontFamily’ => ‘Montserrat’,
							‘src’        => ‘https://fonts.gstatic.com/s/montserrat/v30/JTUSjIg1_i6t8kCHKm459WlhyyTh89Y.woff2’,
							‘fontWeight’ => ‘100 900’,
							‘fontStyle’  => ‘normal’,
						],
						[
							‘fontFamily’ => ‘Montserrat’,
							‘src’        => ‘https://fonts.gstatic.com/s/montserrat/v30/JTUQjIg1_i6t8kCHKm459WxRyS7m0dR9pA.woff2’,
							‘fontWeight’ => ‘100 900’,
							‘fontStyle’  => ‘italic’,
						]
					]
				],
				‘categories’ => [ ‘memes’, ‘sans-serif’ ]
			]
		],
		‘categories’ => [
			[
				‘name’ => __( ‘Memes’, ‘meme-generator’ ),
				‘slug’ => ‘memes’
			],
			[
				‘name’ => __( ‘Sans Serif’, ‘meme-generator’ ),
				‘slug’ => ‘sans-serif’
			],

		]
	] );
}
add_action( ‘init’, __NAMESPACE__ . ‘\meme_generator_block_init’ );
```

The `wp_register_font_collection()` function registers a group of fonts that users can install. A font can come from the system, from Google Fonts, or from a font file in a plugin. The code above shows an example of each.

For more information about custom fonts, read the related article on the WordPress.org Developer Blog.

1. Save the file.
2. Go to **Appearance > Editor > Styles > Typography**.

Make sure that the font library shows the new fonts as ready to install:

![screenshot](image)

After installing the fonts, they are available in the block.

![screenshot](image)

Stick a fork in it, you’re done! Congrats and bon appetite!

