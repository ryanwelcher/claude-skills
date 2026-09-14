# How to add a custom toolbar button to a block

The block toolbar is the first place people look when they want to do something to a block. Core blocks use it all the time: alignment, links, replacing media. When your own block has an action like that, the toolbar is where it belongs, and not buried at the bottom of the Settings sidebar.

The good news is that the API is small. Three components do all the work:

- **`BlockControls`** (from `@wordpress/block-editor`) is a slot that puts its children into the toolbar of the selected block.
- **`ToolbarGroup`** (from `@wordpress/components`) groups related controls and draws the separators between groups.
- **`ToolbarButton`** (from `@wordpress/components`) is the button itself, with the roving focus and keyboard behavior the toolbar expects.

I'm going to build a small image block and add a "Clear image" button to its toolbar. Clearing an attribute is a nice example because it touches every part of the pattern: reading attributes, calling `setAttributes`, and deciding what the button does when there is nothing to clear.

## Prerequisites

- Node.js 20 or later and npm.
- A local WordPress 6.6 or later site. [`wp-env`](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-env/) and [WordPress Playground](https://wordpress.org/playground/) both work.
- Basic knowledge of `block.json`, `useBlockProps`, and `setAttributes`.

## Scaffold the block

I'm starting from `@wordpress/create-block` so the build tooling is already in place. If you have an existing block with an image attribute, skip ahead to the next section.

1. Open a terminal in the `wp-content/plugins` folder of your site.
2. Run this command:

   ```bash
   npx @wordpress/create-block@latest toolbar-image --namespace devblog
   ```

3. Go to the new `toolbar-image` folder.
4. Run `npm start`.
5. In the WordPress admin, go to **Plugins > Installed Plugins**.
6. Activate the **Toolbar Image** plugin.

Make sure that the **Toolbar Image** block shows in the block inserter.

## The basic image block

Before the toolbar gets a button, the block needs something to clear. This version stores the image ID, URL, and alt text, and shows a `MediaPlaceholder` when there is no image.

1. In `src/block.json`, below `"description"`, add:

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

2. Replace the full contents of `src/edit.js` with:

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
   				<img src={ mediaUrl } alt={ mediaAlt } />
   			) : (
   				<MediaPlaceholder
   					icon="format-image"
   					labels={ { title: __( 'Toolbar Image', 'toolbar-image' ) } }
   					accept="image/*"
   					allowedTypes={ [ 'image' ] }
   					onSelect={ onSelectImage }
   				/>
   			) }
   		</div>
   	);
   }
   ```

3. Replace the full contents of `src/save.js` with:

   ```js
   import { useBlockProps } from '@wordpress/block-editor';

   export default function save( { attributes } ) {
   	const { mediaId, mediaUrl, mediaAlt } = attributes;

   	if ( ! mediaUrl ) {
   		return null;
   	}

   	return (
   		<figure { ...useBlockProps.save() }>
   			<img
   				src={ mediaUrl }
   				alt={ mediaAlt }
   				className={ mediaId ? `wp-image-${ mediaId }` : undefined }
   			/>
   		</figure>
   	);
   }
   ```

4. Add the block to a post.
5. Select an image from the Media Library.

Make sure that the image shows in the editor.

## Add the toolbar button

Now for the part this post is actually about. `BlockControls` only renders its children when the block is selected, so you don't need to check `isSelected` yourself. Inside it, a `ToolbarGroup` holds a single `ToolbarButton`. The button's `onClick` resets all three attributes.

**CAUTION:** Do not import `ToolbarButton` or `ToolbarGroup` from `@wordpress/block-editor`. They are in `@wordpress/components`. The wrong import makes the block crash in the editor.

1. In the `toolbar-image` folder, run `npm install @wordpress/icons --save`.
2. In `src/edit.js`, replace the two import lines at the top of the file with:

   ```js
   import { __ } from '@wordpress/i18n';
   import {
   	useBlockProps,
   	MediaPlaceholder,
   	BlockControls,
   } from '@wordpress/block-editor';
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

