"""Thumbnails from real frames of the streamer.

  thumbs.py frames <raw> <start> <end> <outdir>
      Grabs ~30 frames over the range, keeps the 8 with the clearest face,
      best first, and prints them as JSON: [{"path", "t", "box", "quality"}].
  thumbs.py compose <frame> <x> <y> <w> <h> <landscape|portrait> <out.jpg>
                    --line "..." [--line ...] [--side left|right]
                    [--background <frame>] [--profile <name>]
      Cuts the person under that face box out of the frame and builds the
      thumbnail: a blurred, dimmed, blue-tinted background, the person on
      one side, and big upper-case text on the other. Prints the path.

Sizes: landscape 1280x720 (YouTube), portrait 1080x1920 (Shorts); JPEG
under 2 MB."""
import argparse
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

import profiles
import vision

SIZES = {"landscape": (1280, 720), "portrait": (1080, 1920)}
YELLOW, WHITE, OUTLINE, TINT = (255, 212, 0), (255, 255, 255), (17, 17, 17), (11, 30, 63)
DEFAULT_FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
MAX_BYTES = 2 * 1024 * 1024


def frame_times(start, end, count=30):
    step = (end - start) / count
    return [round(start + step * (i + 0.5), 3) for i in range(count)]


def frames(raw, start, end, outdir, count=30, keep=8):
    if profiles.cloud_only(raw):
        raise ValueError(f"{raw} is only in the cloud. Download it in Finder first "
                         "(right-click, Make available offline).")
    os.makedirs(outdir, exist_ok=True)
    grabbed = []
    for t in frame_times(start, end, count):
        p = os.path.join(outdir, f"frame-{t:.2f}.jpg")
        r = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", str(t), "-i", raw,
                            "-frames:v", "1", "-q:v", "2", p], capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(p):
            grabbed.append((t, p))
    found = vision.faces([p for _, p in grabbed])
    ranked = []
    for (t, p), f in zip(grabbed, found):
        if f["faces"]:
            best = max(f["faces"], key=lambda x: x["quality"])
            ranked.append({"path": p, "t": t, "box": best["box"], "quality": best["quality"]})
    ranked.sort(key=lambda r: -r["quality"])
    for r in ranked[keep:]:
        os.remove(r["path"])
    for t, p in grabbed:
        if not any(r["path"] == p for r in ranked):
            os.remove(p)
    return ranked[:keep]


def font_path(profile=None):
    f = (profile or {}).get("thumbnail_font")
    if f:
        for d in (os.path.expanduser("~/Library/Fonts"), "/Library/Fonts"):
            if os.path.exists(os.path.join(d, f["file"])):
                return os.path.join(d, f["file"])
    return DEFAULT_FONT


def _cover(img, size, focus_x):
    """Scale img to cover size, cropping around focus_x (0..1)."""
    w, h = size
    s = max(w / img.width, h / img.height)
    im = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    left = min(max(0, round(im.width * focus_x - w / 2)), im.width - w)
    top = (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))


def _background(src, size, focus_x):
    bg = _cover(src, size, focus_x).filter(ImageFilter.GaussianBlur(18))
    bg = ImageEnhance.Brightness(bg).enhance(0.45)
    return Image.blend(bg, Image.new("RGB", size, TINT), 0.35)


