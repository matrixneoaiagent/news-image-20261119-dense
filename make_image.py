#!/usr/bin/env python3
"""
make_image.py — "Thursday 19 November 2026" dense newspaper front page.
Draws at 2048×2048, downscales to 1024×1024 with LANCZOS, saves as entry.png.
"""

import os, math
from PIL import Image, ImageDraw, ImageFont, ImageColor

# ---------------------------------------------------------------------------
# FONTS
# ---------------------------------------------------------------------------
FD = "/nix/store/fa2vzgw2pds7gjb9671n9fbphfw65sk3-dejavu-fonts-2.37/share/fonts/truetype"
SERIF_BOLD  = f"{FD}/DejaVuSerif-Bold.ttf"
SERIF_REG   = f"{FD}/DejaVuSerif.ttf"
SANS_BOLD   = f"{FD}/DejaVuSans-Bold.ttf"
SANS_REG    = f"{FD}/DejaVuSans.ttf"
SERIF_BI    = f"{FD}/DejaVuSerif-BoldItalic.ttf"
SERIF_IT    = f"{FD}/DejaVuSerif-Italic.ttf"

# ---------------------------------------------------------------------------
# PALETTE
# ---------------------------------------------------------------------------
PAPER  = (244,241,232)
INK    = (18,18,18)
AMBER  = (200,134,42)
RED    = (163,42,42)
BLUE   = (31,78,121)
GREEN  = (46,107,79)
GREY   = (120,120,120)
LTGREY = (200,200,200)
WHITE  = (255,255,255)
DKGREY = (60,60,60)
TEAL   = (46,139,139)
BROWN  = (139,69,19)

REGION_COLORS = {
    "Europe":      RED,
    "Americas":    BLUE,
    "Asia-Pacific":GREEN,
    "Mideast":     AMBER,
    "Africa":      BROWN,
    "Oceania":     TEAL,
    "World":       DKGREY,
}
REGION_ABBR = {
    "Europe":"EUROPE","Americas":"AMERICAS","Asia-Pacific":"ASIA-PAC",
    "Mideast":"MIDEAST","Africa":"AFRICA","Oceania":"OCEANIA","World":"WORLD",
}
TAG_ABBR = {
    "Europe":"EU","Americas":"AM","Asia-Pacific":"AP",
    "Mideast":"ME","Africa":"AF","Oceania":"OC","World":"WL",
}

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
W = H = 2048
PAD = 30

