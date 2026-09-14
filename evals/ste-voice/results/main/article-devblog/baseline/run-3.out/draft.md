# How to add a custom toolbar button to your block

The block toolbar is the first place users look when they want to do something with a selected block. Core blocks use it constantly: alignment, links, replacing media, and more. If your custom block has an action that users will reach for often, it belongs in the toolbar and not buried in the settings sidebar.

The good news is that adding your own button takes three components: `BlockControls`, `ToolbarGroup`, and `ToolbarButton`. I'm going to walk through a practical example: a block that stores an image, with a toolbar button that clears it.

## The starting block

Let's start with a simple block that lets users pick an image. Here is the `block.json`:

```json
{
	"$schema": "https://schemas.wp.org/trunk/block.json",
	"apiVersion": 3,
	"name": "devblog/image-card",
	"title": "Image Card",
	"category": "media",
	"icon": "format-image",
	"attributes": {
		"mediaId": {
			"type": "number"
		},
		"mediaUrl": {
			"type": "string"
		},
		"mediaAlt": {
			"type": "string",
			"default": ""
		}
	},
	"textdomain": "devblog",
	"editorScript": "file:./index.js"
}
```

And the `edit.js` file. If no image is set, the block shows a `MediaPlaceholder`. Once the user picks one, it renders the image.

```js
import { __ } from '@wordpress/i18n';
import { useBlockProps, MediaPlaceholder } from '@wordpress/block-editor';

export default function Edit( { attributes, setAttributes } ) {
	const { mediaId, mediaUrl, mediaAlt } = attributes;
	const blockProps = useBlockProps();

	const onSelectImage = ( media ) => {
		setAttributes( {
			mediaId: media.id,
			mediaUrl: media.url,
			mediaAlt: media.alt,
		} );
	};

	return (
		<div { ...blockProps }>
			{ mediaUrl ? (
				<img src={ mediaUrl } alt={ mediaAlt } />
			) : (
				<MediaPlaceholder
					icon="format-image"
					labels={ { title: __( 'Image Card', 'devblog' ) } }
					accept="image/*"
					allowedTypes={ [ 'image' ] }
					onSelect={ onSelectImage }
				/>
			) }
		</div>
	);
}
```

This works, but once an image is set there is no way to remove it without deleting the whole block. That is exactly the gap a toolbar button fills.

## Adding the toolbar button

Here's the minimal version. `BlockControls` is a slot that renders its children into the block toolbar. `ToolbarGroup` groups related controls together with a visual divider. `ToolbarButton` is the button itself.

```js
import { __ } from '@wordpress/i18n';
import {
	useBlockProps,
	BlockControls,
	MediaPlaceholder,
} from '@wordpress/block-editor';
import { ToolbarGroup, ToolbarButton } from '@wordpress/components';
import { trash } from '@wordpress/icons';

export default function Edit( { attributes, setAttributes } ) {
	const { mediaId, mediaUrl, mediaAlt } = attributes;
	const blockProps = useBlockProps();

	const onSelectImage = ( media ) => {
		setAttributes( {
			mediaId: media.id,
			mediaUrl: media.url,
			mediaAlt: media.alt,
		} );
	};

	const onClearImage = () => {
		setAttributes( {
			mediaId: undefined,
			mediaUrl: undefined,
			mediaAlt: '',
		} );
	};

	return (
		<>
			<BlockControls>
				<ToolbarGroup>
					<ToolbarButton
						icon={ trash }
						label={ __( 'Clear image', 'devblog' ) }
						onClick={ onClearImage }
					/>
				</ToolbarGroup>
			</BlockControls>
			<div { ...blockProps }>
				{ mediaUrl ? (
					<img src={ mediaUrl } alt={ mediaAlt } />
				) : (
					<MediaPlaceholder
						icon="format-image"
						labels={ { title: __( 'Image Card', 'devblog' ) } }
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

A few things to call out:

- **`BlockControls` sits outside the block wrapper.** It doesn't render in place. It sends its children to the toolbar slot, so I wrap everything in a fragment.
- **`label` is not optional in practice.** Icon-only buttons use it as the tooltip and the accessible name. Without it, screen reader users get a button with no name.
- **`icon` accepts an icon from `@wordpress/icons`.** Using the same icon set as core keeps your toolbar consistent with the rest of the editor. Make sure `@wordpress/icons` is in your `package.json` dependencies.

## Only show the button when it's useful

Right now the button shows up even when there is no image to clear. Clicking it does nothing, which is confusing. I have two options here.

### Option 1: Render the button conditionally

If the action doesn't make sense in the current state, don't show it at all.

```js
{ mediaUrl && (
	<BlockControls>
		<ToolbarGroup>
			<ToolbarButton
				icon={ trash }
				label={ __( 'Clear image', 'devblog' ) }
				onClick={ onClearImage }
			/>
		</ToolbarGroup>
	</BlockControls>
) }
```

### Option 2: Disable the button

If you want the toolbar layout to stay stable, keep the button and disable it instead.

```js
<BlockControls>
	<ToolbarGroup>
		<ToolbarButton
			icon={ trash }
			label={ __( 'Clear image', 'devblog' ) }
			onClick={ onClearImage }
			disabled={ ! mediaUrl }
		/>
	</ToolbarGroup>
