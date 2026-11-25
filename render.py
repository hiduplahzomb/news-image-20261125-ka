#!/usr/bin/env python3
"""Render the front-page image for Wednesday 25 November 2026.

Fresh artwork for the make.fun news-image-20261125 competition.
Draws one 1024x1024 PNG with Pillow. No network. Deterministic output:
same code, same bytes. Every text block is measured before it is drawn
and rendering aborts (OverflowError) if any text would spill its box.

Revision: larger type throughout (base sizes roughly two fifths bigger
than the first draft), one single line of detail per panel, the closing
footer line removed, and its items folded into the IN BRIEF band.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

INK = (17, 17, 17)
PAPER = (248, 244, 236)
PANEL = (255, 253, 248)
RED = (178, 34, 34)
NAVY = (27, 58, 95)
TEAL = (18, 92, 84)
GOLD = (176, 124, 24)
GREY = (90, 86, 78)
LINE = (17, 17, 17)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines, all within max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines, label):
    """Wrap text; raise if it needs more than max_lines."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        raise OverflowError(
            "%s: %d lines needed, max %d: %r" % (label, len(lines), max_lines, text)
        )
    return lines


def draw_block(draw, x, y, max_w, max_h, text, fnt, fill, spacing=4,
               label="text", bottom=None):
    """Draw a wrapped block; raise if it exceeds max_h or the bottom limit."""
    lines = fit_lines(draw, text, fnt, max_w, 99, label)
    lh = fnt.getbbox("Ay")[3] - fnt.getbbox("Ay")[1] + spacing
    total = lh * len(lines) - spacing
    if total > max_h:
        raise OverflowError(
            "%s: block height %d exceeds %d" % (label, total, max_h)
        )
    if bottom is not None and y + total > bottom:
        raise OverflowError(
            "%s: block ends at %d, past bottom %d" % (label, y + total, bottom)
        )
    for i, line in enumerate(lines):
        draw.text((x, y + i * lh), line, font=fnt, fill=fill)
    return y + total


def shrink_to_fit(draw, text, path, start, minimum, max_w, max_lines, label):
    """Largest font size in [minimum, start] whose wrap fits max_lines."""
    for size in range(start, minimum - 1, -1):
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines and all(
            draw.textlength(ln, font=fnt) <= max_w for ln in lines
        ):
            return fnt, lines
    raise OverflowError("%s: cannot fit even at %dpt: %r" % (label, minimum, text))


def text_h(fnt):
    """Height of a single line in this font."""
    bb = fnt.getbbox("Ay")
    return bb[3] - bb[1]


# ---------------------------------------------------------------- pictograms
def pic_tanker(d, cx, cy, s):
    """Oil tanker on waves, with a sea mine nearby."""
    # hull
    d.polygon([(cx - 52 * s, cy - 6 * s), (cx + 52 * s, cy - 6 * s),
               (cx + 40 * s, cy + 16 * s), (cx - 40 * s, cy + 16 * s)],
              fill=(58, 74, 92), outline=INK, width=2)
    # deck tanks
    for i, x0 in enumerate((-38, -14, 10)):
        d.rectangle([cx + x0 * s, cy - 26 * s, cx + (x0 + 18) * s, cy - 6 * s],
                    fill=(232, 226, 214), outline=INK, width=2)
    # funnel
    d.rectangle([cx + 34 * s, cy - 30 * s, cx + 48 * s, cy - 6 * s],
                fill=RED, outline=INK, width=2)
    # waves
    for i, x0 in enumerate((-58, -18, 22)):
        d.arc([cx + x0 * s, cy + 20 * s, cx + (x0 + 30) * s, cy + 34 * s],
              0, 180, fill=NAVY, width=3)
    # sea mine
    mx, my = cx + 62 * s, cy - 26 * s
    d.ellipse([mx - 8 * s, my - 8 * s, mx + 8 * s, my + 8 * s],
              fill=INK)
    for ang in range(0, 360, 45):
        import math
        r = 11 * s
        x1 = mx + r * math.cos(math.radians(ang))
        y1 = my + r * math.sin(math.radians(ang))
        d.line([mx, my, x1, y1], fill=INK, width=2)