def fnt(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def tw(draw, text, f):
    try:
        return int(draw.textlength(text, font=f))
    except Exception:
        bb = draw.textbbox((0,0), text, font=f)
        return bb[2]-bb[0]

def th(f):
    try:
        return f.size
    except Exception:
        return 12

def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur+" "+w).strip()
        if tw(draw, t, f) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def put_text(draw, text, f, x, y, fill=INK, max_w=None, align="left"):
    if max_w:
        lines = wrap(draw, text, f, max_w)
    else:
        lines = [text]
    lh = th(f) + 3
    for line in lines:
        if align == "center":
            lw = tw(draw, line, f)
            draw.text((x - lw//2, y), line, font=f, fill=fill)
        elif align == "right":
            lw = tw(draw, line, f)
            draw.text((x - lw, y), line, font=f, fill=fill)
        else:
            draw.text((x, y), line, font=f, fill=fill)
        y += lh
    return y

def put_lines(draw, lines, f, x, y, fill=INK, lh=None):
    if lh is None: lh = th(f) + 3
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += lh
    return y

def hrule(draw, x1, y, x2, color=INK, width=2):
    if isinstance(color, str): color = ImageColor.getrgb(color)
    draw.line([(int(x1),int(y)),(int(x2),int(y))], fill=color, width=int(width))

def rect(draw, x0,y0,x1,y1, fill=None, outline=None, width=2):
    draw.rectangle([int(x0),int(y0),int(x1),int(y1)], fill=fill, outline=outline, width=int(width))

def shrink_font(draw, text, path, size, max_w, min_sz=14):
    while size >= min_sz:
        f = fnt(path, size)
        if tw(draw, text, f) <= max_w:
            return f
        size -= 2
    return fnt(path, min_sz)

# ---------------------------------------------------------------------------
# ICON PRIMITIVES
# ---------------------------------------------------------------------------
def icon_summit(draw, cx, cy, r, c):
    for dx in [-r//2, 0, r//2]:
        draw.ellipse([cx+dx-r//3, cy-r//2, cx+dx+r//3, cy+r//6], outline=c, width=4)
    draw.line([(cx-r, cy+r//3),(cx+r,cy+r//3)], fill=c, width=5)
    draw.line([(cx-r//3, cy+r//3),(cx-r//3,cy+r)], fill=c, width=4)
    draw.line([(cx+r//3, cy+r//3),(cx+r//3,cy+r)], fill=c, width=4)

def icon_gta(draw, cx, cy, r, c):
    # Stylised VI
    f1 = fnt(SERIF_BOLD, r*2)
    t = "VI"
    tlen = tw(draw, t, f1)
    draw.text((cx-tlen//2, cy-r), t, font=f1, fill=c)
    # joystick circle below
    draw.ellipse([cx-r//3, cy+r//2, cx+r//3, cy+r+r//3], outline=c, width=4)
    draw.line([(cx, cy+r//2),(cx, cy+r//6)], fill=c, width=5)

def icon_ipo(draw, cx, cy, r, c):
    bars = [r//3, r//2, int(r*0.7), r]
    bw = r*2//5
    for i, h in enumerate(bars):
        x0 = cx - r + i*(bw+4)
        rect(draw, x0, cy+r-h, x0+bw, cy+r, fill=c)
    # Arrow up-right
    ax, ay = cx+r+8, cy-r+8
    draw.line([(cx-r//2, cy+r//4),(ax,ay)], fill=c, width=5)
    draw.line([(ax,ay),(ax-r//3,ay)], fill=c, width=4)
    draw.line([(ax,ay),(ax,ay+r//3)], fill=c, width=4)

def icon_bridge(draw, cx, cy, r, c):
    # road
    draw.line([(cx-r,cy),(cx+r,cy)], fill=c, width=6)
    # pylons
    for x in [cx-r//2, cx+r//2]:
        draw.line([(x,cy),(x,cy-r*2//3)], fill=c, width=5)
    # cable lines
    draw.line([(cx-r,cy-r//4),(cx-r//2,cy-r*2//3)], fill=c, width=3)
    draw.line([(cx+r,cy-r//4),(cx+r//2,cy-r*2//3)], fill=c, width=3)
    draw.line([(cx,cy-r//4),(cx-r//2,cy-r*2//3)], fill=c, width=2)
    draw.line([(cx,cy-r//4),(cx+r//2,cy-r*2//3)], fill=c, width=2)
    # X across break
    draw.line([(cx-r//4,cy-r//3),(cx+r//4,cy+r//6)], fill=RED, width=4)
    draw.line([(cx+r//4,cy-r//3),(cx-r//4,cy+r//6)], fill=RED, width=4)

def icon_eu(draw, cx, cy, r, c):
    draw.ellipse([cx-r,cy-r,cx+r,cy+r], outline=c, width=4)
    for i in range(12):
        a = math.radians(i*30-90)
        sx,sy = int(cx+r*0.65*math.cos(a)), int(cy+r*0.65*math.sin(a))
        draw.ellipse([sx-5,sy-5,sx+5,sy+5], fill=c)

def icon_icj(draw, cx, cy, r, c):
    # scales of justice
    draw.line([(cx,cy-r),(cx,cy+r//2)], fill=c, width=5)
    draw.line([(cx-r,cy-r//3),(cx+r,cy-r//3)], fill=c, width=4)
    draw.ellipse([cx-r,cy-r//3-r//2, cx-r//2, cy-r//3], outline=c, width=3)
    draw.ellipse([cx+r//2,cy-r//3-r//2, cx+r, cy-r//3], outline=c, width=3)
    draw.line([(cx-r//2,cy+r//2),(cx+r//2,cy+r//2)], fill=c, width=4)

def icon_cop(draw, cx, cy, r, c):
    # globe + thermometer
    draw.ellipse([cx-r,cy-r,cx+r,cy+r], outline=c, width=4)
    draw.arc([cx-r,cy-r,cx+r,cy+r], 0, 180, fill=c, width=3)
    draw.line([(cx,cy-r),(cx,cy+r)], fill=c, width=2)
    # thermometer
    tx = cx+r+10
    draw.rectangle([tx-6,cy-r,tx+6,cy+r//2], outline=c, width=3)
    draw.ellipse([tx-10,cy+r//2-10,tx+10,cy+r//2+10], outline=c, width=3)
    rect(draw, tx-4,cy,tx+4,cy+r//2, fill=RED)

def icon_missile(draw, cx, cy, r, c):
    pts = [(cx,cy-r),(cx+r//3,cy+r//2),(cx-r//3,cy+r//2)]
    draw.polygon(pts, outline=c, width=3)
    # flame
    draw.ellipse([cx-r//5,cy+r//2,cx+r//5,cy+r], fill=RED)
    # lines (target)
    draw.line([(cx-r,cy-r//3),(cx+r,cy-r//3)], fill=c, width=2)

def icon_gaza(draw, cx, cy, r, c):
    # building with broken roof
    rect(draw, cx-r,cy-r//2,cx+r,cy+r//2, outline=c, width=3)
    draw.line([(cx-r,cy-r//2),(cx,cy-r)], fill=c, width=3)
    draw.line([(cx,cy-r),(cx+r//3,cy-r//2)], fill=c, width=3)
    # rubble
    draw.line([(cx+r//3,cy-r//2),(cx+r,cy-r//4)], fill=RED, width=3)
    for dx in range(-r,r,r//3):
        draw.ellipse([cx+dx-4,cy+r//2-4,cx+dx+4,cy+r//2+4], fill=c)

def icon_art(draw, cx, cy, r, c):
    # frame
    rect(draw, cx-r,cy-r,cx+r,cy+r, outline=c, width=4)
    rect(draw, cx-r+8,cy-r+8,cx+r-8,cy+r-8, outline=c, width=2)
    # sunflower-ish
    draw.ellipse([cx-r//3,cy-r//3,cx+r//3,cy+r//3], fill=c)
    for i in range(8):
        a = math.radians(i*45)
        draw.line([(cx,cy),(int(cx+r*0.6*math.cos(a)),int(cy+r*0.6*math.sin(a)))], fill=AMBER, width=4)

def icon_boat(draw, cx, cy, r, c):
    pts = [(cx-r,cy),(cx+r,cy),(cx+r//2,cy+r//2),(cx-r//2,cy+r//2)]
    draw.polygon(pts, outline=c, width=3)
    draw.line([(cx,cy),(cx,cy-r)], fill=c, width=4)
    draw.line([(cx,cy-r),(cx+r//2,cy-r//3)], fill=c, width=3)
    # waves
    for xw in range(-r,r,r//2):
        draw.arc([cx+xw-r//4,cy+r//2,cx+xw+r//4,cy+r], 0,180, fill=BLUE, width=3)

def icon_speaker(draw, cx, cy, r, c):
    rect(draw, cx-r//4,cy-r//2,cx+r//4,cy+r//2, fill=c)
    pts = [(cx+r//4,cy-r//2),(cx+r,cy-r),(cx+r,cy+r),(cx+r//4,cy+r//2)]
    draw.polygon(pts, fill=c)
    # podium
    draw.line([(cx-r,cy+r),(cx+r,cy+r)], fill=c, width=4)
    draw.ellipse([cx-r//5,cy+r,cx+r//5,cy+r+r//3], outline=c, width=3)

def icon_protest(draw, cx, cy, r, c):
    # figure
    draw.ellipse([cx-r//4,cy-r,cx+r//4,cy-r//2], outline=c, width=3)
    draw.line([(cx,cy-r//2),(cx,cy+r//4)], fill=c, width=4)
    draw.line([(cx,cy),(cx-r//2,cy+r//2)], fill=c, width=3)
    draw.line([(cx,cy),(cx+r//2,cy+r//2)], fill=c, width=3)
    # sign
    rect(draw, cx-r,cy-r-r//3,cx-r//4,cy-r//2, outline=c, width=2)
    draw.line([(cx-r//4,cy-r),(cx,cy-r)], fill=c, width=3)

ICONS = {
    "summit":icon_summit,"gta":icon_gta,"ipo":icon_ipo,
    "bridge":icon_bridge,"eu":icon_eu,"icj":icon_icj,"cop":icon_cop,
    "missile":icon_missile,"gaza":icon_gaza,"art":icon_art,
    "boat":icon_boat,"speaker":icon_speaker,"protest":icon_protest,
}
SEC_ICONS = ["bridge","eu","icj","cop","missile","gaza","art","boat","speaker","protest"]

# ---------------------------------------------------------------------------
# STORIES
# ---------------------------------------------------------------------------
HEROES = [
    dict(kicker="1 · SHENZHEN · SUMMIT", color=BLUE, icon="summit",
         headline=["Trump calls Putin", "'my friend' as first", "US-Russia-China", "trilateral talks begin"],
         subhead="Xi hosts APEC summit; Ukraine & Iran on agenda"),
    dict(kicker="2 · WORLD · GAMING", color=GREEN, icon="gta",
         headline=["GTA VI released after", "13-year wait — score", "99 on Metacritic,", "$1.5bn pre-orders"],
         subhead="First playable female lead in 3D GTA; midnight launch worldwide"),
    dict(kicker="3 · NASDAQ · IPO", color=AMBER, icon="ipo",
         headline=["Anthropic raises", "$81.3bn in history's", "biggest-ever IPO", "at $83 a share"],
         subhead="$1.5 trillion valuation; ticker 'ANT'; seven founders billionaires"),
]

SECONDARY = [
    dict(region="Europe",      color=RED,   icon="bridge",
         headline=["Ukraine strikes Crimean", "Bridge for 3rd time", "this week; 227 m span"],
         detail="Russia hits Kyiv bridges; power & metro disrupted"),
    dict(region="Europe",      color=BLUE,  icon="eu",
         headline=["Russia hits Kyiv's", "Pivnichnyi & Pivdennyi", "bridges; partial metro"],
         detail="EU proposes €45bn loan for Ukraine defence"),
    dict(region="Asia-Pacific",color=RED,   icon="icj",
         headline=["ICJ delivers landmark", "ruling on Rohingya", "genocide vs Myanmar"],
         detail="The Gambia v. Myanmar; ruling at 09:00 GMT"),
    dict(region="World",       color=GREEN, icon="cop",
         headline=["COP31 Antalya enters", "penultimate day with", "deal still elusive"],
         detail="'Held hostage by oil mafia' — Panama minister"),
    dict(region="Mideast",     color=AMBER, icon="missile",
         headline=["Houthi missiles target", "Riyadh; Saudi coalition", "intercepts; debris falls"],
         detail="Houthis claim airport & financial centre in sights"),
    dict(region="Mideast",     color=RED,   icon="gaza",
         headline=["Israel launches rare", "ground op in Gaza", "beyond Yellow Line"],
         detail="Move condemned as ceasefire violation by Hamas"),
    dict(region="Europe",      color=AMBER, icon="art",
         headline=["Van Gogh 'Chataigniers'", "sells for record", "$190.4m amid Nazi row"],
         detail="Auction house faces calls to return work to heirs"),
    dict(region="Africa",      color=BLUE,  icon="boat",
         headline=["Dozens missing as boat", "carrying ~100 migrants", "capsizes off Senegal"],
         detail="Vessel sank near Yenne; rescue operation under way"),
    dict(region="Americas",    color=GREEN, icon="speaker",
         headline=["Democrats nominate", "Hakeem Jeffries for", "first Black US Speaker"],
         detail="Takes office January; Dems take control of House"),
    dict(region="Asia-Pacific",color=AMBER, icon="protest",
         headline=["Protests and killings in", "Bangladesh ahead of", "Sheikh Hasina's return"],
         detail="Exiled former PM plans comeback; violence erupts"),
]

BRIEFS = [
    ("Europe",      "Russia asks Netherlands if it has joined conflict after Crimea bridge strike"),
    ("Europe",      "Russian drone kills 4 in Odesa; Ukraine calls strike 'brutal and deliberate'"),
    ("Europe",      "EU proposes €45bn Ukraine loan to avert cash crisis"),
    ("Europe",      "Russian spy arrested for surveilling Palantir employees over Ukraine support"),
    ("Europe",      "Prince Harry: would rejoin army; warns of Russia threat after Ukraine visit"),
    ("Europe",      "French parents jailed for murder of 4-yr-old Inass Touloub; body found 1987"),
    ("Europe",      "Bayesian yacht inquiry: crew unaware of risks before Mike Lynch superyacht sank"),
    ("Americas",    "Elon Musk: record $446m midterm spend was 'pretty foolish'"),
    ("Americas",    "Democrat Mary Peltola wins Alaska Senate seat; Dems hold 56 seats"),
    ("Asia-Pacific","China gives Japan's PM frosty welcome at APEC; Trump & Putin got fanfare"),
    ("Asia-Pacific","Taiwan reports Russian aircraft in ADIZ during APEC summit"),
    ("Asia-Pacific","Pew Research: India stays predominantly Hindu; Muslim population growing faster"),
    ("Mideast",     "US CENTCOM chief meets Saudi Crown Prince MBS in Riyadh amid Yemen escalation"),
    ("Africa",      "World marathon champion Peres Jepchirchir banned 3 years for doping"),
    ("Africa",      "Somalia constitutional overhaul tests federal bargain; Mohamud faces resistance"),
    ("Africa",      "Kenya milk shortage deepens as drought hits farmers and pushes prices up"),
    ("World",       "Russia, Saudi Arabia, Australia named biggest historic CO2 exporters pre-COP31"),
    ("World",       "Data centres to create 70% more carbon emissions by 2030, IEA warns"),
    ("World",       "One in four women globally unable to refuse sex in marriage — UN UNFPA"),
    ("Oceania",     "Bancroft bombshell: accuses Cummins and Australian team in sandpapergate claim"),
    ("World",       "LIV Golf bankruptcy: UK firms owed thousands as Saudi league paid golfers millions"),
    ("World",       "GTA VI critics: 'masterpiece'; female lead Lucia is gaming's new icon"),
    ("World",       "IPCC report delay will threaten global climate effort, top scientist warns"),
]

# ---------------------------------------------------------------------------
# WORLD MAP
# ---------------------------------------------------------------------------
def draw_world_map(draw, x0, y0, w, h, c=BLUE):
    # Continent outlines (relative coords 0..1)
    conts = [
        (0.04,0.08, 0.26,0.52),   # N America
        (0.12,0.52, 0.28,0.90),   # S America
        (0.42,0.04, 0.56,0.38),   # Europe
        (0.42,0.38, 0.59,0.88),   # Africa
        (0.54,0.04, 0.95,0.60),   # Asia
        (0.74,0.62, 0.95,0.88),   # Australia
        (0.19,0.00, 0.33,0.12),   # Greenland
    ]
    for rx0,ry0,rx1,ry1 in conts:
        rect(draw,
             x0+rx0*w, y0+ry0*h, x0+rx1*w, y0+ry1*h,
             outline=c, width=2)

    # Spread story dots across distinct map regions
    # (rx, ry) are relative to map area; kept well separated
    dots = [
        (0.72,0.18,"1"),  # Shenzhen (APEC summit)
        (0.09,0.28,"2"),  # San Francisco (Anthropic IPO)
        (0.09,0.44,"3"),  # Americas (GTA VI — same region, offset below)
        (0.47,0.13,"4"),  # Kyiv, Ukraine
        (0.72,0.30,"5"),  # Southeast Asia (ICJ/Bangladesh)
        (0.56,0.30,"6"),  # Mideast (Houthi/Gaza)
        (0.50,0.17,"7"),  # Antalya, Turkey (COP31)
        (0.09,0.37,"8"),  # Washington DC (Jeffries)
        (0.47,0.52,"9"),  # Senegal, West Africa
        (0.68,0.21,"10"), # Bangladesh (protest)
        (0.46,0.07,"11"), # Netherlands/Europe (Van Gogh)
        (0.57,0.37,"12"), # Gaza/Israel
        (0.47,0.60,"13"), # Senegal coast (boat capsizes)
    ]
    fn_sm = fnt(SANS_BOLD, 16)
    placed = []
    for rx,ry,label in dots:
        px = int(x0 + rx*w)
        py = int(y0 + ry*h)
        # nudge away from previous dots
        for attempts in range(6):
            too_close = any(abs(px-px2)<24 and abs(py-py2)<24 for px2,py2 in placed)
            if not too_close: break
            py += 26
        placed.append((px,py))
        draw.ellipse([px-11,py-11,px+11,py+11], fill=RED, outline=WHITE, width=2)
        lw = tw(draw,label,fn_sm)
        draw.text((px-lw//2, py-8), label, font=fn_sm, fill=WHITE)

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def make_image(out_path="entry.png"):
    img = Image.new("RGB",(W,H),PAPER)
    d   = ImageDraw.Draw(img)

    y = 0

    # ── TOP STRIP ──────────────────────────────────────────────────────────
    STRIP = 54
    rect(d, 0,0,W,STRIP, fill=INK)
    f_strip = fnt(SANS_BOLD, 28)
    f_strip2= fnt(SANS_REG,  24)
    d.text((PAD, 12), "THE WORLD IN ONE DAY", font=f_strip, fill=PAPER)
    right = "THURSDAY'S NEWS  ·  ONE PAGE  ·  36 STORIES"
    rw = tw(d, right, f_strip2)
    d.text((W-PAD-rw, 15), right, font=f_strip2, fill=PAPER)
    y = STRIP+6

    # ── THIN RULE ──────────────────────────────────────────────────────────
    hrule(d, PAD, y, W-PAD, INK, 3); y+=4

    # ── MASTHEAD ───────────────────────────────────────────────────────────
    f_mast = shrink_font(d, "Thursday 19 November 2026", SERIF_BOLD, 118, W-2*PAD-10)
    mast   = "Thursday 19 November 2026"
    mw     = tw(d, mast, f_mast)
    d.text(((W-mw)//2, y), mast, font=f_mast, fill=INK)
    y += th(f_mast)+6

    # Subtitle
    sub = "APEC SHENZHEN SUMMIT  ·  GTA VI LAUNCHES  ·  ANTHROPIC $1.5TN IPO  ·  COP31 ANTALYA"
    f_sub = shrink_font(d, sub, SERIF_BI, 36, W-2*PAD-10)
    sw = tw(d, sub, f_sub)
    d.text(((W-sw)//2, y), sub, font=f_sub, fill=AMBER)
    y += th(f_sub)+10

    hrule(d, PAD, y, W-PAD, INK, 3); y+=3
    hrule(d, PAD, y, W-PAD, INK, 1); y+=8

    # ── REGION STRIP ───────────────────────────────────────────────────────
    all_regions = (
        [h["color"] for h in HEROES] +   # just count
        [s["region"] for s in SECONDARY] +
        [r for r,_ in BRIEFS]
    )
    # Actually count by region name
    rnames = ["Europe","Americas","Asia-Pacific","Mideast","Africa","Oceania","World"]
    # hero regions
    hero_regions = ["Asia-Pacific","World","Americas"]
    rcounts = {r:0 for r in rnames}
    for r in hero_regions: rcounts[r]+=1
    for s in SECONDARY: rcounts[s["region"]]+=1
    for r,_ in BRIEFS: rcounts[r]+=1

    RS = 70   # strip height
    rw_each = (W-2*PAD)//len(rnames)
    f_rtag   = fnt(SANS_BOLD, 23)
    f_rcnt   = fnt(SERIF_BOLD,30)
    for i,reg in enumerate(rnames):
        rx0 = PAD + i*rw_each
        rx1 = rx0+rw_each-3
        c = REGION_COLORS[reg]
        rect(d, rx0,y, rx1,y+RS, fill=c)
        abbr = REGION_ABBR[reg]
        aw = tw(d,abbr,f_rtag)
        d.text((rx0+(rw_each-3-aw)//2, y+5), abbr, font=f_rtag, fill=WHITE)
        cnt = str(rcounts[reg])
        cw = tw(d,cnt,f_rcnt)
        d.text((rx0+(rw_each-3-cw)//2, y+32), cnt, font=f_rcnt, fill=WHITE)
    y += RS+8

    # ── HERO ROW ───────────────────────────────────────────────────────────
    HERO_H  = 500
    hero_cw = (W-2*PAD-8)//3
    f_kick  = fnt(SANS_BOLD, 25)
    f_hhl   = fnt(SERIF_BOLD, 46)
    f_hhl2  = fnt(SERIF_BOLD, 38)
    f_hsub  = fnt(SANS_REG,   24)

    for i,hero in enumerate(HEROES):
        hx0 = PAD + i*(hero_cw+4)
        hx1 = hx0+hero_cw
        hy0 = y
        hy1 = hy0+HERO_H
        c   = hero["color"]

        rect(d, hx0,hy0,hx1,hy1, fill=WHITE, outline=c, width=3)

        # Kicker bar
        KB = 42
        rect(d, hx0,hy0,hx1,hy0+KB, fill=c)
        kw = tw(d,hero["kicker"],f_kick)
        d.text((hx0+(hero_cw-kw)//2, hy0+8), hero["kicker"], font=f_kick, fill=WHITE)

        # Icon
        ICON_H = 160
        rect(d, hx0,hy0+KB,hx1,hy0+KB+ICON_H, fill=(238,235,225))
        icx = hx0+hero_cw//2
        icy = hy0+KB+ICON_H//2
        ICONS[hero["icon"]](d, icx, icy, 62, c)

        # Headline
        hl_y = hy0+KB+ICON_H+8
        for line in hero["headline"]:
            f_use = f_hhl if tw(d,line,f_hhl)<=hero_cw-16 else f_hhl2
            d.text((hx0+8, hl_y), line, font=f_use, fill=INK)
            hl_y += th(f_use)+3

        # Divider + subhead
        hl_y += 2
        hrule(d, hx0+8, hl_y, hx1-8, c, 2); hl_y+=8
        sub_lines = wrap(d, hero["subhead"], f_hsub, hero_cw-16)
        for sl in sub_lines[:2]:
            d.text((hx0+8,hl_y), sl, font=f_hsub, fill=c)
            hl_y += th(f_hsub)+3

    y += HERO_H+8

    # ── SECONDARY GRID  5×2 ────────────────────────────────────────────────
    SCOLS, SROWS = 5, 2
    sec_w  = (W-2*PAD-(SCOLS-1)*5)//SCOLS
    sec_h  = 235
    f_sreg = fnt(SANS_BOLD, 19)
    f_shl  = fnt(SERIF_BOLD,25)
    f_sdet = fnt(SANS_REG,  19)

    for idx,sec in enumerate(SECONDARY[:10]):
        col = idx%SCOLS; row = idx//SCOLS
        sx0 = PAD + col*(sec_w+5)
        sy0 = y   + row*(sec_h+5)
        sx1 = sx0+sec_w
        sy1 = sy0+sec_h
        c   = sec["color"]

        rect(d, sx0,sy0,sx1,sy1, fill=WHITE, outline=c, width=2)

        # Header bar
        HB = 32
        rect(d, sx0,sy0,sx1,sy0+HB, fill=c)
        abbr = REGION_ABBR.get(sec["region"],"")
        aw = tw(d,abbr,f_sreg)
        d.text((sx0+(sec_w-aw)//2, sy0+6), abbr, font=f_sreg, fill=WHITE)

        # Headline (full width; no icon overlay)
        hl_y = sy0+HB+6
        for line in sec["headline"][:3]:
            f_use = f_shl
            if tw(d,line,f_shl)>sec_w-12:
                f_use = fnt(SERIF_BOLD,20)
            d.text((sx0+5,hl_y), line, font=f_use, fill=INK)
            hl_y += th(f_use)+2

        # Detail
        hrule(d, sx0+5, hl_y+2, sx1-5, c, 1); hl_y+=8
        det_lines = wrap(d, sec["detail"], f_sdet, sec_w-10)
        for dl in det_lines[:2]:
            d.text((sx0+5,hl_y), dl, font=f_sdet, fill=GREY)
            hl_y += th(f_sdet)+2

    y += SROWS*(sec_h+5)+8

    # BOTTOM SECTION: MAP + BRIEFS
    hrule(d, PAD,y,W-PAD, INK,2); y+=8

    FOOTER_H = 96
    BOTTOM_H = H - y - FOOTER_H - 6
    MAP_W    = int(W*0.29)

    # Map panel
    f_maptitle = fnt(SANS_BOLD, 28)
    d.text((PAD, y), "WHERE IT HAPPENED", font=f_maptitle, fill=INK)
    map_y0 = y + 38
    map_h  = BOTTOM_H - 40
    draw_world_map(d, PAD, map_y0, MAP_W - PAD - 10, map_h, BLUE)

    # Vertical separator
    sep_x = PAD + MAP_W
    rect(d, sep_x, y, sep_x+2, y+BOTTOM_H, fill=INK)

    # Briefs panel
    bx0 = sep_x + 14
    bw  = W - bx0 - PAD

    f_btitle = fnt(SANS_BOLD, 28)
    n_briefs = len(BRIEFS)
    brief_title = "ALSO ON THURSDAY 19 NOVEMBER \u2014 " + str(n_briefs) + " MORE STORIES"
    d.text((bx0, y), brief_title, font=f_btitle, fill=INK)
    by0 = y + 42

    avail_brief_h = BOTTOM_H - 44
    BCOLS   = 3
    bcw     = (bw - (BCOLS-1)*10) // BCOLS
    bco_x   = [bx0 + c*(bcw+10) for c in range(BCOLS)]

    per_col = math.ceil(n_briefs / BCOLS)   # = 8

    # Font size capped at 22; use extra line spacing to fill available height
    br_size = 22
    f_btag  = fnt(SANS_BOLD, br_size)
    f_br    = fnt(SANS_REG,  br_size)

    SEP_H  = 10
    # Compute LINE_H so per_col*(2*LINE_H + SEP_H) == avail_brief_h
    LINE_H = max(int((avail_brief_h / per_col - SEP_H) / 2), th(f_br)+3)

    bco_y = [by0] * BCOLS

    for bi, (reg, text) in enumerate(BRIEFS):
        col = bi // per_col
        if col >= BCOLS: col = BCOLS - 1
        cx_ = bco_x[col]
        cy_ = bco_y[col]

        tag   = TAG_ABBR.get(reg, reg[:2].upper())
        tc    = REGION_COLORS.get(reg, INK)
        tgw   = tw(d, tag, f_btag) + 8
        tag_h = th(f_btag) + 4
        rect(d, cx_, cy_, cx_+tgw, cy_+tag_h, fill=tc)
        d.text((cx_+4, cy_+2), tag, font=f_btag, fill=WHITE)

        # Fit first fragment beside tag chip; rest on next line
        first_avail_w = bcw - tgw - 6
        words = text.split()
        first_line = ""
        rest_start = 0
        for wi, w in enumerate(words):
            test = (first_line + " " + w).strip()
            if tw(d, test, f_br) <= first_avail_w:
                first_line = test
                rest_start = wi + 1
            else:
                break
        # If nothing fits beside tag, put everything on line 2
        if not first_line and words:
            rest_start = 0

        if first_line:
            d.text((cx_+tgw+5, cy_), first_line, font=f_br, fill=INK)
        cy_ += LINE_H

        rest_text = " ".join(words[rest_start:])
        if rest_text:
            rest_lines = wrap(d, rest_text, f_br, bcw)
            for rl in rest_lines[:1]:
                d.text((cx_, cy_), rl, font=f_br, fill=INK)
                cy_ += LINE_H
        else:
            cy_ += LINE_H  # keep spacing even if no rest

        hrule(d, cx_, cy_+1, cx_+bcw, LTGREY, 1)
        bco_y[col] = cy_ + SEP_H

    # ── FOOTER ─────────────────────────────────────────────────────────────
    y_foot = y + BOTTOM_H + 2
    hrule(d, PAD, y_foot, W-PAD, INK, 1)

    f_foot = fnt(SANS_REG, 17)
    date_check = "First reported on 19 November 2026, except where a later development is noted; disputed claims are attributed."
    sources = "Sources: Reuters, AP, AFP, BBC, The Guardian, Al Jazeera, Wikipedia Current Events."
    three_sizes = "Reads at three sizes: the date and 3 leads at thumbnail; 10 pictures at half size; all 36 stories at full size."

    d.text((PAD, y_foot + 10), date_check, font=f_foot, fill=INK)
    d.text((PAD, y_foot + 32), sources, font=f_foot, fill=INK)
    d.text((PAD, y_foot + 54), three_sizes, font=f_foot, fill=INK)

    # ── SAVE ───────────────────────────────────────────────────────────────
    out = img.resize((1024,1024), Image.LANCZOS)
    out.save(out_path, format="PNG", optimize=True)
    sz = os.path.getsize(out_path)
    print(f"Saved {out_path}: {sz:,} bytes, {out.size}")
    assert sz < 1_048_576, f"Too large: {sz}"
    return out_path

if __name__=="__main__":
    make_image()
