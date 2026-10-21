"""Carrusel 1080×1350 (4:5) para Instagram/Facebook con fotos reales."""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from marca import *

W, H = 1080, 1350
FOT = os.path.join(S, "photos")
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

WA = "998 154 6066  ·  998 430 9472"


def foto(n, fx=0.5, fy=0.5):
    return cubrir(gradar(Image.open(f"{FOT}/p{n:02d}.jpg")), W, H, fx, fy).convert("RGBA")


def lamina_foto(n, kicker, titulo, it, sub, num, fx=0.5, fy=0.5):
    im = foto(n, fx, fy)
    im.alpha_composite(degradado(W, H, int(H * 0.38), int(H * 0.86), alfa_max=245))
    d = ImageDraw.Draw(im)
    texto_espaciado(d, (80, 1030), kicker.upper(), fuente("montserrat", 22, "Medium"), ORO, 0.32)
    ft = fuente("cormorant", 78, "Light")
    fi = fuente("cormorant-it", 78, "Light")
    x = 78
    d.text((x, 1120), titulo, font=ft, fill=MARFIL, anchor="ls")
    if it:
        x += d.textlength(titulo + " ", font=ft)
        d.text((x, 1120), it, font=fi, fill=ORO, anchor="ls")
    if sub:
        d.text((80, 1185), sub, font=fuente("montserrat", 26, "Light"), fill=MARFIL, anchor="ls")
    d.line([(80, 1250), (150, 1250)], fill=ORO, width=2)
    texto_espaciado(d, (W - 80, 1250), f"{num:02d} / 12", fuente("montserrat", 18, "Regular"), MARFIL, 0.25, "rm")
    return im


laminas = []

# 01 Portada
im = foto(8, 0.5, 0.55)
im.alpha_composite(degradado(W, H, 0, 420, alfa_max=150, arriba=True))
im.alpha_composite(degradado(W, H, int(H * 0.5), H, alfa_max=240))
d = ImageDraw.Draw(im)
texto_espaciado(d, (W / 2, 110), "LAGOS DEL SOL  ·  CANCÚN", fuente("montserrat", 24, "Medium"), MARFIL, 0.35, "mm")
d.text((W / 2, 980), "Vivir frente", font=fuente("cormorant", 118, "Light"), fill=MARFIL, anchor="ms")
d.text((W / 2, 1100), "al lago", font=fuente("cormorant-it", 128, "Light"), fill=ORO, anchor="ms")
texto_espaciado(d, (W / 2, 1185), "$23,900,000 MXN", fuente("montserrat", 34, "Regular"), MARFIL, 0.12, "mm")
texto_espaciado(d, (W / 2, 1275), "DESLIZA  →", fuente("montserrat", 18, "Medium"), ORO, 0.4, "mm")
laminas.append(im)

# 02 Fachada + datos
im = foto(1, 0.35, 0.5)
banda = Image.new("RGBA", (W, 400), ESPRESSO + (238,))
im.alpha_composite(banda, (0, H - 400))
d = ImageDraw.Draw(im)
texto_espaciado(d, (80, H - 330), "RESIDENCIA FRENTE AL LAGO", fuente("montserrat", 22, "Medium"), ORO, 0.32)
d.text((78, H - 240), "Diseño, luz", font=fuente("cormorant", 72, "Light"), fill=MARFIL, anchor="ls")
d.text((78 + d.textlength("Diseño, luz ", font=fuente("cormorant", 72, "Light")), H - 240), "y agua",
       font=fuente("cormorant-it", 72, "Light"), fill=ORO, anchor="ls")
datos = [("550", "m² terreno"), ("570", "m² construcción"), ("4", "recámaras"), ("4.5", "baños"), ("4", "estac.")]
cx = 80
for i, (v, t) in enumerate(datos):
    col = 80 + i * 192
    d.text((col, H - 135), v, font=fuente("cormorant", 56, "Regular"), fill=MARFIL, anchor="ls")
    d.text((col, H - 95), t, font=fuente("montserrat", 17, "Regular"), fill=ORO, anchor="ls")
texto_espaciado(d, (W - 80, H - 330), "02 / 12", fuente("montserrat", 18, "Regular"), MARFIL, 0.25, "rm")
laminas.append(im)