def _fit(lines, font_file, start, box_w, box_h):
    size = start
    while size > 24:
        f = ImageFont.truetype(font_file, size)
        stroke = max(4, size // 15)
        widths = [f.getbbox(l, stroke_width=stroke)[2] for l in lines]
        line_h = round(size * 1.05)
        if max(widths) <= box_w and line_h * len(lines) <= box_h:
            return f, stroke, line_h
        size -= 6
    f = ImageFont.truetype(font_file, size)
    return f, max(4, size // 15), round(size * 1.05)


def _text(canvas, lines, font_file, box, start, align):
    x0, y0, bw, bh = box
    f, stroke, line_h = _fit(lines, font_file, start, bw, bh)
    top = y0 + (bh - line_h * len(lines)) // 2
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    spots = []
    for i, line in enumerate(lines):
        w = f.getbbox(line, stroke_width=stroke)[2]
        x = x0 if align == "left" else x0 + bw - w if align == "right" else x0 + (bw - w) // 2
        y = top + i * line_h
        spots.append((x, y, line, YELLOW if i == 0 else WHITE))
        sd.text((x + 6, y + 6), line, font=f, fill=(0, 0, 0, 153), stroke_width=stroke, stroke_fill=(0, 0, 0, 153))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(canvas)
    for x, y, line, colour in spots:
        d.text((x, y), line, font=f, fill=colour, stroke_width=stroke, stroke_fill=OUTLINE)


def compose(frame, face_box, lines, orientation, out, font=None, side=None, background=None):
    if orientation not in SIZES:
        raise ValueError("orientation must be landscape or portrait")
    lines = [l.strip().upper() for l in lines if l.strip()]
    if not 1 <= len(lines) <= 3:
        raise ValueError("give 1 to 3 lines of text")
    W, H = SIZES[orientation]
    src = Image.open(frame).convert("RGB")
    face_x = (face_box[0] + face_box[2] / 2) / src.width
    with tempfile.TemporaryDirectory() as d:
        cut_path = os.path.join(d, "cut.png")
        cx, cy, _, _ = vision.cutout(frame, face_box, cut_path)
        person = Image.open(cut_path).convert("RGBA")
    if background:
        bg_src = Image.open(background).convert("RGB")
    else:
        # The person is moved to the front, so take them out of the
        # background: no blurred ghost of them behind the text.
        bg_src = src.copy()
        hole = Image.new("L", src.size, 0)
        hole.paste(person.getchannel("A"), (cx, cy))
        fill = src.resize((1, 1), Image.BOX).getpixel((0, 0))
        bg_src.paste(Image.new("RGB", src.size, fill), (0, 0), hole.filter(ImageFilter.MaxFilter(9)))
    canvas = _background(bg_src, (W, H), face_x).convert("RGBA")

    margin = round(W * 0.04)
    if orientation == "landscape":
        side = side or ("left" if max(len(l) for l in lines) > 10 else "right")
        s = min(H * 0.95 / person.height, W * 0.5 / person.width)
        person = person.resize((round(person.width * s), round(person.height * s)), Image.LANCZOS)
        px = W - person.width if side == "right" else 0
        canvas.alpha_composite(person, (px, H - person.height))
        tw = round(W * 0.55) - 2 * margin
        tx = margin if side == "right" else W - margin - tw
        _text(canvas, lines, font or DEFAULT_FONT, (tx, margin, tw, H - 2 * margin), 190,
              "left" if side == "right" else "right")
    else:
        s = min(H * 0.55 / person.height, W / person.width)
        person = person.resize((round(person.width * s), round(person.height * s)), Image.LANCZOS)
        canvas.alpha_composite(person, ((W - person.width) // 2, H - person.height))
        _text(canvas, lines, font or DEFAULT_FONT, (margin, margin * 3, W - 2 * margin, round(H * 0.4) - margin * 3),
              170, "center")

    rgb = canvas.convert("RGB")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    for q in (90, 82, 74, 66):
        rgb.save(out, "JPEG", quality=q, optimize=True)
        if os.path.getsize(out) < MAX_BYTES:
            break
    return out


def main(argv):
    ap = argparse.ArgumentParser(prog="thumbs.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("frames")
    f.add_argument("raw")
    f.add_argument("start", type=float)
    f.add_argument("end", type=float)
    f.add_argument("outdir")
    c = sub.add_parser("compose")
    c.add_argument("frame")
    for k in "xywh":
        c.add_argument(k, type=float)
    c.add_argument("orientation", choices=sorted(SIZES))
    c.add_argument("out")
    c.add_argument("--line", action="append", required=True)
    c.add_argument("--side", choices=["left", "right"])
    c.add_argument("--background")
    c.add_argument("--profile")
    a = ap.parse_args(argv)
    if a.cmd == "frames":
        print(json.dumps(frames(a.raw, a.start, a.end, a.outdir), indent=1))
    else:
        p = profiles.load(a.profile or None)
        print(compose(a.frame, [a.x, a.y, a.w, a.h], a.line, a.orientation, a.out,
                      font=font_path(p), side=a.side, background=a.background))


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except (ValueError, vision.VisionError, profiles.ProfileError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
