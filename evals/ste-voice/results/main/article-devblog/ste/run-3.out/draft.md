# How to add a custom toolbar button to your block

The block toolbar is prime real estate. It sits right on top of the block, it only shows up when the block is selected, and it's where users already look when they want to do something to that block. Core blocks use it constantly — alignment, bold, link, replace media — but a lot of custom blocks I review never touch it. Everything ends up in the Settings Sidebar instead, two clicks and a scroll away from where the user is actually working.

Adding your own button takes three components: `BlockControls`, `ToolbarGroup`, and `ToolbarButton`. In this tutorial, we'll build a small image block and add a toolbar button that clears the selected image so the user can start over. It's a simple action, but the pattern is the same one you'll use for any toolbar control you build.

## Prerequisites

- A block plugin made with `@wordpress/create-block`, or a block that builds with `@wordpress/scripts`.
- Node.js and npm installed on your computer.
- WordPress 6.5 or later.
- Basic knowledge of `block.json`, `useBlockProps`, and `setAttributes`.

## How the three components fit together

Before we write any code, it helps to know what each piece does. I think of them as a slot, a container, and a control.

| Component | Package | Job |
|---|---|---|
| `BlockControls` | `@wordpress/block-editor` | A SlotFill. It moves its children into the block toolbar. |
| `ToolbarGroup` | `@wordpress/components` | Groups related controls and adds the divider between groups. |
| `ToolbarButton` | `@wordpress/components` | One button, with an icon, a label, and an `onClick` handler. |

You can put `BlockControls` anywhere in your `Edit` component's output. Because it's a SlotFill, it doesn't matter where it sits in the markup. The editor renders its contents in the toolbar, not inline with your block.

## Start with a basic image block

We need something to clear first. This block stores three attributes for the image, lets the user pick one from the Media Library, and saves a plain `<img>` tag.

### Define the attributes

In `block.json`, replace the `attributes` property with:

```json
"attributes": {
	"imageId": {
		"type": "number"
	},
	"imageUrl": {
		"type": "string"
	},
	"imageAlt": {
		"type": "string",
		"default": ""
	}
}
```

### Build the edit component

Replace the full contents of `src/edit.js` with:

```js
import { __ } from '@wordpress/i18n';
import {
	useBlockProps,
	MediaPlaceholder,
} from '@wordpress/block-editor';

export default function Edit( { attributes, setAttributes } ) {
	const { imageId, imageUrl, imageAlt } = attributes;
	const blockProps = useBlockProps();

	const onSelectImage = ( media ) => {
		setAttributes( {
			imageId: media.id,
			imageUrl: media.url,
			imageAlt: media.alt,
		} );
	};

	return (
		<div { ...blockProps }>
			{ imageUrl ? (
				<img src={ imageUrl } alt={ imageAlt } />
			) : (
				<MediaPlaceholder
					icon="format-image"
					labels={ { title: __( 'Image', 'toolbar-demo' ) } }
					accept="image/*"
					allowedTypes={ [ 'image' ] }
					onSelect={ onSelectImage }
				/>
			) }
		</div>
	);
}
```

### Build the save component

Replace the full contents of `src/save.js` with:

```js
import { useBlockProps } from '@wordpress/block-editor';

export default function save( { attributes } ) {
	const { imageId, imageUrl, imageAlt } = attributes;

	if ( ! imageUrl ) {
		return null;
	}

	return (
		<figure { ...useBlockProps.save() }>
			<img
				src={ imageUrl }
				alt={ imageAlt }
				className={ `wp-image-${ imageId }` }
			/>
		</figure>
	);
}
```

At this point the block works, but there's a problem. After the user selects an image, the placeholder is gone for good. The only way to pick a different one is to delete the block and insert a new one. That's exactly the kind of gap a toolbar button fills.

## Add the toolbar button

The button needs an icon. `@wordpress/icons` is not one of the packages WordPress loads as a global script, so you need to install it.