def pic_flame(d, cx, cy, s):
    """Flame over an oil derrick."""
    # derrick
    d.polygon([(cx - 26 * s, cy + 30 * s), (cx - 8 * s, cy - 22 * s),
               (cx + 8 * s, cy - 22 * s), (cx + 26 * s, cy + 30 * s)],
              outline=INK, width=3)
    d.line([cx - 20 * s, cy + 12 * s, cx + 20 * s, cy + 12 * s], fill=INK, width=2)
    d.line([cx - 14 * s, cy - 8 * s, cx + 14 * s, cy - 8 * s], fill=INK, width=2)
    # flame
    d.polygon([(cx, cy - 52 * s), (cx + 14 * s, cy - 28 * s),
               (cx + 6 * s, cy - 18 * s), (cx + 12 * s, cy - 6 * s),
               (cx, cy - 12 * s), (cx - 12 * s, cy - 6 * s),
               (cx - 6 * s, cy - 18 * s), (cx - 14 * s, cy - 28 * s)],
              fill=(226, 88, 26), outline=RED, width=2)


def pic_carrier(d, cx, cy, s):
    """Aircraft carrier with a jet."""
    d.rectangle([cx - 58 * s, cy - 4 * s, cx + 58 * s, cy + 4 * s],
                fill=(58, 74, 92), outline=INK, width=2)
    d.polygon([(cx - 52 * s, cy + 4 * s), (cx + 52 * s, cy + 4 * s),
               (cx + 40 * s, cy + 20 * s), (cx - 40 * s, cy + 20 * s)],
              fill=(88, 102, 120), outline=INK, width=2)
    d.rectangle([cx + 22 * s, cy - 22 * s, cx + 40 * s, cy - 4 * s],
                fill=(232, 226, 214), outline=INK, width=2)
    # jet above
    d.polygon([(cx - 40 * s, cy - 34 * s), (cx - 16 * s, cy - 34 * s),
               (cx - 10 * s, cy - 30 * s), (cx - 16 * s, cy - 26 * s),
               (cx - 40 * s, cy - 26 * s)], fill=INK)
    d.polygon([(cx - 34 * s, cy - 38 * s), (cx - 28 * s, cy - 38 * s),
               (cx - 26 * s, cy - 34 * s)], fill=INK)
    for i, x0 in enumerate((-56, -16, 24)):
        d.arc([cx + x0 * s, cy + 24 * s, cx + (x0 + 28) * s, cy + 36 * s],
              0, 180, fill=NAVY, width=3)


def pic_burst(d, cx, cy, s):
    """Explosion burst over a coastline (Libya strike)."""
    import math
    pts = []
    for i in range(16):
        ang = math.radians(i * 22.5)
        r = (34 if i % 2 == 0 else 18) * s
        pts.append((cx + r * math.cos(ang), cy - 6 * s + r * math.sin(ang)))
    d.polygon(pts, fill=(240, 178, 44), outline=RED, width=2)
    d.ellipse([cx - 9 * s, cy - 15 * s, cx + 9 * s, cy + 3 * s], fill=RED)
    # ground line
    d.line([cx - 58 * s, cy + 30 * s, cx + 58 * s, cy + 30 * s],
           fill=INK, width=3)
    d.polygon([(cx - 58 * s, cy + 30 * s), (cx - 30 * s, cy + 14 * s),
               (cx - 6 * s, cy + 30 * s)], fill=TEAL, outline=INK, width=2)


def pic_shield(d, cx, cy, s):
    """Shield with a check mark (air-defence aid)."""
    d.polygon([(cx - 30 * s, cy - 34 * s), (cx + 30 * s, cy - 34 * s),
               (cx + 30 * s, cy - 2 * s), (cx, cy + 34 * s),
               (cx - 30 * s, cy - 2 * s)],
              fill=NAVY, outline=INK, width=3)
    d.line([cx - 16 * s, cy - 2 * s, cx - 4 * s, cy + 12 * s,
            cx + 18 * s, cy - 16 * s], fill=(255, 255, 255), width=5)


def pic_rocket(d, cx, cy, s):
    """Rocket lifting off (first astronaut)."""
    d.ellipse([cx - 13 * s, cy - 36 * s, cx + 13 * s, cy + 14 * s],
              fill=(232, 226, 214), outline=INK, width=2)
    d.polygon([(cx - 13 * s, cy - 22 * s), (cx, cy - 48 * s),
               (cx + 13 * s, cy - 22 * s)], fill=RED, outline=INK, width=2)
    d.polygon([(cx - 13 * s, cy + 2 * s), (cx - 26 * s, cy + 20 * s),
               (cx - 13 * s, cy + 14 * s)], fill=RED, outline=INK, width=2)
    d.polygon([(cx + 13 * s, cy + 2 * s), (cx + 26 * s, cy + 20 * s),
               (cx + 13 * s, cy + 14 * s)], fill=RED, outline=INK, width=2)
    d.polygon([(cx - 7 * s, cy + 14 * s), (cx + 7 * s, cy + 14 * s),
               (cx + 3 * s, cy + 34 * s), (cx - 3 * s, cy + 34 * s)],
              fill=(240, 178, 44), outline=RED, width=2)
    # stars
    for sx, sy in ((-48, -30), (46, -38), (52, 6), (-52, 14)):
        d.ellipse([cx + sx * s - 2, cy + sy * s - 2,
                   cx + sx * s + 2, cy + sy * s + 2], fill=GOLD)


