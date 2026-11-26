"""Apple Vision for thumbnails: face boxes with a quality score, and a cutout
of one person. The work is in vision.swift, compiled once with swiftc and
cached in ~/Library/Caches/stream-trim/ under a hash of its source.

Boxes are [x, y, w, h] in pixels, top-left origin."""
import hashlib
import json
import os
import shutil
import subprocess
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "vision.swift")
CACHE = os.path.expanduser("~/Library/Caches/stream-trim")


class VisionError(Exception):
    pass


def binary():
    with open(SOURCE, "rb") as f:
        path = os.path.join(CACHE, "vision-" + hashlib.sha1(f.read()).hexdigest()[:12])
    if os.path.exists(path):
        return path
    if not shutil.which("swiftc"):
        raise VisionError("thumbnails need the Xcode command-line tools: run xcode-select --install")
    os.makedirs(CACHE, exist_ok=True)
    tmp = path + ".tmp"
    r = subprocess.run(["swiftc", "-O", "-o", tmp, SOURCE], capture_output=True, text=True)
    if r.returncode:
        raise VisionError("couldn't build the Vision helper: " + (r.stderr.strip().splitlines() or ["?"])[-1])
    os.replace(tmp, path)
    return path


def _run(args):
    r = subprocess.run([binary(), *args], capture_output=True, text=True)
    if r.returncode:
        raise VisionError((r.stderr.strip() or "Vision helper failed").removeprefix("ERROR: "))
    return r.stdout


def faces(paths):
    """[{"path", "faces": [{"box", "quality"}]}], one per path, in order."""
    if not paths:
        return []
    return [json.loads(line) for line in _run(["faces", *paths]).splitlines() if line.strip()]


def cutout(image, face_box, out_png):
    """An RGBA PNG of just the person under face_box, cropped to them.
    Returns the crop box in source pixels."""
    with tempfile.TemporaryDirectory() as d:
        mask_path = os.path.join(d, "mask.png")
        _run(["mask", image, *[str(v) for v in face_box], mask_path])
        mask = Image.open(mask_path).convert("L")
        src = Image.open(image).convert("RGB")
        if mask.size != src.size:
            mask = mask.resize(src.size)
    # The mask has faint smudges (under ~64) away from the person: the crop
    # comes from the solid part, and anything that faint is dropped. Soft
    # edges above it keep their alpha.
    bbox = mask.point(lambda v: 255 if v >= 128 else 0).getbbox()
    mask = mask.point(lambda v: 0 if v < 64 else v)
    if not bbox:
        raise VisionError("no person under that face")
    rgba = src.copy()
    rgba.putalpha(mask)
    rgba.crop(bbox).save(out_png)
    x0, y0, x1, y1 = bbox
    return [x0, y0, x1 - x0, y1 - y0]
