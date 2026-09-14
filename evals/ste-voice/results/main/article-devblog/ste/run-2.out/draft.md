# Add a custom toolbar button to your block with BlockControls

The block toolbar is the first place people look when they want to do something to a block. Core blocks put their most common actions there: alignment, bold, replace an image. When I build custom blocks, I want mine to feel the same way. Burying a common action in the Settings Sidebar makes it harder to find.

The good news is that the pieces are small. `BlockControls` gives you a spot in the toolbar. `ToolbarGroup` gives you a visual group with a divider. `ToolbarButton` is the button itself. Put them together and you have a toolbar action in about ten lines of code.

The example here is a simple image block with a toolbar button that clears the selected image. It's a small feature, but it covers the whole pattern. That includes the parts that trip people up, like disabling the button and picking the right toolbar group.

## Prerequisites

- WordPress 6.5 or later.
- Node.js 20 or later and npm.
- A block plugin that builds with `@wordpress/scripts`. To make one, run `npx @wordpress/create-block@latest image-card`.
- Knowledge of `block.json`, `useBlockProps`, and `setAttributes`.

## Start with a basic image block

I'm going to keep the block itself as plain as possible so the toolbar code stands out. It stores three attributes: the attachment ID, the URL, and the alt text. If there's no image, it shows a `MediaPlaceholder`.

Replace the contents of `src/block.json` with this:

```json
{
	"$schema": "https://schemas.wp.org/trunk/block.json",
	"apiVersion": 3,
	"name": "devblog/image-card",
	"version": "0.1.0",
	"title": "Image Card",
	"category": "media",
	"icon": "format-image",
	"description": "An image card with a toolbar button to clear the image.",
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
	"textdomain": "image-card",
	"editorScript": "file:./index.js"
}
```

Replace the contents of `src/edit.js` with this:

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
					labels={ { title: __( 'Image Card', 'image-card' ) } }
					accept="image/*"
					allowedTypes={ [ 'image' ] }
					onSelect={ onSelectImage }
				/>
			) }
		</div>
	);
}
```

Replace the contents of `src/save.js` with this:

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
				className={ mediaId ? `wp-image-${ mediaId }` : undefined }
			/>
		</div>
	);
}
```

To test the basic block:

1. In the plugin folder, run `npm start`.
2. Activate the **Image Card** plugin in **Plugins > Installed Plugins**.
3. Open a post in the editor.
4. Add the **Image Card** block.
5. Select an image from the Media Library.
6. Make sure that the block shows the image.

Right now, the only way to remove that image is to delete the block and add a new one. That's the gap our toolbar button fills.

## Add the toolbar button

Here's how the three components fit together:

| Component | Package | What it does |
|---|---|---|
| `BlockControls` | `@wordpress/block-editor` | Puts its children in the toolbar of the selected block. |
| `ToolbarGroup` | `@wordpress/components` | Wraps a set of controls. The toolbar shows a divider between groups. |
| `ToolbarButton` | `@wordpress/components` | Shows one button. It takes an `icon`, a `label`, and an `onClick` handler. |

`BlockControls` is a Slot/Fill under the hood. You can render it anywhere in your `Edit` component, and the editor moves its contents into the block toolbar. That's why it sits next to your block markup in a fragment rather than inside it.

**CAUTION:** Do not render `ToolbarButton` outside a `ToolbarGroup`. The button loses toolbar keyboard navigation and styles.

1. In `src/edit.js`, change the `@wordpress/block-editor` import to this:

	```js
	import {
		useBlockProps,
		MediaPlaceholder,
		BlockControls,
	} from '@wordpress/block-editor';
	```

2. In `src/edit.js`, below the `@wordpress/block-editor` import, add:

	```js
	import { ToolbarGroup, ToolbarButton } from '@wordpress/components';
	import { trash } from '@wordpress/icons';
	```

3. In `src/edit.js`, below the `onSelectImage` function, add:

	```js
	const onClearImage = () => {
		setAttributes( {
			mediaId: undefined,
			mediaUrl: undefined,
			mediaAlt: '',
		} );
	};
	```

4. In `src/edit.js`, replace the `return` statement with this:

	```js
	return (
		<>
			<BlockControls>
				<ToolbarGroup>
					<ToolbarButton
						icon={ trash }
						label={ __( 'Clear image', 'image-card' ) }
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
						labels={ { title: __( 'Image Card', 'image-card' ) } }
						accept="image/*"
						allowedTypes={ [ 'image' ] }
						onSelect={ onSelectImage }
					/>
				) }
			</div>
		</>
	);
	```

