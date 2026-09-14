# How to add a custom toolbar button to your block

The block toolbar is the first place users look when they want to do something to a block. Core blocks use it for alignment, text formatting, and replacing media. Your custom blocks can use it too, and it takes less code than you might expect.

I see a lot of custom blocks that put every action in the Settings Sidebar. That works, but it hides common actions behind an extra click. If an action applies to the block as a whole and users reach for it often, it belongs in the toolbar.

Let's build a toolbar button that removes the image from a block. You'll use three components:

- **`BlockControls`** from `@wordpress/block-editor`: a slot that renders its children in the block's toolbar
- **`ToolbarGroup`** from `@wordpress/components`: groups related controls and adds the divider between them
- **`ToolbarButton`** from `@wordpress/components`: the button itself, with keyboard navigation handled for you

## The starting block

The examples use a simple block that stores an image ID and URL. If you want to follow along, scaffold a block with `npx @wordpress/create-block@latest toolbar-demo` and replace the generated files with the code below.

Here's `block.json`:

```json
{
	"$schema": "https://schemas.wp.org/trunk/block.json",
	"apiVersion": 3,
	"name": "toolbar-demo/image-card",
	"version": "0.1.0",
	"title": "Image Card",
	"category": "media",
	"icon": "format-image",
	"attributes": {
		"mediaId": {
			"type": "number"
		},
		"mediaUrl": {
			"type": "string"
		}
	},
	"supports": {
		"html": false
	},
	"textdomain": "toolbar-demo",
	"editorScript": "file:./index.js",
	"style": "file:./style-index.css"
}
```

And here's the starting `edit.js`. It shows a `MediaPlaceholder` when there's no image and the image when there is one:

```js
import { __ } from '@wordpress/i18n';
import { useBlockProps, MediaPlaceholder } from '@wordpress/block-editor';

export default function Edit( { attributes, setAttributes } ) {
	const { mediaId, mediaUrl } = attributes;
	const blockProps = useBlockProps();

	if ( ! mediaUrl ) {
		return (
			<div { ...blockProps }>
				<MediaPlaceholder
					icon="format-image"
					labels={ { title: __( 'Image Card', 'toolbar-demo' ) } }
					accept="image/*"
					allowedTypes={ [ 'image' ] }
					onSelect={ ( media ) =>
						setAttributes( { mediaId: media.id, mediaUrl: media.url } )
					}
				/>
			</div>
		);
	}

	return (
		<div { ...blockProps }>
			<img src={ mediaUrl } alt="" className={ `wp-image-${ mediaId }` } />
		</div>
	);
}
```

Once a user picks an image, there's no way to get back to the placeholder. That's the gap our toolbar button fills.

## Adding the button

Wrap a `ToolbarButton` in a `ToolbarGroup`, then wrap that in `BlockControls`. Place it anywhere in the returned JSX. `BlockControls` is a slot fill, so it renders in the toolbar no matter where it sits in your component tree.

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
	const { mediaId, mediaUrl } = attributes;
	const blockProps = useBlockProps();

	if ( ! mediaUrl ) {
		return (
			<div { ...blockProps }>
				<MediaPlaceholder
					icon="format-image"
					labels={ { title: __( 'Image Card', 'toolbar-demo' ) } }
					accept="image/*"
					allowedTypes={ [ 'image' ] }
					onSelect={ ( media ) =>
						setAttributes( { mediaId: media.id, mediaUrl: media.url } )
					}
				/>
			</div>
		);
	}

	return (
		<>
			<BlockControls>
				<ToolbarGroup>
					<ToolbarButton
						icon={ trash }
						label={ __( 'Remove image', 'toolbar-demo' ) }
						onClick={ () =>
							setAttributes( {
								mediaId: undefined,
								mediaUrl: undefined,
							} )
						}
					/>
				</ToolbarGroup>
			</BlockControls>
			<div { ...blockProps }>
				<img
					src={ mediaUrl }
					alt=""
					className={ `wp-image-${ mediaId }` }
				/>
			</div>
		</>
	);
}
```

The `@wordpress/icons` package isn't a dependency of the scaffolded block, so install it first:

```bash
npm install @wordpress/icons --save
```

Select the block with an image in it, and you'll see a trash icon in the toolbar. Click it, and the block goes back to the placeholder.

A few things are worth calling out:

- **`label`** does double duty. It becomes the button's `aria-label` and the tooltip that appears on hover.
- **`onClick`** sets both attributes to `undefined`. That removes them from the block's comment delimiter entirely, rather than saving an empty string.
- **The fragment** (`<>...</>`) lets `BlockControls` sit next to the block wrapper. Keep `blockProps` on the outer `div`, not on the fragment.

## Showing the button all the time

Right now the button only exists when there's an image. That's fine for this block, but sometimes you want the button visible in both states and disabled when it can't do anything. Moving `BlockControls` above the conditional handles that.

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
	const { mediaId, mediaUrl } = attributes;
	const blockProps = useBlockProps();

	const removeImage = () => {
		setAttributes( { mediaId: undefined, mediaUrl: undefined } );
	};

	return (
		<>
			<BlockControls>
				<ToolbarGroup>
					<ToolbarButton
						icon={ trash }
						label={ __( 'Remove image', 'toolbar-demo' ) }
						onClick={ removeImage }
						disabled={ ! mediaUrl }
					/>
				</ToolbarGroup>
			</BlockControls>
			<div { ...blockProps }>
				{ mediaUrl ? (
					<img
						src={ mediaUrl }
						alt=""
						className={ `wp-image-${ mediaId }` }
					/>
				) : (
					<MediaPlaceholder
						icon="format-image"
						labels={ { title: __( 'Image Card', 'toolbar-demo' ) } }
						accept="image/*"
						allowedTypes={ [ 'image' ] }
						onSelect={ ( media ) =>
							setAttributes( {
								mediaId: media.id,
								mediaUrl: media.url,
							} )
						}
					/>
				) }
			</div>
		</>
	);
}
```