4. In `src/edit.js`, change the `return` statement to:

   ```js
   return (
   	<>
   		<BlockControls>
   			<ToolbarGroup>
   				<ToolbarButton
   					icon={ trash }
   					label={ __( 'Clear image', 'toolbar-image' ) }
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
   					labels={ { title: __( 'Toolbar Image', 'toolbar-image' ) } }
   					accept="image/*"
   					allowedTypes={ [ 'image' ] }
   					onSelect={ onSelectImage }
   				/>
   			) }
   		</div>
   	</>
   );
   ```

5. Save the file and refresh the editor.
6. Select the block.
7. In the block toolbar, click the **Clear image** button.

Make sure that the image is removed and the `MediaPlaceholder` shows again.

## Disable the button when there is nothing to clear

Right now the button shows even when the block is already empty. Clicking it does nothing, which is confusing. I think disabling it is the better choice here instead of hiding it. The toolbar layout stays stable, and people can still discover the action before they add an image.

1. In `src/edit.js`, in the `ToolbarButton` props, below `onClick={ onClearImage }`, add:

   ```js
   disabled={ ! mediaUrl }
   accessibleWhenDisabled
   ```

2. Remove the image from the block.

Make sure that the **Clear image** button is gray and does not respond to a click.

The `accessibleWhenDisabled` prop matters more than it looks. Without it, the button gets the native `disabled` attribute, which drops it out of the tab order. When you click **Clear image**, the button disables itself while it still has focus, and keyboard users lose their place in the toolbar. With `accessibleWhenDisabled`, the button uses `aria-disabled` instead and keeps focus.

## Put the button in the right toolbar group

By default, `BlockControls` adds its children to the `default` group, which sits after the block switcher and the block movers. The `group` prop lets you target a different area:

| `group` value | Where the controls show |
|---|---|
| `default` | The main group for block-specific controls |
| `block` | Next to the block switcher, where alignment controls usually go |
| `inline` | The group for inline formatting, like **Bold** and **Link** |
| `other` | Near the end of the toolbar, after the other groups |

A clear action is secondary, so I like it in `other`. That keeps it away from the controls people use most.

1. In `src/edit.js`, change the opening `<BlockControls>` tag to:

   ```js
   <BlockControls group="other">
   ```

2. Refresh the editor and select the block.

Make sure that the **Clear image** button shows near the end of the block toolbar.

## Gotchas

A few things tend to trip people up with this pattern.

- **Always pass a `label`.** An icon-only `ToolbarButton` uses `label` for its tooltip and its accessible name. Without it, screen readers announce "button" and nothing else.
- **Clear to `undefined`, not an empty string, for attributes without a default.** An attribute set to `''` is still serialized into the block comment delimiter. `undefined` removes it, so the saved markup matches a freshly inserted block.
- **Changing `save` changes the saved markup.** If your block already exists in published content, changing `save.js` causes block validation errors. Add a [deprecation](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-deprecation/) before you ship a change like that.
- **Don't nest a `ToolbarGroup` in a `ToolbarGroup`.** For a set of related actions, use `ToolbarDropdownMenu`, or add more `ToolbarButton` components to the same group.
- **`BlockControls` is editor-only.** It belongs in `edit.js`. It does nothing in `save.js`, and it has no effect on the front end.

### Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| The button does not show in the toolbar. | The block is not selected, or `BlockControls` is outside the returned JSX. | Select the block. Make sure that `BlockControls` is in the component's `return` statement. |
| The editor shows "This block has encountered an error" after you add the button. | The import comes from `@wordpress/block-editor`. | Import `ToolbarGroup` and `ToolbarButton` from `@wordpress/components`. |
| The editor shows "This block contains unexpected or invalid content." | The `save` output changed for existing content. | Add a deprecation for the old `save` function. |
| Keyboard focus leaves the toolbar after a click. | The button is `disabled` without `accessibleWhenDisabled`. | Add the `accessibleWhenDisabled` prop to the `ToolbarButton`. |

The same three components cover almost any block toolbar action. Swap `onClearImage` for a function that toggles an attribute, opens a modal, or replaces media, and the rest of the code stays the same.
