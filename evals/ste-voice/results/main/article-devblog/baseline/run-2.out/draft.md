# Adding a custom toolbar button to your block

Every block gets a toolbar. Core blocks use it for alignment, formatting, replacing media, and more. When your custom block needs a quick action, the toolbar is usually the right home for it. It sits right next to the content, it follows the block around, and users already know to look there.

The block editor gives you three pieces to make this happen:

- **`BlockControls`** from `@wordpress/block-editor` — a slot that renders its children in the selected block's toolbar
- **`ToolbarGroup`** from `@wordpress/components` — groups related controls and adds the divider between groups
- **`ToolbarButton`** from `@wordpress/components` — the button itself, with keyboard navigation handled for you

I'm going to build a small example: a block that displays an image, with a toolbar button that clears it. It's a simple action, but it covers everything you need for your own controls.

## The starting block

Here is the `block.json` for the example. The block stores the image ID, URL, and alt text as attributes.

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

And here is the `edit` component before we add anything to the toolbar. It uses `MediaPlaceholder` when there is no image and renders the image when there is one.

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

The `save` function outputs the image when one is set:

```js
import { useBlockProps } from '@wordpress/block-editor';

export default function save( { attributes } ) {
	const { mediaUrl, mediaAlt } = attributes;

	return (
		<div { ...useBlockProps.save() }>
			{ mediaUrl && <img src={ mediaUrl } alt={ mediaAlt } /> }
		</div>
	);
}
```

Right now, once a user picks an image, there is no way to get back to the placeholder. Let's fix that.

## Adding the button

Import `BlockControls` alongside the other block editor components, and pull `ToolbarGroup` and `ToolbarButton` from `@wordpress/components`. I'm also grabbing the `trash` icon from `@wordpress/icons`.

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

	const onRemoveImage = () => {
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
						label={ __( 'Remove image', 'devblog' ) }
						onClick={ onRemoveImage }
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

That's the whole pattern. A few things worth pointing out:

- **The fragment:** `BlockControls` renders into the toolbar through a slot, not into your markup. It can live anywhere in the returned tree, but I keep it outside the element with `blockProps` so the block wrapper stays clean.
- **`label`:** This is the accessible name for the button, and it also becomes the tooltip. An icon-only button without a `label` is unusable for screen reader users.
- **`onClick`:** It's just a function. Anything you can do in `edit`, you can do here.

Select the block, pick an image, and you'll see the new trash button in the toolbar. Click it and the block goes back to the placeholder.

## Only showing the button when it's useful

Clearing an image that doesn't exist makes no sense. You have two options here, and I think the right one depends on the control.

### Hide the button

If the action only exists in one state of the block, render it conditionally:

```js
{ mediaUrl && (
	<BlockControls>
		<ToolbarGroup>
			<ToolbarButton
				icon={ trash }
				label={ __( 'Remove image', 'devblog' ) }
				onClick={ onRemoveImage }
			/>
		</ToolbarGroup>
	</BlockControls>
) }
```

This is what I'd use for this example. The placeholder already tells the user what to do, so an empty toolbar group adds nothing.

### Disable the button

If the button should stay put so the toolbar doesn't shift around, use the `disabled` prop instead:

```js
<BlockControls>
	<ToolbarGroup>
		<ToolbarButton
			icon={ trash }
			label={ __( 'Remove image', 'devblog' ) }
			onClick={ onRemoveImage }
			disabled={ ! mediaUrl }
		/>
	</ToolbarGroup>
</BlockControls>
```

This works well when the button sits next to other controls that are always visible.

## Placing the button with the `group` prop

By default, `BlockControls` adds your controls to the `default` group. You can move them with the `group` prop. The options are `block`, `inline`, `other`, `parent`, and `default`.

For a media action, `other` is a good fit. It's the same group core blocks use for their **Replace** media control, so your button lands where users expect it.

```js
<BlockControls group="other">
	<ToolbarGroup>
		<ToolbarButton
			icon={ trash }
			label={ __( 'Remove image', 'devblog' ) }
			onClick={ onRemoveImage }
		/>
	</ToolbarGroup>
</BlockControls>
```

## Using text instead of an icon

Not every action has an obvious icon. `ToolbarButton` accepts children, so you can render a text label instead:

```js
<BlockControls group="other">
	<ToolbarGroup>
		<ToolbarButton onClick={ onRemoveImage }>
			{ __( 'Remove', 'devblog' ) }
		</ToolbarButton>
	</ToolbarGroup>
</BlockControls>
```

When the text is visible, you don't need the `label` prop. Core does exactly this for its **Replace** button.

## Gotchas

### Don't reach for `Button`

`Button` from `@wordpress/components` will render in the toolbar, and it will look close enough. It won't behave correctly. The block toolbar uses roving tabindex, so keyboard users move between controls with the arrow keys. `ToolbarButton` registers itself with the toolbar to make that work. A plain `Button` breaks the keyboard flow.

### Clear attributes with `undefined`

Setting `mediaUrl` to `undefined` removes it from the block's comment delimiter entirely. Setting it to an empty string or `null` keeps a key hanging around in the serialized markup. For attributes that have a `default` in `block.json`, like `mediaAlt`, set them back to that default value so the block matches a freshly inserted one.

### Clear every related attribute

It's easy to reset `mediaUrl` and forget `mediaId` and `mediaAlt`. The block looks correct in the editor, but it still carries the old ID. If anything else relies on that ID (a server-side render, a `useSelect` call for the media object, and more...), you'll end up with confusing bugs later. Reset every attribute that belongs to the thing you're clearing in the same `setAttributes` call.

### You don't need to check `isSelected`

The toolbar only renders for the selected block, so `BlockControls` content only shows up when the block is selected. Wrapping it in `isSelected &&` does nothing useful.

### Watch out for block locking and content-only mode

When a block is inside a pattern or template that uses `templateLock: 'contentOnly'`, the editor hides the `default` group. If your button disappears in that context, check the `group` you're using. The `other` group stays visible, which is another reason to use it for content actions like replacing or removing media.