The `disabled` prop greys the button out and stops `onClick` from firing. The button stays in the tab order through the toolbar's arrow-key navigation, so keyboard users still discover it.

## Using a text button instead of an icon

Icons are compact, but "trash" can read as "delete the whole block." If you think that's confusing for your users, drop the `icon` prop and pass the text as children:

```js
<BlockControls>
	<ToolbarGroup>
		<ToolbarButton onClick={ removeImage } disabled={ ! mediaUrl }>
			{ __( 'Remove image', 'toolbar-demo' ) }
		</ToolbarButton>
	</ToolbarGroup>
</BlockControls>
```

This matches the text "Replace" button on the core Image block. I think text is the better choice for any action that's destructive or easy to misread.

## Controlling where the button appears

`BlockControls` accepts a `group` prop that decides which section of the toolbar your controls render in:

- **`default`**: the main group, and what you get when you omit the prop
- **`block`**: the group near the start of the toolbar, where core puts alignment controls
- **`inline`**: the group for inline formatting, next to bold and italic
- **`other`**: the group toward the end, where core puts "Replace"

A remove button pairs naturally with replace actions, so `other` is a good home for it:

```js
<BlockControls group="other">
	<ToolbarGroup>
		<ToolbarButton onClick={ removeImage } disabled={ ! mediaUrl }>
			{ __( 'Remove image', 'toolbar-demo' ) }
		</ToolbarButton>
	</ToolbarGroup>
</BlockControls>
```

## Adding more than one button

Every `ToolbarGroup` renders with a divider around it. Put related buttons in the same group and unrelated buttons in separate groups. Here's the remove button alongside a button that opens the image in a new tab:

```js
import { __ } from '@wordpress/i18n';
import { BlockControls } from '@wordpress/block-editor';
import { ToolbarGroup, ToolbarButton } from '@wordpress/components';
import { external, trash } from '@wordpress/icons';

function ImageCardToolbar( { mediaUrl, onRemove } ) {
	return (
		<BlockControls group="other">
			<ToolbarGroup>
				<ToolbarButton
					icon={ external }
					label={ __( 'Open image in new tab', 'toolbar-demo' ) }
					href={ mediaUrl }
					target="_blank"
					disabled={ ! mediaUrl }
				/>
				<ToolbarButton
					icon={ trash }
					label={ __( 'Remove image', 'toolbar-demo' ) }
					onClick={ onRemove }
					disabled={ ! mediaUrl }
				/>
			</ToolbarGroup>
		</BlockControls>
	);
}

export default ImageCardToolbar;
```

Pulling the toolbar into its own component keeps `Edit` readable once you have more than one or two controls. Render it with `<ImageCardToolbar mediaUrl={ mediaUrl } onRemove={ removeImage } />`.

## Gotchas

### Don't render `ToolbarButton` without a `ToolbarGroup`

`ToolbarButton` expects toolbar context. Without a wrapping `ToolbarGroup` (or `ToolbarItem`), you lose the roving tab index that lets users move between toolbar controls with the arrow keys. It looks fine with a mouse and breaks for keyboard users.

### Always pass a `label` to icon buttons

An icon-only `ToolbarButton` without `label` has no accessible name. Screen readers announce it as "button" and nothing else. You also lose the tooltip.

### Clear every related attribute

If you only clear `mediaUrl`, the block still holds a stale `mediaId`. That leads to confusing bugs later, like a `wp-image-123` class pointing at an image that's gone, or a `useSelect` call fetching media that no longer belongs to the block. Reset every attribute that describes the image in a single `setAttributes` call. One call also means one undo step.

### `undefined` and empty strings aren't the same

Setting `mediaUrl: ''` saves `"mediaUrl":""` in the block markup. Setting `mediaUrl: undefined` removes the key. If your attribute has a `default` in `block.json`, `undefined` falls back to that default. Pick the one that matches what your `save` function and any PHP rendering expect.

### The toolbar only shows when the block is selected

`BlockControls` renders nothing until a user selects the block. If you're testing and don't see your button, click the block first. For multi-block selections, the editor hides custom block controls entirely, so don't put anything there that users need during bulk edits.

### The button is removing the image, not the attachment

Clearing the attribute detaches the image from the block. The file stays in the Media Library. If your label says "Delete image," users will reasonably expect it to be gone from the site. "Remove image" sets the right expectation.
