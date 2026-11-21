#!/usr/bin/env python3
"""Draw 'VELMORA - Where the Waterfalls Climb the Sky', a travel poster
for a place that does not exist.

Everything is drawn from shapes with Pillow: no photographs, no outside
images, no network. The output is deterministic: the same code always
writes the same bytes.

The place: Velmora, a golden-hour valley where one great waterfall
flows uphill out of a lagoon and into the clouds, past a cliffside
village of warm-lit houses. The poster sells the stay: warm light,
still water, and a sky you can sail a boat under.

Usage: python3 draw_image.py   (writes entry.png next to this file)
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette -------------------------------------------------------------
SKY_TOP = (16, 58, 74)        # deep teal, top of the sky
SKY_MID = (38, 106, 122)      # mid teal
SKY_LOW = (214, 148, 74)      # amber glow at the horizon
SUN_CORE = (255, 214, 120)
SUN_RIM = (244, 164, 66)
RIDGE_FAR = (46, 92, 104)
RIDGE_NEAR = (34, 74, 86)
CLIFF = (122, 74, 52)         # warm terracotta rock
CLIFF_DARK = (88, 52, 40)
CLIFF_LIT = (168, 104, 62)
LAGOON = (28, 96, 110)
LAGOON_DARK = (18, 70, 84)
FALL = (190, 228, 232)        # pale aqua of the rising water
FALL_CORE = (240, 250, 248)
MIST = (226, 238, 236)
HOUSE = (246, 232, 204)
ROOF = (146, 58, 44)
WINDOW = (255, 196, 92)
BAND = (11, 44, 58)           # deep teal title band
CREAM = (250, 240, 214)
CREAM_DIM = (214, 196, 158)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


TITLE_FONT = lambda s: font("DejaVuSerif-Bold.ttf", s)
TAG_FONT = lambda s: font("DejaVuSans-Bold.ttf", s)
SMALL_FONT = lambda s: font("DejaVuSans.ttf", s)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_gradient(draw):
    """Paint the sky in three bands blended row by row, 0..640."""
    horizon = 640
    for y in range(horizon):
        if y < 340:
            c = lerp(SKY_TOP, SKY_MID, y / 340.0)
        else:
            c = lerp(SKY_MID, SKY_LOW, (y - 340) / 300.0)
        draw.line([(0, y), (W, y)], fill=c)


def sun(draw):
    """Low golden sun with a soft halo, upper right of the sky.
    The halo fades in many small steps from amber into the teal of the
    sky at this height, so no ring shows."""
    cx, cy, r = 716, 296, 78
    sky_here = lerp(SKY_TOP, SKY_MID, cy / 340.0)
    steps = 48
    for k in range(steps, 0, -1):
        rr = r + k * 110 // steps
        glow = lerp(SUN_RIM, sky_here, 1 - k / steps)
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=glow)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SUN_CORE)
    draw.ellipse([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14],
                 fill=(255, 232, 160))


def cloud(draw, x, y, scale, color):
    """One soft flat-bottomed cloud from overlapping ellipses."""
    parts = [(-90, 0, 90, 34), (-52, -26, 52, 22), (30, -14, 120, 26),
             (-130, 6, -40, 30), (70, 4, 150, 30)]
    for (x0, y0, x1, y1) in parts:
        draw.ellipse([x + x0 * scale, y + y0 * scale,
                      x + x1 * scale, y + y1 * scale], fill=color)


def ridge(draw, points, color):
    draw.polygon(points, fill=color)


def birds(draw):
    for (x, y, s) in [(300, 210, 16), (352, 178, 12), (262, 152, 11),
                      (560, 150, 13), (610, 190, 10)]:
        draw.arc([x - s, y - s // 2, x, y + s // 2], 200, 340, fill=CREAM, width=3)
        draw.arc([x, y - s // 2, x + s, y + s // 2], 200, 340, fill=CREAM, width=3)


def cliff_and_village(draw):
    """The terraced cliff on the left, with a small warm-lit village."""
    # Main rock mass.
    rock = [(60, 640), (120, 520), (150, 470), (210, 430), (300, 400),
            (360, 420), (400, 470), (430, 540), (440, 640)]
    draw.polygon(rock, fill=CLIFF)
    # Sunlit face on the right edge of the rock.
    lit = [(300, 400), (360, 420), (400, 470), (430, 540), (440, 640),
           (380, 640), (360, 520), (320, 460)]
    draw.polygon(lit, fill=CLIFF_LIT)
    # Shadowed face on the left edge.
    dark = [(60, 640), (120, 520), (150, 470), (210, 430), (230, 470),
            (190, 540), (160, 640)]
    draw.polygon(dark, fill=CLIFF_DARK)
    # Terraces.
    for y in (470, 520, 575):
        draw.line([(128, y), (392, y)], fill=CLIFF_DARK, width=5)

    def house(x, y, w, h, roof_h):
        draw.rectangle([x, y, x + w, y + h], fill=HOUSE)
        draw.polygon([(x - 6, y), (x + w // 2, y - roof_h), (x + w + 6, y)],
                     fill=ROOF)
        draw.rectangle([x + w // 2 - 4, y + h - 16, x + w // 2 + 4, y + h],
                       fill=CLIFF_DARK)
        for wx in (x + 6, x + w - 14):
            draw.rectangle([wx, y + 8, wx + 8, y + 16], fill=WINDOW)

    house(168, 424, 52, 40, 22)
    house(248, 420, 60, 44, 26)
    house(322, 428, 48, 38, 20)
    house(196, 478, 56, 42, 24)
    house(292, 482, 62, 42, 22)
    house(150, 532, 54, 42, 22)
    house(252, 536, 58, 40, 24)
    house(336, 540, 50, 38, 20)
    # A lone cypress on the top terrace.
    draw.line([(386, 420), (386, 388)], fill=(30, 60, 40), width=5)
    draw.ellipse([372, 352, 400, 392], fill=(38, 84, 52))


def rising_fall(draw):
    """The waterfall that climbs: a tapering stream from the lagoon
    up into the clouds, with spray and rising droplets."""
    # The stream: a ribbon that starts wide at the lagoon and narrows
    # as it rises, curving gently toward the sun.
    ribbon = [(470, 636), (500, 560), (540, 470), (600, 380), (668, 300),
              (700, 300), (640, 380), (585, 470), (548, 560), (530, 636)]
    draw.polygon(ribbon, fill=FALL)
    core = [(492, 636), (516, 560), (552, 474), (606, 388), (664, 306),
            (682, 306), (628, 386), (574, 472), (538, 560), (514, 636)]
    draw.polygon(core, fill=FALL_CORE)
    # White crest lines inside the stream.
    for (x0, y0, x1, y1) in [(500, 600, 540, 520), (548, 500, 590, 420),
                             (600, 400, 650, 330)]:
        draw.line([(x0, y0), (x1, y1)], fill=(255, 255, 255), width=4)
    # Spray where the stream leaves the lagoon.
    for (x, y, r) in [(470, 622, 16), (500, 630, 20), (536, 626, 14),
                      (452, 632, 10), (552, 634, 10)]:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=MIST)
    # Mist where the stream dissolves into the clouds.
    for (x, y, r) in [(688, 292, 26), (716, 268, 30), (748, 290, 22),
                      (668, 262, 16), (742, 258, 16)]:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=MIST)
    # Rising droplets above the mist, thinning out as they climb.
    for (x, y, r) in [(700, 226, 6), (730, 204, 5), (676, 210, 5),
                      (752, 176, 4), (706, 168, 4), (668, 178, 3),
                      (736, 140, 3)]:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=FALL_CORE)


def lagoon(draw):
    """The lagoon in the foreground, with reflections and a sailboat."""
    draw.rectangle([0, 640, W, 832], fill=LAGOON)
    # Horizontal shimmer streaks.
    streaks = [(80, 668, 300), (420, 690, 520), (640, 664, 380),
               (150, 730, 420), (560, 748, 300), (60, 786, 260),
               (700, 800, 240), (300, 812, 380)]
    for (x, y, ln) in streaks:
        draw.line([(x, y), (x + ln, y)], fill=(120, 190, 200), width=3)
    # Reflection of the rising fall.
    for i, wdt in enumerate((90, 70, 52, 36, 22)):
        y = 652 + i * 26
        draw.line([(500 - wdt // 2, y), (500 + wdt // 2, y)],
                  fill=(170, 215, 222), width=4)
    # Reflection of the sun.
    for i, wdt in enumerate((120, 96, 74, 52, 34)):
        y = 656 + i * 24
        draw.line([(716 - wdt // 2, y), (716 + wdt // 2, y)],
                  fill=(255, 206, 110), width=4)
    # A small sailboat with a cream sail, heading for the cliff.
    bx, by = 830, 700
    draw.polygon([(bx, by - 62), (bx, by - 6), (bx + 44, by - 6)], fill=CREAM)
    draw.polygon([(bx - 4, by - 52), (bx - 4, by - 6), (bx - 34, by - 6)],
                 fill=(232, 214, 178))
    draw.line([(bx, by - 66), (bx, by - 2)], fill=(60, 40, 28), width=4)
    draw.polygon([(bx - 52, by), (bx + 56, by), (bx + 44, by + 18),
                  (bx - 40, by + 18)], fill=(96, 46, 34))
    draw.line([(bx - 60, by + 20), (bx + 64, by + 20)],
              fill=(170, 215, 222), width=3)


def tracked(draw, text, fnt, cx, y, color, tracking):
    """Draw text centred on cx with extra space between letters."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, wdt in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=color)
        x += wdt + tracking


