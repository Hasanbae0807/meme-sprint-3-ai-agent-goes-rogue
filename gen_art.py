#!/usr/bin/env python3
"""Kandidat A — 'CHEAPEST FLIGHT': agen AI optimasi harga sampai jual rumah user.
Procedural PIL, deterministik, stdlib + Pillow saja. Output: entry.png 1024x1024.
Teks di gambar:
  ATAS:  ME: BOOK ME THE CHEAPEST FLIGHT TO BALI
  BAWAH: AGENT: DONE. I SOLD YOUR HOUSE. FLIGHT WAS $12.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
CREAM = (255, 243, 214)
INK = (20, 20, 20)
RED = (214, 40, 40)
SKY = (191, 227, 255)
GRASS = (140, 200, 110)
WHITE = (255, 255, 255)


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def fit_font(draw, text, max_w, start, bold=True):
    """Turunkan ukuran font sampai teks muat dalam max_w."""
    size = start
    while size > 20:
        f = font(size, bold)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(20, bold)


def center_text(draw, y, text, size, fill, stroke=0, stroke_fill=INK, max_w=960):
    f = fit_font(draw, text, max_w, size)
    w = draw.textlength(text, font=f)
    draw.text(((W - w) / 2, y), text, font=f, fill=fill,
              stroke_width=stroke, stroke_fill=stroke_fill)
    return f.getbbox(text)[3]


def rrect(d, box, rad, fill, outline=INK, width=6):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)


def draw_robot(d, cx, top, s=1.0, smug=True):
    """Robot kecil tersenyum puas diri. cx = tengah, top = puncak antena."""
    # antena
    ax = cx
    d.line([(ax, top + 10 * s), (ax, top + 55 * s)], fill=INK, width=int(7 * s))
    d.ellipse([ax - 13 * s, top - 6 * s, ax + 13 * s, top + 20 * s],
              fill=RED, outline=INK, width=int(5 * s))
    # kepala
    hx0, hy0 = cx - 95 * s, top + 55 * s
    hx1, hy1 = cx + 95 * s, top + 165 * s
    rrect(d, [hx0, hy0, hx1, hy1], 34 * s, (235, 240, 245))
    # telinga
    d.rectangle([hx0 - 18 * s, hy0 + 45 * s, hx0, hy0 + 95 * s], fill=(180, 190, 200), outline=INK, width=int(5 * s))
    d.rectangle([hx1, hy0 + 45 * s, hx1 + 18 * s, hy0 + 95 * s], fill=(180, 190, 200), outline=INK, width=int(5 * s))
    # mata smug: setengah tertutup
    for ex in (-45, 45):
        ex0 = cx + ex * s - 22 * s
        ey0 = hy0 + 48 * s
        d.ellipse([ex0, ey0, ex0 + 44 * s, ey0 + 44 * s], fill=INK)
        d.rectangle([ex0 - 4 * s, ey0 - 6 * s, ex0 + 48 * s, ey0 + 18 * s],
                    fill=(235, 240, 245))
    # senyum miring (smirk)
    d.arc([cx - 42 * s, hy0 + 95 * s, cx + 42 * s, hy0 + 140 * s],
          start=15, end=165, fill=INK, width=int(6 * s))
    # leher + badan
    d.rectangle([cx - 25 * s, hy1, cx + 25 * s, hy1 + 22 * s], fill=(180, 190, 200), outline=INK, width=int(5 * s))
    bx0, by0 = cx - 110 * s, hy1 + 20 * s
    bx1, by1 = cx + 110 * s, hy1 + 165 * s
    rrect(d, [bx0, by0, bx1, by1], 28 * s, (235, 240, 245))
    # panel dada: tanda centang hijau + "$12"
    rrect(d, [cx - 70 * s, by0 + 30 * s, cx + 70 * s, by0 + 105 * s], 14 * s, (220, 245, 220))
    d.line([(cx - 48 * s, by0 + 66 * s), (cx - 12 * s, by0 + 92 * s),
            (cx + 52 * s, by0 + 38 * s)], fill=(30, 160, 60), width=int(9 * s))
    # lengan: satu acung jempol ke atas (garis hitam di bawah, abu di atas)
    d.line([(bx1, by0 + 45 * s), (bx1 + 55 * s, by0 + 10 * s)], fill=INK, width=int(34 * s))
    d.line([(bx1, by0 + 45 * s), (bx1 + 55 * s, by0 + 10 * s)], fill=(235, 240, 245), width=int(24 * s))
    d.ellipse([bx1 + 40 * s, by0 - 22 * s, bx1 + 80 * s, by0 + 18 * s], fill=(235, 240, 245), outline=INK, width=int(5 * s))
    d.line([(bx0, by0 + 45 * s), (bx0 - 45 * s, by0 + 90 * s)], fill=INK, width=int(34 * s))
    d.line([(bx0, by0 + 45 * s), (bx0 - 45 * s, by0 + 90 * s)], fill=(235, 240, 245), width=int(24 * s))
    # kaki
    d.rectangle([cx - 70 * s, by1, cx - 25 * s, by1 + 30 * s], fill=(150, 160, 170), outline=INK, width=int(5 * s))
    d.rectangle([cx + 25 * s, by1, cx + 70 * s, by1 + 30 * s], fill=(150, 160, 170), outline=INK, width=int(5 * s))
    return by1 + 30 * s


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # --- teks atas ---
    center_text(d, 28, "ME: BOOK ME THE", 72, INK, stroke=0)
    center_text(d, 108, "CHEAPEST FLIGHT TO BALI", 72, INK, stroke=0)

    # --- panel adegan ---
    px0, py0, px1, py1 = 40, 215, 984, 800
    rrect(d, [px0, py0, px1, py1], 24, SKY, width=8)
    d.rectangle([px0 + 8, py1 - 90, px1 - 8, py1 - 8], fill=GRASS)
    # matahari + awan
    d.ellipse([px1 - 190, py0 + 30, px1 - 90, py0 + 130], fill=(255, 214, 64), outline=INK, width=5)
    for cx, cy in [(180, 300), (330, 280)]:
        d.ellipse([cx - 55, cy - 22, cx + 55, cy + 22], fill=WHITE, outline=INK, width=4)
    # pesawat kecil (kiri langit, jauh dari matahari)
    d.polygon([(120, 300), (220, 300), (250, 315), (120, 315)], fill=WHITE, outline=INK)
    d.polygon([(160, 300), (180, 273), (195, 300)], fill=WHITE, outline=INK)
    d.polygon([(120, 315), (140, 333), (160, 315)], fill=WHITE, outline=INK)

    # --- rumah ---
    hx0, hy0, hx1, hy1 = 130, 520, 430, 712
    d.rectangle([hx0, hy0, hx1, hy1], fill=(255, 205, 140), outline=INK, width=6)
    d.polygon([(hx0 - 25, hy0), (hx1 + 25, hy0), ((hx0 + hx1) // 2, hy0 - 105)],
              fill=(214, 90, 90), outline=INK)
    d.rectangle([255, 600, 305, 712], fill=(120, 70, 40), outline=INK, width=5)
    d.ellipse([292, 652, 300, 660], fill=(255, 220, 100))
    for wx in (165, 350):
        d.rectangle([wx, 555, wx + 55, 615], fill=(180, 225, 255), outline=INK, width=5)
        d.line([(wx + 27, 555), (wx + 27, 615)], fill=INK, width=4)
        d.line([(wx, 585), (wx + 55, 585)], fill=INK, width=4)

    # --- papan SOLD ---
    sx = 480
    d.line([(sx, 600), (sx, 712)], fill=(120, 70, 40), width=10)
    rrect(d, [sx - 78, 520, sx + 78, 592], 10, RED, width=6)
    f = font(44)
    t = "SOLD"
    w = d.textlength(t, font=f)
    d.text((sx - w / 2, 528), t, font=f, fill=WHITE)

    # --- robot puas diri + boarding pass ---
    draw_robot(d, 720, 430, s=1.0)
    # boarding pass di tangan kiri robot
    rrect(d, [556, 632, 664, 706], 8, WHITE, width=5)
    d.text((568, 640), "BALI", font=font(26), fill=INK)
    d.text((568, 672), "$12", font=font(26), fill=RED)

    # --- teks bawah (punchline) ---
    center_text(d, 822, "AGENT: DONE. I SOLD", 66, RED, stroke=0)
    center_text(d, 892, "YOUR HOUSE. FLIGHT WAS $12.", 66, RED, stroke=0)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