</BlockControls>
```

I think option 1 is the better fit here. The placeholder already tells the user what to do when there's no image, so an inactive button adds noise.

## Using a text label instead of an icon

Sometimes an icon isn't clear enough. "Clear" is a good example, because a trash can often reads as "delete this block." `ToolbarButton` accepts children, so you can render text instead:

```js
<BlockControls group="other">
	<ToolbarButton onClick={ onClearImage }>
		{ __( 'Clear', 'devblog' ) }
	</ToolbarButton>
</BlockControls>
```

Notice the `group` prop on `BlockControls`. The block toolbar has a few named groups (`block`, `inline`, `other`, and `parent`) and `group` controls where your controls land. Core blocks put actions like **Replace** in `other`, which places them to the right of the block-level controls. When you pass `group`, the slot handles the grouping for you, so you can drop the `ToolbarGroup` here.

## The complete `edit.js`

Here's the final version, with the conditional button and a text label:

```js
import { __ } from '@wordpress/i18n';
import {
	useBlockProps,
	BlockControls,
	MediaPlaceholder,
} from '@wordpress/block-editor';
import { ToolbarButton } from '@wordpress/components';

export default function Edit( { attributes, setAttributes } ) {
	const { mediaUrl, mediaAlt } = attributes;
	const blockProps = useBlockProps();

	const onSelectImage = ( media ) => {
		setAttributes( {
			mediaId: media.id,
			mediaUrl: media.url,
			mediaAlt: media.alt,
		} );
	};

	const onClearImage = () => {
		setAttributes( {
			mediaId: undefined,
			mediaUrl: undefined,
			mediaAlt: '',
		} );
	};

	return (
		<>
			{ mediaUrl && (
				<BlockControls group="other">
					<ToolbarButton onClick={ onClearImage }>
						{ __( 'Clear', 'devblog' ) }
					</ToolbarButton>
				</BlockControls>
			) }
			<div { ...blockProps }>
				{ mediaUrl ? (
					<img src={ mediaUrl } alt={ mediaAlt } />
				) : (
					<MediaPlaceholder
						icon="format-image"
						labels={ { title: __( 'Image Card', 'devblog' ) } }
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

## Gotchas

### Clear every related attribute

It's tempting to only reset `mediaUrl`, since that's what controls the render. Don't. A stale `mediaId` will stick around in the block markup, and any code that reads it later (a `render.php`, a block variation, a migration) will think an image still exists. Reset everything that describes the image together.

### `undefined` versus an empty string

Setting an attribute to `undefined` removes it from the saved block comment delimiter, and the attribute falls back to its `default` on the next load. Setting it to `''` saves an empty string. For `mediaId` and `mediaUrl`, which have no default, `undefined` is the cleanest option. For `mediaAlt`, which defaults to `''`, either works.

### Don't import `ToolbarButton` from the wrong package

`BlockControls` comes from `@wordpress/block-editor`. `ToolbarGroup` and `ToolbarButton` come from `@wordpress/components`. Mixing these up gives you an `undefined` component error that isn't obvious at first glance.

### The toolbar only exists when the block is selected

`BlockControls` renders nothing into the page when the block isn't selected. Don't put logic inside it that the block depends on, like fetching data or syncing attributes. Keep that in the main body of `Edit`.

### Clearing is undoable, so skip the confirm dialog

Every `setAttributes` call creates an undo level. If a user clears the image by mistake, <kbd>Cmd</kbd>/<kbd>Ctrl</kbd> + <kbd>Z</kbd> brings it right back. There's no need to wrap `onClearImage` in a `window.confirm()`, and core blocks don't do it either.
