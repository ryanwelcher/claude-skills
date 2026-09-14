# Meme Generator

Skill Level:

⏲️ 25 minutes

## Overview

In this recipe, we’re whipping up a meme generator block that’s sure to spice up your WordPress site! You’ll learn how to connect to a third-party meme API, let users add their own text, and even register custom fonts to give their creations that perfect punchline. It’s a flavorful mix of fun, functionality, and font finesse—so grab your spatula, and let’s get silly in the editor! 🧂😎🖼️

## Setup

Use one of two ways to set up the plugin:

- The repository, which gives you a full development environment.
- The standalone plugin.

## Standalone

1. Run the following command in a terminal, from the plugins directory of your local WordPress installation.

```bash
npx @wordpress/create-block@latest meme-generator –template @block-developer-cookbook/meme-generator
```

2. After the command finishes, start the build process from the new plugin directory.

```bash
cd meme-generator && npm run start
```

3. Activate the plugin.

Make sure that the plugin is active before you continue.

## Repository

1. Optional: Clone the repository.

```bash
git clone git@github.com:ryanwelcher/block-developer-cookbook.git
```

2. Install the dependencies.

```bash
npm install
```

3. Before you continue, make sure that Docker is installed. Start the development environment.

```bash
npm run env start
```

4. Run the following script from the root of the repository.

```bash
npm run prep:meme-generator
```

5. After the script finishes, start the build process from the new plugin directory.

```bash
cd plugins/meme-generator && npm run start
```

Make sure that the build process starts without errors.

## Step 1 – Setting up the block attributes

A meme consists of an image overlayed with some text. In our case, we’re going to have two text boxes; one at the top of the image and one at the bottom.

The `image` attribute is an object. It stores details about the image. The `topText` and `bottomText` attributes store the meme text.

Open `block.json`. Change it to the following attribute definitions:

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

Save the file, refresh the page, and open the console. The console shows many messages from the fetch call. If you leave the page open, the browser crashes.

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

Save and refresh the page and notice that every time we select the block in the editor, there is a console message. This is much better but in our case, we only want `useEffect` to run when the block first mounts in the block editor. We can use the hooks dependency parameter to control this further. This parameter accepts an array of dependencies. A change to any dependency starts `useEffect` again. If the parameter is not added as we have done, the hook is run when ANYTHING is changed. It we add an empty array, it will only run when the component is first rendered.

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

Now, you’ll see that the hook is only run once ever. This is the exact case we want for our initial fetch so let’s add that into the hook.

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

At this point, we have the data being loaded once and then being stored in the addImages variable.

## Step 8 – Formatting the text

Each image has a different color and layout. The block needs controls for how the text looks and where it sits on the image.

Let’s start with choosing the font color.

Open up block.json and add the following to the supports property:

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

This configuration lets the user select a text color from the list of colors provided by the active theme. The background color option is enabled by default. Disable it because the block does not use it. We also disable the contrast checker as it will appear based on the contrast between the text color and the default theme background color which might show a false positive and confuse the user.

Refresh the block. The option to select the text color appears:

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

Open `meme-generator.php`. Add the following code inside the `init` hook callback:

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

There is a lot of code here. The `wp_register_font_collection` function lets you register a group of fonts that are available to be installed. The fonts can be available on the system, loaded from Google fonts, or even from a font file provided by a plugin. The code above shows examples of all three,

For a deeper dive into registering custom fonts, read the related article on the WordPress.org Developer Blog.

Save the change. Go to **Appearance > Editor > Styles > Typography**. The new fonts are ready to install.

![screenshot](image)

After installing the fonts, they are available in the block.

![screenshot](image)

Stick a fork in it, you’re done! Congrats and bon appetite!

