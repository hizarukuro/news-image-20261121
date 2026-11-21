#!/usr/bin/env python3
"""
Saturday front page v2 - one square page for Saturday 21 November 2026.
Clean-room renderer (PIL only). Every number on the page comes from ONE
ordered story list: heroes 1-3, grid 4-13, briefs 14-35. Map pins and the
region bar read the same list, so numbering cannot drift.
Drawn at 2x (2048) and downscaled to 1024x1024.
"""
from PIL import Image, ImageDraw, ImageFont
import math

S = 2
W = H = 1024 * S
M = 56
CW = W - 2 * M

PAPER = (247, 241, 227)
INK = (26, 23, 18)
RED = (168, 32, 22)
DARKRED = (128, 24, 16)
GREY = (92, 84, 72)
RULE = (26, 23, 18)

FD = "/usr/share/fonts/truetype/noto/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_BLACK = "NotoSerifDisplay-Black.ttf"
SERIF_B = "NotoSerif-Bold.ttf"
SERIF = "NotoSerif-Regular.ttf"
SERIF_I = "NotoSerif-Italic.ttf"
SANS_B = "NotoSans-Bold.ttf"
SANS_SB = "NotoSans-SemiBold.ttf"
SANS = "NotoSans-Regular.ttf"

# ---------------------------------------------------------------- stories
STORIES = [
 dict(kind="hero", place="ANTALYA, TÜRKIYE", field="CLIMATE", region="AS",
      chip="COP31: OVERTIME", tag="No deal yet · day 13",
      headline="Climate talks run past their deadline",
      deck="COP31 missed its Friday close as nearly 200 countries split "
           "over a draft with no mention of fossil fuels. A third text was "
           "due Saturday morning.",
      source="(AP, AFP)", status="CONFIRMED", art="cop", pin=(30.7, 36.9)),
 dict(kind="hero", place="RIYADH, SAUDI ARABIA", field="WAR", region="ME",
      chip="RIYADH: MISSILES DOWN", tag="Coalition statement",
      headline="Three Houthi missiles downed over Riyadh",
      deck="The Saudi-led coalition said three ballistic missiles aimed at "
           "the capital were destroyed before dawn, after a 1:53 a.m. "
           "air-threat alert. No casualties reported.",
      source="(Reuters, AFP)", status="OFFICIAL", art="riyadh",
      pin=(46.7, 24.6)),
 dict(kind="hero", place="CARHUAMAYO, PERU", field="EARTHQUAKE", region="AM",
      chip="PERU: QUAKE 6.7", tag="00:09 UTC · 108 km deep",
      headline="Deep quake rattles central Peru",
      deck="The magnitude 6.7 tremor struck 9 km from Carhuamayo at 00:09 "
           "UTC, 108 km down. Felt in Lima; Peru's institute reported no "
           "deaths and no tsunami risk.",
      source="(USGS, IGP)", status="OFFICIAL", art="peru",
      pin=(-76.0, -10.9)),
 dict(kind="grid", place="KYIV", field="WAR", region="EU",
      chip="KYIV: WARNING",
      headline="Zelensky: Crimea bridge \u201cwill not stay\u201d",
      deck="He warns Russia is stepping up double-tap strikes on rescuers.",
      source="(NBC)", status="REPORTED", art="kyiv", pin=(30.5, 50.4)),
 dict(kind="grid", place="STRAIT OF HORMUZ", field="WAR", region="ME",
      chip="HORMUZ: DRONE",
      headline="Iran says it downed a US drone",
      deck="The IRGC calls it the 58th MQ-9; Washington has not confirmed it.",
      source="(IRIB)", status="CLAIM", art="hormuz", pin=(58.5, 24.5)),
 dict(kind="grid", place="TEHRAN", field="DIPLOMACY", region="ME",
      chip="IRAN: URANIUM",
      headline="Iran: uranium stock stays at home",
      deck="The reserves serve national needs; a \u201cfair solution\u201d "
           "is still sought.",
      source="(Tasnim)", status="OFFICIAL", art="tehran", pin=(51.4, 35.7)),
 dict(kind="grid", place="WASHINGTON", field="TECHNOLOGY", region="AM",
      chip="TRUMP: AI TAX",
      headline="Trump vows tax on data centres abroad",
      deck="\u201cTremendous\u201d penalty promised; no rate or details yet.",
      source="(Reuters)", status="REPORTED", art="trump", pin=(-77.0, 38.9)),
 dict(kind="grid", place="BEIJING", field="DIPLOMACY", region="AS",
      chip="CHINA\u2013JAPAN",
      headline="China tells Japan to \u201ccorrect\u201d Taiwan words",
      deck="Tokyo says its stance is unchanged.",
      source="(Ministry, AFP)", status="OFFICIAL", art="chinajapan",
      pin=(116.4, 39.9)),
 dict(kind="grid", place="DAVAO", field="AVIATION", region="AS",
      chip="DAVAO: ALL SAFE",
      headline="Jet lands safely after engine fire alert",
      deck="Air Niugini's 767 diverted after midnight and landed safely.",
      source="(AP)", status="CONFIRMED", art="davao", pin=(125.6, 7.1)),
 dict(kind="grid", place="CANBERRA", field="DIPLOMACY", region="OC",
      chip="CANBERRA: AI TALKS",
      headline="Australia and China agree to AI talks",
      deck="A formal dialogue on AI safety; Albanese ends an 11-day trip.",
      source="(ABC)", status="OFFICIAL", art="canberra", pin=(149.1, -35.3)),
 dict(kind="grid", place="WORLD", field="MARKETS", region="GL",
      chip="BITCOIN: BELOW $59K",
      headline="Bitcoin trades below $59,000",
      deck="Ether near $1,619 as the slide deepened early Saturday.",
      source="(CoinGecko)", status="CONFIRMED", art="bitcoin",
      pin=(-150.0, -48.0)),
 dict(kind="grid", place="LAS VEGAS", field="FORMULA ONE", region="AM",
      chip="RUSSELL: FASTEST",
      headline="Russell fastest in final practice",
      deck="1:34.041, a Mercedes one-two in a messy final session.",
      source="(Formula 1)", status="CONFIRMED", art="vegas",
      pin=(-115.1, 36.2)),
 dict(kind="grid", place="WELLINGTON", field="CRICKET", region="OC",
      chip="RAHUL: CENTURY",
      headline="Rahul's century puts India on top",
      deck="India 344 for 2 at tea on day three, replying to 368.",
      source="(AFP)", status="CONFIRMED", art="cricket", pin=(174.8, -41.3)),
]
BRIEFS = [
 ("Kryvyi Rih", "28 still in hospital after double strike kills 2, injures 42", "Kyiv Independent"),
 ("Copenhagen", "Russia's defence attaché expelled over a foiled plot", "Reuters"),
 ("Antalya", "EU warns COP31 risks a \u201cfossil summit\u201d label", "AFP"),
 ("Antalya", "Panama threatens to walk away over the fossil-free text", "AFP"),
 ("Antalya", "Indonesia's PLN signs six clean-power deals", "Antara"),
 ("Yemen", "Houthis threaten Jeddah and Red Sea ports", "Al Jazeera"),
 ("Washington", "Vance says the Iran strikes were Trump's decision", "Reuters"),
 ("Washington", "Lawmaker threatens SpaceX funding over Starshield", "CNN"),
 ("Texas", "Execution of a man of 70 takes 63 minutes", "AP"),
 ("Los Angeles", "Jury convicts man of starting the Palisades fire", "AP"),
 ("Missouri", "Judge approves $7.25bn Roundup settlement", "AP"),
 ("Vancouver", "Canada rests its defence in youth climate trial", "AFP"),
 ("Pyongyang", "Kim tours factories after no Trump meeting", "KCNA"),
 ("Sejong", "Freight train derails at dawn; no one hurt", "Yonhap"),
 ("Taipei", "NT$20,000 cash payout for every citizen approved", "Taipei Times"),
 ("Bangkok", "Six-point plan on arsenic in two rivers", "The Nation"),
 ("New Delhi", "Pakistani minister joins SCO forum in India", "Dawn"),
 ("Eastern India", "Rain alerts as Akvan's remnants move inland", "IMD"),
 ("Naypyidaw", "Rights groups urge sanctions after genocide ruling", "AP"),
 ("Port Louis", "African rating agency talks to 15 states", "Al Jazeera"),
 ("Melbourne", "Cummins keeps the Australian captaincy", "ABC"),
 ("Las Vegas", "Verstappen warned after contact in practice", "AP"),
]
BRIEF_REGIONS = ["EU", "EU", "AS", "AS", "AS", "ME", "AM", "AM", "AM", "AM",
                 "AM", "AM", "AS", "AS", "AS", "AS", "AS", "AS", "AS", "AF",
                 "OC", "AM"]

