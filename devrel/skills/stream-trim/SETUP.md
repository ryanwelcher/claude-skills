# stream-trim: what you need

stream-trim turns a raw OBS recording into a finished stream without Premiere. You run `/stream-trim <recording>` in Claude Code, and it does this:

1. Checks your tools and your recording setup (a **profile**).
2. Prepares the recording: a 720p preview, the mic waveform, and a first guess at In and Out.
3. Opens a page in your browser. You trim, and it renders the final in 4K.
4. Finds shorts in the stream while you trim. You pick them on the page and it renders them as 9:16 with captions.
5. Puts title options on the page. Picking one renames the file to it.
6. Writes the descriptions.

Everything runs on your Mac. Nothing is uploaded anywhere.

## Required

| What | Why | How to get it |
|---|---|---|
| A Mac with Apple Silicon (M1 or later) | The transcriber (`mlx-whisper`) only runs on Apple Silicon. | |
| Claude Code, with the `devrel` plugin | It's the skill. | `/plugin marketplace add ryanwelcher/claude-skills`, then `/plugin install devrel@ryan-claude-skills` |
| Homebrew | Installs the tools below. | https://brew.sh |
| ffmpeg with libass, libx265 and VideoToolbox | Cuts, mixes and encodes everything. libass burns in the captions, libx265 encodes the final, VideoToolbox makes the preview. The stock Homebrew ffmpeg has no libass. | `brew tap homebrew-ffmpeg/ffmpeg && brew install homebrew-ffmpeg/ffmpeg/ffmpeg` (if you already have ffmpeg: `brew uninstall ffmpeg` first) |
| mlx-whisper | Transcribes the stream on your Mac, for the shorts and the chapters. | `brew install uv && uv tool install mlx-whisper` |
| The Jost SemiBold font | The caption font. | Download Jost from Google Fonts and put the static `Jost-SemiBold.ttf` in `~/Library/Fonts`. A profile can name a different font. |
| A profile for your OBS setup | Says which audio tracks to keep, which one is your mic, and how late your mic runs. | Claude builds one with you on your first run (below). |
| Your voice on OBS audio track 1 | The transcript, and so the shorts and chapters, comes from track 1. In most OBS setups track 1 is the full mix, which works. | Check your OBS output settings. Claude warns you during setup if track 1 has no voice on it. |

Claude checks these at the start of every run. If ffmpeg (or its libass) or mlx-whisper is missing, it tells you which and why, and offers to install it. It never installs anything without asking. If your ffmpeg has no libx265 or VideoToolbox, Claude stops and tells you, because that needs a different ffmpeg build.

## Optional

| What | What it adds | Without it |
|---|---|---|
| The viDIQ connector in Claude | Scores each title option (0 to 100) so you can see which is likely to get clicks. Each score uses 5 viDIQ credits. | You still get title options to pick from, just without scores. Claude tells you it skipped the scoring. |
| Keeping recordings on your Mac | Prepare reads the whole recording once. From a local file that takes about 6 minutes for a 1.5-hour stream. | If the recording is only in Google Drive or iCloud, Claude stops and asks you to make it available offline first. Streaming it from the cloud took 84 minutes. |

## Only for Ryan's setup

These are tied to Ryan's channel, so they only run with his `ryan-obs` profile:

- The full YouTube description in his template, with his links and hashtags (`youtube-stream-description`, which also needs `yt-dlp`).
- The voice pass against his voice cards (`sounds-like-me`).
- His tuned voice chain, matched to his Premiere "Podcast Voice" settings.

With your own profile you get the chapter list for the full video, and plain titles and descriptions for the shorts, written from what you said in each clip.

## Your first run

When you don't have a profile yet, Claude walks you through making one:

1. Claude cuts a 5-second sample of each audio track and gives you the files to listen to. Tell it which track is which (mic, guest, music, alerts) and which to drop.
2. Claude asks how many frames late your mic runs. If you don't know, say 0. You can check it later: press Play on a short and watch your lips.
3. Claude grabs a frame from your usual scene and works out where your camera and screen are, for the short layout.
4. Claude saves the profile to `~/.config/stream-trim/profiles/<name>.json` and makes it your default. Your profile stays on your Mac.

Your profile starts with the voice processing off. The audio is still mixed and brought to a standard loudness (-17 LUFS for the final, -14 for shorts), but your voice isn't compressed or EQ'd. Shorts come out about 1 dB quieter than Ryan's until you tune your own voice chain.

## Where things go

Next to your recording:

- `renders/<Title>.mp4`: the final, named after the title you pick (`renders/<name>-final.mp4` until then)
- `renders/youtube-description.txt`: the description (Ryan's setup only)
- `shorts/01 - <Title>.mp4` and so on: the shorts
- `shorts/shorts-descriptions.txt`: their titles and descriptions

The preview and waveform go in `~/Library/Caches/stream-trim/`, never in your recording's folder. The page's Streams tab lists every stream you've worked on, with how much cache space each one uses. Deleting a cache folder is safe.