laminas.append(lamina_foto(46, "Acceso cubierto", "La", "llegada", "Madera cálida sobre piedra.", 3, 0.5, 0.5))
laminas.append(lamina_foto(31, "Sala a doble altura", "La luz entra", "desde el lago", "", 4, 0.5, 0.35))
laminas.append(lamina_foto(4, "Terraza techada a doble altura", "Abierta al", "jardín", "", 5, 0.5, 0.4))
laminas.append(lamina_foto(5, "Alberca infinity", "Se funde con", "el lago", "", 6, 0.5, 0.5))
laminas.append(lamina_foto(44, "Jardín · Acceso al lago", "El horizonte,", "en casa", "", 7, 0.5, 0.5))
laminas.append(lamina_foto(24, "Planta alta", "Amanecer", "frente al agua", "", 8, 0.5, 0.5))
laminas.append(lamina_foto(26, "Vestidor y baño completo", "En cada", "recámara", "4 recámaras · 4.5 baños", 9, 0.5, 0.45))
laminas.append(lamina_foto(34, "Baños", "Materiales", "nobles", "Madera, piedra y cristal.", 10, 0.5, 0.5))

# 11 Ubicación
im = foto(21, 0.5, 0.5)
im.alpha_composite(Image.new("RGBA", (W, H), ESPRESSO + (175,)))
d = ImageDraw.Draw(im)
texto_espaciado(d, (W / 2, 250), "UBICACIÓN", fuente("montserrat", 22, "Medium"), ORO, 0.4, "mm")
d.text((W / 2, 380), "Residencial", font=fuente("cormorant", 90, "Light"), fill=MARFIL, anchor="ms")
d.text((W / 2, 480), "Lagos del Sol", font=fuente("cormorant-it", 100, "Light"), fill=ORO, anchor="ms")
texto_espaciado(d, (W / 2, 545), "CANCÚN, QUINTANA ROO", fuente("montserrat", 20, "Regular"), MARFIL, 0.3, "mm")
d.line([(W / 2 - 40, 610), (W / 2 + 40, 610)], fill=ORO, width=2)
items = ["40 hectáreas de lagos", "Más de 30 amenidades", "Casa club · Parque del Lago",
         "Gimnasio · SPA · Albercas", "Ciclovía · Canchas deportivas", "Privado, seguro y tranquilo"]
for i, t in enumerate(items):
    d.text((W / 2, 700 + i * 80), t, font=fuente("montserrat", 30, "Light"), fill=MARFIL, anchor="ms")
texto_espaciado(d, (W / 2, 1250), "11 / 12", fuente("montserrat", 18, "Regular"), MARFIL, 0.25, "mm")
laminas.append(im)

# 12 Cierre / CTA (marfil para que el logo oficial se lea tal cual)
im = Image.new("RGBA", (W, H), MARFIL + (255,))
d = ImageDraw.Draw(im)
lg = logo(250)
im.alpha_composite(lg, ((W - lg.width) // 2, 150))
d.line([(W / 2 - 40, 480), (W / 2 + 40, 480)], fill=ORO, width=2)
d.text((W / 2, 590), "Agende su", font=fuente("cormorant", 92, "Light"), fill=ESPRESSO, anchor="ms")
d.text((W / 2, 690), "visita privada", font=fuente("cormorant-it", 96, "Light"), fill=ORO, anchor="ms")
texto_espaciado(d, (W / 2, 790), "CASA FRENTE AL LAGO · LAGOS DEL SOL", fuente("montserrat", 20, "Medium"), ESPRESSO, 0.25, "mm")
texto_espaciado(d, (W / 2, 860), "$23,900,000 MXN", fuente("montserrat", 38, "Regular"), ESPRESSO, 0.1, "mm")
box = Image.new("RGBA", (W - 200, 170), ESPRESSO + (255,))
im.alpha_composite(box, (100, 960))
texto_espaciado(d, (W / 2, 1010), "WHATSAPP", fuente("montserrat", 20, "Medium"), ORO, 0.4, "mm")
d.text((W / 2, 1075), WA, font=fuente("montserrat", 36, "Regular"), fill=MARFIL, anchor="ms")
texto_espaciado(d, (W / 2, 1230), "@ALTAVIDAINMUEBLES", fuente("montserrat", 20, "Medium"), ESPRESSO, 0.3, "mm")
laminas.append(im)

for i, im in enumerate(laminas, 1):
    im.convert("RGB").save(f"{OUT}/carrusel_{i:02d}.jpg", quality=93, subsampling=0)
print(len(laminas), "láminas")