STATS = [
 ("13", "COP31 DAY 13 \u2014 PAST ITS FRIDAY CLOSE"),
 ("3", "MISSILES DOWNED OVER RIYADH"),
 ("6.7", "MAGNITUDE OF THE PERU QUAKE"),
 ("146", "PEOPLE SAFE AFTER THE DAVAO LANDING"),
 ("$58,810", "BITCOIN EARLY SATURDAY, DOWN 4.1% IN A DAY"),
 ("124*", "K L RAHUL'S SCORE AT TEA IN WELLINGTON"),
]

REGIONS = [
 ("AM", "AMERICAS", (109, 91, 168)),
 ("EU", "EUROPE", (62, 111, 176)),
 ("AF", "AFRICA", (78, 141, 90)),
 ("ME", "MIDDLE EAST", (179, 84, 63)),
 ("AS", "ASIA", (203, 148, 57)),
 ("OC", "OCEANIA", (63, 141, 132)),
 ("GL", "GLOBAL", (133, 133, 140)),
]

DATE_CHECK = ("Left out as other days' news: Wall Street's fall into "
 "correction (Friday) \u00b7 the barrage that hit Kyiv's bridges (Friday) "
 "\u00b7 the missile in Poland (Friday) \u00b7 the World Court's Myanmar "
 "ruling (Thursday) \u00b7 the UK\u2013EU deal (Friday) \u00b7 Akvan's "
 "landfall (Friday) \u00b7 the Shenzhen summit (Thursday). Older: Voyager "
 "1's light-day (18 Nov). Unconfirmed when drawn: a final COP31 text "
 "\u00b7 US word on the drone claim.")

