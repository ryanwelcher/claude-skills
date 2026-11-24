"""Render a short's audio: the stream-trim mix and voice chain, two-pass
loudness at the shorts level, to a WAV that stream-shorts' render-short.sh
uses in place of the mic track (its --mix-audio flag).

  python3 short_audio.py <raw.mp4> <video_start_s> <seconds> <out.wav>

video_start_s is on the video clock, the time render-short.sh cuts the video at."""
import copy
import os
import sys

import audio_chain

HERE = os.path.dirname(os.path.abspath(__file__))
# Shorts, Reels and TikTok play at about -14 LUFS; stream-shorts used the same.
SHORTS_LOUDNESS = {"I": -14, "TP": -1.5}


def shorts_chain(chain):
    out = copy.deepcopy(chain)
    out["loudness"].update(SHORTS_LOUDNESS)
    return out


def main(argv):
    if len(argv) != 4:
        raise ValueError("usage: short_audio.py <raw.mp4> <video_start_s> <seconds> <out.wav>")
    raw, start, seconds, out = argv[0], float(argv[1]), float(argv[2]), argv[3]
    chain = audio_chain.load_chain(os.path.join(HERE, "chain.json"))
    audio_chain.render_stretch(raw, start, seconds, shorts_chain(chain), out)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:  # one clear line for render-short.sh to pass on
        print(f"ERROR: {str(e).strip().splitlines()[-1] if str(e).strip() else type(e).__name__}",
              file=sys.stderr)
        sys.exit(1)
