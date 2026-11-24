"""Build the stream-trim audio: the voice chain that stands in for Premiere's
Podcast Voice, and the mix of the kept OBS tracks. Everything comes from one
settings file (the profile's chain) so the final render, the preview proxy
and the shorts all sound the same. Which tracks go in, and what they are,
comes from the profile (profiles.py)."""
import copy
import json

import profiles

OUT_FORMAT = "aformat=sample_rates=48000:channel_layouts=stereo"


def load_chain(path):
    with open(path) as f:
        return json.load(f)


def _num(x):
    """Format a number the way ffmpeg arguments are written here: no
    trailing .0 on whole numbers."""
    return str(int(x)) if float(x).is_integer() else str(x)


def voice_filters(chain):
    """Comma-joined filters for one voice track, without labels. A step set
    to null (or a 0 Hz highpass, or no EQ bands) is left out, so a plain
    chain gives an empty string."""
    filters = []
    if chain["rumble_hz"]:
        filters.append(f"highpass=f={_num(chain['rumble_hz'])}")
    c = chain["compand"]
    if c is not None:
        points = "|".join(f"{_num(i)}/{_num(o)}" for i, o in c["points"])
        filters.append(f"compand=attacks={_num(c['attacks'])}:decays={_num(c['decays'])}:points={points}")
    d = chain["deesser"]
    if d is not None:
        filters.append(f"deesser=i={_num(d['i'])}:m={_num(d['m'])}:f={_num(d['f'])}")
    # One octave wide (Q 1.41) peaking band per graphic EQ setting.
    for hz, db in chain["eq_db"].items():
        filters.append(f"equalizer=f={hz}:t=q:w=1.41:g={_num(db)}")
    p = chain["presence"]
    if p is not None and p["db"] != 0:
        filters.append(f"equalizer=f={_num(p['hz'])}:t=q:w={_num(p['q'])}:g={_num(p['db'])}")
    return ",".join(filters)


def build_filtergraph(chain, inputs, mic_shift_s, voice_roles, mic_role):
    """A -filter_complex string that mixes every role in `inputs` into
    [mix], in the dict's order. inputs maps role -> ffmpeg stream spec (e.g.
    "0:a:1"). The mic role is trimmed by mic_shift_s to undo OBS's lag and
    gets mic_gain_db; other roles get their levels_db entry (0 dB if none).
    Voice roles get the voice chain. Loudness is left to the caller, since
    it needs two passes."""
    voice = voice_filters(chain)
    levels = chain["levels_db"]
    branches = []
    for role in inputs:
        f = []
        if role == mic_role:
            f.append(f"atrim=start={mic_shift_s},asetpts=PTS-STARTPTS")
            gain = chain["mic_gain_db"]
        else:
            gain = levels.get(role, 0)
        if gain != 0:
            f.append(f"volume={_num(gain)}dB")
        if role in voice_roles and voice:
            f.append(voice)
        f.append(OUT_FORMAT)
        branches.append(f"[{inputs[role]}]{','.join(f)}[{role}]")
    labels = "".join(f"[{r}]" for r in inputs)
    branches.append(f"{labels}amix=inputs={len(inputs)}:normalize=0[mix]")
    return ";".join(branches)


def probe(path, video=True):
    """(audio track count, duration in s, fps) of a media file. fps is None
    when video is False."""
    import subprocess

    def ff(*args):
        return subprocess.run(["ffprobe", "-v", "error", *args, path],
                              capture_output=True, text=True, check=True).stdout.split()

    tracks = len(ff("-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0"))
    duration = float(ff("-show_entries", "format=duration", "-of", "csv=p=0")[0])
    if not video:
        return tracks, duration, None
    num, _, den = ff("-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                     "-of", "csv=p=0")[0].partition("/")
    return tracks, duration, float(num) / float(den or 1)


def mix_graph(profile, fps):
    """(filtergraph ending in [mix] for a raw OBS file, mic shift in s)."""
    shift = profiles.mic_shift(profile, fps)
    inputs = {role: f"0:a:{track - 1}" for role, track in profiles.roles(profile)}
    graph = build_filtergraph(profile["chain"], inputs, shift, profiles.voice_roles(profile),
                              profiles.mic_role(profile))
    return graph, shift


def loudness_target(chain):
    L = chain["loudness"]
    return f"I={L['I']}:TP={L['TP']}:LRA={L['LRA']}"


def second_pass(chain, first):
    """The pass-2 loudnorm filter, from pass 1's printed measurements."""
    return (f"loudnorm={loudness_target(chain)}:measured_I={first['input_i']}"
            f":measured_TP={first['input_tp']}:measured_LRA={first['input_lra']}"
            f":measured_thresh={first['input_thresh']}:offset={first['target_offset']}"
            ":linear=true,aresample=48000")


def render_stretch(raw, start_s, seconds, profile, out_wav, loudness=None):
    """Render `seconds` of the final mix from the raw OBS file, starting at
    raw time `start_s` (video clock), through the voice chain and two-pass
    loudness, to a 48 kHz 24-bit stereo WAV. `loudness` overrides keys of the
    chain's loudness target (the shorts use their own)."""
    import measure

    tracks, duration, fps = probe(raw)
    profiles.check_recording(profile, tracks)
    chain = profile["chain"]
    if loudness:
        chain = copy.deepcopy(chain)
        chain["loudness"].update(loudness)
    shift = profiles.mic_shift(profile, fps)
    if start_s < 0 or seconds <= 0:
        raise ValueError(f"bad stretch: start {start_s}, length {seconds}")
    if start_s + seconds + shift > duration:
        raise ValueError(f"stretch {start_s}+{seconds} s runs past the end ({duration:.2f} s)")

    graph, _ = mix_graph(profile, fps)
    graph += f";[mix]atrim=duration={seconds}[cut]"
    target = loudness_target(chain)
    src = ["-ss", str(start_s), "-t", str(seconds + shift), "-i", raw]

    first = measure.parse_loudnorm(measure.run_ffmpeg(
        src + ["-filter_complex", graph + f";[cut]loudnorm={target}:print_format=json[out]",
               "-map", "[out]", "-f", "null", "-"]))
    second = second_pass(chain, first)
    measure.run_ffmpeg(src + ["-filter_complex", graph + f";[cut]{second}[out]",
                              "-map", "[out]", "-c:a", "pcm_s24le", "-y", out_wav])