TOTAL = len(STORIES) + len(BRIEFS)

def region_counts():
    counts = {c: 0 for c, _, _ in REGIONS}
    for s in STORIES:
        counts[s["region"]] += 1
    for r in BRIEF_REGIONS:
        counts[r] += 1
    assert sum(counts.values()) == TOTAL
    return counts

# ---------------------------------------------------------------- helpers
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

def tw(font, text):
    return d.textlength(text, font=font)

def fit_font(name, text, maxw, start):
    size = start
    while size > 10 and tw(F(name, size), text) > maxw:
        size -= 2
    return F(name, size)

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(font, t) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def spaced_w(text, font, tracking):
    return sum(tw(font, ch) + tracking for ch in text) - tracking

def draw_spaced(x, y, text, font, fill, tracking=1):
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += tw(font, ch) + tracking

def chip(x, y, text, font):
    w_ = tw(font, text) + 20
    d.rectangle([x, y, x + w_, y + font.size + 12], fill=RED)
    d.text((x + 10, y + 4), text, font=font, fill=(255, 255, 255))

def tag(x, y, text, font):
    w_ = tw(font, text) + 18
    d.rectangle([x, y, x + w_, y + font.size + 10], fill=(24, 26, 34, 235))
    d.text((x + 9, y + 3), text, font=font, fill=(255, 255, 255))

def pill_right(x_right, y, text):
    f = F(SANS_B, 18)
    w_ = tw(f, text) + 18
    d.rounded_rectangle([x_right - w_, y, x_right, y + 26], radius=12,
                        outline=RED, width=2)
    d.text((x_right - w_ + 9, y + 3), text, font=f, fill=RED)

def num_badge(x, y, n, diam=32):
    d.ellipse([x, y, x + diam, y + diam], fill=RED)
    f = F(SANS_B, 20 if n < 10 else 18)
    t = str(n)
    d.text((x + (diam - tw(f, t)) / 2, y + diam / 2 - f.size / 2 - 2), t,
           font=f, fill=(255, 255, 255))

# ---------------------------------------------------------------- art
def art_cop(x, y, w_, h):
    d.rectangle([x, y, x + w_, y + h], fill=(203, 226, 205))
    d.ellipse([x + 24, y + 26, x + 168, y + 170], fill=(70, 130, 190))
    d.polygon([(x + 56, y + 62), (x + 106, y + 48), (x + 124, y + 82),
               (x + 86, y + 104), (x + 54, y + 88)], fill=(96, 168, 96))
    d.polygon([(x + 84, y + 118), (x + 124, y + 110), (x + 134, y + 140),
               (x + 96, y + 152)], fill=(96, 168, 96))
    cx = x + w_ - 196
    d.rounded_rectangle([cx, y + 20, cx + 30, y + h - 52], radius=15,
                        outline=INK, width=5)
    d.rectangle([cx + 10, y + 62, cx + 20, y + h - 62], fill=RED)
    d.ellipse([cx - 11, y + h - 92, cx + 41, y + h - 40], fill=RED)
    for i in range(4):
        yy = y + 40 + i * 28
        d.line([cx + 36, yy, cx + 52, yy], fill=INK, width=4)
    cx2 = x + w_ - 106
    d.ellipse([cx2, y + 24, cx2 + 76, y + 100], fill=(255, 255, 255),
              outline=INK, width=5)
    d.line([cx2 + 38, y + 62, cx2 + 38, y + 40], fill=INK, width=5)
    d.line([cx2 + 38, y + 62, cx2 + 56, y + 72], fill=INK, width=5)

