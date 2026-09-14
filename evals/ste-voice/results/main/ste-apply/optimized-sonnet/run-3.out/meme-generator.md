# Meme Generator

Skill Level:

⏲️ 25 minutes

## Overview

In this recipe, we’re whipping up a meme generator block that’s sure to spice up your WordPress site! You’ll learn how to connect to a third-party meme API, let users add their own text, and even register custom fonts to give their creations that perfect punchline. It’s a flavorful mix of fun, functionality, and font finesse—so grab your spatula, and let’s get silly in the editor! 🧂😎🖼️

## Setup

Select a setup method: the repository, which provides a development environment, or the standalone plugin.

## Standalone

Instructions
Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation.

```bash
npx @wordpress/create-block@latest meme-generator –template @block-developer-cookbook/meme-generator
```

After the scaffold is complete, start the build process from inside the newly created plugin.

```bash
cd meme-generator && npm run start
```

Finally, make sure to activate the plugin.

## Repository

Instructions
If you already cloned the repository, skip this step. Check out the repository:

```bash
git clone git@github.com:ryanwelcher/block-developer-cookbook.git
```

Install the dependencies

```bash
npm install
```

**NOTE:** Make sure that Docker is installed. Start the development environment:

```bash
npm run env start
```

Run the following script from the root of the repository

```bash
npm run prep:meme-generator
```

After the scaffold is complete, start the build process from inside the newly created plugin.

```bash
cd plugins/meme-generator && npm run start
```

## Step 1 – Setting up the block attributes

A meme consists of an image overlayed with some text. In our case, we’re going to have two text boxes; one at the top of the image and one at the bottom.

The image attribute must be an object to store the image details. Add `topText` and `bottomText` attributes to store the meme text.

Open the block.json file and change it to the following attribute definitions:

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

Now that we have the text fields in place, we need to get the images. This block uses a third-party API, the imgflip API (https://imgflip.com/api), to get a list of common meme images.

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

Use JavaScript’s built-in fetch function to get the data. Use React’s useState hook to store the list of images after they load.

Add the following to edit.js:

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

**CAUTION:** Do not leave the fetch call running. It sends many requests and can crash the browser.

1. Save the file.
2. Refresh the page.
3. Open the browser console.

You will see many messages from the fetch call.

To fix this, we need to control when the request is run and more importantly, how many times it’s run. Luckily for us, React has a built in hook that can do exactly this called useEffect. This hooks entire purpose is to help a component work with external systems. Any function that is passed to the hook will be run when something in the component changes.

Remove the fetch call. Change `edit.js` to the following:

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

Save the file. Refresh the page. Notice that every time you select the block in the editor, there is a console message. This is much better but in our case, we only want the useEffect to run when the block is first mounted in the block editor. We can use the hooks dependency parameter to control this further. This parameter accepts an array of dependencies that will start the useEffect to run. If the parameter is not added as we have done, the hook is run when ANYTHING is changed. If we add an empty array, it will only run when the component is first rendered.

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

Now, you’ll see that the hook is only run once ever. This is the case we want for the initial fetch. Add the fetch call to the hook:

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

At this point, the code loads the data once and stores it in the `allImages` variable.

## Step 8 – Formatting the text

You can now select and change the image. Each image differs in color and layout, so add controls for how the text looks and where it appears.

First, configure the font color.

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

This configuration lets the user select a text color from the theme's color list. The background color option for text is enabled by default. Disable it because the block does not use it. Disable the contrast checker too. It compares the text color to the default theme background color, which can show a false result and confuse the user.

Refresh the block and you should now see the option to choose the text color:

![screenshot](image)

Next, add typography controls for text size and alignment.

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

Refresh the block. Make sure that you can set the font size and align the text.

![screenshot](image)

Finally, add controls for font family, style, and weight. Use experimental properties in `block.json`.

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

Refresh the page. Make sure that new font options appear in the block sidebar.

![screenshot](image)

Great work! Now this block is really starting to take shape!

## Step 9 – Meme fonts

Part of what makes memes great are the fonts they use. The block can only use fonts that the active theme defines or that the user installs.

The block cannot install fonts automatically, but it can offer fonts for the user to install.

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

This code uses the `wp_register_font_collection` function to register a group of fonts that the user can install. The code above shows three font sources:

| Source | Example |
|---|---|
| System font | Arial |
| Google Fonts | Montserrat |
| Font file from the plugin | Impact |

For more information about registering custom fonts, read the related article on the WordPress.org Developer Blog.

Save the change. Go to **Appearance > Editor > Styles** to see the new fonts, ready to install.

![screenshot](image)

After installing the fonts, they are available in the block.

![screenshot](image)

Make sure that the meme block shows the image with your text and font.

Stick a fork in it, you’re done! Congrats and bon appetite!

