# Add a Toolbar Button to Your Custom Block with BlockControls — Teleprompter

> Read copy only — spoken words, no stage directions. Each block is tagged: **🎥 ON CAMERA** = talking head, look at the lens and perform; **🎙️ VOICEOVER** = read over screen-capture, you're not on screen. `* * *` marks a beat break (don't read it). Pause at the line breaks. Spoken code/symbols are spelled out the way you'd say them.

**🎥 ON CAMERA**

So you pick an image in your block, and you immediately regret it. And there's no way to get rid of it. You can delete the whole block and start over, or you can open the code editor and hand-edit the block comment like an animal. I've done both. I'm not proud of it.

**🎙️ VOICEOVER**

So we're going to put a button right up here in the block toolbar that fixes it.

**🎥 ON CAMERA**

I'm Ryan Welcher, a developer advocate at Automattic. And I want to show you how to add your own buttons to the block toolbar with BlockControls, because it's a lot less code than you'd think.

* * *

**🎙️ VOICEOVER**

Okay, so this is the meme generator block from the Block Developer Cookbook. When there's no image, we show a placeholder with a bunch of memes from the Imgflip API. I pick one, it drops in, I add my setup, my punchline… and yeah, that's not funny. I want a different one.

And there's nothing here. The placeholder only shows up when the image attribute is empty, and right now nothing in the UI ever empties it. So once you pick, you're stuck with it.

* * *

**🎥 ON CAMERA**

So the thing we want is BlockControls. And the easiest way to think about it is kind of like a mail slot. Your block's sitting over here in the canvas, the toolbar's sitting up there, and BlockControls lets you drop stuff through the slot so it shows up in the toolbar.

**🎙️ VOICEOVER**

Under the hood, it's a Slot slash Fill. The block toolbar renders a slot, and BlockControls is the fill. So in your J S X it sits right next to your block markup, but whatever you put inside it gets rendered up in the toolbar. And the editor only renders those controls for the block that's selected, so you don't have to check is-selected yourself.

* * *

**🎙️ VOICEOVER**

All right, so in edit dot j s. BlockControls comes from block-editor, and ToolbarGroup and ToolbarButton come from components. Two different packages, which gets me every single time.

Now down in the return, right after the section, we add BlockControls. Inside that goes a ToolbarGroup, which gives us that little divider so our button isn't jammed up against the core ones. And then the ToolbarButton.

Give it an icon and give it a label. Don't skip the label. It's the tooltip, and it's what a screen reader announces, because an icon button with no label is just a mystery square.

And the on-click is one line. We set image to false. The edit function already checks if there's no image to decide whether to show the placeholder, so the second that attribute goes falsy, the block re-renders and we're back at the picker.

And notice where this lives. It's only in the branch that renders the image. So when there's no image, there's no button, which makes sense, right? There's nothing to remove.

* * *

**🎙️ VOICEOVER**

Let's see what this does. Refresh, click the block, and there's our button. Hover over it and there's the label.

Click it, and the image is gone and the placeholder's back. So now I can pick a better one. Much better. Arguably.

And the text stuck around, because we only cleared the image attribute. Which is actually what I want here, since it's the picture that was bad, not my joke. Okay, maybe also my joke.

* * *

**🎥 ON CAMERA**

There's one caveat here, and then I'll let you go. The image attribute is typed as an object in block dot json, and we're setting it to false. It works, because the check is just "is this falsy." But if you want to keep your types honest, set it to undefined instead, and the attribute just gets left out when the block saves.

* * *

**🎥 ON CAMERA**

So that's the whole trick. Wrap your button in BlockControls, put it in a ToolbarGroup, give it a label, and have the on-click update your attributes. The editor handles getting it into the toolbar for you.

Let me know in the comments what button you're adding to your own block toolbar. And if you haven't already, hit subscribe, because there's more block development stuff coming. Thanks for watching and I'll see you in the next one.