def art_riyadh(x, y, w_, h):
    d.rectangle([x, y, x + w_, y + h], fill=(16, 24, 48))
    for sx, sy in [(40, 24), (150, 46), (300, 20), (470, 38), (560, 24)]:
        d.ellipse([x + sx, y + sy, x + sx + 5, y + sy + 5],
                  fill=(255, 255, 240))
    base = y + h
    for bx, bw, bh in [(0, 74, 74), (82, 58, 104), (148, 88, 62),
                       (244, 62, 116), (314, 96, 78), (418, 60, 96),
                       (486, 84, 66), (578, 48, 84)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(8, 12, 26))
        for wy in range(int(base - bh) + 10, int(base) - 8, 20):
            for wx in range(int(x + bx) + 9, int(x + bx + bw) - 12, 18):
                d.rectangle([wx, wy, wx + 7, wy + 9], fill=(250, 205, 90))
    for (x0, y0, x1, y1, x2, y2) in [(70, 158, 300, 52, 520, 122),
                                    (30, 122, 260, 32, 470, 98),
                                    (120, 170, 340, 78, 580, 144)]:
        pts = []
        for t in [i / 24 for i in range(25)]:
            px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * x1 + t ** 2 * x2
            py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * y1 + t ** 2 * y2
            pts.append((x + px, y + py))
        d.line(pts, fill=(255, 220, 130), width=3)
        ex, ey = x + x2, y + y2
        for a in range(8):
            ang = a * math.pi / 4
            d.line([ex, ey, ex + 17 * math.cos(ang), ey + 17 * math.sin(ang)],
                   fill=(255, 170, 60), width=4)
        d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 200, 80))

def art_peru(x, y, w_, h):
    d.rectangle([x, y, x + w_, y + h], fill=(238, 226, 196))
    d.polygon([(x, y + h), (x + 140, y + 62), (x + 290, y + h)],
              fill=(168, 120, 78))
    d.polygon([(x + 200, y + h), (x + 366, y + 48), (x + 520, y + h)],
              fill=(146, 100, 62))
    d.polygon([(x + 342, y + 66), (x + 366, y + 48), (x + 390, y + 66)],
              fill=(255, 255, 255))
    for hx, hy, hw in [(416, 138, 68), (502, 152, 56)]:
        d.rectangle([x + hx, y + hy, x + hx + hw, y + hy + 44],
                    fill=(250, 248, 240))
        d.polygon([(x + hx - 7, y + hy), (x + hx + hw / 2, y + hy - 26),
                   (x + hx + hw + 7, y + hy)], fill=(150, 60, 40))
    pts = []
    for i in range(121):
        px = x + 16 + i * (w_ - 32) / 120
        amp = 6 + 20 * math.exp(-((i - 46) / 13) ** 2) \
            + 14 * math.exp(-((i - 74) / 9) ** 2)
        py = y + h - 34 + amp * math.sin(i * 1.15) * 0.6 \
            + 9 * math.sin(i * 0.9)
        pts.append((px, py))
    d.line(pts, fill=RED, width=4)

