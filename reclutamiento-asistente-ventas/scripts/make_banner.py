import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "static")

# ---- Brand palette ----
DARK = (28, 21, 16)        # #1C1510
GOLD = (201, 169, 110)     # #C9A96E
CREAM = (253, 252, 248)    # #FDFCF8
CREAM2 = (245, 239, 230)   # #F5EFE6
GOLD_DIM = (150, 126, 82)

W, H = 1080, 1350

def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)

def text_w(draw, s, f, tracking=0):
    if not s:
        return 0
    total = 0
    for ch in s:
        adv = draw.textlength(ch, font=f)
        total += adv + tracking
    return total - tracking

def draw_tracked(draw, xy, s, f, fill, tracking=0, anchor_center_x=None):
    if anchor_center_x is not None:
        w = text_w(draw, s, f, tracking)
        x = anchor_center_x - w / 2
    else:
        x = xy[0]
    y = xy[1]
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        adv = draw.textlength(ch, font=f)
        x += adv + tracking
    return x

def centered_text(draw, cx, y, s, f, fill, tracking=0):
    draw_tracked(draw, (0, y), s, f, fill, tracking=tracking, anchor_center_x=cx)

# ---- Base canvas ----
img = Image.new("RGB", (W, H), DARK)
draw = ImageDraw.Draw(img)

# Subtle vignette / radial glow near top for depth
glow = Image.new("L", (W, H), 0)
gdraw = ImageDraw.Draw(glow)
gdraw.ellipse([W/2 - 700, -650, W/2 + 700, 650], fill=60)
glow = glow.filter(ImageFilter.GaussianBlur(180))
glow_img = Image.new("RGB", (W, H), (60, 48, 32))
img = Image.composite(glow_img, img, glow)
draw = ImageDraw.Draw(img)

# ---- Coastal gradient zone (bottom ~34%) ----
coast_top = int(H * 0.665)
coast_h = H - coast_top
coast = Image.new("RGB", (W, coast_h))
top_c = (22, 46, 48)     # deep teal
mid_c = (58, 110, 108)   # turquoise-teal
bot_c = (198, 168, 108)  # sand/gold
for y in range(coast_h):
    t = y / coast_h
    if t < 0.55:
        tt = t / 0.55
        c = tuple(int(top_c[i] + (mid_c[i]-top_c[i])*tt) for i in range(3))
    else:
        tt = (t-0.55)/0.45
        c = tuple(int(mid_c[i] + (bot_c[i]-mid_c[i])*tt) for i in range(3))
    draw2 = ImageDraw.Draw(coast)
    draw2.line([(0,y),(W,y)], fill=c)
img.paste(coast, (0, coast_top))
draw = ImageDraw.Draw(img)

# soft blend seam between dark panel and coast
seam = Image.new("L", (W, 140), 0)
sdraw = ImageDraw.Draw(seam)
for y in range(140):
    a = int(255 * (1 - y/140))
    sdraw.line([(0,y),(W,y)], fill=a)
dark_rect = Image.new("RGB", (W, 140), DARK)
img.paste(Image.composite(dark_rect, img.crop((0, coast_top-70, W, coast_top+70)), seam), (0, coast_top-70))
draw = ImageDraw.Draw(img)

# Thin gold horizon line + minimalist sun arc, positioned low in the coastal zone
horizon_y = coast_top + int(coast_h * 0.62)
draw.line([(0, horizon_y), (W, horizon_y)], fill=GOLD, width=2)
sun_r = 34
sun_cx, sun_cy = W/2, horizon_y
draw.arc([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r], start=180, end=360, fill=CREAM, width=3)
draw.arc([sun_cx - sun_r-20, sun_cy - sun_r-20, sun_cx + sun_r+20, sun_cy + sun_r+20], start=200, end=340, fill=GOLD_DIM, width=1)

# gentle wave lines between horizon and footer
for i, dy in enumerate([26, 50, 74]):
    y = horizon_y + dy
    pts = []
    for x in range(0, W+20, 20):
        yy = y + math.sin((x/W)*4*math.pi + i) * (3 + i*1.2)
        pts.append((x, yy))
    draw.line(pts, fill=(255,255,255), width=1, joint="curve")

# ============ HEADER ============
cx = W/2
top_y = 92

# Diamond logomark
dia_size = 15
dx, dy = cx, top_y + dia_size
draw.polygon([(dx, dy-dia_size), (dx+dia_size, dy), (dx, dy+dia_size), (dx-dia_size, dy)], outline=GOLD, width=2)

wordmark_f = font("CormorantGaramond-SemiBold.ttf", 54)
y_word = top_y + dia_size*2 + 18
centered_text(draw, cx, y_word, "ALTA VIDA", wordmark_f, CREAM, tracking=10)

