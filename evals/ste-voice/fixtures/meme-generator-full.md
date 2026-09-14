# Meme Generator

Skill Level:

⏲️ 25 minutes

## Overview

In this recipe, we’re whipping up a meme generator block that’s sure to spice up your WordPress site! You’ll learn how to connect to a third-party meme API, let users add their own text, and even register custom fonts to give their creations that perfect punchline. It’s a flavorful mix of fun, functionality, and font finesse—so grab your spatula, and let’s get silly in the editor! 🧂😎🖼️

## Setup

You can choose to either use the repository which provides a development environment or to just download the standalone plugin

## Standalone

Instructions
Run the following command in a terminal of your choice from inside the plugins directory of your local WordPress installation.

```bash
npx @wordpress/create-block@latest meme-generator –template @block-developer-cookbook/meme-generator
```

Once the scaffold has completed completed, start the build process from inside the newly created plugin

```bash
cd meme-generator && npm run start
```

Finally, make sure to activate the plugin.

## Repository

Instructions
Checkout the repository (skip this step if already done)

```bash
git clone git@github.com:ryanwelcher/block-developer-cookbook.git
```

Install the dependencies

```bash
npm install
```

Start the development environment (make sure you have Docker installed )

```bash
npm run env start
```

Run the following script from the root of the repository

```bash
npm run prep:meme-generator
```

Once the scaffold has completed completed, start the build process from inside the newly created plugin

```bash
cd plugins/meme-generator && npm run start
```

## Step 1 – Setting up the block attributes

A meme consists of an image overlayed with some text. In our case, we’re going to have two text boxes; one at the top of the image and one at the bottom.

The image attribute be an object so we can store various details about the image and then we need to store a topText and bottomText attributes to save our hilarious meme text.

Open the block.json file and update it with the following attribute definitions

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

## Step 2 – Adding editable text fields

Now that we have some attributes, we can update the edit.js to allow the user to input some text. To do this, we’ll use the RichText component from the @wordpress/block-editor package but before we add the component, we need to retrieve the attributes from the block.

Open edit.js and add the following to the Edit component:

```js
/* eslint-disable no-undef */
/**
 * WordPress dependencies
 */
import { __ } from ‘@wordpress/i18n’;
import {
	useBlockProps,
	RichText,
	BlockControls,
} from ‘@wordpress/block-editor’;
import {
	Placeholder,
	ToolbarGroup,
	ToolbarButton,
	TextControl,
} from ‘@wordpress/components’;
import { useState, useEffect } from ‘@wordpress/element’;

/**
 * Internal dependencies
 */
import { ApiImageSelect } from ‘./components’;
import MemeIcon from ‘./icon’;
import ‘./editor.scss’;

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
	return (
		<>
			<section { …blockProps }>
				<div className=”meme-wrapper”>
					<div
						className=”text-overlay text-overlay__top”
						style={ { color: ‘white’ } }
					>
						Top Text
					</div>
					<div
						className=”text-overlay text-overlay__bottom”
						style={ { color: ‘white’ } }
					>
						Bottom Text
					</div>
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

Now, we can update the static div tags with instances of the RichText component and connect them to the attributes.

```js
/* eslint-disable no-undef */
/**
 * WordPress dependencies
 */
import { __ } from ‘@wordpress/i18n’;
import {
	useBlockProps,
	RichText,
	BlockControls,
} from ‘@wordpress/block-editor’;
import {
	Placeholder,
	ToolbarGroup,
	ToolbarButton,
	TextControl,
} from ‘@wordpress/components’;
import { useState, useEffect } from ‘@wordpress/element’;

/**
 * Internal dependencies
 */
import { ApiImageSelect } from ‘./components’;
import MemeIcon from ‘./icon’;
import ‘./editor.scss’;

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

The RichText component has a lot of properties and you can see the full list here. The ones we’re using are pretty self explanatory but you may ask why is allowsFormats set to an empty array? This is because we’re going to control the formatting for all of the text at the block level. Just ignore that style property, it’s just so we can see the text for now 🙂

Now that we have the text editable, we need to update the save.js to output the attributes using the RichText.Content component.

Open save.js and update it with the following:

```js
/**
 * WordPress dependencies
 */
import { useBlockProps, RichText } from ‘@wordpress/block-editor’;

/**
 * The save function defines the way in which the different attributes should
 * be combined into the final markup, which is then serialized by the block
 * editor into `post_content`.
 *
 * @param {Object} root0
 * @param {Object} root0.attributes
 * @see https://developer.wordpress.org/block-editor/developers/block-api/block-edit-save/#save
 */
export default function save( { attributes } ) {

	const { topText, bottomText } = attributes;
	
	return (
		<section { …useBlockProps.save() }>
			<div className=”meme-wrapper”>
				<RichText.Content
					value={ topText }
					tagName=”div”
					className=”text-overlay text-overlay__top”
					style={ { color: ‘white’ } }
				/>
				<RichText.Content
					value={ bottomText }
					tagName=”div”
					className=”text-overlay text-overlay__bottom”
					style={ { color: ‘white’ } }
				/>
				<img
					src=”https://i.imgflip.com/1bh8.jpg”
					alt=”The Most Interesting Man In The World”
				/>
			</div>
		</section>
	);
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

Save, refresh, and open the console. Do you notice that something? There are A LOT of messages from our fetch. In fact, if you leave it long enough you’ll crash browser.

To fix this, we need to control when the request is run and more importantly, how many times it’s run. Luckily for us, React has a built in hook that can do exactly this called useEffect. This hooks entire purpose is to help a component work with external systems. Any function that is passed to the hook will be run when something in the component changes.

Remove the fetch call (for now) and update edit.js with the following:

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

Save and refresh the page and notice that every time we select the block in the editor, there is a console message. This is much better but in our case, we only want the useEffect to run when the block is first mounted in the block editor. We can use the hooks dependency parameter to control this further. This parameter accepts an array of dependencies the will trigger the useEffect to run. If the parameter is not added as we have done, the hook is run when ANYTHING is changed. It we add an empty array, it will only run when the component is first rendered.

Update the hook with the following:

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

## Step 4 – Async/await in a useEffect hook

Async/await is a really nice way of dealing Promises in JavaScript. It allows us to avoid chaining then statements and makes the code generally more readable. It is implemented by defining an asynchronous function and using await inside it’s body to pause execution until the promise is resolved.

Unfortunately, we can’t just add the async keyword to the function that is being passed to useEffect because they are by default synchronous to avoid race conditions.

This will have unexpected results and will trigger a warning in your IDE:

```js
useEffect( async () => {
	const response = await fetch( ‘https://api.imgflip.com/get_memes’ );
	const { success, data } = await response.json();
	if ( success ) {
		console.log( data.memes );
		setAllImages( data.memes );
	} else {
		console.log( ‘no data’ );
	}
}, [] );
```

What we can do is define an async function inside the hook and call it immediately:

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
		// Define the async function.
		const loadImages = async () => {
			const response = await fetch( ‘https://api.imgflip.com/get_memes’ );
			const { success, data } = await response.json();
			if ( success ) {
				setAllImages( data.memes );
			}
		};
		// Call the function
		loadImages();
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

## Step 5 – Filtering the images and caching them

The list of images returned from the API contain memes that have different amount of text boxes associated with them. Some only have one while others have as many as five.

For our block, we’re going to only use the ones that have two. Let’s add a filter to the useEffect hook:

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
		// Define the async function.
		const loadImages = async () => {
			const response = await fetch( ‘https://api.imgflip.com/get_memes’ );
			const { success, data } = await response.json();
			if ( success ) {
				const filteredMemes = data.memes.filter(
					( meme ) => meme.box_count === 2
				);
				setAllImages( filteredMemes );
			}
		};
		// Call the function
		loadImages();
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

To make this even more performant, let’s use browser session storage to cache the list of images for any other instances of this block.

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
		// Define the async function.
		const loadImages = async () => {
			const sessionImages = sessionStorage.getItem( ‘meme_images’ );
			if ( sessionImages ) {
				setAllImages( JSON.parse( sessionImages ) );
			} else {
				const response = await fetch(
					‘https://api.imgflip.com/get_memes’
				);
				const { success, data } = await response.json();
				if ( success ) {
					const filteredMemes = data.memes.filter(
						( meme ) => meme.box_count === 2
					);
					setAllImages( filteredMemes );
					sessionStorage.setItem(
						‘meme_images’,
						JSON.stringify( filteredMemes )
					);
				}
			}
		};
		// Call the function
		loadImages();
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

## Step 6 – Building the image selector

Now that we have some images, we need to create the UI for the user to select one. This is probably the most important step to creating the meme so let’s make sure the user is presented with the choice immediately by using the <Placeholder /> component if there is no image saved. This component will contain the instructions and UI elements associated with selecting the image.

Update the edit.js with the following:

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
		// Define the async function.
		const loadImages = async () => {
			const sessionImages = sessionStorage.getItem( ‘meme_images’ );
			if ( sessionImages ) {
				setAllImages( JSON.parse( sessionImages ) );
			} else {
				const response = await fetch(
					‘https://api.imgflip.com/get_memes’
				);
				const { success, data } = await response.json();
				if ( success ) {
					const filteredMemes = data.memes.filter(
						( meme ) => meme.box_count === 2
					);
					setAllImages( filteredMemes );
					sessionStorage.setItem(
						‘meme_images’,
						JSON.stringify( filteredMemes )
					);
				}
			}
		};
		// Call the function
		loadImages();
	}, [] );

	// If we don’t have an image, show the placeholder
	if ( ! image ) {
		return (
			<section { …blockProps }>
				<Placeholder
					icon={ <MemeIcon /> }
					instructions={ __(
						‘Choose an image for your meme:’,
						‘meme-generator’
					) }
					label={ __( ‘Meme Generator’, ‘meme-generator’ ) }
				>
					<ApiImageSelect
						images={ allImages }
						setAttributes={ setAttributes }
					/>
				</Placeholder>
			</section>
		);
	}
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
					<img src={ image.url } alt={ image.name } />
				</div>
			</section>
		</>
	);
}
```

The code above renders a <Placeholder /> component when there is no image selected. Inside of that there is a custom component called <ApiImageSelect /> that handles displaying and selecting the images. The component is provided to speed things along but feel free to have a look at that code to see how it’s built.

Once you save and reload the block, you should see this:

![screenshot](image)

When you select an image, it should be displayed in the block but we need to be sure it’s saved correctly for the front end so we also need to make some changes to save.js

```js
/**
 * WordPress dependencies
 */
import { useBlockProps, RichText } from ‘@wordpress/block-editor’;

/**
 * The save function defines the way in which the different attributes should
 * be combined into the final markup, which is then serialized by the block
 * editor into `post_content`.
 *
 * @param {Object} root0
 * @param {Object} root0.attributes
 * @see https://developer.wordpress.org/block-editor/developers/block-api/block-edit-save/#save
 */
export default function save( { attributes } ) {

	const {
		topText,
		bottomText,
		image: { url: src, name: imageAlt, width, height } = {},
	} = attributes;
	
	return (
		<section { …useBlockProps.save() }>
			<div className=”meme-wrapper”>
				<RichText.Content
					value={ topText }
					tagName=”div”
					className=”text-overlay text-overlay__top”
					style={ { color: ‘white’ } }
				/>
				<RichText.Content
					value={ bottomText }
					tagName=”div”
					className=”text-overlay text-overlay__bottom”
					style={ { color: ‘white’ } }
				/>
				<img
					src={ src }
					alt={ imageAlt }
					width={ width }
					height={ height }
				/>
			</div>
		</section>
	);
}
```

Refresh the block and select an image to make sure it’s working.

## Step 7 – Adding block controls to manage the image.

At this point, we have a working block that can select an image and add some text. However, there is not a way to change the image. Let’s add a button to the block controls to allow the user to remove the image and choose another.

In order add a new button to the blocks controls we need to use the <BlockControls> component. This component is a SlotFill that will inject any of its child components into the control bar.

Inside it, we create a new <ToolbarGroup> and place a <ToolbarButton/> inside it.

Update the edit.js with the following code:

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
		// Define the async function.
		const loadImages = async () => {
			const sessionImages = sessionStorage.getItem( ‘meme_images’ );
			if ( sessionImages ) {
				setAllImages( JSON.parse( sessionImages ) );
			} else {
				const response = await fetch(
					‘https://api.imgflip.com/get_memes’
				);
				const { success, data } = await response.json();
				if ( success ) {
					const filteredMemes = data.memes.filter(
						( meme ) => meme.box_count === 2
					);
					setAllImages( filteredMemes );
					sessionStorage.setItem(
						‘meme_images’,
						JSON.stringify( filteredMemes )
					);
				}
			}
		};
		// Call the function
		loadImages();
	}, [] );

	// If we don’t have an image, show the placeholder
	if ( ! image ) {
		return (
			<section { …blockProps }>
				<Placeholder
					icon={ <MemeIcon /> }
					instructions={ __(
						‘Choose an image for your meme:’,
						‘meme-generator’
					) }
					label={ __( ‘Meme Generator’, ‘meme-generator’ ) }
				>
					<ApiImageSelect
						images={ allImages }
						setAttributes={ setAttributes }
					/>
				</Placeholder>
			</section>
		);
	}
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
					<img src={ image.url } alt={ image.name } />
				</div>
			</section>
			<BlockControls>
				<ToolbarGroup>
					<ToolbarButton
						icon=”remove”
						label={ __( ‘Remove Meme Image’, ‘meme-generator’ ) }
						onClick={ () => setAttributes( { image: false } ) }
					/>
				</ToolbarGroup>
			</BlockControls>
		</>
	);
}
```

The <ToolbarButton/> will show the icon and sets the image attribute to false.

Refresh the page and you should now see the new icon:

![screenshot](image)

Press the button to remove the image and choose another one!

## Step 8 – Formatting the text

Now that we can choose and update the image, you’ve probably noticed that each image are pretty different in color and layout and we need some control over how the text looks and where it sits on the image.

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

This configuration allows the user to pick a text color from the list of colors provded by the active theme. Choosing the background color for text is enabled by default so we disable that as it’s not being used. We also disable the contrast checker as it will appear based on the contrast between the text color and the default theme background color which might show a false positive and confuse the user.

Refresh the block and you should now see the option to choose the text color:

![screenshot](image)

Next, let’s add some typography controls for the size and alignment of the text.

Update block.json with the following:

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

Open up meme-generator.php and add the following code inside the init hook callback:

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

Save the change and if you look in the Style section of the Site Editor, you can see the new fonts are ready to be installed

![screenshot](image)

After installing the fonts, they are available in the block.

![screenshot](image)

Stick a fork in it, you’re done! Congrats and bon appetite!

## Bonus Challenge – Searching for images by name.

At this point, we have a working block but we can always improve on our recipe. Let’s add the ability to search for a specific meme image based on the name. I’ll give you some guidelines/hints:

- The search should take place in the <Placeholder/> component.

- You may need to store some new items in state.

- You may want to use a hook that we already used.

- You’ll only need to modify edit.js

Chef’s solution
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
	const [ filteredImages, setFilteredImages ] = useState( [] );
	const [ searchTerm, setSearchTerm ] = useState( ” );

	useEffect( () => {
		// Define the async function.
		const loadImages = async () => {
			const sessionImages = sessionStorage.getItem( ‘meme_images’ );
			if ( sessionImages ) {
				setAllImages( JSON.parse( sessionImages ) );
				setFilteredImages( JSON.parse( sessionImages );
			} else {
				const response = await fetch(
					‘https://api.imgflip.com/get_memes’
				);
				const { success, data } = await response.json();
				if ( success ) {
					const filteredMemes = data.memes.filter(
						( meme ) => meme.box_count === 2
					);
					setAllImages( filteredMemes );
					setFilteredImages( filteredMemes );
					sessionStorage.setItem(
						‘meme_images’,
						JSON.stringify( filteredMemes )
					);
				}
			}
		};
		// Call the function
		loadImages();
	}, [] );

	// Filter the Meme based on the search term
	useEffect( () => {
		const searchTermLower = searchTerm.toLowerCase();
		const filtered = allImages.filter( ( meme ) =>
			meme.name.toLowerCase().includes( searchTermLower )
		);
		setFilteredImages( filtered );
	}, [ searchTerm, allImages ] );

	// If we don’t have an image, show the placeholder
	if ( ! image ) {
		return (
			<section { …blockProps }>
				<Placeholder
					icon={ <MemeIcon /> }
					instructions={ __(
						‘Choose an image for your meme:’,
						‘meme-generator’
					) }
					label={ __( ‘Meme Generator’, ‘meme-generator’ ) }
				>
					<TextControl
						label={ __( ‘Search’, ‘meme-generator’ ) }
						value={ searchTerm }
						onChange={ ( newSearchTerm ) =>
							setSearchTerm( newSearchTerm )
						}
					/>
					<ApiImageSelect
						images={ filteredImages }
						setAttributes={ setAttributes }
					/>
				</Placeholder>
			</section>
		);
	}
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
					<img src={ image.url } alt={ image.name } />
				</div>
			</section>
			<BlockControls>
				<ToolbarGroup>
					<ToolbarButton
						icon=”remove”
						label={ __( ‘Remove Meme Image’, ‘meme-generator’ ) }
						onClick={ () => setAttributes( { image: false } ) }
					/>
				</ToolbarGroup>
			</BlockControls>
		</>
	);
}
```