def art_strip(kind, x, y, w_, h):
    if kind == "kyiv":
        d.rectangle([x, y, x + w_, y + h / 2], fill=(240, 205, 70))
        d.rectangle([x, y + h / 2, x + w_, y + h], fill=(70, 120, 185))
        d.arc([x + 34, y + 20, x + w_ - 34, y + h + 40], 180, 360,
              fill=INK, width=5)
        d.line([x + 34, y + h - 6, x + w_ - 34, y + h - 6], fill=INK, width=5)
    elif kind == "hormuz":
        d.rectangle([x, y, x + w_, y + h], fill=(90, 150, 180))
        d.rectangle([x, y + h - 20, x + w_, y + h], fill=(40, 90, 130))
        d.polygon([(x + 84, y + h - 20), (x + 112, y + h - 42),
                   (x + 268, y + h - 42), (x + 286, y + h - 20)],
                  fill=(30, 30, 36))
        d.rectangle([x + 142, y + h - 58, x + 226, y + h - 42],
                    fill=(190, 60, 40))
        cx, cy = x + w_ - 84, y + 22
        d.ellipse([cx - 11, cy - 7, cx + 11, cy + 7], fill=(30, 30, 36))
        for dx, dy in [(-27, -12), (27, -12), (-27, 12), (27, 12)]:
            d.line([cx, cy, cx + dx, cy + dy], fill=(30, 30, 36), width=3)
            d.ellipse([cx + dx - 8, cy + dy - 4, cx + dx + 8, cy + dy + 4],
                      outline=(30, 30, 36), width=3)
    elif kind == "tehran":
        d.rectangle([x, y, x + w_, y + h], fill=(24, 70, 74))
        cx, cy = x + w_ / 2, y + h / 2
        for a in range(3):
            ang = a * math.pi / 3 + 0.3
            pts = []
            for t in range(41):
                th = t / 40 * 2 * math.pi
                ex = 46 * math.cos(th)
                ey = 17 * math.sin(th)
                rx = ex * math.cos(ang) - ey * math.sin(ang)
                ry = ex * math.sin(ang) + ey * math.cos(ang)
                pts.append((cx + rx, cy + ry))
            d.line(pts, fill=(240, 200, 90), width=4)
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED)
    elif kind == "trump":
        d.rectangle([x, y, x + w_, y + h], fill=(24, 34, 64))
        f = F(SANS_B, 62)
        d.text((x + 22, y + 6), "%", font=f, fill=(250, 205, 90))
        for i, bh in enumerate([30, 46, 36, 56]):
            bx = x + 124 + i * 54
            d.rectangle([bx, y + h - 12 - bh, bx + 36, y + h - 12],
                        fill=(110, 150, 200))
        d.line([x + 112, y + h - 10, x + w_ - 14, y + h - 10],
               fill=(255, 255, 255), width=3)
    elif kind == "chinajapan":
        d.rectangle([x, y, x + w_ / 2, y + h], fill=(206, 44, 36))
        d.rectangle([x + w_ / 2, y, x + w_, y + h], fill=(248, 246, 240))
        d.ellipse([x + w_ / 4 - 17, y + h / 2 - 17, x + w_ / 4 + 17,
                   y + h / 2 + 17], fill=(250, 205, 60))
        d.ellipse([x + 3 * w_ / 4 - 19, y + h / 2 - 19, x + 3 * w_ / 4 + 19,
                   y + h / 2 + 19], fill=(190, 30, 45))
    elif kind == "davao":
        d.rectangle([x, y, x + w_, y + h], fill=(120, 180, 225))
        d.polygon([(x + 56, y + 46), (x + 236, y + 30), (x + 284, y + 42),
                   (x + 112, y + 60)], fill=(245, 245, 245))
        d.polygon([(x + 112, y + 34), (x + 140, y + 14), (x + 164, y + 16),
                   (x + 148, y + 36)], fill=RED)
        d.rectangle([x, y + h - 13, x + w_, y + h], fill=(70, 70, 76))
        for i in range(7):
            d.rectangle([x + 16 + i * 50, y + h - 8, x + 40 + i * 50,
                         y + h - 4], fill=(250, 205, 90))
    elif kind == "canberra":
        d.rectangle([x, y, x + w_, y + h], fill=(238, 230, 208))
        d.rounded_rectangle([x + 40, y + 12, x + 182, y + 50], radius=11,
                            fill=(63, 141, 132))
        d.polygon([(x + 62, y + 50), (x + 80, y + 50), (x + 62, y + 66)],
                  fill=(63, 141, 132))
        d.rounded_rectangle([x + 176, y + 34, x + 318, y + 72], radius=11,
                            fill=(190, 60, 40))
        d.polygon([(x + 296, y + 72), (x + 278, y + 72), (x + 296, y + 86)],
                  fill=(190, 60, 40))
        for bx in (62, 90, 118):
            d.ellipse([x + bx, y + 26, x + bx + 9, y + 35],
                      fill=(255, 255, 255))
        for bx in (208, 236, 264):
            d.ellipse([x + bx, y + 48, x + bx + 9, y + 57],
                      fill=(255, 255, 255))
    elif kind == "bitcoin":
        d.rectangle([x, y, x + w_, y + h], fill=(250, 244, 228))
        cx, cy = x + 72, y + h / 2
        d.ellipse([cx - 31, cy - 31, cx + 31, cy + 31], fill=(242, 146, 30))
        f = F(SANS_B, 44)
        d.text((cx - tw(f, "B") / 2, cy - 26), "B", font=f,
               fill=(255, 255, 255))
        d.line([cx - 7, cy - 29, cx - 7, cy + 29], fill=(255, 255, 255),
               width=4)
        d.line([cx + 5, cy - 29, cx + 5, cy + 29], fill=(255, 255, 255),
               width=4)
        pts = [(x + 140, y + 18), (x + 188, y + 30), (x + 226, y + 24),
               (x + 268, y + 44), (x + 312, y + 60)]
        d.line(pts, fill=RED, width=5)
        d.polygon([(x + 312, y + 60), (x + 297, y + 58), (x + 308, y + 47)],
                  fill=RED)
    elif kind == "vegas":
        d.rectangle([x, y, x + w_, y + h], fill=(52, 52, 60))
        d.polygon([(x + 150, y), (x + 222, y), (x + w_, y + h),
                   (x + 40, y + h)], fill=(30, 30, 36))
        for t in (0.16, 0.38, 0.62, 0.86):
            cx0 = 186 + ((40 + w_) / 2 - 186) * t
            cy0 = t * h
            cx1 = 186 + ((40 + w_) / 2 - 186) * (t + 0.09)
            cy1 = (t + 0.09) * h
            d.line([x + cx0, y + cy0, x + cx1, y + cy1],
                   fill=(250, 205, 90), width=max(2, int(2 + 5 * t)))
        for r in range(2):
            for c in range(4):
                col = (240, 240, 240) if (r + c) % 2 == 0 else (20, 20, 20)
                d.rectangle([x + w_ - 62 + c * 14, y + 6 + r * 14,
                             x + w_ - 48 + c * 14, y + 20 + r * 14], fill=col)
    elif kind == "cricket":
        d.rectangle([x, y, x + w_, y + h], fill=(84, 148, 74))
        d.rectangle([x + 124, y + 9, x + 232, y + h - 9], fill=(216, 190, 140))
        d.line([x + 240, y + 56, x + 306, y + 16], fill=(120, 74, 30),
               width=6)
        d.ellipse([x + 274, y + 50, x + 292, y + 68], fill=RED)
        for sx in (142, 176, 210):
            d.line([x + sx, y + 15, x + sx, y + 27], fill=(90, 60, 30),
                   width=4)

