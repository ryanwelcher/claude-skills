# Meme Generator

Skill Level:

⏲️ 25 minutes

## Overview

In this recipe, we’re whipping up a meme generator block that’s sure to spice up your WordPress site! You’ll learn how to connect to a third-party meme API, let users add their own text, and even register custom fonts to give their creations that perfect punchline. It’s a flavorful mix of fun, functionality, and font finesse—so grab your spatula, and let’s get silly in the editor! 🧂😎🖼️

## Setup

Select one of these setup options:

| Option | Use it when |
|---|---|
| **Standalone** | You have a local WordPress installation and want only the plugin. |
| **Repository** | You want the development environment that the repository provides. |

## Standalone

Instructions
Open a terminal in the `plugins` directory of your local WordPress installation.

Run this command:

```bash
npx @wordpress/create-block@latest meme-generator –template @block-developer-cookbook/meme-generator
```

After the scaffold completes, start the build from the new `meme-generator` directory:

```bash
cd meme-generator && npm run start
```

Go to **Plugins > Installed Plugins** and activate **Meme Generator**.

Make sure that **Meme Generator** shows as active in the plugin list.

## Repository

Instructions
If you already cloned the repository, skip this step. Clone the repository:

```bash
git clone git@github.com:ryanwelcher/block-developer-cookbook.git
```

Install the dependencies:

```bash
npm install
```

**CAUTION:** Do not start the development environment without Docker. The command fails if Docker is not installed and running.

Start the development environment:

```bash
npm run env start
```

From the root of the repository, run this script:

```bash
npm run prep:meme-generator
```

After the scaffold completes, start the build from the new `plugins/meme-generator` directory:

```bash
cd plugins/meme-generator && npm run start
```

Make sure that the terminal shows no build errors.

## Step 1 – Setting up the block attributes

A meme consists of an image overlayed with some text. In our case, we’re going to have two text boxes; one at the top of the image and one at the bottom.

The image attribute be an object so we can store various details about the image and then we need to store a topText and bottomText attributes to save our hilarious meme text.

In `block.json`, replace the contents with this code:

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

We can use JavaScript’s built in fetch function to retrieve the data but we need to store the results somewhere. We can use Reacts useState hook store the list of images after they have been loaded.

In `src/edit.js`, replace the `Edit` function with this code:

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

**CAUTION:** Do not keep the editor open for a long time with this code. The fetch runs again and again and can crash the browser.

Save `src/edit.js`.

Refresh the editor.

Open the browser console. Make sure that the console shows many messages from the fetch.

To fix this, we need to control when the request is run and more importantly, how many times it’s run. Luckily for us, React has a built in hook that can do exactly this called useEffect. This hooks entire purpose is to help a component work with external systems. Any function that is passed to the hook will be run when something in the component changes.

In `src/edit.js`, replace the `Edit` function with this code. This code removes the fetch call for now:

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

Save the file and refresh the editor.

Select the block. Make sure that the console shows a message each time you select the block.

This is much better but in our case, we only want the useEffect to run when the block is first mounted in the block editor. We can use the hooks dependency parameter to control this further. This parameter accepts an array of dependencies the will trigger the useEffect to run. If the parameter is not added as we have done, the hook is run when ANYTHING is changed. It we add an empty array, it will only run when the component is first rendered.

In `src/edit.js`, change the `useEffect` hook to match this code:

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

Save the file and refresh the editor. Make sure that the console shows the message only one time.

This is the exact case we want for our initial fetch. In `src/edit.js`, move the fetch call into the `useEffect` hook:

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

Save the file and refresh the editor. Make sure that the console shows the list of memes one time.

At this point, we have the data being loaded once and then being stored in the addImages variable.

## Step 8 – Formatting the text

Now that we can choose and update the image, you’ve probably noticed that each image are pretty different in color and layout and we need some control over how the text looks and where it sits on the image.

Let’s start with choosing the font color.

In `block.json`, change the `supports` property to match this code:

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

These settings change the block controls:

| Property | Value | Result |
|---|---|---|
| `color.text` | `true` | The user can select a text color from the colors of the active theme. |
| `color.background` | `false` | The background color control does not show. The block does not use a background color. |
| `color.enableContrastChecker` | `false` | The contrast checker does not show. The checker compares the text color with the theme background color and can show a false warning. |

Refresh the editor and select the block. Make sure that the block sidebar shows the text color control:

![screenshot](image)

Next, let’s add some typography controls for the size and alignment of the text.

In `block.json`, add the `typography` settings to the `supports` property:

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

Refresh the editor and select the block. Make sure that the font size and text alignment controls show for the block.

![screenshot](image)

Finally, let’s add some controls to be able to set the font family, style, and weight.

**NOTE:** Properties that start with `__experimental` can change in a future WordPress release.

In `block.json`, add these experimental properties to the `supports` property:

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

Refresh the editor and select the block. Make sure that the block sidebar shows the font family, style, and weight controls:

![screenshot](image)

Great work! Now this block is really starting to take shape!

## Step 9 – Meme fonts

Part of what makes memes great are the fonts they use. At this point, we’re at the mercy of the fonts that have been defined by the active theme or have been installed by the user.

While we can’t automatically install fonts, we can provide some for the user to install. Let’s do that now.

In `meme-generator.php`, in the `meme_generator_block_init()` function, below `register_block_type()`, add the `wp_register_font_collection()` call:

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

There’s a lot of code here but the wp_register_font_collection function allows us to register a group of fonts that are available to be installed. The fonts can be available on the system, loaded from Google fonts, or even from a font file provided by a plugin. The code above shows examples of all three,

For a deeper dive into registering custom fonts, read the related article on the WordPress.org Developer Blog.

Save `meme-generator.php`.

Go to **Appearance > Editor > Styles > Typography**.

Open the font library. Make sure that the **Meme fonts** collection shows the new fonts:

![screenshot](image)

Install the fonts. Make sure that the fonts show in the font family control of the block:

![screenshot](image)

Stick a fork in it, you’re done! Congrats and bon appetite!

