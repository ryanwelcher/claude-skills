# How to add a custom toolbar button to a block

The block toolbar is prime real estate. It's the first thing a user sees when they select a block, and it's where they expect the quick actions to live. Bold, alignment, replace media: they're all right there. If your block has an action that users reach for often, it belongs in the toolbar, not three clicks deep in the Settings sidebar.

I see a lot of custom blocks that store an image and give users no clean way to remove it. The user can replace the image, but they can't get back to the empty placeholder without deleting the whole block and starting over. That's a small thing that gets annoying fast.

So let's fix it. We'll add a "Remove image" button to the block toolbar with three components: `BlockControls`, `ToolbarGroup`, and `ToolbarButton`. The button clears the image attributes and returns the block to its placeholder state.

## Prerequisites

- WordPress 6.6 or later.
- Node.js 20 or later and npm.
- A local WordPress site, for example [`wp-env`](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-env/) or [WordPress Playground](https://wordpress.org/playground/).
- A block that uses the `@wordpress/scripts` build process.

## The starting block

I'm starting from a block scaffolded with `@wordpress/create-block`. If you already have a block that stores an image, you can skip ahead to the next section and follow along in your own code.

1. Open a terminal in the `wp-content/plugins` folder.
2. Run this command:

```bash
npx @wordpress/create-block@latest toolbar-image-demo
```

3. Open the `toolbar-image-demo` folder in your code editor.

Make sure that the `toolbar-image-demo/src` folder contains `block.json` and `edit.js`.

The block needs somewhere to keep the image. Three attributes cover it: the attachment ID, the URL, and the alt text.

4. In `src/block.json`, below the `"textdomain"` line, add the `attributes` object:

```json
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
```

Notice that `mediaId` and `mediaUrl` have no default. That matters later, when we clear them.

Next, the edit component. If there is no image, the block shows a `MediaPlaceholder`. If there is an image, the block shows the image. Here is the full file:

5. Replace the contents of `src/edit.js` with this code:

```js
/**
 * WordPress dependencies
 */
import { __ } from '@wordpress/i18n';
import { useBlockProps, MediaPlaceholder } from '@wordpress/block-editor';

/**
 * Internal dependencies
 */
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

	if ( ! mediaUrl ) {
		return (
			<div { ...blockProps }>
				<MediaPlaceholder
					icon="format-image"
					labels={ { title: __( 'Image', 'toolbar-image-demo' ) } }
					onSelect={ onSelectImage }
					accept="image/*"
					allowedTypes={ [ 'image' ] }
				/>
			</div>
		);
	}

	return (
		<div { ...blockProps }>
			<img src={ mediaUrl } alt={ mediaAlt } data-id={ mediaId } />
		</div>
	);
}
```

6. Run `npm start` in the `toolbar-image-demo` folder.
7. Activate the **Toolbar Image Demo** plugin in **Plugins > Installed Plugins**.
8. Add the block to a post and select an image.

Make sure that the block shows the image you selected.

Right now, the only way to get the placeholder back is to delete the block. Let's give users a button.

## Add the toolbar button

Here's the mental model for the three components:

| Component | Package | Job |
|---|---|---|
| `BlockControls` | `@wordpress/block-editor` | A slot. Anything you put inside it shows in the toolbar of the selected block. |
| `ToolbarGroup` | `@wordpress/components` | A visual group of controls, with a divider between it and the other groups. |
| `ToolbarButton` | `@wordpress/components` | One button. It handles keyboard navigation inside the toolbar for you. |

`BlockControls` is a [SlotFill](https://developer.wordpress.org/block-editor/reference-guides/slotfills/), so it doesn't matter where you place it in your JSX. The content gets moved to the toolbar either way. I like to put it at the top of the returned markup so it's easy to find.

1. In `src/edit.js`, change the `@wordpress/block-editor` import to this:

```js
import {
	useBlockProps,
	MediaPlaceholder,
	BlockControls,
} from '@wordpress/block-editor';
```

2. Below that import, add the imports for the toolbar components and the icon:

```js
import { ToolbarGroup, ToolbarButton } from '@wordpress/components';
import { trash } from '@wordpress/icons';
```

The `@wordpress/icons` package isn't a dependency of a freshly scaffolded block, so install it.

3. Run this command in the `toolbar-image-demo` folder:

```bash
npm install @wordpress/icons --save
```

Now the handler. Clearing the image is the reverse of selecting it: set every image attribute back to its empty state.

4. In `src/edit.js`, below the `onSelectImage` function, add the `onRemoveImage` function:

```js
	const onRemoveImage = () => {
		setAttributes( {
			mediaId: undefined,
			mediaUrl: undefined,
			mediaAlt: '',
		} );
	};
```

5. In `src/edit.js`, replace the final `return` statement with this code:

```js
	return (
		<>
			<BlockControls>
				<ToolbarGroup>
					<ToolbarButton
						icon={ trash }
						label={ __( 'Remove image', 'toolbar-image-demo' ) }
						onClick={ onRemoveImage }
					/>
				</ToolbarGroup>
			</BlockControls>
			<div { ...blockProps }>
				<img src={ mediaUrl } alt={ mediaAlt } data-id={ mediaId } />
			</div>
		</>
	);
```

6. Refresh the editor and select the block.
7. Click the trash icon in the block toolbar.

Make sure that the block shows the placeholder again.

I put the `BlockControls` in the final `return` only, not in the placeholder branch. That's deliberate. There's nothing to remove when the block is empty, so the button shouldn't be there. Putting the toolbar in the branch that has an image is the simplest way to show the button only when it's useful.

## Place the button in a specific toolbar group

By default, `BlockControls` adds your controls to the `default` group, which sits after the block-level controls like alignment. That's fine for a lot of cases. For a media action, though, I think it reads better next to the other media controls.

`BlockControls` accepts a `group` prop for this:

| `group` value | Where the controls show |
|---|---|
| `default` | The main group of block controls. This is the default. |
| `block` | The group for block-level settings, such as alignment. |
| `inline` | The group for inline formatting controls. |
| `other` | The group for media and other secondary actions. |
| `parent` | The group next to the parent block selector. |

1. In `src/edit.js`, change the opening `<BlockControls>` tag to this:

```js
			<BlockControls group="other">
```

2. Refresh the editor and select the block.

Make sure that the trash icon shows at the end of the toolbar, after the other controls.

## Add a replace button next to it

A remove button on its own is only half of the story. Users usually want to swap the image too. `MediaReplaceFlow` gives you the core "Replace" dropdown, and it drops straight into the same `BlockControls`.

1. In `src/edit.js`, change the `@wordpress/block-editor` import to this:

```js
import {
	useBlockProps,
	MediaPlaceholder,
	BlockControls,
	MediaReplaceFlow,
} from '@wordpress/block-editor';
```

2. In `src/edit.js`, replace the `<BlockControls group="other">` element and its contents with this code:

```js
			<BlockControls group="other">
				<MediaReplaceFlow
					mediaId={ mediaId }
					mediaURL={ mediaUrl }
					allowedTypes={ [ 'image' ] }
					accept="image/*"
					onSelect={ onSelectImage }
					name={ __( 'Replace', 'toolbar-image-demo' ) }
				/>
				<ToolbarGroup>
					<ToolbarButton
						icon={ trash }
						label={ __( 'Remove image', 'toolbar-image-demo' ) }
						onClick={ onRemoveImage }
					/>
				</ToolbarGroup>
			</BlockControls>
```

3. Refresh the editor and select the block.

Make sure that the toolbar shows a **Replace** button and a trash icon.

`MediaReplaceFlow` renders its own toolbar group, so you don't wrap it in a `ToolbarGroup`. The trash button keeps its own group, which gives it a divider and separates the "swap" action from the "remove" action. I like that separation. A destructive action shouldn't sit flush against a harmless one.

## Gotchas

### Set cleared attributes to `undefined`, not an empty string

It's tempting to write `mediaUrl: ''`. That works in the editor, but WordPress then saves `"mediaUrl":""` in the block comment delimiter. When you set an attribute to `undefined`, WordPress drops it from the delimiter, and the attribute falls back to its default. That's why `mediaId` and `mediaUrl` have no default in `block.json`: `undefined` is the true "empty" state.

`mediaAlt` has a default of `''`, so clearing it to `''` and clearing it to `undefined` give the same result.

### Always give `ToolbarButton` a `label`

An icon-only button with no `label` is invisible to screen readers. The `label` prop does double duty. It sets the `aria-label`, and it shows as the tooltip on hover. Don't skip it, and wrap it in `__()` so it gets translated.

### Use `ToolbarButton`, not `Button`

**CAUTION:** Do not put a plain `Button` inside `BlockControls`. Keyboard users cannot reach it with the arrow keys.

The block toolbar uses a roving tab index. Tab moves focus into the toolbar, and the arrow keys move between the controls. `ToolbarButton` registers itself with that system. A plain `Button` from `@wordpress/components` doesn't, so it breaks keyboard navigation for the whole toolbar.

### Focus disappears after the image is removed

When a user clicks the trash icon, the block rerenders into its placeholder branch. The button they just clicked no longer exists, so keyboard focus has nowhere to go. For a small demo block that's acceptable. For a production block, move focus to something sensible after the removal. The block wrapper is a good target:

1. In `src/edit.js`, below the `@wordpress/icons` import, add this import:

```js
import { useRef } from '@wordpress/element';
```

2. In `src/edit.js`, replace the `const blockProps = useBlockProps();` line with this code:

```js
	const blockRef = useRef();
	const blockProps = useBlockProps( { ref: blockRef } );
```

3. In `src/edit.js`, replace the `onRemoveImage` function with this code:

```js
	const onRemoveImage = () => {
		setAttributes( {
			mediaId: undefined,
			mediaUrl: undefined,
			mediaAlt: '',
		} );
		blockRef.current?.focus();
	};
```

4. Select the block with the keyboard and press Enter on the trash icon.

Make sure that focus stays on the block after the placeholder shows.

### The toolbar only shows for the selected block

`BlockControls` renders nothing when the block isn't selected. That's the correct behavior, but it trips people up when they write tests or try to debug a "missing" button. Select the block first, then look for the control.

### Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| The build fails with `Module not found: @wordpress/icons`. | The package is not installed. | Run `npm install @wordpress/icons --save`. |
| The button does not show in the toolbar. | The block is not selected, or the block has no image. | Select the block. Then select an image. |
| The button shows but nothing changes when you click it. | `onClick` does not call `setAttributes`. | Make sure that `onClick` is `onRemoveImage` and that `onRemoveImage` calls `setAttributes`. |
| The saved post still contains `"mediaUrl":""`. | The handler sets the attribute to an empty string. | Set `mediaUrl` to `undefined` in `onRemoveImage`. |
