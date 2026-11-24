#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: a one-page newspaper front page
summing up Tuesday 24 November 2026 world news.

Stories were researched from world news wires on 24 Nov 2026 (all events
that happened or were first reported that day):
  HERO   Ukraine sea drones sink the Russian corvette Merkury off Libya
         (Zelenskyy confirms) -- war at sea reaches the Mediterranean.
  MARKET Nvidia: Jensen Huang returns as CEO, shares jump about a third.
  CARDS  Kyiv/Odesa strikes; Banten factory fire (24 dead); Lisbon
         cost-of-living march; COP31 fossil-fuel deadlock in Antalya;
         Mexico captures 'El Chapo Isidro'; US sanctions Iran shadow banks.
  TICKER Vanuatu 6.5 quake; Seoul names new ministers; ICJ Rohingya ruling
         backed by 14 states; India-Nepal rail link opens; Ferrari 296 duo.

Output: 1024x1024 PNG, flat clean design, high-contrast text.
Run: python3 draw.py  -> writes entry.png beside this file.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)      # warm newsprint
INK = (18, 28, 44)           # near-black navy
NAVY = (15, 42, 74)
NAVY2 = (23, 64, 110)
GOLD = (198, 154, 52)
RED = (178, 34, 34)
GREEN = (27, 120, 70)
TEAL = (14, 110, 110)
ORANGE = (204, 92, 16)
GREY = (74, 82, 94)
LIGHT = (255, 255, 255)
MINT = (226, 240, 230)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FD}/{name}", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading=None):
    """Draw lines; return y below last line."""
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def rrect(draw, box, radius, **kw):
    draw.rounded_rectangle(box, radius=radius, **kw)


# ---------------------------------------------------------------- icons
def icon_burst(d, cx, cy, r, fill):
    """Starburst / explosion pictogram."""
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill)


def icon_flame(d, cx, cy, r, fill):
    d.polygon([(cx, cy - r), (cx + r * 0.75, cy - r * 0.1),
               (cx + r * 0.55, cy + r * 0.55), (cx + r * 0.2, cy + r * 0.85),
               (cx - r * 0.25, cy + r * 0.85), (cx - r * 0.6, cy + r * 0.5),
               (cx - r * 0.7, cy - r * 0.15)], fill=fill)
    d.ellipse([cx - r * 0.28, cy + r * 0.1, cx + r * 0.28, cy + r * 0.75],
              fill=(255, 214, 90))


def icon_crowd(d, cx, cy, r, fill):
    for dx, dy, rr in [(-r * 0.55, -r * 0.25, r * 0.34),
                       (r * 0.55, -r * 0.25, r * 0.34),
                       (0, -r * 0.45, r * 0.38)]:
        d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                  fill=fill)
    d.pieslice([cx - r, cy - r * 0.05, cx + r, cy + r * 1.05], 180, 360,
               fill=fill)


def icon_globe(d, cx, cy, r, fill):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fill, width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=fill,
              width=3)
    d.line([cx - r, cy, cx + r, cy], fill=fill, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360, fill=fill,
          width=3)


def icon_shield(d, cx, cy, r, fill):
    d.polygon([(cx, cy - r), (cx + r * 0.85, cy - r * 0.55),
               (cx + r * 0.7, cy + r * 0.45), (cx, cy + r),
               (cx - r * 0.7, cy + r * 0.45), (cx - r * 0.85, cy - r * 0.55)],
              fill=fill)
    d.text((cx, cy - r * 0.42), "*", font=SANS_B(int(r * 0.9)),
           fill=(255, 255, 255), anchor="mm")


def icon_bank(d, cx, cy, r, fill):
    d.polygon([(cx - r, cy - r * 0.25), (cx, cy - r * 0.85),
               (cx + r, cy - r * 0.25)], fill=fill)
    for dx in (-r * 0.62, 0, r * 0.62):
        d.rectangle([cx + dx - r * 0.13, cy - r * 0.12,
                     cx + dx + r * 0.13, cy + r * 0.62], fill=fill)
    d.rectangle([cx - r, cy + r * 0.68, cx + r, cy + r * 0.88], fill=fill)


