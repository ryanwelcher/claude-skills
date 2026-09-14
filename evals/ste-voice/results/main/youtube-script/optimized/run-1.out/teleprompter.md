# Teleprompter — Add a Toolbar Button to Your Custom Block with BlockControls

> Read copy only — spoken words, no stage directions. Each block is tagged: **🎥 ON CAMERA** = talking head, look at the lens and perform; **🎙️ VOICEOVER** = read over screen-capture, you're not on screen. `* * *` marks a beat break (don't read it). Pause at the line breaks. Spoken code/symbols are spelled out the way you'd say them.

**🎥 ON CAMERA**

So I built a meme generator block. You pick an image, you type some top text and some bottom text, and boom, you've got a meme. Great. Now try to get rid of the image. You can't. There's no button for it, so you delete the block and start over, which is a pretty embarrassing thing to find in a block I wrote myself.

I'm Ryan Welcher, a developer advocate at Automattic. And I want to show you how to put your own button right in the block toolbar with BlockControls, so you never have to ship a block like this one.

* * *

**🎙️ VOICEOVER**

Okay, so here's the block. Image, top text, bottom text. When I select it, we get the block toolbar up here, and it's got the stuff WordPress gives every block. The block switcher, the drag handle, the up and down movers, and then the three-dot menu, which is kind of where features go to hide. What I want is a little trash can right in this toolbar that clears out the image and puts the placeholder back.

* * *

**🎥 ON CAMERA**

So what is BlockControls? If you've used InspectorControls to put settings in the sidebar, you already know this one. It's a Slot Fill. The toolbar has a slot sitting in it, and anything you wrap in BlockControls inside your block's edit component gets rendered into that slot.

**🎙️ VOICEOVER**

It's kind of like the mail slot in your front door. You don't walk into the house to drop off a letter, you just push it through the slot and it shows up on the other side. Your edit component lives in the block canvas, but the button ends up in the toolbar, which is a totally different part of the React tree. And BlockControls only renders its fill when your block is selected, so you don't have to wrap anything in an is-selected check yourself.

* * *

**🎙️ VOICEOVER**

All right, let's go write it. Up top, I'm pulling BlockControls in from the block-editor package, ToolbarButton from components, and the trash icon from the icons package.

Then down in the return, I drop in BlockControls, and I'm giving it a group of "other". The group prop tells it which section of the toolbar to land in, and because the slot wraps each group in its own toolbar group for you, I can put a ToolbarButton straight inside. Icon is trash, and the label is "Remove image". That label isn't just for looks, by the way. It's the tooltip, and it's what a screen reader announces, since the button has no visible text.

Let's see what this does. Refresh, select the block, and there it is. We've got a trash can. It doesn't do anything yet, because I haven't written remove-image, but it's in there.

* * *

**🎙️ VOICEOVER**

So the way this block stores the image is two attributes, the image ID and the image URL. Removing the image is just setting both of those back to undefined.

And under the hood, when an attribute is undefined, it just gets left out when the block serializes. It's not stored as an empty string or anything like that, it's gone. So the edit component sees no URL and renders the placeholder again, the same way it did when you first inserted the block.

Click it, and the image is gone, and we're back to the placeholder. And because this all goes through set-attributes, undo just works. Look at that. I didn't write anything for undo.

* * *

**🎙️ VOICEOVER**

Now there's one problem left. If I insert a fresh meme block with no image, the trash button is still sitting there, and clicking it removes nothing. That's a button that lies to you, and I've shipped a few of those.

The fix is small. I only render BlockControls when there's actually an image URL.

Empty block, no button. Pick an image, and the button shows up. Remove it, and the button goes away with it. Cool.

* * *

**🎥 ON CAMERA**

So that's it. BlockControls is a fill for the block toolbar, you put a ToolbarButton inside it, and the on-click is just a regular set-attributes call, so undo comes along for free. And if the button only makes sense sometimes, only render it sometimes. That's really all there is to it, and my meme block is a little less embarrassing now.

* * *

**🎥 ON CAMERA**

Let me know in the comments what button you'd add to your own block's toolbar. And if you haven't already, hit subscribe, because there's more block stuff coming. Thanks for watching and I'll see you in the next one.
