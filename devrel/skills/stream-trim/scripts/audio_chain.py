"""Build the stream-trim audio: the voice chain that stands in for Premiere's
Podcast Voice, and the mix of the kept OBS tracks. Everything comes from one
settings file (chain.json) so the final render, the preview proxy and the
shorts all sound the same."""
import json

# OBS track numbers (1-based) for each role in the final mix.
TRACKS = {"mic": 2, "guest": 3, "theme": 5, "firebot": 6}
ROLES = ("mic", "guest", "theme", "firebot")
VOICE_ROLES = ("mic", "guest")
OUT_FORMAT = "aformat=sample_rates=48000:channel_layouts=stereo"


def load_chain(path):
    with open(path) as f:
        return json.load(f)


def _num(x):
    """Format a number the way ffmpeg arguments are written here: no
    trailing .0 on whole numbers."""
    return str(int(x)) if float(x).is_integer() else str(x)


def voice_filters(chain):
    """Comma-joined filters for one voice track, without labels."""
    c = chain["compand"]
    points = "|".join(f"{_num(i)}/{_num(o)}" for i, o in c["points"])
    d = chain["deesser"]
    filters = [
        f"highpass=f={_num(chain['rumble_hz'])}",
        f"compand=attacks={_num(c['attacks'])}:decays={_num(c['decays'])}:points={points}",
        f"deesser=i={_num(d['i'])}:m={_num(d['m'])}:f={_num(d['f'])}",
    ]
    # One octave wide (Q 1.41) peaking band per graphic EQ setting.
    for hz, db in chain["eq_db"].items():
        filters.append(f"equalizer=f={hz}:t=q:w=1.41:g={_num(db)}")
    p = chain["presence"]
    if p["db"] != 0:
        filters.append(f"equalizer=f={_num(p['hz'])}:t=q:w={_num(p['q'])}:g={_num(p['db'])}")
    return ",".join(filters)


def build_filtergraph(chain, inputs, mic_shift_s):
    """A -filter_complex string that mixes the four roles into [mix].
    inputs maps role -> ffmpeg stream spec (e.g. "0:a:1"). The mic is
    trimmed by mic_shift_s to undo OBS's lag. Loudness is left to the
    caller, since it needs two passes."""
    voice = voice_filters(chain)
    levels = chain["levels_db"]
    branches = []
    for role in ROLES:
        f = []
        if role == "mic":
            f.append(f"atrim=start={mic_shift_s},asetpts=PTS-STARTPTS")
            gain = chain["mic_gain_db"]
        else:
            gain = levels[role]
        if gain != 0:
            f.append(f"volume={_num(gain)}dB")
        if role in VOICE_ROLES:
            f.append(voice)
        f.append(OUT_FORMAT)
        branches.append(f"[{inputs[role]}]{','.join(f)}[{role}]")
    labels = "".join(f"[{r}]" for r in ROLES)
    branches.append(f"{labels}amix=inputs={len(ROLES)}:normalize=0[mix]")
    return ";".join(branches)
