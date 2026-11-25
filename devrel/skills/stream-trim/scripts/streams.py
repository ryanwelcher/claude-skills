"""Every recording stream-trim has a cache for, newest first, and what's been
made from it: the final, the shorts, the full video's description. The page's
Streams tab lists these, and Show in Finder opens them.

Built from the caches alone (analysis.json names the raw), so there's
nothing extra to keep in step.
"""
import json
import os

import profiles

TARGETS = ("raw", "final", "shorts", "description")


def default_root():
    return os.path.expanduser("~/Library/Caches/stream-trim")


def _json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _final(raw, edit):
    import render

    for path in ((edit or {}).get("output"), render.final_path(raw)):
        if path and os.path.exists(path):
            return path
    return None


def _shorts(folder):
    manifest = _json(os.path.join(folder, "shorts", "shorts.json"))
    if not isinstance(manifest, dict):
        return None
    clips = [c for c in manifest.get("clips", []) if isinstance(c, dict) and c.get("file")]
    rendered = sum(os.path.exists(os.path.join(folder, "shorts", c["file"])) for c in clips)
    return {"picked": len(clips), "rendered": rendered}


def _stream(cache):
    analysis = _json(os.path.join(cache, "analysis.json"))
    if not isinstance(analysis, dict) or not analysis.get("raw"):
        return None
    raw = analysis["raw"]
    folder = os.path.dirname(raw)
    files = [os.path.join(cache, f) for f in os.listdir(cache)]
    size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(cache) for f in fs)
    exists = os.path.exists(raw)
    description = os.path.join(folder, "renders", "youtube-description.txt")
    return {
        "id": os.path.basename(cache),
        "raw": raw,
        "name": os.path.basename(raw),
        "folder": folder,
        "profile": analysis.get("profile", "ryan-obs"),
        "state": "missing" if not exists else "cloud-only" if profiles.cloud_only(raw) else "local",
        "final": _final(raw, _json(os.path.join(cache, "edit.json"))) if exists else None,
        "shorts": _shorts(folder) if exists else None,
        "description": description if exists and os.path.exists(description) else None,
        "cache_bytes": size,
        "last_used": max(os.path.getmtime(f) for f in files),
    }


def list_streams(root=None):
    root = root or default_root()
    try:
        names = sorted(os.listdir(root))
    except FileNotFoundError:
        return []
    out = [s for s in (_stream(os.path.join(root, n)) for n in names if os.path.isdir(os.path.join(root, n))) if s]
    return sorted(out, key=lambda s: s["last_used"], reverse=True)


def reveal_target(stream, target):
    """The `open` command that shows one of a stream's items in Finder, or
    None when it doesn't exist. Folders open; files are selected in theirs."""
    if target not in TARGETS:
        raise ValueError(f"target must be one of {', '.join(TARGETS)}")
    if target == "shorts":
        path = os.path.join(stream["folder"], "shorts")
        return ["open", path] if stream["state"] != "missing" and os.path.isdir(path) else None
    path = stream["raw"] if target == "raw" else stream[target]
    return ["open", "-R", path] if path and os.path.exists(path) else None
