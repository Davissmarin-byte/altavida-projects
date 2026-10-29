"""Rótulos de marca para los videos (PNG RGBA a cuadro completo).

Zonas seguras 9:16: arriba desde y=230 (barra de la app) y abajo hasta y=1560
(la descripción y los botones de Reels/TikTok tapan el último tramo y el borde derecho).
"""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from marca import *

WA = "998 154 6066"
WA2 = "998 430 9472"
NOTA_MUESTRA = "DEPTO MUESTRA · MUEBLES Y DECORACIÓN NO INCLUIDOS"
NOTA_PRECIO = "Precio según forma de pago y paquete. Sujeto a cambio sin previo aviso. Gastos de escrituración no incluidos."


def lienzo(W, H):
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def partir(d, txt, f, ancho):
    """Divide en líneas que quepan en `ancho`."""
    lineas, cur = [], ""
    for p in txt.split():
        prueba = (cur + " " + p).strip()
        if d.textlength(prueba, font=f) <= ancho or not cur:
            cur = prueba
        else:
            lineas.append(cur)
            cur = p
    if cur:
        lineas.append(cur)
    return lineas


def caja(c, x0, y0, x1, y1, color=ESPRESSO, alfa=215, r=22):
    capa = lienzo(*c.size)
    ImageDraw.Draw(capa).rounded_rectangle((x0, y0, x1, y1), r, fill=color + (alfa,))
    c.alpha_composite(capa)


def subtitulo(W, H, txt, oro=(), y=None, tam=None):
    """Subtítulo grande centrado; las palabras de `oro` van en color oro."""
    c = lienzo(W, H)
    d = ImageDraw.Draw(c)
    vertical = H > W
    tam = tam or (58 if vertical else 46)
    f = fuente("montserrat", tam, "Bold")
    ancho = W - (200 if vertical else 700)
    lineas = partir(d, txt, f, ancho)
    alto_l = int(tam * 1.28)
    y = y or (1330 if vertical else H - 120 - alto_l * len(lineas))
    mx = max(d.textlength(l, font=f) for l in lineas)
    cx = W / 2
    caja(c, cx - mx / 2 - 34, y - 26, cx + mx / 2 + 34, y + alto_l * len(lineas) + 14, alfa=205)
    d = ImageDraw.Draw(c)
    oro = {o.lower().strip(".,:") for o in oro}
    for i, l in enumerate(lineas):
        palabras = l.split()
        lw = d.textlength(l, font=f)
        x = cx - lw / 2
        for p in palabras:
            col = ORO if p.lower().strip(".,:¿?") in oro else MARFIL
            d.text((x, y + i * alto_l), p, font=f, fill=col, anchor="la")
            x += d.textlength(p + " ", font=f)
    return c


def etiqueta(W, H, txt, y, x=None, oro=False, tam=24, alfa=200):
    """Píldora pequeña (ej. ENTREGA INMEDIATA, DEPTO MUESTRA)."""
    c = lienzo(W, H)
    d = ImageDraw.Draw(c)
    f = fuente("montserrat", tam, "SemiBold")
    esp = tam * 0.18
    ancho = sum(d.textlength(ch, font=f) for ch in txt) + esp * (len(txt) - 1)
    x = W / 2 - ancho / 2 if x is None else x
    fondo, tinta = (ORO, ESPRESSO) if oro else (ESPRESSO, MARFIL)
    caja(c, x - 22, y - tam * 0.95, x + ancho + 22, y + tam * 0.75, color=fondo, alfa=255 if oro else alfa, r=int(tam))
    d = ImageDraw.Draw(c)
    texto_espaciado(d, (x, y), txt, f, tinta, 0.18, "lm")
    return c


