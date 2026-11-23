"""Render the final video: frame-accurate In/Out on the raw OBS file, 4K
H.264, the stream-trim mix and voice chain, two-pass loudness on the whole
mix. Writes <name>-final.mp4 next to the recording, never over an existing one."""
import os
import subprocess
import tempfile

import audio_chain
import measure

VIDEO = ["-c:v", "h264_videotoolbox", "-b:v", "5M", "-tag:v", "avc1"]
AUDIO = ["-c:a", "aac", "-b:a", "320k", "-ar", "48000"]


def final_path(raw):
    stem, _ = os.path.splitext(raw)
    return f"{stem}-final.mp4"


def parse_progress(line, total_s):
    key, _, value = line.strip().partition("=")
    if key != "out_time_us" or not value.isdigit() or total_s <= 0:
        return None
    return min(100.0, int(value) / 1e6 / total_s * 100)


def _run(args, total_s, phase, progress, stop):
    """Run ffmpeg with -progress, report percent, kill it if stop is set.
    Returns stderr."""
    with tempfile.TemporaryFile(mode="w+") as err:
        p = subprocess.Popen(["ffmpeg", "-nostdin", "-hide_banner", "-nostats",
                              "-progress", "pipe:1", *args],
                             stdout=subprocess.PIPE, stderr=err, text=True)
        if progress:
            progress(0.0, phase)
        for line in p.stdout:
            if stop is not None and stop.is_set():
                p.kill()
                break
            pct = parse_progress(line, total_s)
            if pct is not None and progress:
                progress(pct, phase)
        p.wait()
        err.seek(0)
        stderr = err.read()
    if stop is not None and stop.is_set():
        raise RuntimeError("stopped")
    if p.returncode != 0:
        tail = "\n".join(stderr.strip().splitlines()[-20:])
        raise RuntimeError(f"ffmpeg failed:\n{tail}")
    return stderr


def render_final(raw, in_s, out_s, chain, progress=None, stop=None):
    out = final_path(raw)
    if os.path.exists(out):
        raise FileExistsError(f"{out} already exists")
    tracks, duration, fps = audio_chain.probe(raw)
    if tracks != 6:
        raise ValueError(f"expected 6 audio tracks, found {tracks}")
    if not (0 <= in_s < out_s <= duration):
        raise ValueError(f"bad In/Out {in_s}/{out_s} for a {duration:.2f} s recording")

    # Snap to the frame grid. With -ss on the input, audio starts exactly at
    # in_s but video at the next frame, so an off-grid In would put the
    # video up to a frame early against the audio.
    in_s = round(in_s * fps) / fps
    out_s = min(duration, round(out_s * fps) / fps)
    if out_s <= in_s:
        raise ValueError(f"In/Out {in_s}/{out_s} are less than a frame apart")

    graph, shift = audio_chain.mix_graph(chain, fps)
    length = out_s - in_s
    graph += f";[mix]atrim=duration={length}[cut]"
    # The mic needs `shift` more seconds of input than the cut, but never
    # past the end of the file.
    src = ["-ss", str(in_s), "-t", str(min(length + shift, duration - in_s)), "-i", raw]

    first = measure.parse_loudnorm(_run(
        src + ["-vn", "-filter_complex",
               graph + f";[cut]loudnorm={audio_chain.loudness_target(chain)}:print_format=json[a]",
               "-map", "[a]", "-f", "null", "-"], length, "measuring", progress, stop))

    partial = out.replace("-final.mp4", "-final.partial.mp4")
    try:
        _run(src + ["-filter_complex",
                    graph + f";[cut]{audio_chain.second_pass(chain, first)},atrim=duration={length}[a]"
                    f";[0:v]trim=duration={length},setpts=PTS-STARTPTS[v]",
                    "-map", "[v]", "-map", "[a]", *VIDEO, *AUDIO,
                    "-movflags", "+faststart", "-y", partial],
             length, "encoding", progress, stop)
        if stop is not None and stop.is_set():
            raise RuntimeError("stopped")
        os.replace(partial, out)
    finally:
        if os.path.exists(partial):
            os.remove(partial)
    return out
