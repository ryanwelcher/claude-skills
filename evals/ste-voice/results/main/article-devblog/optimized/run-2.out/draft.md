# How to add a custom toolbar button to your block

The block toolbar is the first place people look when they want to do something to a selected block. Core blocks use it all the time: alignment, links, replacing media, and more. When your own block has an action that belongs there, the `BlockControls` slot is how you get it into the toolbar, next to the core controls.

I see a lot of custom blocks that put this kind of action in the sidebar, or as a button inside the block's own markup. Both work. But a user who wants to remove an image from a block looks at the toolbar first, not the Settings sidebar. Putting the action where people expect it is a small change that makes a block feel like it belongs in the editor.

This tutorial uses three pieces:

- **`BlockControls`** from `@wordpress/block-editor`: a Slot/Fill that places its children in the toolbar of the selected block.
- **`ToolbarGroup`** from `@wordpress/components`: wraps related controls and adds the divider between groups.
- **`ToolbarButton`** from `@wordpress/components`: the button itself, with the correct keyboard behavior for a toolbar.

The example is a block that stores an image in its attributes. We'll add a "Remove image" button that clears those attributes and returns the block to its placeholder.

## Prerequisites

- WordPress 6.6 or later.
- Node.js 20 or later and npm.
- A local WordPress site where you can activate plugins.
- Familiarity with `block.json`, `useBlockProps`, and `setAttributes`.

## The starting block

If you want to follow along from scratch, scaffold a plugin with `@wordpress/create-block`:

```bash
npx @wordpress/create-block@latest toolbar-demo
cd toolbar-demo
```

The block needs three attributes for the image. Here is the complete `src/block.json`:

```json
{
	"$schema": "https://schemas.wp.org/trunk/block.json",
	"apiVersion": 3,
	"name": "create-block/toolbar-demo",
	"version": "0.1.0",
	"title": "Toolbar Demo",
	"category": "media",
	"icon": "format-image",
	"description": "An image block with a custom toolbar button.",
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
	"textdomain": "toolbar-demo",
	"editorScript": "file:./index.js",
	"editorStyle": "file:./index.css",
	"style": "file:./style-index.css"
}
```

The edit component shows a `MediaPlaceholder` when there is no image, and the image when there is one. Here is the complete `src/edit.js` before any toolbar work:

```js
import { __ } from '@wordpress/i18n';
import { useBlockProps, MediaPlaceholder } from '@wordpress/block-editor';
import './editor.scss';

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
				<img
					src={ mediaUrl }
					alt={ mediaAlt }
					className={ mediaId ? `wp-image-${ mediaId }` : undefined }
				/>
			) : (
				<MediaPlaceholder
					icon="format-image"
					labels={ { title: __( 'Toolbar Demo', 'toolbar-demo' ) } }
					accept="image/*"
					allowedTypes={ [ 'image' ] }
					onSelect={ onSelectImage }
				/>
			) }
		</div>
	);
}
```

And the matching `src/save.js`:

```js
import { useBlockProps } from '@wordpress/block-editor';

export default function save( { attributes } ) {
	const { mediaId, mediaUrl, mediaAlt } = attributes;

	return (
		<div { ...useBlockProps.save() }>
			{ mediaUrl && (
				<img
					src={ mediaUrl }
					alt={ mediaAlt }
					className={ mediaId ? `wp-image-${ mediaId }` : undefined }
				/>
			) }
		</div>
	);
}
```

Right now, the only way to get rid of an image is to delete the whole block and insert a new one. That's the gap the toolbar button fills.

## Add the toolbar button

The button uses an icon from `@wordpress/icons`. Unlike most `@wordpress/*` packages, `@wordpress/icons` is not a script that WordPress loads for you. It gets bundled into your build, so it has to be in `package.json`.

1. In the plugin folder, run `npm install @wordpress/icons --save`.
2. Open `src/edit.js`.
3. In `src/edit.js`, replace the `@wordpress/block-editor` import line with these lines:

```js
import {
	useBlockProps,
	MediaPlaceholder,
	BlockControls,
} from '@wordpress/block-editor';
import { ToolbarGroup, ToolbarButton } from '@wordpress/components';
import { trash } from '@wordpress/icons';
```

4. In `src/edit.js`, below the `onSelectImage` function, add this function:

```js
	const onRemoveImage = () => {
		setAttributes( {
			mediaId: undefined,
			mediaUrl: undefined,
			mediaAlt: '',
		} );
	};
```

5. In `src/edit.js`, replace the `return (` line with this code:

```js
	return (
		<>
			{ mediaUrl && (
				<BlockControls group="other">
					<ToolbarGroup>
						<ToolbarButton
							icon={ trash }
							label={ __( 'Remove image', 'toolbar-demo' ) }
							onClick={ onRemoveImage }
						/>
					</ToolbarGroup>
				</BlockControls>
			) }
```

6. In `src/edit.js`, below the closing `</div>` of the block wrapper, add `</>`.
7. Run `npm start`.
8. In the block editor, add the **Toolbar Demo** block to a post.
9. In the placeholder, select **Upload** or **Media Library** and add an image.
10. Select the block.
11. In the block toolbar, click the **Remove image** button.

Make sure that the image is removed and the block shows the placeholder again. Make sure that the **Remove image** button does not show in the toolbar when the block has no image.

Here is the complete `src/edit.js` with the button in place:

```js
import { __ } from '@wordpress/i18n';
import {
	useBlockProps,
	MediaPlaceholder,
	BlockControls,
} from '@wordpress/block-editor';
import { ToolbarGroup, ToolbarButton } from '@wordpress/components';
import { trash } from '@wordpress/icons';
import './editor.scss';

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
			{ mediaUrl && (
				<BlockControls group="other">
					<ToolbarGroup>
						<ToolbarButton
							icon={ trash }
							label={ __( 'Remove image', 'toolbar-demo' ) }
							onClick={ onRemoveImage }
						/>
					</ToolbarGroup>
				</BlockControls>
			) }
			<div { ...blockProps }>
				{ mediaUrl ? (
					<img
						src={ mediaUrl }
						alt={ mediaAlt }
						className={ mediaId ? `wp-image-${ mediaId }` : undefined }
					/>
				) : (
					<MediaPlaceholder
						icon="format-image"
						labels={ { title: __( 'Toolbar Demo', 'toolbar-demo' ) } }
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

A few things are worth calling out in that code.

`BlockControls` lives *outside* the `<div { ...blockProps }>`. It doesn't render anything in place. It's a Fill, so its children get moved into the toolbar Slot for the selected block. Putting it inside the wrapper works too, but I like keeping it as a sibling so it's obvious it isn't part of the block's markup.

The button is wrapped in `{ mediaUrl && ( ... ) }`, so it only appears when there is something to remove. An always-visible button that does nothing is confusing, and hiding it keeps the toolbar clean when the placeholder is showing.

## Pick the right toolbar group

The `group` prop on `BlockControls` decides where your controls land in the toolbar. If you leave it off, you get `default`.

| `group` value | Where the controls show |
|---|---|
| `block` | Near the start of the toolbar, with block-level controls such as alignment |
| `inline` | With inline formatting controls, such as bold and link |
| `default` | The main group, after the block-level controls |
| `other` | After the default group, where core puts actions like **Replace** |
| `parent` | With the controls that select a parent block |

I used `other` because that's where the Image block keeps **Replace**. Removing an image is the same kind of action, so it should sit in the same spot. If your button changes how the block looks, like alignment or layout, `block` is usually a better fit.

## Disable instead of hide

Hiding the button is my default, but some controls should stay put so the toolbar doesn't shift around. `ToolbarButton` accepts a `disabled` prop for that. Here is the `BlockControls` section written that way:

```js
			<BlockControls group="other">
				<ToolbarGroup>
					<ToolbarButton
						icon={ trash }
						label={ __( 'Remove image', 'toolbar-demo' ) }
						onClick={ onRemoveImage }
						disabled={ ! mediaUrl }
					/>
				</ToolbarGroup>
			</BlockControls>
```

If you go this route, drop the `mediaUrl &&` check around `BlockControls`. The button stays in the same spot whether or not the block has an image.

## Gotchas

### `ToolbarButton` needs a `ToolbarGroup`

It's tempting to drop a `ToolbarButton` straight into `BlockControls`. Don't. `ToolbarGroup` gives you the divider between your controls and the next group. The toolbar also relies on the toolbar components to manage focus, so arrow keys move between buttons the way they should. A plain `Button` from `@wordpress/components` skips all of that and breaks keyboard navigation in the toolbar.

### Always pass a `label`

An icon-only button has no visible text. The `label` prop becomes the `aria-label` and the tooltip. Without it, screen reader users get an unlabeled button, and everyone else has to guess what the trash can removes.

### Clear to `undefined`, not an empty string

Look at `onRemoveImage` again. `mediaId` and `mediaUrl` get `undefined`, not `''` or `0`. When an attribute is `undefined`, the block editor leaves it out of the block comment delimiter completely. An empty string gets saved as `"mediaUrl":""`, which is still falsy in JavaScript, but now there is a leftover value in the post content that PHP code or a future block version has to handle. `mediaAlt` has a `default` of `''` in `block.json`, so setting it to `''` returns it to that default and it isn't saved either.

### Removing the image is undoable

`setAttributes` goes through the editor's undo stack, so **Undo** brings the image back. That's why this button doesn't need a confirmation dialog. If your toolbar action does something the editor can't undo, like deleting a file on the server, that's a different conversation.

### The toolbar only exists for the selected block

`BlockControls` content only shows when the block is selected. If a user can't find your button, have them select the block first.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| The build fails with `Module not found: Can't resolve '@wordpress/icons'`. | The package is not in `package.json`. | Run `npm install @wordpress/icons --save`. Then run `npm start` again. |
| The button does not show in the toolbar. | The block has no image, or the block is not selected. | Add an image to the block. Then select the block. |
| The button shows, but it has no tooltip. | The `label` prop is missing. | Add a `label` prop to `ToolbarButton`. |
| The arrow keys do not move focus to the button. | The button is not a `ToolbarButton` inside a `ToolbarGroup`. | Use `ToolbarButton` from `@wordpress/components`. Put it inside a `ToolbarGroup`. |
| The editor shows "This block contains unexpected or invalid content." | The `save.js` output changed after you saved the post. | Do not change the markup in `save.js` without a block deprecation. Add a [deprecation](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-deprecation/) for the old markup. |

The same pattern works for any action that belongs to the block as a whole: toggling a setting with `isPressed`, opening a modal, or resetting a group of attributes. For a menu of related actions, swap `ToolbarButton` for [`ToolbarDropdownMenu`](https://developer.wordpress.org/block-editor/reference-guides/components/toolbar-dropdown-menu/) and keep the same `BlockControls` and `ToolbarGroup` wrapper around it.