def nota(W, H, txt, y=None, tam=None):
    """Texto legal pequeño, legible pero discreto."""
    c = lienzo(W, H)
    d = ImageDraw.Draw(c)
    vertical = H > W
    tam = tam or (22 if vertical else 20)
    f = fuente("montserrat", tam, "Medium")
    lineas = partir(d, txt, f, W - 200)
    y = y or (1575 if vertical else H - 40 - len(lineas) * tam * 1.3)
    mx = max(d.textlength(l, font=f) for l in lineas)
    caja(c, W / 2 - mx / 2 - 20, y - tam, W / 2 + mx / 2 + 20, y + (len(lineas) - 1) * tam * 1.3 + tam, alfa=190, r=12)
    d = ImageDraw.Draw(c)
    for i, l in enumerate(lineas):
        yy = y + i * tam * 1.3
        d.text((W / 2 + 2, yy + 2), l, font=f, fill=(0, 0, 0, 170), anchor="mm")
        d.text((W / 2, yy), l, font=f, fill=MARFIL + (235,), anchor="mm")
    return c


def gancho(W, H, kicker, titulo, it=None, y=330):
    """Título grande superior con degradado (Cormorant + Montserrat)."""
    c = lienzo(W, H)
    c.alpha_composite(degradado(W, H, 0, y + 330, alfa_max=235, arriba=True))
    d = ImageDraw.Draw(c)
    if kicker:
        texto_espaciado(d, (W / 2, y - 135), kicker.upper(), fuente("montserrat", 28, "SemiBold"), ORO, 0.3, "mm")
    ft = fuente("cormorant", 124, "SemiBold")
    lineas = partir(d, titulo, ft, W - 120)
    for i, l in enumerate(lineas):
        d.text((W / 2 + 3, y + i * 122 + 3), l, font=ft, fill=(0, 0, 0, 140), anchor="ms")
        d.text((W / 2, y + i * 122), l, font=ft, fill=MARFIL, anchor="ms")
    if it:
        fi = fuente("cormorant-it", 128, "SemiBold")
        yy = y + len(lineas) * 122 + 8
        d.text((W / 2 + 3, yy + 3), it, font=fi, fill=(0, 0, 0, 150), anchor="ms")
        d.text((W / 2, yy), it, font=fi, fill=ORO, anchor="ms")
    return c


def precio(W, H, cifra="$1,880,000", y=None):
    """Bloque de precio con créditos aceptados."""
    c = lienzo(W, H)
    vertical = H > W
    y = y or (820 if vertical else 360)
    bw = 900 if vertical else 860
    x0 = (W - bw) / 2
    caja(c, x0, y, x0 + bw, y + 520, alfa=228, r=28)
    d = ImageDraw.Draw(c)
    texto_espaciado(d, (W / 2, y + 70), "DESDE", fuente("montserrat", 30, "SemiBold"), ORO, 0.4, "mm")
    d.text((W / 2, y + 205), cifra, font=fuente("cormorant", 150, "SemiBold"), fill=MARFIL, anchor="ms")
    texto_espaciado(d, (W / 2, y + 255), "MXN", fuente("montserrat", 26, "Medium"), MARFIL, 0.4, "mm")
    d.line([(W / 2 - 50, y + 300), (W / 2 + 50, y + 300)], fill=ORO, width=3)
    d.text((W / 2, y + 365), "Infonavit · Fovissste · Bancario", font=fuente("montserrat", 38, "SemiBold"), fill=MARFIL, anchor="mm")
    d.text((W / 2, y + 440), "Entrega inmediata", font=fuente("cormorant-it", 62, "SemiBold"), fill=ORO, anchor="mm")
    return c