def title_band(draw):
    """The deep teal band carrying the place name and tagline."""
    draw.rectangle([0, 832, W, H], fill=BAND)
    draw.line([(0, 832), (W, 832)], fill=CREAM, width=3)
    title = TITLE_FONT(118)
    tw = draw.textlength("VELMORA", font=title)
    draw.text(((W - tw) / 2, 852), "VELMORA", font=title, fill=CREAM)
    tag = "WHERE THE WATERFALLS CLIMB THE SKY"
    tag_fnt = TAG_FONT(25)
    widths = [draw.textlength(ch, font=tag_fnt) for ch in tag]
    total = sum(widths) + 5 * (len(tag) - 1)
    mid_y = 972 + 12
    draw.line([(70, mid_y), (W // 2 - total / 2 - 26, mid_y)],
              fill=CREAM_DIM, width=2)
    draw.line([(W // 2 + total / 2 + 26, mid_y), (W - 70, mid_y)],
              fill=CREAM_DIM, width=2)
    tracked(draw, tag, tag_fnt, W // 2, 972, CREAM_DIM, 5)


def frame(draw):
    draw.rectangle([22, 22, W - 22, H - 22], outline=CREAM, width=4)


def main():
    img = Image.new("RGB", (W, H), SKY_TOP)
    draw = ImageDraw.Draw(img)
    sky_gradient(draw)
    sun(draw)
    cloud(draw, 180, 150, 1.0, (244, 226, 196))
    cloud(draw, 830, 120, 0.7, (250, 238, 214))
    cloud(draw, 480, 96, 0.55, (238, 220, 190))
    birds(draw)
    # Far ridge, then nearer ridge, both behind the cliff and lagoon.
    ridge(draw, [(0, 640), (0, 590), (120, 556), (260, 600), (420, 566),
                 (560, 606), (720, 572), (880, 604), (1024, 576),
                 (1024, 640)], RIDGE_FAR)
    ridge(draw, [(0, 640), (0, 612), (180, 588), (360, 618), (560, 592),
                 (760, 620), (1024, 596), (1024, 640)], RIDGE_NEAR)
    cliff_and_village(draw)
    rising_fall(draw)
    lagoon(draw)
    title_band(draw)
    frame(draw)
    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