def pic_court(d, cx, cy, s):
    """Courthouse with columns and pediment (trial)."""
    # pediment
    d.polygon([(cx - 50 * s, cy - 18 * s), (cx + 50 * s, cy - 18 * s),
               (cx, cy - 38 * s)],
              fill=(232, 226, 214), outline=INK, width=2)
    # oculus in the pediment
    d.ellipse([cx - 5 * s, cy - 30 * s, cx + 5 * s, cy - 20 * s],
              fill=GOLD, outline=INK, width=2)
    # entablature
    d.rectangle([cx - 50 * s, cy - 18 * s, cx + 50 * s, cy - 12 * s],
                fill=(232, 226, 214), outline=INK, width=2)
    # columns
    for x0 in (-32, 0, 32):
        d.rectangle([cx + (x0 - 5) * s, cy - 12 * s,
                     cx + (x0 + 5) * s, cy + 18 * s],
                    fill=(255, 253, 248), outline=INK, width=2)
    # steps
    d.rectangle([cx - 50 * s, cy + 18 * s, cx + 50 * s, cy + 24 * s],
                fill=(200, 196, 188), outline=INK, width=2)
    d.rectangle([cx - 56 * s, cy + 24 * s, cx + 56 * s, cy + 30 * s],
                fill=(200, 196, 188), outline=INK, width=2)


PANELS = [
    ("PUTIN VOWS RETALIATION",
     "'Inevitable', Putin says.",
     pic_flame, (240, 178, 44)),
    ("TRUMP WARNS IRAN",
     "'Traumatic' if deal fails.",
     pic_carrier, (214, 228, 240)),
    ("UKRAINE HITS LIBYA, 2 DEAD",
     "Self-defence, says Kyiv.",
     pic_burst, (250, 226, 210)),
    ("NORWAY GIVES UKRAINE $7BN",
     "$7bn pledged for 2027.",
     pic_shield, (216, 232, 224)),
    ("PAKISTAN IN ORBIT",
     "First Pakistani in orbit.",
     pic_rocket, (226, 222, 240)),
    ("SARKOZY LIBYA TRIAL",
     "The Sarkozys face trial.",
     pic_court, (238, 230, 200)),
]

