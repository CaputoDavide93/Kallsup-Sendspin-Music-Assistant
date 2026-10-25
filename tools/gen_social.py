#!/usr/bin/env python3
"""Draw docs/assets/social-preview.png (1280x640): icon, name, tagline, chips.

  python3 tools/gen_social.py

Needs Pillow (pip install pillow). Uses Arial from the system font folders and
falls back to Pillow's built-in font. The PNG carries no metadata. GitHub takes
the file by hand: Settings, Social preview, Upload an image.
"""
from __future__ import annotations

import math
import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "social-preview.png"
W, H, K = 1280, 640, 2  # K: supersampling for smooth edges

NAME = "KALLSUP Sendspin"
TAGLINE = "An IKEA KALLSUP rebuilt as a battery-powered Music Assistant Wi-Fi speaker"
CHIPS = ["ESPHome", "ESP32-S3", "MAX98357A", "MIT"]


def font(size: int, bold: bool) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = ["Arial Bold.ttf" if bold else "Arial.ttf"]
    for folder in ("/System/Library/Fonts/Supplemental", "/Library/Fonts",
                   "/usr/share/fonts/truetype/msttcorefonts", "/usr/share/fonts/truetype/dejavu"):
        for name in names + (["DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]):
            path = pathlib.Path(folder) / name
            if path.exists():
                return ImageFont.truetype(str(path), size * K)
    return ImageFont.load_default()


def gradient(w, h, c0, c1):
    base = Image.new("RGB", (w, h))
    px = base.load()
    for y in range(h):
        for x in range(w):
            t = (x / w + y / h) / 2
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(c0, c1))
    return base


def icon(size: int) -> Image.Image:
    """The brand/icon.svg shapes, drawn at `size` px (512 design units)."""
    s = size / 512
    img = gradient(size, size, (0x43, 0x78, 0xEA), (0x1F, 0x47, 0xA8)).convert("RGBA")
    d = ImageDraw.Draw(img)

    def r(x, y, w, h, rad, fill):
        d.rounded_rectangle([x * s, y * s, (x + w) * s, (y + h) * s], rad * s, fill=fill)

    def c(cx, cy, rad, fill):
        d.ellipse([(cx - rad) * s, (cy - rad) * s, (cx + rad) * s, (cy + rad) * s], fill=fill)

    d.ellipse([96 * s, 456 * s, 416 * s, 492 * s], fill=(0x0B, 0x1F, 0x55, 90))
    r(104, 226, 304, 212, 52, (0xF2, 0xF4, 0xF8, 255))
    r(126, 248, 260, 168, 34, (0xCF, 0xD5, 0xDE, 255))
    for gx in range(133, 380, 14):
        for gy in range(255, 410, 14):
            c(gx, gy, 3.2, (0x9E, 0xA7, 0xB5, 255))
    for rad, col in ((62, "#262b33"), (50, "#4a5261"), (36, "#3a414d"), (17, "#1a1d22")):
        c(256, 332, rad, col)
    for rad in (40, 86, 132):
        ro = rad + 13  # PIL widens an arc inward, so draw from the outer radius
        box = [(256 - ro) * s, (206 - ro) * s, (256 + ro) * s, (206 + ro) * s]
        d.arc(box, 225, 315, fill="white", width=round(26 * s))
        for ang in (225, 315):  # round caps
            x = 256 + rad * math.cos(math.radians(ang))
            y = 206 + rad * math.sin(math.radians(ang))
            c(x, y, 13, "white")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size, size], 114 * s, fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def main() -> None:
    img = gradient(W * K, H * K, (0x12, 0x1A, 0x2E), (0x1B, 0x2C, 0x57)).convert("RGBA")
    ic = icon(300 * K)
    img.alpha_composite(ic, (90 * K, (H - 300) // 2 * K))
    d = ImageDraw.Draw(img)
    x = 450 * K
    d.text((x, 150 * K), NAME, font=font(76, True), fill="white")
    # tagline, wrapped at the card width
    f = font(34, False)
    words, lines, line = TAGLINE.split(), [], ""
    for w in words:
        trial = (line + " " + w).strip()
        if d.textlength(trial, font=f) > (W - 450 - 70) * K:
            lines.append(line)
            line = w
        else:
            line = trial
    lines.append(line)
    y = 262 * K
    for ln in lines:
        d.text((x, y), ln, font=f, fill=(0xC9, 0xD3, 0xEE))
        y += 48 * K
    cf = font(26, True)
    cx, cy = x, 440 * K
    for chip in CHIPS:
        tw = d.textlength(chip, font=cf)
        d.rounded_rectangle([cx, cy, cx + tw + 44 * K, cy + 56 * K], 28 * K,
                            fill=(0x2A, 0x3F, 0x78), outline=(0x4A, 0x6B, 0xC0), width=2 * K)
        d.text((cx + 22 * K, cy + 11 * K), chip, font=cf, fill="white")
        cx += tw + 44 * K + 16 * K
    out = img.convert("RGB").resize((W, H), Image.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT, "PNG", optimize=True)  # no exif/text chunks are written
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