def pregunta(W, H, txt, num=None):
    """Tarjeta de pregunta a pantalla completa (FAQ)."""
    c = Image.new("RGBA", (W, H), ESPRESSO + (255,))
    d = ImageDraw.Draw(c)
    if num:
        texto_espaciado(d, (W / 2, 640), f"PREGUNTA {num}", fuente("montserrat", 30, "SemiBold"), ORO, 0.4, "mm")
    ft = fuente("cormorant-it", 118, "SemiBold")
    lineas = partir(d, txt, ft, W - 160)
    y0 = 960 - len(lineas) * 62
    for i, l in enumerate(lineas):
        d.text((W / 2, y0 + i * 124), l, font=ft, fill=MARFIL, anchor="mm")
    d.line([(W / 2 - 50, y0 + len(lineas) * 124 + 10), (W / 2 + 50, y0 + len(lineas) * 124 + 10)], fill=ORO, width=3)
    texto_espaciado(d, (W / 2, 1480), "ALTA VIDA INMUEBLES", fuente("montserrat", 24, "SemiBold"), ORO, 0.4, "mm")
    return c


def respuesta(W, H, txt, oro=()):
    """Respuesta grande sobre el video (mitad inferior)."""
    return subtitulo(W, H, txt, oro=oro, y=1180, tam=62)


def firma(W, H):
    """Marca discreta arriba: ALTA VIDA INMUEBLES."""
    c = lienzo(W, H)
    d = ImageDraw.Draw(c)
    y = 250 if H > W else 60
    texto_espaciado(d, (W / 2 + 2, y + 2), "ALTA VIDA INMUEBLES", fuente("montserrat", 24, "SemiBold"), (0, 0, 0, 150), 0.42, "mm")
    texto_espaciado(d, (W / 2, y), "ALTA VIDA INMUEBLES", fuente("montserrat", 24, "SemiBold"), MARFIL, 0.42, "mm")
    return c