# ---------------------------------------------------------------- page
y = 26
strap_f = F(SANS_B, 24)
d.text((M, y), "THE WORLD IN ONE DAY", font=strap_f, fill=DARKRED)
right = "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
draw_spaced(W - M - spaced_w(right, strap_f, 1), y, right, strap_f, INK, 1)
y += 40
d.line([M, y, W - M, y], fill=RULE, width=4)
d.line([M, y + 6, W - M, y + 6], fill=RULE, width=1)
y += 14

mast = fit_font(SERIF_BLACK, "Saturday 21 November 2026", CW, 140)
mast_text = "Saturday 21 November 2026"
d.text(((W - tw(mast, mast_text)) / 2, y), mast_text, font=mast, fill=INK)
y += mast.size + 8
deck_f = F(SERIF_I, 30)
deck_text = ("Climate talks run into overtime \u00b7 three missiles fall over "
             "Riyadh \u00b7 a deep quake shakes Peru")
d.text(((W - tw(deck_f, deck_text)) / 2, y), deck_text, font=deck_f,
       fill=(60, 52, 40))
y += 42
d.line([M, y, W - M, y], fill=RULE, width=2)
y += 12

# stat band
cellw = CW / 6
lab_f = F(SANS_SB, 15)
for i, (num, lab) in enumerate(STATS):
    cx = M + i * cellw
    d.rectangle([cx + 2, y, cx + cellw - 10, y + 7], fill=RED)
    nf = fit_font(SERIF_B, num, cellw - 18, 54)
    d.text((cx + 4, y + 10), num, font=nf, fill=RED)
    ly = y + 71
    for line in wrap(lab, lab_f, cellw - 16):
        d.text((cx + 4, ly), line, font=lab_f, fill=INK)
        ly += 12
    if i:
        d.line([cx - 4, y + 8, cx - 4, y + 100], fill=(200, 190, 168),
               width=2)
y += 100

# region bar
counts = region_counts()
bar_f = F(SANS_B, 22)
seg_min = {code: tw(bar_f, f"{label} {counts[code]}") + 28
           for code, label, _ in REGIONS}
rest = CW - sum(seg_min.values())
x = M
for code, label, col in REGIONS:
    wseg = seg_min[code] + rest * counts[code] / TOTAL
    d.rectangle([x, y, x + wseg, y + 42], fill=col)
    t = f"{label} {counts[code]}"
    d.text((x + (wseg - tw(bar_f, t)) / 2, y + 8), t, font=bar_f,
           fill=(255, 255, 255))
    x += wseg
y += 52

# heroes
gap = 28
colw = (CW - 2 * gap) / 3
art_h = 168
kick_f = F(SANS_B, 23)
head_f = F(SERIF_B, 43)
deckf = F(SERIF, 25)
src_f = F(SERIF_I, 23)
hero_top = y
hero_decks = [wrap(s["deck"], deckf, colw)[:4] for s in STORIES[:3]]
deck_h = max(len(l) for l in hero_decks) * 30
for i, s in enumerate(STORIES[:3]):
    x = M + i * (colw + gap)
    {"cop": art_cop, "riyadh": art_riyadh, "peru": art_peru}[s["art"]](
        x, y, colw, art_h)
    chip(x + 12, y + 12, s["chip"], F(SANS_B, 25))
    tag(x + 12, y + art_h - 38, s["tag"], F(SANS_SB, 19))
    yy = y + art_h + 12
    num_badge(x, yy, i + 1)
    d.text((x + 44, yy + 3), f"{s['place']} \u00b7 {s['field']}",
           font=kick_f, fill=DARKRED)
    yy += 44
    for line in wrap(s["headline"], head_f, colw)[:2]:
        d.text((x, yy), line, font=head_f, fill=INK)
        yy += 49
    yy += 2
    for line in hero_decks[i]:
        d.text((x, yy), line, font=deckf, fill=(40, 36, 28))
        yy += 30
    yy = y + art_h + 12 + 44 + 98 + 2 + deck_h + 5
    d.text((x, yy), s["source"], font=src_f, fill=GREY)
    pill_right(x + colw, yy - 2, s["status"])
    if i == 0:
        hero_bottom = yy + 32