1. Open a terminal in the root folder of your plugin.
2. Run this command:

   ```bash
   npm install @wordpress/icons --save
   ```

3. Run `npm start` to start the build in watch mode.

Now for the button itself.

4. In `src/edit.js`, change the `@wordpress/block-editor` import to include `BlockControls`:

   ```js
   import {
   	useBlockProps,
   	MediaPlaceholder,
   	BlockControls,
   } from '@wordpress/block-editor';
   ```

5. Below the `@wordpress/block-editor` import, add these two imports:

   ```js
   import { ToolbarGroup, ToolbarButton } from '@wordpress/components';
   import { trash } from '@wordpress/icons';
   ```

6. Below the `onSelectImage` function, add the `onClearImage` function:

   ```js
   const onClearImage = () => {
   	setAttributes( {
   		imageId: undefined,
   		imageUrl: undefined,
   		imageAlt: '',
   	} );
   };
   ```

7. Replace the `return` statement with this code:

   ```js
   return (
   	<>
   		{ imageUrl && (
   			<BlockControls group="other">
   				<ToolbarGroup>
   					<ToolbarButton
   						icon={ trash }
   						label={ __( 'Clear image', 'toolbar-demo' ) }
   						onClick={ onClearImage }
   					/>
   				</ToolbarGroup>
   			</BlockControls>
   		) }
   		<div { ...blockProps }>
   			{ imageUrl ? (
   				<img src={ imageUrl } alt={ imageAlt } />
   			) : (
   				<MediaPlaceholder
   					icon="format-image"
   					labels={ { title: __( 'Image', 'toolbar-demo' ) } }
   					accept="image/*"
   					allowedTypes={ [ 'image' ] }
   					onSelect={ onSelectImage }
   				/>
   			) }
   		</div>
   	</>
   );
   ```

8. Save the file.

To test the button:

1. In the editor, add the block to a post.
2. Select an image from the Media Library.
3. Click the block to select it.
4. In the block toolbar, click the **Clear image** button.
5. Make sure that the image is removed and the placeholder shows again.

Here's the complete `src/edit.js` so you can compare it against yours:

```js
import { __ } from '@wordpress/i18n';
import {
	useBlockProps,
	MediaPlaceholder,
	BlockControls,
} from '@wordpress/block-editor';
import { ToolbarGroup, ToolbarButton } from '@wordpress/components';
import { trash } from '@wordpress/icons';

export default function Edit( { attributes, setAttributes } ) {
	const { imageId, imageUrl, imageAlt } = attributes;
	const blockProps = useBlockProps();

	const onSelectImage = ( media ) => {
		setAttributes( {
			imageId: media.id,
			imageUrl: media.url,
			imageAlt: media.alt,
		} );
	};

	const onClearImage = () => {
		setAttributes( {
			imageId: undefined,
			imageUrl: undefined,
			imageAlt: '',
		} );
	};

	return (
		<>
			{ imageUrl && (
				<BlockControls group="other">
					<ToolbarGroup>
						<ToolbarButton
							icon={ trash }
							label={ __( 'Clear image', 'toolbar-demo' ) }
							onClick={ onClearImage }
						/>
					</ToolbarGroup>
				</BlockControls>
			) }
			<div { ...blockProps }>
				{ imageUrl ? (
					<img src={ imageUrl } alt={ imageAlt } />
				) : (
					<MediaPlaceholder
						icon="format-image"
						labels={ { title: __( 'Image', 'toolbar-demo' ) } }
						accept="image/*"
						allowedTypes={ [ 'image' ] }
						onSelect={ onSelectImage }
					/>
				) }
			</div>
		</>
	);
}
```

A couple of things are worth calling out in there.

