"""Render a short's audio: the stream-trim mix and voice chain, two-pass
loudness at the shorts level, to a WAV that stream-shorts' render-short.sh
uses in place of the mic track (its --mix-audio flag).

  python3 short_audio.py <raw.mp4> <video_start_s> <seconds> <out.wav>

video_start_s is on the video clock, the time render-short.sh cuts the video at.
The profile is $STREAM_TRIM_PROFILE, or this machine's default; its
shorts_loudness sets the level (Ryan's: -14 LUFS, where Shorts, Reels and
TikTok play)."""
import os
import sys

import audio_chain
import profiles


def main(argv):
    if len(argv) != 4:
        raise ValueError("usage: short_audio.py <raw.mp4> <video_start_s> <seconds> <out.wav>")
    raw, start, seconds, out = argv[0], float(argv[1]), float(argv[2]), argv[3]
    p = profiles.load(os.environ.get("STREAM_TRIM_PROFILE") or None)
    audio_chain.render_stretch(raw, start, seconds, p, out, loudness=p["shorts_loudness"])


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:  # one clear line for render-short.sh to pass on
        print(f"ERROR: {str(e).strip().splitlines()[-1] if str(e).strip() else type(e).__name__}",
              file=sys.stderr)
        sys.exit(1)
