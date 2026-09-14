# Ryan Welcher — Voice Excerpt Reel

A curated set of VERBATIM excerpts from the full livestream transcripts in this folder (Q6F9EjNor3Q.txt, wBvJZQbGC5o.txt, US-E_0X2djQ.txt, TMV-Ko_7I_M.txt) — a fast way to re-anchor on Ryan's spoken rhythm without re-reading 13k words.
These are livestreams, which are looser than an edited tutorial: mine them for sentence-level voice (stutters, restarts, asides, self-talk), not macro structure.
Trimming is marked with […]; nothing is paraphrased or cleaned up. Note: TMV-Ko_7I_M and wBvJZQbGC5o are two captures of the same stream.

---

## 1. Opens / greetings

**US-E_0X2djQ.txt**
> All right. Hey everybody. How's it going today? Um, yeah, stream day. Excited. Excited. So, oh, hey, Joe Cooper. Thanks for the, uh, say hi. How you doing? How's it going? Morning, Paul. Hello, Chad. Hello, everyone. […] So today is um yesterday I was supposed to be making a video and I got spent the whole day working on um the icon block because we are like about a week and a bit away maybe two weeks 19th. What is that? That is like 14 days from today. So two weeks away I guess from uh beta 1 for WordPress 7.0.

**wBvJZQbGC5o.txt**
> All right. Hi, everybody. How's it going? Oh, my microphone. It's way over here. Hi, everybody. How's it going? Um, welcome to the stream today. It's been a while since I've streamed. It's been a couple of weeks, I think. Um, I was sick last week and then I was at work at Asia which was an absolute blast. […] I'm putting on my glasses because I can't see anything anymore. So, there's that. Today, um, is kind of exciting. I'm I'm I I'm pretty excited.

**Q6F9EjNor3Q.txt** (guest episode open)
> ALL RIGHT. HI EVERYBODY. HERE WE ARE. We're here. We're here and I'm joined by a special guest, friend, um Lovekesh, TheLovekesh as he likes to go by. Um welcome. How's it going, man? Great to have you on.

---

## 2. Type-it-and-narrate explanations

**wBvJZQbGC5o.txt** (pitching the idea while demoing it)
> So, so the premise is I I want to create a video using like of a of a demo in WordPress. So, you know, Playright is a really great way of doing endtoend testing and it's basically like a human or like it's a, you know, you get a headless browser and it will click through and do things for you. So, what I thought I would be really cool is the ability to use natural language, say things like go and create a post and then have that be translated into playright end to end like playright uh selectors and then generate a video. So, playright will will spit out videos for you. So the idea here is that I I can say things like uh create a new post then install jetack right so I click that hit go and then so it's got the it it's got these these two directions as as I'm calling them

**wBvJZQbGC5o.txt** (explaining architecture mid-demo)
> we have this concept of like uh playground pools. So behind the scenes when we start up the server there is the ability like so the like playground takes a long time to spin up right. So when we hit preview we don't want to wait 10 seconds 14 seconds or whatever it takes. So we have these like these these pools kind of um ready like warmed and ready. So, so there's two in instances of playground that are being run and and so so if if I were to come in here and grab I don't know what this block select, it should be pretty quick to spin up like that that that's pretty fast considering we have to spin up an entire instance of playground with a blueprint using this CLI. So, it's it's it's pretty fast, right?

**US-E_0X2djQ.txt** (teaching a tool aside, mid-flow)
> So, if you're not familiar with git amend, basically, if you haven't pushed your your like if you commit something and you haven't pushed it up yet, you can add something to that last commit. And so, if I look at the if if I were to look at the graph, um you can see this thing here. You can see I've actually changed I've removed this and now that last change is actually part of this commit, which is really handy. It doesn't work if you've already pushed it up because you you're you're just you got to just do another commit for that. But, you know, if you're dumb like me and you forgot to add something, we can just do it that way. Cool.

**US-E_0X2djQ.txt** (explaining an API he just learned)
> This unstable mark next change is not persistent. So, I didn't know what this did. um I was told that I need to use it because what we're doing here is when you when you change the value the width value to anything less than what the default is. Um this changes it back to the default which we've set at 48. But you have to call this and this is in sorry this is inside of a use effect. Um but if if you don't call this this basically adds it to the undo stack. So if you undo it, it'll get you in like this weird loop where like it goes around. So this is basically saying don't add this to the undo history.

---

## 3. Reactions & course-corrections

**wBvJZQbGC5o.txt** (first demo breaks)
> and then if I click preview now what should happen uh oh it's taking There we go. So, we're going to create a new post, I hope. Is this just failing on my first demo? Why? Okay. All right. Hold on. Stop this. I've got some some other ones. So, let's do one basic insert test. Okay. So, so this is saying create a new post. So, if I preview this, I I wonder if my branch is is breaking this.

