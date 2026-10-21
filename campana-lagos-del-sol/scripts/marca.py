"""Utilidades de marca ALTA VIDA: color, tipografía, gradación y recortes."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

ESPRESSO = (28, 21, 16)
ORO = (201, 169, 110)
MARFIL = (253, 252, 248)

S = os.environ.get("CAMP_SRC", "")
FONTS = os.path.join(S, "fonts")
LOGO = os.path.join(S, "src", "ALTA_VIDA_PNG_.png")


def fuente(familia, tam, estilo):
    archivos = {
        "cormorant": "CormorantGaramond%5Bwght%5D.ttf",
        "cormorant-it": "CormorantGaramond-Italic%5Bwght%5D.ttf",
        "montserrat": "Montserrat%5Bwght%5D.ttf",
    }
    f = ImageFont.truetype(os.path.join(FONTS, archivos[familia]), tam)
    pesos = {"Thin": 100, "ExtraLight": 200, "Light": 300, "Regular": 400,
             "Medium": 500, "SemiBold": 600, "Bold": 700}
    f.set_variation_by_axes([pesos[estilo]])
    return f


def gradar(im):
    """Gradación cálida y suave tipo editorial."""
    im = im.convert("RGB")
    im = ImageEnhance.Color(im).enhance(0.9)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.035 + 3)))
    b = b.point(lambda v: int(v * 0.96))
    im = Image.merge("RGB", (r, g, b))
    return im


def cubrir(im, w, h, fx=0.5, fy=0.5):
    """Recorta y escala para llenar w×h con punto focal (fx, fy)."""
    iw, ih = im.size
    esc = max(w / iw, h / ih)
    nw, nh = int(iw * esc + 0.5), int(ih * esc + 0.5)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = int((nw - w) * fx)
    y = int((nh - h) * fy)
    return im.crop((x, y, x + w, y + h))


def degradado(w, h, desde, hasta, color=ESPRESSO, alfa_max=230, arriba=False):
    """Capa RGBA con degradado vertical del color de marca."""
    capa = Image.new("RGBA", (w, h), color + (0,))
    d = ImageDraw.Draw(capa)
    for y in range(h):
        t = (y - desde) / max(1, hasta - desde)
        if arriba:
            t = 1 - (y / max(1, hasta))
        t = max(0.0, min(1.0, t))
        d.line([(0, y), (w, y)], fill=color + (int(alfa_max * t ** 1.4),))
    return capa


def texto_espaciado(d, xy, txt, f, fill, track=0.0, anchor="la"):
    """Dibuja texto con interletrado (track en fracción del tamaño)."""
    x, y = xy
    esp = f.size * track
    ancho = sum(d.textlength(c, font=f) for c in txt) + esp * (len(txt) - 1)
    if anchor[0] == "m":
        x -= ancho / 2
    elif anchor[0] == "r":
        x -= ancho
    for c in txt:
        d.text((x, y), c, font=f, fill=fill, anchor="l" + anchor[1])
        x += d.textlength(c, font=f) + esp
    return ancho


def logo(alto):
    lg = Image.open(LOGO).convert("RGBA")
    # recorta el margen transparente sin alterar el diseño
    lg = lg.crop(lg.getbbox())
    esc = alto / lg.height
    return lg.resize((int(lg.width * esc), alto), Image.LANCZOS)
