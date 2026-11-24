#!/usr/bin/env python3
"""Profiles: one file per recording setup (which OBS tracks to keep and what
they are, how late the mic runs, the voice chain, loudness, caption font,
short layouts, whether Claude's voice pass runs).

Built-in profiles live in ../profiles (ryan-obs is Ryan's). Personal ones
live in ~/.config/stream-trim/profiles/<name>.json and win over a built-in
with the same name. ~/.config/stream-trim/default names this machine's
default; with no such file there is no default.

  profiles.py check <raw> [--profile NAME]    PROFILE <name>, or ERROR: ... and exit 1
  profiles.py samples <raw> <outdir> [--at S] 5 s of each audio track, track-N.wav
  profiles.py set-default <name>
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILTIN = os.path.normpath(os.path.join(HERE, "..", "profiles"))
REQUIRED = ("name", "audio_tracks", "tracks", "mic", "mic_lag_frames", "transcript_lag_frames",
            "chain", "shorts_loudness", "caption_font", "voice_pass")


class ProfileError(ValueError):
    pass


class NoDefault(ProfileError):
    pass


def config_dir():
    return os.environ.get("STREAM_TRIM_CONFIG") or os.path.expanduser("~/.config/stream-trim")


def default_name():
    try:
        with open(os.path.join(config_dir(), "default")) as f:
            return f.read().strip() or None
    except FileNotFoundError:
        return None


def find(name):
    for d in (os.path.join(config_dir(), "profiles"), BUILTIN):
        path = os.path.join(d, name + ".json")
        if os.path.exists(path):
            return path
    raise ProfileError(f"no profile named {name} (looked in {os.path.join(config_dir(), 'profiles')} and {BUILTIN})")


def load(name=None):
    if name is None:
        name = default_name()
        if name is None:
            raise NoDefault(f"no default profile on this machine ({os.path.join(config_dir(), 'default')} is missing)")
    path = find(name)
    try:
        with open(path) as f:
            p = json.load(f)
    except ValueError as e:
        raise ProfileError(f"{path} is not valid JSON: {e}")
    where = os.path.dirname(path)

    def bad(msg):
        return ProfileError(f"{path}: {msg}")

    if not isinstance(p, dict):
        raise bad("expected a JSON object")
    for key in REQUIRED:
        if key not in p:
            raise bad(f'missing "{key}"')
    n = p["audio_tracks"]
    if not isinstance(n, int) or n < 1:
        raise bad('"audio_tracks" must be a whole number of tracks')
    tracks = p["tracks"]
    if not isinstance(tracks, dict) or not tracks:
        raise bad('"tracks" must list at least one track')
    seen = set()
    for key, t in tracks.items():
        if not key.isdigit() or not 1 <= int(key) <= n:
            raise bad(f"track {key} is not between 1 and {n}")
        if not isinstance(t, dict) or not t.get("role"):
            raise bad(f"track {key} needs a \"role\"")
        if t["role"] in seen:
            raise bad(f"role {t['role']} is used twice")
        seen.add(t["role"])
    mic = tracks.get(str(p["mic"]))
    if mic is None or not mic.get("voice"):
        raise bad(f'"mic" must name a kept track with "voice": true')
    p["path"] = path
    p["chain_path"] = os.path.normpath(os.path.join(where, p["chain"]))
    try:
        with open(p["chain_path"]) as f:
            p["chain"] = json.load(f)
    except (OSError, ValueError) as e:
        raise bad(f"can't read its chain file {p['chain_path']}: {e}")
    extra = set(p["chain"].get("levels_db", {})) - seen
    if extra:
        raise bad(f"its chain sets levels for {', '.join(sorted(extra))}, which no track has as a role")
    layouts = p.get("layouts")
    p["layouts_path"] = os.path.normpath(os.path.join(where, layouts)) if layouts else None
    return p


def roles(p):
    """(role, OBS track number) for each kept track, in track order."""
    return sorted(((t["role"], int(k)) for k, t in p["tracks"].items()), key=lambda r: r[1])


def voice_roles(p):
    return {t["role"] for t in p["tracks"].values() if t.get("voice")}


def mic_role(p):
    return p["tracks"][str(p["mic"])]["role"]


def mic_index(p):
    """The mic's 0-based audio stream index, as in ffmpeg's 0:a:N."""
    return int(p["mic"]) - 1


def mic_shift(p, fps):
    return round(p["mic_lag_frames"] / fps, 6)


def transcript_shift(p, fps):
    return round(p["transcript_lag_frames"] / fps, 6)


def check_recording(p, tracks):
    if tracks != p["audio_tracks"]:
        raise ProfileError(f"this recording has {tracks} audio tracks; "
                           f"profile {p['name']} expects {p['audio_tracks']}")


def samples(raw, outdir, at=None):
    import audio_chain

    tracks, duration, _ = audio_chain.probe(raw, video=False)
    at = duration * 0.1 if at is None else at
    os.makedirs(outdir, exist_ok=True)
    paths = []
    for i in range(tracks):
        path = os.path.join(outdir, f"track-{i + 1}.wav")
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", str(at), "-t", "5",
                        "-i", raw, "-map", f"0:a:{i}", path], check=True)
        paths.append(path)
    return paths


def main(argv):
    import audio_chain

    if len(argv) >= 2 and argv[0] == "check":
        name = argv[argv.index("--profile") + 1] if "--profile" in argv else None
        try:
            p = load(name)
        except NoDefault as e:
            print(f"ERROR: NO_DEFAULT {e}", file=sys.stderr)
            return 1
        check_recording(p, audio_chain.probe(argv[1], video=False)[0])
        print(f"PROFILE {p['name']}")
    elif len(argv) >= 3 and argv[0] == "samples":
        at = float(argv[argv.index("--at") + 1]) if "--at" in argv else None
        for path in samples(argv[1], argv[2], at):
            print(path)
    elif len(argv) == 2 and argv[0] == "set-default":
        load(argv[1])
        os.makedirs(config_dir(), exist_ok=True)
        with open(os.path.join(config_dir(), "default"), "w") as f:
            f.write(argv[1] + "\n")
        print(f"DEFAULT {argv[1]}")
    else:
        print(__doc__.split("\n\n")[-1], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except (ProfileError, OSError, subprocess.CalledProcessError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