sub_f = font("Montserrat-Regular.ttf", 15)
centered_text(draw, cx, y_word + 62, "I N M U E B L E S", sub_f, GOLD, tracking=0)

# thin rule
rule_y = y_word + 100
draw.line([(cx-70, rule_y), (cx+70, rule_y)], fill=GOLD_DIM, width=1)

# ============ ESTAMOS BUSCANDO ============
label_f = font("Montserrat-SemiBold.ttf", 20)
centered_text(draw, cx, rule_y + 34, "E S T A M O S   B U S C A N D O", label_f, GOLD, tracking=0)

# ============ HEADLINE ============
head_f = font("CormorantGaramond-SemiBold.ttf", 92)
head_y1 = rule_y + 78
centered_text(draw, cx, head_y1, "ASISTENTE", head_f, CREAM, tracking=2)
head_y2 = head_y1 + 96
centered_text(draw, cx, head_y2, "DE VENTAS", head_f, GOLD, tracking=2)

italic_f = font("CormorantGaramond-MediumItalic.ttf", 30)
sub2_y = head_y2 + 108
centered_text(draw, cx, sub2_y, "Energía joven. Visión de futuro.", italic_f, CREAM2, tracking=1)

# rule
rule2_y = sub2_y + 56
draw.line([(cx-90, rule2_y), (cx+90, rule2_y)], fill=GOLD_DIM, width=1)

# ============ FEATURE ROW (3 cols) ============
feat_y = rule2_y + 40
cols_x = [W*0.19, W*0.5, W*0.81]
icon_f = font("Montserrat-Medium.ttf", 15)
big_f = font("CormorantGaramond-SemiBold.ttf", 40)

def icon_person(cx_, cy_):
    r = 10
    draw.ellipse([cx_-r, cy_-r-8, cx_+r, cy_+r-8], outline=GOLD, width=2)
    draw.arc([cx_-16, cy_+2, cx_+16, cy_+34], start=180, end=360, fill=GOLD, width=2)

def icon_bolt(cx_, cy_):
    pts = [(cx_+6, cy_-16), (cx_-8, cy_+2), (cx_+1, cy_+2), (cx_-6, cy_+16), (cx_+9, cy_-2), (cx_+1, cy_-2)]
    draw.polygon(pts, fill=GOLD)

def icon_coin(cx_, cy_):
    r = 15
    draw.ellipse([cx_-r, cy_-r, cx_+r, cy_+r], outline=GOLD, width=2)
    f = font("CormorantGaramond-SemiBold.ttf", 20)
    bbox = draw.textbbox((0,0), "$", font=f)
    draw.text((cx_-(bbox[2]-bbox[0])/2, cy_-(bbox[3]-bbox[1])/2-3), "$", font=f, fill=GOLD)

icon_person(cols_x[0], feat_y)
icon_bolt(cols_x[1], feat_y)
icon_coin(cols_x[2], feat_y)

label_y = feat_y + 34
centered_text(draw, cols_x[0], label_y, "19–27", big_f, CREAM, tracking=1)
centered_text(draw, cols_x[1], label_y, "ACTITUD", big_f, CREAM, tracking=1)
centered_text(draw, cols_x[2], label_y, "$10–12K", big_f, CREAM, tracking=1)

small_f = font("Montserrat-Regular.ttf", 14)
label_y2 = label_y + 48
centered_text(draw, cols_x[0], label_y2, "AÑOS", small_f, GOLD_DIM, tracking=2)
centered_text(draw, cols_x[1], label_y2, "GANADORA", small_f, GOLD_DIM, tracking=2)
centered_text(draw, cols_x[2], label_y2, "BASE + BONO", small_f, GOLD_DIM, tracking=1)

# vertical dividers between columns
div_y1 = feat_y - 26
div_y2 = label_y2 + 10
for dvx in [ (cols_x[0]+cols_x[1])/2, (cols_x[1]+cols_x[2])/2 ]:
    draw.line([(dvx, div_y1),(dvx, div_y2)], fill=(90,78,60), width=1)

# ============ CTA / CONTACT (top of coastal zone, clear of horizon+waves) ============
cta_f = font("Montserrat-SemiBold.ttf", 17)
cta_y = coast_top + 24
centered_text(draw, cx, cta_y, "P O S T Ú L A T E   H O Y", cta_f, CREAM, tracking=1)

phone_f = font("CormorantGaramond-SemiBold.ttf", 38)
phone_y = cta_y + 32
centered_text(draw, cx, phone_y, "WhatsApp 998 489 4142", phone_f, CREAM, tracking=1)

foot_f = font("Montserrat-Regular.ttf", 13)
foot_y = H - 34
centered_text(draw, cx, foot_y, "ALTA VIDA INMUEBLES  ·  CANCÚN, MÉXICO", foot_f, (250, 246, 238), tracking=2)

img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "banner", "banner-asistente-ventas.png"))
print("done")