y = hero_bottom + 12

# grid
ggap = 20
gcolw = (CW - 4 * ggap) / 5
gstrip = 66
gk_f = F(SANS_B, 19)
gh_f = F(SERIF_B, 28)
gd_f = F(SERIF, 20)
gs_f = F(SERIF_I, 19)
grid_top = y
for r in range(2):
    row_h = 0
    for c in range(5):
        idx = 3 + r * 5 + c
        s = STORIES[idx]
        x = M + c * (gcolw + ggap)
        yy = grid_top
        art_strip(s["art"], x, yy, gcolw, gstrip)
        chip(x + 8, yy + 8, s["chip"], F(SANS_B, 18))
        yy += gstrip + 8
        d.text((x, yy), str(idx + 1), font=F(SANS_B, 20), fill=RED)
        d.text((x + 30, yy + 1), f"{s['place']} \u00b7 {s['field']}",
               font=gk_f, fill=DARKRED)
        yy += 29
        for line in wrap(s["headline"], gh_f, gcolw)[:2]:
            d.text((x, yy), line, font=gh_f, fill=INK)
            yy += 32
        yy += 2
        for line in wrap(s["deck"], gd_f, gcolw)[:2]:
            d.text((x, yy), line, font=gd_f, fill=(40, 36, 28))
            yy += 24
        yy += 3
        d.text((x, yy), s["source"], font=gs_f, fill=GREY)
        pill_right(x + gcolw, yy - 4, s["status"])
        yy += 24
        row_h = max(row_h, yy - grid_top)
    grid_top += row_h + 10
y = grid_top + 2

# bottom: map + briefs
bot_top = y
map_w = 688
title_f = F(SANS_B, 23)
d.text((M, bot_top), "WHERE IT HAPPENED \u2014 STORIES 1\u201313",
       font=title_f, fill=INK)
map_y = bot_top + 34
SEA = (38, 74, 98)
LAND = (216, 194, 140)

LANDS = [
 [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
  (-82, 62), (-95, 60), (-100, 52), (-110, 50), (-125, 48), (-124, 40),
  (-120, 34), (-110, 29), (-105, 22), (-97, 18), (-92, 15), (-86, 13),
  (-83, 9), (-90, 14), (-97, 16), (-105, 20), (-114, 28), (-122, 36),
  (-132, 44), (-150, 58), (-162, 60)],
 [(-80, 9), (-77, 4), (-80, -3), (-75, -10), (-70, -18), (-70, -28),
  (-72, -38), (-74, -48), (-70, -54), (-66, -55), (-68, -45), (-65, -35),
  (-58, -28), (-50, -20), (-44, -10), (-38, -5), (-42, 0), (-50, 2),
  (-58, 6), (-66, 10), (-72, 12), (-77, 8)],
 [(-17, 15), (-10, 5), (-2, 5), (8, 4), (10, -2), (12, -12), (14, -22),
  (18, -30), (24, -34), (30, -32), (32, -26), (34, -18), (36, -8),
  (40, -2), (44, 4), (48, 10), (51, 12), (44, 14), (36, 20), (30, 28),
  (22, 32), (12, 33), (0, 32), (-8, 28), (-14, 22)],
 [(-9, 43), (-2, 44), (0, 46), (-4, 48), (-2, 50), (2, 51), (5, 53),
  (8, 55), (8, 57), (12, 56), (18, 56), (24, 58), (30, 60), (30, 64),
  (24, 66), (18, 68), (12, 70), (20, 72), (30, 70), (40, 68), (48, 66),
  (40, 62), (32, 58), (28, 54), (30, 50), (28, 46), (24, 44), (20, 42),
  (16, 40), (12, 38), (8, 38), (3, 42), (-2, 37), (-6, 36), (-9, 37)],
 [(48, 66), (60, 68), (75, 70), (90, 72), (105, 74), (120, 73), (135, 72),
  (150, 70), (165, 68), (178, 66), (178, 60), (162, 56), (155, 52),
  (142, 50), (140, 44), (135, 38), (128, 34), (122, 30), (118, 26),
  (112, 22), (108, 18), (105, 12), (103, 6), (100, 2), (98, 8), (95, 14),
  (92, 16), (88, 21), (82, 19), (78, 9), (74, 19), (72, 27), (68, 28),
  (62, 26), (58, 24), (54, 26), (50, 28), (48, 34), (46, 40), (44, 46),
  (46, 54), (47, 60)],
 [(113, -22), (122, -14), (130, -12), (136, -14), (142, -18), (147, -24),
  (150, -30), (148, -36), (142, -38), (136, -36), (130, -32), (124, -34),
  (118, -32), (114, -28)],
 [(167, -45), (174, -41), (176, -38), (174, -36), (169, -40)],
 [(95, 5), (100, 0), (105, -3), (110, -4), (108, 2), (102, 6), (97, 8)],
]

