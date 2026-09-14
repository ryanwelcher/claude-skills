# Add a custom toolbar button to your block with BlockControls

The block toolbar is the first place users look when they want to do something to a block. Core blocks use it all the time: the Image block puts **Replace** there, and the Paragraph block puts alignment and formatting there. Custom blocks can do the same thing, but most of the custom blocks I review put every action in the Inspector sidebar instead. That works, but the sidebar is one extra click away and easy to miss.

The good news is that the toolbar API is small. You need three components: `BlockControls`, `ToolbarGroup`, and `ToolbarButton`. The example in this post is a simple image block that has a toolbar button to remove the selected image. It's a small feature, but it covers every part of the pattern you'll reuse for bigger ones.

## What you need

- A block plugin built with [`@wordpress/create-block`](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-create-block/) or a similar `@wordpress/scripts` setup.
- WordPress 6.5 or later.
- The `@wordpress/block-editor`, `@wordpress/components`, and `@wordpress/icons` packages.
- A local WordPress site that runs the plugin, for example with `wp-env` or WordPress Playground.

## The starting block

Here's the block before it has a toolbar. It stores three attributes for the image and uses `MediaPlaceholder` to let the user select one from the Media Library.

`block.json`:

```json
{
	"$schema": "https://schemas.wp.org/trunk/block.json",
	"apiVersion": 3,
	"name": "devblog/featured-image",
	"version": "0.1.0",
	"title": "Featured Image Card",
	"category": "media",
	"icon": "format-image",
	"description": "A card that shows a single image.",
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
	"supports": {
		"html": false
	},
	"textdomain": "devblog",
	"editorScript": "file:./index.js"
}
```

`src/edit.js`:

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
					labels={ { title: __( 'Card image', 'devblog' ) } }
					onSelect={ onSelectImage }
					accept="image/*"
					allowedTypes={ [ 'image' ] }
				/>
			) }
		</div>
	);
}
```

`src/save.js`:

```js
import { useBlockProps } from '@wordpress/block-editor';

