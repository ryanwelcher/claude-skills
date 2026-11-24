"""Shorts view logic for the stream-trim server: which candidate clips sit
inside the final edit, and how Ryan's picks merge into shorts/shorts.json.

Clip start/end are on the transcript clock (the mic clock, `shift` seconds
late). render-short.sh pads a clip PAD_BEFORE before start and PAD_AFTER
after end, and cuts the video `shift` earlier."""
import json

PAD_BEFORE = 0.2
PAD_AFTER = 0.4


def to_secs(t):
    if isinstance(t, (int, float)) and not isinstance(t, bool):
        return float(t)
    total = 0.0
    for part in str(t).split(":"):
        total = total * 60 + float(part)
    return total


def fmt(t):
    h, rest = divmod(round(t * 100), 360000)
    m, rest = divmod(rest, 6000)
    return f"{h:02d}:{m:02d}:{rest // 100:02d}.{rest % 100:02d}"


def number(clip):
    head = str(clip.get("file", "")).split("-", 1)[0]
    return int(head) if head.isdigit() else None


def video_span(clip, shift):
    return (to_secs(clip["start"]) - PAD_BEFORE - shift, to_secs(clip["end"]) + PAD_AFTER - shift)


def inside(clip, edit, shift):
    start, end = video_span(clip, shift)
    return edit["in"] <= start and end <= edit["out"]


def load_candidates(path, edit, shift):
    try:
        with open(path) as f:
            data = json.load(f)
    except ValueError as e:
        raise ValueError(f"{path}: {e}")
    if not isinstance(data, dict) or not isinstance(data.get("clips"), list):
        raise ValueError(f"{path} needs a \"clips\" list")
    out = []
    for c in data["clips"]:
        if not isinstance(c, dict) or any(k not in c for k in ("file", "start", "end")):
            raise ValueError(f"a candidate needs file, start and end: {json.dumps(c)}")
        n = number(c)
        if n is None:
            raise ValueError(f"candidate file needs an NN- prefix: {c['file']}")
        start, end = to_secs(c["start"]), to_secs(c["end"])
        out.append({**c, "n": n, "inside": inside(c, edit, shift),
                    "edit_start": start - shift - edit["in"], "edit_end": end - shift - edit["in"]})
    return out


def profile_fields(profile):
    """The profile's recording setup, as stream-shorts' shorts.json fields."""
    out = {"profile": profile["name"], "mic_track": int(profile["mic"]), "mic_lag_frames": profile["mic_lag_frames"],
           "transcript_lag_frames": profile["transcript_lag_frames"],
           "caption_font": profile["caption_font"]}
    if profile.get("layouts_path"):
        out["layouts"] = profile["layouts_path"]
    return out


def merge_picks(existing, recording, words, mix_audio, picks, profile):
    if isinstance(existing, list):
        existing = {"clips": existing}
    kept = [c for c in (existing or {}).get("clips", [])
            if c.get("file") not in {p["file"] for p in picks}]
    clips = sorted(kept + list(picks), key=lambda c: (number(c) is None, number(c) or 0))
    existing = {k: v for k, v in (existing or {}).items() if k != "layouts"}
    return {**existing, "recording": recording, "words": words,
            "mix_audio": mix_audio, **profile_fields(profile), "clips": clips}
