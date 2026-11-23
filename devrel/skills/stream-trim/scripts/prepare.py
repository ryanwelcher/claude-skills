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


def prepare(raw, chain, progress=None):
    """Write proxy.mp4, peaks.json and analysis.json for `raw`, and return
    the analysis. Cached: a second call just reads analysis.json."""
    out = cache_dir(raw)
    analysis_path = os.path.join(out, "analysis.json")
    if os.path.exists(analysis_path):
        with open(analysis_path) as f:
            return json.load(f)

    tracks, duration, fps = audio_chain.probe(raw)
    if tracks != 6:
        raise ValueError(f"expected 6 audio tracks, found {tracks}")
    os.makedirs(out, exist_ok=True)
    graph, shift = audio_chain.mix_graph(chain, fps)
    mic = audio_chain.TRACKS["mic"] - 1
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
                "silences": silences, **defaults(silences, duration)}
    with open(analysis_path, "w") as f:
        json.dump(analysis, f, indent=2)
    with open(analysis_path) as f:
        return json.load(f)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: prepare.py <raw.mp4>")
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        a = prepare(sys.argv[1], audio_chain.load_chain(os.path.join(here, "chain.json")))
    except (ValueError, RuntimeError, OSError) as e:
        sys.exit(f"ERROR: {e}")
    print(f"In {a['in']:.2f} s, Out {a['out']:.2f} s, duration {a['duration']:.2f} s")
    print(f"CACHE {cache_dir(sys.argv[1])}")