**wBvJZQbGC5o.txt** (chasing a bug report he can't trigger)
> And do I hit do I make another change and then hit save again? I can't reproduce this. Huh? Okay. Huh? Okay. […] I can't I can't reproduce that. Huh. Okay. Well, I mean, I can weird. I mean, it's working. I'm just not and I'm not getting that error. So, I'm not really sure.

**Q6F9EjNor3Q.txt** (live test refuses to cooperate)
> Okay, so I can't do it here, which is super annoying. Um I I don't know why that's happening. Do I have to enable WP-CLI on this? Come on. Come on, y'all. That's super annoying. Hm. I could try it. Let me try it on a different site. Uh let me try it on my Badge Press site. Sure, why not? Let's just see. […] I give up. Studio, what's your problem? What is your problem, Studio? Um Okay, I don't have any way to test this right now.

**US-E_0X2djQ.txt** (finding his own mistake)
> I don't know why this thing is doing Oh, you dirty son of a what? icon edit. Well, what have I done? Okay, you know what? I'm gonna close. I got too many windows open here. So in here I got edit on 30 and then 39 30. Oh, okay. That's the problem.

---

## 4. Humor & self-deprecation

**US-E_0X2djQ.txt** (on his own code)
> So, I spent yesterday afternoon adding that back in and uh yeah, so we're looking at that and we got some design input and we got some code input and I realized just how rusty I am at writing actual production code because I forget how to do like anything. Some of the errors are so dumb and like I would I would be mad at like if I was reviewing my own code, I'd be like who is this idiot? Fire him. He's he's he's garbage. So that's that. Yeah. So hopefully I'm getting better.

**Q6F9EjNor3Q.txt** (plugging his own plugin during a guest's demo)
> Well, there's only one plugin that everyone should be installing. I think it's called Advanced Query Loop. And it's by the best looking guy named Ryan on this stream. Cuz if I do WPM install Advanced Query Loop, boom. Resolving. Okay. So, let's look at Let's I'm just going to open this up in Visual Studio so we can just see what's going on. What's going on? Here we go. All right. So, content plugins, Advanced Query Loop. Okay. So, it installed. That was super painless. Um all right, demo over. We can go home.

**wBvJZQbGC5o.txt** (on his collaborator)
> See, the way the way this works on this project is Aanus is way smarter than me and way better at being a developer. So, what I do is I come up with these ideas and I and and I vibe vibe code the crap out of it. And uh you know what? Yeah. And then and then he comes in and goes, "Oh, hold on now. let's fix this, this, and this. And I go, okay. And then I fix it. Um, so without him, this this project would just be spaghetti code wrapped up with duct tape and best wishes.

**US-E_0X2djQ.txt** (the glasses bit)
> you know, you know what? I'm I'm gonna Okay, I got glasses, everybody. I have glasses now, so I can read because I'm 400 years old, but I can actually read that fairly well. So, I'm not going to wear my glasses today.

**TMV-Ko_7I_M.txt** (mock-insulting the absent teammate)
> Yeah. Yeah, he doesn't know what he's doing. No, he's not. He's a wonderful guy. I'm I'm being facicious. Um, but I want to I I want to impress him. I want him to think I'm smart.

---

## 5. Closes / sign-offs

**US-E_0X2djQ.txt**
> So, uh, but anyways, on that note, I'm going to, um, drop off and I'm gonna thank everyone for hanging out with me today and I'm I'm going to continue to work on this, uh, for the next few days to get it into a much better shape so we can actually get this thing merged hopefully uh, before the 19th and that'll be great. Awesome. Okay. Well, thanks everyone. I'll talk to you all soon. Thanks for hanging out with me. We will chat later. So, if anyone wants to come on the next um edition of Talk Debbie to me, um I'm open. That would be great. […] Anyway, so if you're interested, let me know. Be great to h have everyone on. And that and on that note, I'm gonna let you all go. Thanks. You're the best.

**TMV-Ko_7I_M.txt**
> But um I think I'm going to probably drop off now, but thanks so much for hanging out with me, Mr. Adam Silver. Thank you for hanging out with me. Uh if you haven't already, go and subscribe to his podcast, which I'll drop in chat right here. Um, and uh, yeah, I'll talk to everybody uh, not next week because I will be on a plane, but uh, probably the week after. So, thanks for joining me. It's always always a good time. And I will talk to you all later. Bye.

**Q6F9EjNor3Q.txt**
> All right. Well, we're going to call it. But uh thanks for hanging out today um everyone in chat and we will I won't be streaming next week cuz I will be at WordCamp Europe, but then the week after I will be streaming and then I think I have my next guest set up. You know him and love him as Terrence. Uh he's he's he's going to come on and show us something that he built that I'm going to completely make fun of cuz that's how we do things. Anyways, okay. Enough about that. Love guest, thanks so much, man. And we'll talk to you all later. Okay. We'll talk to you soon. Have a good one. Bye.
