"""Thumbnails from real frames of the streamer.

  thumbs.py frames <raw> <start> <end> <outdir> [--shift <s>]
      start and end are seconds or HH:MM:SS.xx; --shift is subtracted from both.
      Grabs ~30 frames over the range, keeps the 8 with the clearest face,
      best first, and prints them as JSON: [{"path", "t", "box", "quality"}].
  thumbs.py compose <frame> <x> <y> <w> <h> <landscape|portrait> <out.jpg>
                    --line "..." [--line ...] [--side left|right]
                    [--background <frame>] [--style label|card|stack] [--profile <name>]
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

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

import profiles
import vision

SIZES = {"landscape": (1280, 720), "portrait": (1080, 1920)}
YELLOW, WHITE, OUTLINE, TINT = (255, 212, 0), (255, 255, 255), (17, 17, 17), (8, 24, 60)
RED, GLOW = (230, 40, 45), (255, 176, 0)
STYLES = ("label", "card", "stack")
DEFAULT_FONT = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
MAX_BYTES = 2 * 1024 * 1024


def parse_time(t):
    """Seconds from "71.5" or a clip's "HH:MM:SS.xx"."""
    secs = 0.0
    for part in str(t).split(":"):
        secs = secs * 60 + float(part)
    return round(secs, 3)


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
    """Blurred, darkened, blue-tinted and vignetted."""
    W, H = size
    bg = _cover(src, size, focus_x).filter(ImageFilter.GaussianBlur(14))
    bg = ImageEnhance.Brightness(bg).enhance(0.42)
    bg = Image.blend(bg, Image.new("RGB", size, TINT), 0.42)
    v = Image.new("L", size, 0)
    ImageDraw.Draw(v).ellipse((-W * 0.2, -H * 0.3, W * 1.2, H * 1.3), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(min(W, H) // 6))
    return Image.composite(bg, Image.new("RGB", size, (0, 0, 0)), v).convert("RGBA")


def _place_person(canvas, person, face_box, crop_xy, face_h, face_cx, face_top):
    """Scale the cutout so the face is face_h tall with its centre at
    face_cx and its top at face_top, with a warm glow behind it. Returns
    the box it was drawn in."""
    s = face_h / face_box[3]
    p = person.resize((max(1, round(person.width * s)), max(1, round(person.height * s))), Image.LANCZOS)
    x = round(face_cx - (face_box[0] + face_box[2] / 2 - crop_xy[0]) * s)
    y = round(face_top - (face_box[1] - crop_xy[1]) * s)
    # The cutout ends where the camera box did (often the shoulders): sit it
    # on the bottom edge rather than leave it floating.
    y = max(y, canvas.height - p.height)
    alpha = Image.new("L", canvas.size, 0)
    alpha.paste(p.getchannel("A"), (x, y))
    glow = alpha.filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.GaussianBlur(40))
    g = Image.new("RGBA", canvas.size, GLOW + (0,))
    g.putalpha(glow.point(lambda v: int(v * 0.85)))
    canvas.alpha_composite(g)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.paste(p, (x, y))
    canvas.alpha_composite(layer)
    return x, y, p.width, p.height


def _screen_card(canvas, src, face_box, xy, width, angle):
    """A sharp, tilted card of the screen: the part of the frame away from the face."""
    sw, sh = src.size
    face_right = face_box[0] + face_box[2] / 2 > sw / 2
    crop = src.crop((0, 0, int(sw * 0.6), sh)) if face_right else src.crop((int(sw * 0.4), 0, sw, sh))
    crop = ImageEnhance.Contrast(ImageOps.fit(crop, (width, round(width * 0.62)))).enhance(1.15)
    r = max(8, width // 28)
    m = Image.new("L", crop.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, *crop.size), r, fill=255)
    card = Image.new("RGBA", (crop.width + 12, crop.height + 12), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, card.width - 1, card.height - 1), r + 4, fill=WHITE + (255,))
    card.paste(crop, (6, 6), m)
    card = card.rotate(angle, expand=True, resample=Image.BICUBIC)
    _shadowed(canvas, card, xy, 20)