# briefs first (flow) to size the bottom block
bx = M + map_w + 28
bw = W - M - bx
bcol_w = (bw - 24) / 2
bf = F(SANS, 19)
bn_f = F(SANS_B, 19)
per = (len(BRIEFS) + 1) // 2
col_heights = []
for col in range(2):
    items = BRIEFS[col * per:(col + 1) * per]
    hh = 0
    for j, (place, text, src) in enumerate(items):
        n = 14 + col * per + j
        numw = tw(bn_f, str(n)) + 8
        lines = wrap(f"{place}: {text} ({src})", bf, bcol_w - numw)
        hh += len(lines) * 21 + 5
    col_heights.append(hh)
briefs_h = max(col_heights)
map_h = briefs_h - 30

d.rectangle([M, map_y, M + map_w, map_y + map_h], fill=SEA)
def proj(lon, lat):
    return (M + (lon + 180) / 360 * map_w, map_y + (90 - lat) / 180 * map_h)
for poly in LANDS:
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND)
for i, s in enumerate(STORIES[:13]):
    px, py = proj(*s["pin"])
    r = 12
    d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
              outline=(255, 255, 255), width=2)
    f = F(SANS_B, 16 if i + 1 < 10 else 14)
    t = str(i + 1)
    d.text((px - tw(f, t) / 2, py - f.size / 2 - 1), t, font=f,
           fill=(255, 255, 255))
cap_f = F(SERIF_I, 18)
d.text((M, map_y + map_h + 5),
       "Each number is the story with that number on this page.",
       font=cap_f, fill=GREY)

bt = f"ALSO ON SATURDAY 21 NOVEMBER \u2014 {len(BRIEFS)} MORE STORIES"
d.text((bx, bot_top), bt, font=title_f, fill=INK)
for col in range(2):
    items = BRIEFS[col * per:(col + 1) * per]
    x = bx + col * (bcol_w + 24)
    yy = bot_top + 34
    for j, (place, text, src) in enumerate(items):
        n = 14 + col * per + j
        d.text((x, yy), str(n), font=bn_f, fill=RED)
        numw = tw(bn_f, str(n)) + 8
        nx = x + numw
        lines = wrap(f"{place}: {text} ({src})", bf, bcol_w - numw)
        for k, line in enumerate(lines):
            if k == 0:
                lead = f"{place}:"
                d.text((nx, yy), lead, font=bn_f, fill=INK)
                rest = line[len(lead):].lstrip()
                d.text((nx + tw(bn_f, lead) + 5, yy), rest, font=bf,
                       fill=INK)
            else:
                d.text((nx, yy + k * 21), line, font=bf, fill=INK)
        yy += len(lines) * 21 + 5

y = bot_top + 34 + briefs_h + 6

# date check
dc_title = F(SANS_B, 21)
dc_f = F(SERIF, 19)
lines = wrap(DATE_CHECK, dc_f, CW - 200)
dc_h = len(lines) * 25 + 18
d.rectangle([M, y, W - M, y + dc_h], outline=RED, width=3)
d.text((M + 14, y + 9), "DATE CHECK", font=dc_title, fill=RED)
tx = M + 168
for i, line in enumerate(lines):
    d.text((tx, y + 9 + i * 25), line, font=dc_f, fill=INK)
y += dc_h + 8

# footer
foot_f = F(SANS, 18)
foot = ("Every story here happened, or was first reported, on Saturday 21 "
        "November 2026. Sources named beside each story \u00b7 Original drawings")
d.text(((W - tw(foot_f, foot)) / 2, y), foot, font=foot_f, fill=GREY)
y += 24
leg_f = F(SANS_SB, 18)
leg = ("HOW WE CHECKED: CONFIRMED = 2+ OUTLETS \u00b7 OFFICIAL = ON THE RECORD "
       "\u00b7 REPORTED = ONE OUTLET \u00b7 CLAIM = ONE SIDE'S ACCOUNT")
d.text(((W - tw(leg_f, leg)) / 2, y), leg, font=leg_f, fill=DARKRED)
y += 28
print("final y:", y, "of", H)

img = img.resize((1024, 1024), Image.LANCZOS)
img.save("/home/hatch/workspace/news-image-20261121/v2-entry/entry.png",
         optimize=True)
print("saved entry.png")