def cierre(W, H, linea="Te precalificamos gratis hoy", ia=False):
    """Cierre marfil con logo oficial, CTA único y WhatsApp."""
    c = Image.new("RGBA", (W, H), MARFIL + (255,))
    d = ImageDraw.Draw(c)
    vertical = H > W
    if vertical:
        lg = logo(300)
        c.alpha_composite(lg, ((W - lg.width) // 2, 300))
        y = 800
    else:
        lg = logo(220)
        c.alpha_composite(lg, ((W - lg.width) // 2, 70))
        y = 420
    d.text((W / 2, y), "Escríbenos por WhatsApp", font=fuente("cormorant", 84 if vertical else 76, "SemiBold"), fill=ESPRESSO, anchor="ms")
    d.text((W / 2, y + 95), linea, font=fuente("cormorant-it", 84 if vertical else 76, "SemiBold"), fill=ORO, anchor="ms")
    bw = 880 if vertical else 1000
    caja(c, (W - bw) / 2, y + 150, (W + bw) / 2, y + (420 if vertical else 300), alfa=255, r=26)
    d = ImageDraw.Draw(c)
    texto_espaciado(d, (W / 2, y + 205), "WHATSAPP", fuente("montserrat", 26, "SemiBold"), ORO, 0.45, "mm")
    if vertical:
        d.text((W / 2, y + 290), WA, font=fuente("montserrat", 76, "Bold"), fill=MARFIL, anchor="mm")
        d.text((W / 2, y + 370), WA2, font=fuente("montserrat", 44, "Medium"), fill=MARFIL, anchor="mm")
    else:
        d.text((W / 2, y + 255), f"{WA}   ·   {WA2}", font=fuente("montserrat", 56, "Bold"), fill=MARFIL, anchor="mm")
    yb = y + (520 if vertical else 370)
    texto_espaciado(d, (W / 2, yb), "@ALTAVIDAINMUEBLES", fuente("montserrat", 26, "SemiBold"), ESPRESSO, 0.35, "mm")
    texto_espaciado(d, (W / 2, yb + 50), "AV. HUAYACÁN · CANCÚN", fuente("montserrat", 22, "Medium"), ORO, 0.35, "mm")
    if ia:
        d.text((W / 2, H - (380 if vertical else 40)), "Voz en off generada con IA", font=fuente("montserrat", 20, "Medium"), fill=ESPRESSO + (170,), anchor="mm")
    return c


def lista(W, H, titulo, items, kicker=None, y=520):
    """Tarjeta translúcida con lista (amenidades, ficha)."""
    c = lienzo(W, H)
    c.alpha_composite(Image.new("RGBA", (W, H), ESPRESSO + (150,)))
    d = ImageDraw.Draw(c)
    if kicker:
        texto_espaciado(d, (W / 2, y - 90), kicker.upper(), fuente("montserrat", 28, "SemiBold"), ORO, 0.35, "mm")
    d.text((W / 2, y), titulo, font=fuente("cormorant", 100, "SemiBold"), fill=MARFIL, anchor="ms")
    d.line([(W / 2 - 50, y + 50), (W / 2 + 50, y + 50)], fill=ORO, width=3)
    f = fuente("montserrat", 44, "Medium")
    for i, t in enumerate(items):
        d.text((W / 2, y + 140 + i * 82), t, font=f, fill=MARFIL, anchor="mm")
    return c


def panel(W, H, kicker, titulo, it=None, cuerpo=(), x=960):
    """Panel de texto a la derecha del video vertical en 16:9 (YouTube)."""
    c = lienzo(W, H)
    d = ImageDraw.Draw(c)
    y = 330
    if kicker:
        texto_espaciado(d, (x, y), kicker.upper(), fuente("montserrat", 26, "SemiBold"), ORO, 0.32, "lm")
    ft = fuente("cormorant", 88, "SemiBold")
    lineas = partir(d, titulo, ft, W - x - 90)
    for i, l in enumerate(lineas):
        d.text((x, y + 100 + i * 90), l, font=ft, fill=MARFIL, anchor="ls")
    yy = y + 100 + len(lineas) * 90
    if it:
        d.text((x, yy), it, font=fuente("cormorant-it", 88, "SemiBold"), fill=ORO, anchor="ls")
        yy += 90
    d.line([(x, yy - 30), (x + 90, yy - 30)], fill=ORO, width=3)
    f = fuente("montserrat", 34, "Medium")
    for i, t in enumerate(cuerpo):
        d.text((x, yy + 30 + i * 56), t, font=f, fill=MARFIL, anchor="ls")
    return c


def tarjeta(W, H, kicker, titulo, it=None, cuerpo=(), fondo=None, nota_txt=None):
    """Tarjeta informativa a cuadro completo (16:9 o 9:16) sobre foto oscurecida o espresso."""
    c = Image.new("RGBA", (W, H), ESPRESSO + (255,))
    if fondo is not None:
        c.alpha_composite(cubrir(gradar(fondo), W, H).convert("RGBA"))
        c.alpha_composite(Image.new("RGBA", (W, H), ESPRESSO + (185,)))
    d = ImageDraw.Draw(c)
    vertical = H > W
    y = 560 if vertical else 250
    texto_espaciado(d, (W / 2, y - 90), kicker.upper(), fuente("montserrat", 28, "SemiBold"), ORO, 0.35, "mm")
    ft = fuente("cormorant", 110 if vertical else 100, "SemiBold")
    lineas = partir(d, titulo, ft, W - 160)
    for i, l in enumerate(lineas):
        d.text((W / 2, y + i * 108), l, font=ft, fill=MARFIL, anchor="ms")
    y += len(lineas) * 108
    if it:
        d.text((W / 2, y), it, font=fuente("cormorant-it", 104 if vertical else 96, "SemiBold"), fill=ORO, anchor="ms")
        y += 100
    d.line([(W / 2 - 50, y - 40), (W / 2 + 50, y - 40)], fill=ORO, width=3)
    f = fuente("montserrat", 42 if vertical else 38, "Medium")
    for i, t in enumerate(cuerpo):
        d.text((W / 2, y + 40 + i * (74 if vertical else 62)), t, font=f, fill=MARFIL, anchor="mm")
    if nota_txt:
        c.alpha_composite(nota(W, H, nota_txt, y=H - (330 if H >= 1900 else 110 if vertical else 50)))
    return c
