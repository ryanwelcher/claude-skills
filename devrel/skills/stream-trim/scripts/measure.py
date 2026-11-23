"""Loudness and tone measurements of an audio file, using only ffmpeg."""
import json
import re
import subprocess

# Octave band centres (Hz) used to compare the tone of two files.
BANDS = [63, 125, 250, 500, 1000, 2000, 4000, 8000]


def run_ffmpeg(args):
    """Run ffmpeg with argv `args` and return its stderr. Raise RuntimeError
    with the last 20 lines of stderr if it fails."""
    p = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-nostats"] + args,
                       capture_output=True, text=True)
    if p.returncode != 0:
        tail = "\n".join(p.stderr.strip().splitlines()[-20:])
        raise RuntimeError(f"ffmpeg failed:\n{tail}")
    return p.stderr


def parse_ebur128(stderr):
    """I, LRA and TP from the Summary block of ffmpeg's ebur128 filter."""
    summary = stderr[stderr.rindex("Summary:"):]

    def grab(label):
        return float(re.search(label + r":\s+(-?[\d.]+|-inf)", summary).group(1))

    return {"I": grab("I"), "LRA": grab("LRA"), "TP": grab("Peak")}


def parse_loudnorm(stderr):
    """The JSON block that loudnorm prints with print_format=json."""
    start = stderr.rindex("{")
    end = stderr.index("}", start) + 1
    return json.loads(stderr[start:end])


def band_rms(path, hz):
    err = run_ffmpeg(["-i", path, "-af",
                      f"bandpass=f={hz}:width_type=o:w=1,"
                      "astats=measure_overall=RMS_level:measure_perchannel=none",
                      "-f", "null", "-"])
    return float(re.findall(r"RMS level dB:\s+(-?[\d.]+|-inf)", err)[-1])


def measure(path):
    """Loudness (I, LRA, TP) plus RMS dB per octave band for `path`."""
    result = parse_ebur128(run_ffmpeg(["-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"]))
    result["bands"] = {hz: band_rms(path, hz) for hz in BANDS}
    return result