def _shadowed(canvas, layer, xy, blur):
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 165), (xy[0] + blur // 2, xy[1] + blur // 2 + 4), layer.getchannel("A"))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
    top = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    top.paste(layer, xy, layer)
    canvas.alpha_composite(top)


def _word(font_file, line, size, fill, box=None, angle=0):
    """One line as a tilted layer: outlined text, or dark text in a solid box."""
    f = ImageFont.truetype(font_file, size)
    stroke = 0 if box else max(5, size // 12)
    l, t, r, b = f.getbbox(line, stroke_width=stroke)
    pad = round(size * 0.18) if box else 0
    w, h = r - l + 2 * pad, b - t + 2 * pad
    layer = Image.new("RGBA", (w + 4, h + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if box:
        d.rounded_rectangle((2, 2, w + 1, h + 1), max(6, size // 10), fill=box + (255,))
    d.text((2 + pad - l, 2 + pad - t), line, font=f, fill=fill, stroke_width=stroke, stroke_fill=OUTLINE)
    return layer.rotate(angle, expand=True, resample=Image.BICUBIC) if angle else layer


def _fit_word(font_file, line, start, max_w, max_h, **kw):
    size = start
    while True:
        layer = _word(font_file, line, size, **kw)
        if (layer.width <= max_w and layer.height <= max_h) or size <= 24:
            return layer
        size -= 6


def _stack(canvas, font_file, specs, x, y, max_w, max_h, align):
    """Draw lines top to bottom from (x, y), each fitted to max_w and an
    equal share of max_h. specs: [(line, start size, kwargs)]."""
    share = max_h // len(specs)
    for line, start, kw in specs:
        layer = _fit_word(font_file, line, start, max_w, share, **kw)
        lx = x if align == "left" else x + max_w - layer.width if align == "right" else x + (max_w - layer.width) // 2
        _shadowed(canvas, layer, (lx, y), 10)
        y += layer.height - round(layer.height * 0.04)


def _specs(style, lines, big):
    """Per-line look for a style. big is the starting font size."""
    out = []
    for i, line in enumerate(lines):
        if style == "label":
            kw = dict(fill=OUTLINE, box=YELLOW, angle=3) if i == 0 else dict(fill=WHITE)
        elif style == "card":
            kw = dict(fill=YELLOW) if i == 0 else dict(fill=WHITE, box=RED, angle=-3)
        else:  # stack
            kw = (dict(fill=WHITE) if i == 0 else dict(fill=OUTLINE, box=YELLOW, angle=-3) if i == 1
                  else dict(fill=WHITE, box=RED, angle=2))
        size = big if i == 0 else round(big * (0.85 if style != "stack" else 0.75 if i == 1 else 0.45))
        out.append((line, size, kw))
    return out


def compose(frame, face_box, lines, orientation, out, font=None, side=None, background=None, style="label"):
    """style: label (first line in a yellow box), card (a tilted card of the
    screen, last line in a red box) or stack (person on the left, lines
    stacked as white, yellow box, red tag)."""
    if orientation not in SIZES:
        raise ValueError("orientation must be landscape or portrait")
    if style not in STYLES:
        raise ValueError(f"style must be one of {', '.join(STYLES)}")
    lines = [l.strip().upper() for l in lines if l.strip()]
    if not 1 <= len(lines) <= 3:
        raise ValueError("give 1 to 3 lines of text")
    font = font or DEFAULT_FONT
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
    canvas = _background(bg_src, (W, H), face_x)

    m = round(min(W, H) * 0.04)
    specs = _specs(style, lines, 150 if orientation == "landscape" else 200)
    if orientation == "landscape":
        side = side or ("left" if style == "stack" else "right")
        face_cx = W * 0.73 if side == "right" else W * 0.26
        tx = m if side == "right" else round(W * 0.48)
        tw = round(W * 0.52) - m
        if style == "card":
            _screen_card(canvas, src, face_box, (m if side == "right" else round(W * 0.5), m * 2),
                         round(W * 0.48), -5 if side == "right" else 5)
            _place_person(canvas, person, face_box, (cx, cy), H * 0.40, face_cx, H * 0.24)
            _stack(canvas, font, specs, tx, round(H * 0.58), tw, round(H * 0.38), "left" if side == "right" else "right")
        else:
            _place_person(canvas, person, face_box, (cx, cy), H * 0.40, face_cx, H * 0.26)
            _stack(canvas, font, specs, tx, round(H * 0.18), tw, round(H * 0.66), "left" if side == "right" else "right")
    else:
        if style == "card":
            _screen_card(canvas, src, face_box, (m * 2, round(H * 0.25)), W - 4 * m, -4)
            _stack(canvas, font, specs, m, m * 3, W - 2 * m, round(H * 0.2), "center")
        else:
            _stack(canvas, font, specs, m, m * 5, W - 2 * m, round(H * 0.34), "center")
        _place_person(canvas, person, face_box, (cx, cy), H * (0.17 if style == "card" else 0.23),
                      W * 0.5, H * (0.52 if style == "card" else 0.47 if len(lines) == 3 else 0.42))

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
    f.add_argument("start", type=parse_time)
    f.add_argument("end", type=parse_time)
    f.add_argument("outdir")
    f.add_argument("--shift", type=float, default=0.0,
                   help="subtract this from start and end (a short's transcript times: pass /api/shorts' shift)")
    c = sub.add_parser("compose")
    c.add_argument("frame")
    for k in "xywh":
        c.add_argument(k, type=float)
    c.add_argument("orientation", choices=sorted(SIZES))
    c.add_argument("out")
    c.add_argument("--line", action="append", required=True)
    c.add_argument("--side", choices=["left", "right"])
    c.add_argument("--background")
    c.add_argument("--style", choices=STYLES, default="label")
    c.add_argument("--profile")
    a = ap.parse_args(argv)
    if a.cmd == "frames":
        print(json.dumps(frames(a.raw, round(a.start - a.shift, 3), round(a.end - a.shift, 3), a.outdir), indent=1))
    else:
        p = profiles.load(a.profile or None)
        print(compose(a.frame, [a.x, a.y, a.w, a.h], a.line, a.orientation, a.out,
                      font=font_path(p), side=a.side, background=a.background, style=a.style))


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except (ValueError, vision.VisionError, profiles.ProfileError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