- **The `group` prop:** `BlockControls` has four groups — `default`, `inline`, `block`, and `other`. They control where your controls land relative to core's. `block` sits near alignment, `inline` is for text formatting, and `other` goes at the end. A destructive action like clearing an image belongs at the end, so I went with `other`.
- **Conditional rendering:** The whole `BlockControls` only renders when there's an image. There's nothing to clear otherwise, and an extra button that does nothing is just noise.
- **`label`:** This is the tooltip, and it's also the accessible name for screen readers. Icon-only buttons need it.

## Show the button as active

`ToolbarButton` accepts an `isPressed` prop, which is how core shows toggle state for things like bold or italic. Clearing an image isn't a toggle, so our example doesn't need it. But if your button flips an attribute on and off, you want the button to reflect that state.

Here's a second button that toggles a rounded-corners style on the same block. First, the attribute.

1. In `block.json`, add this property inside `attributes`:

   ```json
   "isRounded": {
   	"type": "boolean",
   	"default": false
   }
   ```

2. In `src/edit.js`, change the `@wordpress/icons` import to:

   ```js
   import { trash, cornerAll } from '@wordpress/icons';
   ```

3. In `src/edit.js`, change the destructured attributes to:

   ```js
   const { imageId, imageUrl, imageAlt, isRounded } = attributes;
   ```

4. Inside `<ToolbarGroup>`, above the **Clear image** `ToolbarButton`, add:

   ```js
   <ToolbarButton
   	icon={ cornerAll }
   	label={ __( 'Rounded corners', 'toolbar-demo' ) }
   	isPressed={ isRounded }
   	onClick={ () => setAttributes( { isRounded: ! isRounded } ) }
   />
   ```

5. In `src/save.js`, change the destructured attributes to:

   ```js
   const { imageId, imageUrl, imageAlt, isRounded } = attributes;
   ```

6. In `src/save.js`, change the `useBlockProps.save()` call to:

   ```js
   useBlockProps.save( {
   	className: isRounded ? 'is-rounded' : undefined,
   } )
   ```

7. Make sure that the **Rounded corners** button shows as pressed after you click it.

Two buttons in one `ToolbarGroup` share a section of the toolbar. If you want a divider between them, wrap each one in its own `ToolbarGroup`.

## Gotchas

### Clearing with `undefined`, not `null` or an empty string

This one trips people up. When you set an attribute to `undefined`, the block editor drops it from the block's comment delimiter completely, and any `default` in `block.json` applies again. If you set `imageUrl` to an empty string, the attribute is still stored, and a check like `imageUrl ? … : …` happens to work, but `imageId` set to `''` doesn't match the `number` type, and the editor quietly ignores it the next time the post loads. Stick with `undefined` for attributes that have no default.

### Changing `save` breaks existing blocks

**CAUTION:** Do not change the `save` output on a block that is already in use. Existing blocks will fail validation.

The `isRounded` change in the previous section changes the saved markup. That's fine while you're building a new block. On a block that's already out in the world, add a [deprecation](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-deprecation/) first.

### The icon package is not a global

If you import from `@wordpress/icons` without installing it, the build still resolves it from `node_modules` when another dependency happens to pull it in. Then a fresh install on a different machine breaks. Add it to your own `package.json` so the dependency is explicit.

### The button doesn't show

If the button does not show in the toolbar, check these causes:

| Cause | Fix |
|---|---|
| The block is not selected. | Click the block. `BlockControls` shows only for the selected block. |
| The `imageUrl` attribute is empty. | Select an image. The code shows the button only when an image exists. |
| The toolbar is in **Top toolbar** mode. | Look at the top of the editor, not above the block. |
| `BlockControls` is imported from `@wordpress/components`. | Import `BlockControls` from `@wordpress/block-editor`. |
| The build is not running. | Run `npm start`, then reload the editor. |

### Don't hide important actions only in the toolbar

The toolbar is great for quick, contextual actions. It's also invisible until the block is selected. If an action is something users need to discover — not just reach quickly — consider adding it to `InspectorControls` too. The toolbar gets it done fast, and the sidebar makes it easy to find.