BRIEF = ("Trade: Trump seals Japan, Indonesia deals; EU threatens $84bn "
         "tariffs. \u00b7 Senegal regain CAN-2025. \u00b7 Bangladesh pay up "
         "36%. \u00b7 Gaza strikes kill 7.")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 20
    sizes = {}

    # ---- masthead ----
    f_mast, _ = shrink_to_fit(
        d, "THE WORLD TODAY", SERIF_B, 84, 72, W - 2 * MX, 1, "masthead")
    sizes["masthead"] = f_mast.size
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    mast_y = 4
    d.text(((W - tw) / 2, mast_y), title, font=f_mast, fill=INK)
    rule1 = mast_y + text_h(f_mast) + 8
    d.line([MX, rule1, W - MX, rule1], fill=INK, width=3)
    d.line([MX, rule1 + 6, W - MX, rule1 + 6], fill=INK, width=1)

    # ---- dateline ----
    f_date, _ = shrink_to_fit(
        d, "WEDNESDAY 25 NOVEMBER 2026", SANS_B, 53, 46, W - 2 * MX, 1, "date")
    sizes["date"] = f_date.size
    date = "WEDNESDAY 25 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    date_y = rule1 + 14
    d.text(((W - tw) / 2, date_y), date, font=f_date, fill=RED)
    f_sub = font(SANS_B, 25)
    sizes["sub"] = 25
    sub = "ONE DAY  ·  ONE PAGE  ·  THE WORLD'S NEWS"
    tw = d.textlength(sub, font=f_sub)
    sub_y = date_y + text_h(f_date) + 6
    d.text(((W - tw) / 2, sub_y), sub, font=f_sub, fill=GREY)

    # ---- lead story ----
    lead_y = sub_y + text_h(f_sub) + 10
    d.line([MX, lead_y, W - MX, lead_y], fill=INK, width=2)
    f_kick = font(SANS_B, 28)
    sizes["kicker"] = 28
    kick_y = lead_y + 8
    d.text((40, kick_y), "LEAD STORY — MIDDLE EAST", font=f_kick, fill=RED)
    head_y = kick_y + text_h(f_kick) + 8
    f_head, head_lines = shrink_to_fit(
        d, "THREE OIL TANKERS HIT BY MINES IN THE STRAIT OF HORMUZ",
        SERIF_B, 56, 44, 640, 3, "lead headline")
    sizes["lead headline"] = f_head.size
    lh = text_h(f_head) + 6
    y = head_y
    for ln in head_lines:
        d.text((40, y), ln, font=f_head, fill=INK)
        y += lh
    head_end = y - 6
    # lead pictogram box, right of the headline
    d.rectangle([712, head_y - 4, 984, head_end + 4], fill=(214, 228, 240),
                outline=INK, width=2)
    pic_tanker(d, 848, (head_y + head_end) // 2, 1.35)
    # lead detail: a single line across the full width
    f_det, det_lines = shrink_to_fit(
        d, "Tankers hit under US escort; the world's busiest oil route at risk.",
        SANS, 27, 22, W - 80, 1, "lead detail")
    sizes["lead detail"] = f_det.size
    det_y = head_end + 10
    d.text((40, det_y), det_lines[0], font=f_det, fill=INK)
    det_end = det_y + text_h(f_det)
    lead_rule = det_end + 10
    d.line([MX, lead_rule, W - MX, lead_rule], fill=INK, width=2)

    # ---- 6-panel grid ----
    grid_y = lead_rule + 12
    col_w, row_h, gap = 320, 210, 12
    for i, (ptitle, pdetail, pic, tint) in enumerate(PANELS):
        col, row = i % 3, i // 3
        x = MX + col * (col_w + gap)
        y = grid_y + row * (row_h + gap)
        d.rectangle([x, y, x + col_w, y + row_h], fill=PANEL,
                    outline=INK, width=2)
        # pictogram strip
        d.rectangle([x + 2, y + 2, x + col_w - 2, y + 66], fill=tint)
        d.line([x + 2, y + 66, x + col_w - 2, y + 66], fill=INK, width=2)
        pic(d, x + col_w // 2, y + 34, 0.62)
        # panel title, large and fitted (max 2 lines)
        f_t, t_lines = shrink_to_fit(
            d, ptitle, SANS_B, 42, 30, col_w - 24, 2, "panel %d title" % i)
        sizes["panel %d title" % i] = f_t.size
        ty = y + 74
        lh = text_h(f_t) + 4
        for ln in t_lines:
            d.text((x + 12, ty), ln, font=f_t, fill=INK)
            ty += lh
        # panel detail: exactly one line
        f_d, d_lines = shrink_to_fit(
            d, pdetail, SANS, 25, 20, col_w - 24, 1, "panel %d detail" % i)
        sizes["panel %d detail" % i] = f_d.size
        dy = ty + 2
        d.text((x + 12, dy), d_lines[0], font=f_d, fill=GREY)
        if dy + text_h(f_d) > y + row_h - 6:
            raise OverflowError(
                "panel %d detail ends past panel bottom" % i)

    # ---- summary band ----
    band_y = grid_y + 2 * row_h + gap + 10
    band_h = 108
    if band_y + band_h > H:
        raise OverflowError(
            "band ends at %d, past image height %d" % (band_y + band_h, H))
    d.rectangle([MX, band_y, W - MX, band_y + band_h], fill=NAVY)
    f_b = font(SANS_B, 26)
    sizes["brief header"] = 26
    d.text((36, band_y + 8), "IN BRIEF", font=f_b, fill=(255, 255, 255))
    f_bt, b_lines = shrink_to_fit(
        d, BRIEF, SANS, 26, 20, W - 72, 2, "brief text")
    sizes["brief text"] = f_bt.size
    by = band_y + 40
    lh = text_h(f_bt) + 4
    for ln in b_lines:
        d.text((36, by), ln, font=f_bt, fill=(255, 255, 255))
        by += lh
    if by - 4 > band_y + band_h - 4:
        raise OverflowError("brief text ends past band bottom")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")
    print("sizes:", sizes)


if __name__ == "__main__":
    try:
        main()
    except OverflowError as exc:
        print("OVERFLOW:", exc, file=sys.stderr)
        sys.exit(1)
