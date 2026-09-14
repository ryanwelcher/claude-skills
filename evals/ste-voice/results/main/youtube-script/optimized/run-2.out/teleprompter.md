# Add a Toolbar Button to Your Custom Block with BlockControls — Teleprompter

> Read copy only — spoken words, no stage directions. Each block is tagged: **🎥 ON CAMERA** = talking head, look at the lens and perform; **🎙️ VOICEOVER** = read over screen-capture, you're not on screen. `* * *` marks a beat break (don't read it). Pause at the line breaks. Spoken code/symbols are spelled out the way you'd say them.

**🎥 ON CAMERA**

So I built a meme generator block. You pick an image, you type your setup, you type your punchline. Great.

And then you realize you picked the wrong image, and there's no way to change it. You have to delete the whole block and start over, which is a pretty bad experience, and yeah, I shipped it like that for a while.

**🎙️ VOICEOVER**

So let's fix it by putting a button right up here in the block toolbar.

**🎥 ON CAMERA**

I'm Ryan Welcher, a developer advocate at Automattic. And I want to show you how to add your own button to a block's toolbar with Block Controls. It's a lot less code than you'd think.

* * *

**🎙️ VOICEOVER**

Okay, so here's the block. If there's no image, we return a Placeholder with the image picker in it. Once you pick one, we save it to the image attribute and render the meme with the two Rich Text fields on top of it.

So that "if not image" check is doing all the work here. If we can get image back to empty, the placeholder comes back and you can pick again.

* * *

**🎥 ON CAMERA**

So before we write anything, what is Block Controls actually doing? The toolbar isn't part of your block's markup. It lives somewhere else entirely in the editor.

Block Controls is a Slot Fill. The editor puts a slot up in the toolbar, and anything you put inside Block Controls gets rendered into that slot, even though you wrote it right in the middle of your Edit component.

**🎙️ VOICEOVER**

It's kind of like forwarding your mail. You write the address in one place and it shows up somewhere else.

And because the editor only shows those controls for the selected block, you don't have to worry about your button showing up on every block on the page.

* * *

**🎙️ VOICEOVER**

All right, so down in the second return, the one that renders the actual meme, right after the closing section, I'm going to add Block Controls. Inside that we want a Toolbar Group. The group is what gives you that little divider, so your button gets its own section instead of being jammed up against the core controls.

And then the button itself. Toolbar Button. For the icon I'm just passing the string "remove", which is a dashicon, because I'm a developer and not a designer and nobody wants to see me draw an SVG.

The label is what shows up in the tooltip, and it's what a screen reader announces, so don't skip it. And then on-click just calls set attributes and sets image to false. That's it.

And notice where this lives. It's only in the return that has an image. So when there's no image, there's no button, which makes sense, right? There's nothing to remove.

* * *

**🎙️ VOICEOVER**

Okay, let's save and see what this does. Select the block, and there's our button, with its own little group. Hover it, and you get the tooltip. And if I click it…

…the image is gone and we're right back at the picker. Pick a better meme, and the text is still there, because we only cleared the image. We never touched top text or bottom text.

* * *

**🎥 ON CAMERA**

So that's all there is to it. Block Controls is a fill that drops whatever you give it into the toolbar slot. You group your buttons with Toolbar Group, and each Toolbar Button is just an icon, a label, and an on-click that updates your attributes.

And that same pattern works for anything you want one click away. Toggles, resets, whatever your block needs.

* * *

**🎥 ON CAMERA**

If you add a toolbar button to one of your own blocks, let me know in the comments what it does. I want to see what you build.

There's a lot more block development stuff coming, so if you haven't already, hit subscribe.

Thanks for watching and I'll see you in the next one.