ICONS = {"burst": icon_burst, "flame": icon_flame, "crowd": icon_crowd,
         "globe": icon_globe, "shield": icon_shield, "bank": icon_bank}


# ---------------------------------------------------------------- hero art
def hero_art(d, x0, y0, x1, y1):
    """Flat illustration: warship burning at sea, drone boat approaching."""
    d.rectangle([x0, y0, x1, y1], fill=(24, 68, 110))
    # sky glow + sun
    d.ellipse([x1 - 105, y0 + 18, x1 - 35, y0 + 88], fill=(255, 214, 90))
    # smoke
    for (sx, sy, sr) in [(x0 + 150, y0 + 62, 26), (x0 + 185, y0 + 38, 32),
                         (x0 + 228, y0 + 22, 24)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 128, 138))
    # sea
    sea_y = y0 + int((y1 - y0) * 0.52)
    d.rectangle([x0, sea_y, x1, y1], fill=(13, 48, 84))
    for wy in (sea_y + 38, sea_y + 78, sea_y + 118):
        for wx in range(x0 + 10, x1 - 20, 64):
            d.arc([wx, wy, wx + 44, wy + 18], 180, 360, fill=(90, 150, 200),
                  width=4)
    # warship hull + superstructure (dark silhouette)
    hull_y = sea_y + 6
    d.polygon([(x0 + 30, hull_y + 34), (x0 + 300, hull_y + 34),
               (x0 + 268, hull_y + 62), (x0 + 62, hull_y + 62)],
              fill=(12, 20, 32))
    d.rectangle([x0 + 120, hull_y - 6, x0 + 210, hull_y + 34],
                fill=(12, 20, 32))
    d.rectangle([x0 + 168, hull_y - 30, x0 + 188, hull_y - 6],
                fill=(12, 20, 32))
    # fire on deck
    d.polygon([(x0 + 138, hull_y - 4), (x0 + 158, hull_y - 52),
               (x0 + 176, hull_y - 4)], fill=(255, 140, 30))
    d.polygon([(x0 + 150, hull_y - 4), (x0 + 160, hull_y - 30),
               (x0 + 170, hull_y - 4)], fill=(255, 214, 90))
    # drone boat, bottom right
    bx, by = x1 - 108, y1 - 46
    d.polygon([(bx, by), (bx + 72, by), (bx + 58, by + 16), (bx + 12, by + 16)],
              fill=(200, 210, 220))
    d.rectangle([bx + 26, by - 12, bx + 46, by], fill=(200, 210, 220))
    d.line([bx + 36, by - 26, bx + 36, by - 12], fill=(200, 210, 220),
           width=3)
    # caption chip
    d.rounded_rectangle([x0 + 14, y1 - 34, x0 + 250, y1 - 10], radius=8,
                        fill=(10, 26, 46))
    d.text((x0 + 24, y1 - 31), "THE MERKURY, OFF BENGHAZI",
           font=SANS_B(14), fill=(255, 255, 255))


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)

    # ---- masthead
    d.rectangle([10, 10, W - 11, 132], fill=NAVY)
    d.text((W // 2, 18), "THE WORLD TODAY", font=SERIF_B(58),
           fill=(255, 255, 255), anchor="ma")
    d.line([70, 94, W - 70, 94], fill=GOLD, width=3)
    d.text((W // 2, 102), "TUESDAY, 24 NOVEMBER 2026  •  ONE DAY, ONE PAGE",
           font=SANS_B(20), fill=(232, 196, 106), anchor="ma")

    # ---- hero: war at sea
    d.text((44, 146), "WAR AT SEA  •  UKRAINE — LIBYA",
           font=SANS_B(21), fill=RED)
    hero_lines = ["UKRAINE SINKS", "RUSSIAN WARSHIP", "OFF LIBYA"]
    y = 174
    y = text_block(d, 44, y, hero_lines, SANS_B(54), INK, leading=58)
    deck = wrap(d, "Zelenskyy confirms sea drones destroyed the "
                   "corvette Merkury off Benghazi.", SANS(23), 560)
    y = text_block(d, 44, y + 10, deck, SANS(23), GREY, leading=30)
    hero_art(d, 628, 146, 980, 424)
    d.line([44, 434, 980, 434], fill=(180, 170, 150), width=2)

    # ---- markets strip
    rrect(d, [36, 448, 988, 526], 10, fill=MINT)
    d.rectangle([36, 448, 48, 526], fill=GREEN)
    d.text((66, 458), "MARKETS  •  WALL STREET", font=SANS_B(19),
           fill=GREEN)
    d.text((66, 484), "NVIDIA SOARS AS HUANG RETURNS AS CEO",
           font=SANS_B(26), fill=INK)
    d.text((968, 484), "SHARES +33%", font=SANS_B(24), fill=GREEN,
           anchor="ra")
    d.text((968, 460), "FOUNDER BACK", font=SANS_B(15), fill=GREY,
           anchor="ra")

    # ---- story cards
    cards = [
        ("burst", RED, "RUSSIA — UKRAINE",
         "Kyiv region hit as Russian drones strike",
         "Odesa loses power, heat and water; several missing."),
        ("flame", ORANGE, "INDONESIA",
         "Factory fire kills 24 in Banten",
         "Rescue teams search the sweets factory after the blaze."),
        ("crowd", TEAL, "EUROPE",
         "Thousands march in Lisbon on living costs",
         "Lisbon fills with protesters as prices squeeze households."),
        ("globe", GREEN, "CLIMATE — COP31",
         "Antalya climate talks stall on fossil fuels",
         "Negotiators split over phasing out oil, gas and coal."),
        ("shield", NAVY2, "AMERICAS — MEXICO",
         "Mexico captures 'El Chapo Isidro'",
         "Raid that caught the Sinaloa figure leaves 16 suspects dead."),
        ("bank", (120, 60, 140), "UNITED STATES",
         "US hits Iran 'shadow banks'",
         "Washington sanctions networks it says move Tehran's money."),
    ]
    cw, ch, gx, gy = 304, 176, 16, 14
    x0, y0 = 36, 536
    for i, (icon, colour, kicker, head, body) in enumerate(cards):
        cx = x0 + (i % 3) * (cw + gx)
        cy = y0 + (i // 3) * (ch + gy)
        rrect(d, [cx, cy, cx + cw, cy + ch], 10, fill=LIGHT,
              outline=(200, 192, 176), width=2)
        d.rectangle([cx + 10, cy + 10, cx + cw - 10, cy + 16], fill=colour)
        # icon chip
        ix, iy, ir = cx + 40, cy + 46, 21
        d.ellipse([ix - ir - 4, iy - ir - 4, ix + ir + 4, iy + ir + 4],
                  fill=colour)
        ICONS[icon](d, ix, iy, ir - 4, (255, 255, 255))
        d.text((cx + 74, cy + 34), kicker, font=SANS_B(16), fill=colour)
        hl = wrap(d, head, SANS_B(21), cw - 28)
        yy = text_block(d, cx + 14, cy + 74, hl[:2], SANS_B(21), INK,
                        leading=24)
        bl = wrap(d, body, SANS(16), cw - 28)
        text_block(d, cx + 14, yy + 4, bl[:2], SANS(16), GREY, leading=19)

    # ---- footer ticker
    d.line([44, 914, 980, 914], fill=(180, 170, 150), width=2)
    d.text((44, 924), "ALSO TODAY:", font=SANS_B(17), fill=RED)
    tick = ("Vanuatu 6.5 quake, no tsunami threat  •  Seoul names a new "
            "foreign minister  •  14 states back the ICJ Rohingya ruling  "
            "•  India–Nepal rail link opens  •  Ferrari unveils two 296s")
    tl = wrap(d, tick, SANS(15), 790)
    text_block(d, 190, 924, tl[:2], SANS(15), INK, leading=19)
    d.text((W // 2, 974), "Compiled from world news wires  •  Tuesday 24 November 2026",
           font=SANS(13), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