export default function save( { attributes } ) {
	const { mediaId, mediaUrl, mediaAlt } = attributes;

	if ( ! mediaUrl ) {
		return null;
	}

	return (
		<div { ...useBlockProps.save() }>
			<img
				src={ mediaUrl }
				alt={ mediaAlt }
				className={ `wp-image-${ mediaId }` }
			/>
		</div>
	);
}
```

Right now, the only way to remove the image is to delete the block and insert it again. Let's fix that.

## How the three components fit together

Each component has one job:

| Component | Package | Job |
|---|---|---|
| `BlockControls` | `@wordpress/block-editor` | A slot. Anything inside it shows in the toolbar of the selected block. |
| `ToolbarGroup` | `@wordpress/components` | Wraps related controls and adds the divider between groups. |
| `ToolbarButton` | `@wordpress/components` | A button that joins the toolbar's keyboard navigation. |

`BlockControls` is a [SlotFill](https://developer.wordpress.org/block-editor/reference-guides/slotfills/), so it doesn't matter where you put it in your JSX. The editor moves its contents into the toolbar for you. I usually put it at the top of the returned fragment so it's easy to find.

## Add the button

1. Open `src/edit.js`.
2. Replace the `@wordpress/block-editor` import with this import:

	```js
	import {
		useBlockProps,
		MediaPlaceholder,
		BlockControls,
	} from '@wordpress/block-editor';
	```

3. Below the `@wordpress/block-editor` import, add these imports:

	```js
	import { ToolbarGroup, ToolbarButton } from '@wordpress/components';
	import { trash } from '@wordpress/icons';
	```

4. Below the `onSelectImage` function, add this function:

	```js
	const onRemoveImage = () => {
		setAttributes( {
			mediaId: undefined,
			mediaUrl: undefined,
			mediaAlt: '',
		} );
	};
	```

5. Replace the `return` statement with this code:

	```js
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
						labels={ { title: __( 'Card image', 'devblog' ) } }
						onSelect={ onSelectImage }
						accept="image/*"
						allowedTypes={ [ 'image' ] }
					/>
				) }
			</div>
		</>
	);
	```

6. Run `npm run start`.
7. In the editor, add the **Featured Image Card** block to a post.
8. Select an image from the Media Library.
9. In the block toolbar, click **Remove image**.
10. Make sure that the image is removed and the placeholder shows again.

I set `mediaId` and `mediaUrl` to `undefined` instead of an empty string on purpose. An `undefined` attribute is removed from the block comment delimiter, so the saved markup looks exactly like a block that never had an image. An empty string gets serialized as `"mediaUrl":""`, which is noise at best and a truthy-check bug at worst.

## Only show the button when it does something

There's a problem with the code above. The **Remove image** button shows in the toolbar even when the block has no image. Clicking it does nothing, and a button that does nothing is worse than no button.

The fix is a conditional around the group. I also like to pass `group="other"` to `BlockControls`. When you use the `group` prop, `BlockControls` makes the `ToolbarGroup` for you, and the editor places your controls in the same position core blocks use for their media actions.

1. In `src/edit.js`, find the `<BlockControls>` element.
2. Replace the complete `<BlockControls>` element with this code:

	```js
	{ mediaUrl && (
		<BlockControls group="other">
			<ToolbarButton
				icon={ trash }
				label={ __( 'Remove image', 'devblog' ) }
				onClick={ onRemoveImage }
			/>
		</BlockControls>
	) }
	```

3. Remove `ToolbarGroup` from the `@wordpress/components` import.
4. Save the file.
5. In the editor, select a **Featured Image Card** block that has no image.
6. Make sure that the block toolbar does not show the **Remove image** button.

The `group` prop accepts `block`, `inline`, `other`, and `parent`. Here's how I think about them:

| `group` value | Use it for |
|---|---|
| `block` | Controls that change the whole block, such as alignment. |
| `inline` | Formatting controls for text inside the block. |
| `other` | Actions that don't fit the other groups. Media actions go here in core. |
| `parent` | Controls that act on the parent block. Rarely needed. |

If you leave `group` off, you're back to wrapping your buttons in `ToolbarGroup` yourself, like the first example. Both approaches work. The `group` prop just gets you consistent placement for free.

## Add a text label next to the icon

An icon-only button relies on the tooltip to explain itself. For a destructive action like this one, I think a visible label is worth the extra toolbar space. `ToolbarButton` accepts children, so you can put text right in it.

1. In `src/edit.js`, find the `<ToolbarButton>` element.
2. Replace the `<ToolbarButton>` element with this code:

	```js
	<ToolbarButton
		icon={ trash }
		label={ __( 'Remove image', 'devblog' ) }
		onClick={ onRemoveImage }
		showTooltip
	>
		{ __( 'Remove', 'devblog' ) }
	</ToolbarButton>
	```

3. Save the file.
4. In the editor, select a **Featured Image Card** block that has an image.
5. Make sure that the toolbar shows the trash icon and the word "Remove".

Here's the final `src/edit.js`, with all of the changes in place:

```js
import { __ } from '@wordpress/i18n';
import {
	useBlockProps,
	MediaPlaceholder,
	BlockControls,
} from '@wordpress/block-editor';
import { ToolbarButton } from '@wordpress/components';
import { trash } from '@wordpress/icons';

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

	const onRemoveImage = () => {
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
					<ToolbarButton
						icon={ trash }
						label={ __( 'Remove image', 'devblog' ) }
						onClick={ onRemoveImage }
						showTooltip
					>
						{ __( 'Remove', 'devblog' ) }
					</ToolbarButton>
				</BlockControls>
			) }
			<div { ...blockProps }>
				{ mediaUrl ? (
					<img src={ mediaUrl } alt={ mediaAlt } />
				) : (
					<MediaPlaceholder
						icon="format-image"
						labels={ { title: __( 'Card image', 'devblog' ) } }
						onSelect={ onSelectImage }
						accept="image/*"
						allowedTypes={ [ 'image' ] }
					/>
				) }
			</div>
		</>
	);
}
```

## Gotchas

These are the traps I see most often when people add toolbar controls.

### Use `ToolbarButton`, not `Button`

A plain `Button` from `@wordpress/components` renders inside the toolbar and looks right. It doesn't join the toolbar's roving tabindex, though, so keyboard users can't reach it with the arrow keys the way they reach every other toolbar control.

**CAUTION:** Do not put a plain `Button` inside `BlockControls`. Keyboard users cannot reach it with the arrow keys.

1. In `src/edit.js`, find each `Button` inside `BlockControls`.
2. Replace each `Button` with `ToolbarButton`.
3. Make sure that the arrow keys move focus to the new button in the block toolbar.

### Always pass a `label`

The `label` prop is the accessible name for the button, and it's the tooltip text. Without it, an icon-only button is announced to screen readers as "button" and nothing else. Treat `label` as required, even when the button also has visible text.

### `BlockControls` only shows for the selected block

The toolbar belongs to the selected block, so your controls only show when the user selects your block. That's usually what you want. If you need an action that's always visible, the toolbar is the wrong place for it. Put it in the block's canvas instead.

### Removing the image does not delete the file

`onRemoveImage` clears the block attributes. The image stays in the Media Library, and that's the right behavior for a block. If you ever want a button that deletes the attachment itself, that's a different action with different permissions, and it needs a confirmation step.

### Undo already works

Every `setAttributes` call is a normal change in the editor's history. If a user removes the image by accident, **Undo** (Ctrl+Z or Cmd+Z) brings it back. You don't need to add your own confirmation for attribute changes like this one.

### Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| The button does not show in the toolbar. | The block has no image, so `mediaUrl` is empty. | Select an image, then select the block again. |
| The button does not show in the toolbar, and the block has an image. | `BlockControls` is imported from `@wordpress/components`. | Import `BlockControls` from `@wordpress/block-editor`. |
| The toolbar shows an empty square instead of an icon. | The `trash` icon is not imported. | Add `import { trash } from '@wordpress/icons';` to `src/edit.js`. |
| The editor shows "This block contains unexpected or invalid content." | The `save` function changed after you saved the post. | Click **Attempt Block Recovery**, or add a [block deprecation](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-deprecation/). |

The same pattern works for any action you want one click away: toggles with `isPressed`, dropdowns with `ToolbarDropdownMenu`, or a **Replace** flow with `MediaReplaceFlow`. Start with `BlockControls`, pick a `group`, and drop your controls in.