5. Save `src/edit.js`.
6. Reload the editor.
7. Select the **Image Card** block that has an image.
8. In the block toolbar, click the **Clear image** button.
9. Make sure that the block shows the `MediaPlaceholder` again.

If the build can't find `@wordpress/icons`, add it to the project with `npm install @wordpress/icons`.

A quick note on the clear handler. I set `mediaId` and `mediaUrl` to `undefined` instead of an empty string. An `undefined` attribute drops out of the block comment delimiter entirely, so the saved markup stays clean. I also do it in a single `setAttributes` call, which gives the user one undo step instead of three.

## Disable the button when there's nothing to clear

The button works, but it shows even when the block is empty. Clicking it then does nothing, and that feels broken. I have two options: hide the button, or disable it. I think disabling is the better choice here. The toolbar keeps the same shape, and the user still learns the action exists.

1. In `src/edit.js`, in the `ToolbarButton` props, below `onClick={ onClearImage }`, add:

	```js
	disabled={ ! mediaUrl }
	```

2. Reload the editor.
3. Add a new **Image Card** block.
4. Make sure that the **Clear image** button is disabled.

If you prefer to hide the button, wrap the whole `BlockControls` element in `{ mediaUrl && ( … ) }` instead. Both approaches are fine. Pick one and use it across all your blocks.

## Put the button in the right toolbar group

By default, `BlockControls` adds your controls to the `default` group, which sits after the block-level tools. The component also takes a `group` prop that places the controls in a specific area of the toolbar:

| `group` value | Where the controls show |
|---|---|
| `default` | The main area, after the block-level tools. |
| `block` | With the block-level tools, for example alignment. |
| `inline` | With the inline formatting tools, for example bold and link. |
| `other` | At the end of the toolbar, after the other groups. |
| `parent` | With the parent block tools. |

Clearing the image acts on the whole block, so I like it in `other`. That's also where core puts **Replace** on the Image block, so the button lands where people already look.

1. In `src/edit.js`, change the opening `BlockControls` tag to this:

	```js
	<BlockControls group="other">
	```

2. Reload the editor.
3. Select an **Image Card** block that has an image.
4. Make sure that the **Clear image** button shows at the end of the block toolbar.

Here's the finished `src/edit.js`:

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
			<BlockControls group="other">
				<ToolbarGroup>
					<ToolbarButton
						icon={ trash }
						label={ __( 'Clear image', 'image-card' ) }
						onClick={ onClearImage }
						disabled={ ! mediaUrl }
					/>
				</ToolbarGroup>
			</BlockControls>
			<div { ...blockProps }>
				{ mediaUrl ? (
					<img src={ mediaUrl } alt={ mediaAlt } />
				) : (
					<MediaPlaceholder
						icon="format-image"
						labels={ { title: __( 'Image Card', 'image-card' ) } }
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

These are the ones I see most often in code reviews.

- **`label` is not optional.** An icon-only button has no visible text. The `label` becomes the tooltip and the accessible name for screen readers. Leave it out and the button is a mystery icon for everyone.
- **`BlockControls` only shows when the block is selected.** That's by design. Don't put anything in the toolbar that the user needs to see at all times.
- **`undefined` versus an empty string.** An empty string is still a value, so it gets saved in the block comment. If your `save` or `render.php` checks for a truthy value, both work, but `undefined` keeps the markup cleaner.
- **Attributes sourced from markup.** This block stores its attributes in the comment delimiter. If yours read from the `<img>` tag with `"source": "attribute"`, the saved markup is the source of truth. Make sure `save` drops the `<img>` when the URL is empty, or the image comes back on the next load.
- **One `setAttributes` call per action.** Several calls in a row can show up as several undo steps. Group the changes into one object.
- **Core already has a replace flow.** If you want "replace" rather than "clear", look at `MediaReplaceFlow` from `@wordpress/block-editor` before you build your own.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| The button does not show in the toolbar. | The block is not selected, or `BlockControls` is not in the `Edit` return. | Select the block. Make sure that `Edit` returns `BlockControls`. |
| The build fails with "Module not found: @wordpress/icons". | The package is not installed. | Run `npm install @wordpress/icons`. |
| The button shows no tooltip. | The `label` prop is missing. | Add a `label` prop to `ToolbarButton`. |
| The button does not respond to arrow keys. | `ToolbarButton` is not inside a `ToolbarGroup`. | Wrap `ToolbarButton` in `ToolbarGroup`. |
| The image shows again after a reload. | The editor did not save the post. | Click **Save** in the editor header. Reload the editor. |
