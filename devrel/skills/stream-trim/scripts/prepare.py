"""Prepare a raw OBS recording for the trim page, in one ffmpeg pass:
a 720p preview with the final mix, mic waveform peaks, mic silences, and
the default In/Out. Results are cached per recording, so reruns are instant.

  python3 prepare.py <raw.mp4>     prints: CACHE <dir>"""
import array
import hashlib
import json
import os
import re
import subprocess
import sys
import threading

import audio_chain
import profiles

LEAD_IN = 0.5   # s before the first word
TAIL = 1.0      # s after the last word
INTRO_MIN = 60  # the opening silence must last this long to count as Starting Soon
PEAK_RATE = 8000  # Hz the mic is resampled to for peaks; keeps the voice band (up to 4 kHz)
PER_S = 20      # waveform buckets per second
END_SLACK = 1.0  # s; a silence ending this close to the end counts as closing
SILENCE = "silencedetect=noise=-45dB:d=2"


def cache_dir(raw):
    st = os.stat(raw)
    key = f"{os.path.realpath(raw)}|{st.st_size}|{st.st_mtime}"
    digest = hashlib.sha1(key.encode()).hexdigest()[:16]
    return os.path.expanduser(f"~/Library/Caches/stream-trim/{digest}")


def parse_silences(stderr, duration):
    """[(start, end), ...] from silencedetect output; an unclosed silence
    runs to `duration`."""
    silences, start = [], None
    for kind, value in re.findall(r"silence_(start|end): (-?[\d.]+)", stderr):
        t = float(value)
        t = int(t) if t.is_integer() else t
        if kind == "start":
            start = max(0, t)
        elif start is not None:
            silences.append((start, t))
            start = None
    if start is not None:
        silences.append((start, int(duration) if float(duration).is_integer() else duration))
    return silences


def defaults(silences, duration):
    if silences and silences[0][0] <= 0 and silences[0][1] >= duration - END_SLACK:
        # The mic is silent the whole way (muted?): nothing to go on.
        return {"voice_start": 0, "voice_end": duration, "in": 0, "out": duration}
    voice_start = 0
    if silences and silences[0][0] <= 0 and silences[0][1] >= INTRO_MIN:
        voice_start = silences[0][1]
    voice_end = duration
    # The mic stream ends `shift` early, so a closing silence may stop just short.
    if silences and silences[-1][1] >= duration - END_SLACK and silences[-1][0] > voice_start:
        voice_end = silences[-1][0]
    return {"voice_start": voice_start, "voice_end": voice_end,
            "in": max(0, voice_start - LEAD_IN) if voice_start else 0,
            "out": min(duration, voice_end + TAIL)}


def peaks_from_pcm(pcm, rate, per_s):
    samples = array.array("h")
    samples.frombytes(pcm[: len(pcm) // 2 * 2])
    size = rate // per_s
    peaks = []
    for i in range(0, len(samples), size):
        chunk = samples[i:i + size]
        peaks.append(round(min(32767, max(max(chunk), -min(chunk))) / 32767, 4))
    return peaks


def prepare(raw, profile, progress=None):
    """Write proxy.mp4, peaks.json and analysis.json for `raw`, and return
    the analysis. Cached: a second call with the same profile, unedited,
    just reads analysis.json. A cache from before profiles has no "profile"
    and was made with Ryan's setup, so it counts as ryan-obs."""
    out = cache_dir(raw)
    analysis_path = os.path.join(out, "analysis.json")
    if os.path.exists(analysis_path):
        with open(analysis_path) as f:
            cached = json.load(f)
        same = cached.get("profile", "ryan-obs") == profile["name"]
        if same and cached.get("profile_key", profiles.cache_key(profile)) == profiles.cache_key(profile):
            return cached

    tracks, duration, fps = audio_chain.probe(raw)
    profiles.check_recording(profile, tracks)
    os.makedirs(out, exist_ok=True)
    chain = profile["chain"]
    graph, shift = audio_chain.mix_graph(profile, fps)
    mic = profiles.mic_index(profile)
    graph += (f";[0:a:{mic}]atrim=start={shift},asetpts=PTS-STARTPTS,asplit[m1][m2]"
              f";[m1]{SILENCE},anullsink"
              f";[m2]aresample={PEAK_RATE},aformat=sample_fmts=s16:channel_layouts=mono[pk]"
              f";[mix]loudnorm={audio_chain.loudness_target(chain)},aresample=48000[pa]"
              ";[0:v]scale=-2:720[pv]")
    partial = os.path.join(out, "proxy.partial.mp4")
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-y", "-i", raw, "-filter_complex", graph,
           "-map", "[pv]", "-map", "[pa]", "-c:v", "h264_videotoolbox", "-b:v", "2M",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", partial,
           "-map", "[pk]", "-f", "s16le", "pipe:1"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    err_lines = []

    def read_stderr():
        for line in iter(p.stderr.readline, b""):
            text = line.decode(errors="replace")
            err_lines.append(text)
            m = re.search(r"time=(\d+):(\d+):([\d.]+)", text)
            if progress and m:
                h, mi, s = m.groups()
                progress(min(100.0, 100 * (int(h) * 3600 + int(mi) * 60 + float(s)) / duration))

    reader = threading.Thread(target=read_stderr, daemon=True)
    reader.start()
    pcm = p.stdout.read()
    p.wait()
    reader.join()
    stderr = "".join(err_lines)
    if p.returncode != 0:
        if os.path.exists(partial):
            os.remove(partial)
        tail = "\n".join(stderr.strip().splitlines()[-20:])
        raise RuntimeError(f"ffmpeg failed:\n{tail}")
    os.replace(partial, os.path.join(out, "proxy.mp4"))

    with open(os.path.join(out, "peaks.json"), "w") as f:
        json.dump({"per_s": PER_S, "peaks": peaks_from_pcm(pcm, PEAK_RATE, PER_S)}, f)
    silences = parse_silences(stderr, duration)
    analysis = {"raw": os.path.realpath(raw), "duration": duration, "fps": fps,
                "silences": silences, **defaults(silences, duration), "profile": profile["name"],
                "profile_key": profiles.cache_key(profile)}
    with open(analysis_path, "w") as f:
        json.dump(analysis, f, indent=2)
    with open(analysis_path) as f:
        return json.load(f)


if __name__ == "__main__":
    args = sys.argv[1:]
    name = None
    if "--profile" in args:
        i = args.index("--profile")
        name = args[i + 1] if i + 1 < len(args) else ""
        del args[i:i + 2]
    if len(args) != 1 or name == "":
        sys.exit("usage: prepare.py <raw.mp4> [--profile NAME]")
    try:
        a = prepare(args[0], profiles.load(name))
    except (ValueError, RuntimeError, OSError) as e:
        sys.exit(f"ERROR: {e}")
    print(f"In {a['in']:.2f} s, Out {a['out']:.2f} s, duration {a['duration']:.2f} s")
    print(f"CACHE {cache_dir(args[0])}")
