"""Carrusel 1080×1350 (4:5) para Instagram/Facebook con cuadros 4K del recorrido real.

Uso: python carrusel.py <carpeta_salida>
"""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from capas import *
from montaje import cuadro

W, H = 1080, 1350
N = 10
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
TMP = os.path.join(OUT, "_cuadros")
os.makedirs(TMP, exist_ok=True)


def foto(src, t, fx=0.5, fy=0.5, w=W, h=H):
    p = cuadro(src, t, os.path.join(TMP, f"{src}_{t}.jpg"))
    return cubrir(gradar(Image.open(p)), w, h, fx, fy).convert("RGBA")


def pie(d, num):
    d.line([(80, 1270), (150, 1270)], fill=ORO, width=2)
    texto_espaciado(d, (W - 80, 1270), f"{num:02d} / {N:02d}", fuente("montserrat", 18, "Medium"), MARFIL, 0.25, "rm")


def lamina(src, t, kicker, titulo, it, sub, num, fx=0.5, fy=0.5, muestra=True):
    im = foto(src, t, fx, fy)
    im.alpha_composite(degradado(W, H, int(H * 0.42), int(H * 0.86), alfa_max=245))
    d = ImageDraw.Draw(im)
    texto_espaciado(d, (80, 1015), kicker.upper(), fuente("montserrat", 24, "SemiBold"), ORO, 0.3)
    ft = fuente("cormorant", 84, "SemiBold")
    d.text((78, 1120), titulo, font=ft, fill=MARFIL, anchor="ls")
    if it:
        d.text((78 + d.textlength(titulo + " ", font=ft), 1120), it, font=fuente("cormorant-it", 84, "SemiBold"), fill=ORO, anchor="ls")
    if sub:
        d.text((80, 1185), sub, font=fuente("montserrat", 30, "Medium"), fill=MARFIL, anchor="ls")
    if muestra:
        im.alpha_composite(etiqueta(W, H, "DEPTO MUESTRA · MUEBLES NO INCLUIDOS", 70, x=80, tam=16))
    pie(d, num)
    return im


laminas = []

# 01 Gancho
im = foto("k6564", 0.3, 0.5, 0.6)
im.alpha_composite(degradado(W, H, 0, 520, alfa_max=210, arriba=True))
im.alpha_composite(degradado(W, H, int(H * 0.45), H, alfa_max=245))
d = ImageDraw.Draw(im)
texto_espaciado(d, (W / 2, 110), "CANCÚN  ·  AV. HUAYACÁN", fuente("montserrat", 24, "SemiBold"), MARFIL, 0.35, "mm")
d.text((W / 2, 900), "Deja de rentar", font=fuente("cormorant", 128, "SemiBold"), fill=MARFIL, anchor="ms")
d.text((W / 2, 1020), "estrena con tu Infonavit", font=fuente("cormorant-it", 92, "SemiBold"), fill=ORO, anchor="ms")
d.text((W / 2, 1110), "3 recámaras · 2 baños · desde $1,880,000", font=fuente("montserrat", 34, "SemiBold"), fill=MARFIL, anchor="ms")
im.alpha_composite(etiqueta(W, H, "ENTREGA INMEDIATA", 1190, oro=True, tam=24))
d = ImageDraw.Draw(im)
texto_espaciado(d, (W / 2, 1285), "DESLIZA  →", fuente("montserrat", 20, "SemiBold"), ORO, 0.4, "mm")
laminas.append(im)

laminas.append(lamina("k6564", 12.2, "Sala y comedor", "Espacio para", "convivir", "Luz natural y ventilación", 2))
laminas.append(lamina("k6564", 6.0, "Cocina incluida", "Lista para", "estrenar", "Incluida en todos los paquetes", 3))
laminas.append(lamina("k6564", 65.3, "Recámara principal", "Tu descanso,", "tuyo", "Clóset en paquete Master", 4))

# 05 Díptico recámaras 2 y 3
im = Image.new("RGBA", (W, H), ESPRESSO + (255,))
im.alpha_composite(foto("k6564", 31.0, w=W // 2 - 6, h=H), (0, 0))
im.alpha_composite(foto("k6564", 45.5, w=W // 2 - 6, h=H), (W // 2 + 6, 0))
im.alpha_composite(degradado(W, H, int(H * 0.42), int(H * 0.86), alfa_max=245))
d = ImageDraw.Draw(im)
texto_espaciado(d, (80, 1015), "3 RECÁMARAS · 2 BAÑOS COMPLETOS", fuente("montserrat", 24, "SemiBold"), ORO, 0.3)
ft = fuente("cormorant", 84, "SemiBold")
d.text((78, 1120), "Un cuarto", font=ft, fill=MARFIL, anchor="ls")
d.text((78 + d.textlength("Un cuarto ", font=ft), 1120), "para cada quien", font=fuente("cormorant-it", 84, "SemiBold"), fill=ORO, anchor="ls")
d.text((80, 1185), "Estudio, cuarto de niños o visitas", font=fuente("montserrat", 30, "Medium"), fill=MARFIL, anchor="ls")
im.alpha_composite(etiqueta(W, H, "DEPTO MUESTRA · MUEBLES NO INCLUIDOS", 70, x=80, tam=16))
pie(d, 5)
laminas.append(im)

# 06 Ficha
fondo = Image.open(cuadro("k6564", 24.5, os.path.join(TMP, "ficha.jpg")))
im = tarjeta(W, H, "Ficha del departamento", "3 recámaras", "2 baños completos",
             ["80.93 m² de construcción", "Sala-comedor", "Cocina incluida", "Área de servicio",
              "Entrega inmediata*"], fondo=fondo,
             nota_txt="*30 días después de la firma de escrituras. Aires acondicionados y clósets según paquete.")
pie(ImageDraw.Draw(im), 6)
laminas.append(im)

# 07 Amenidades
fondo = Image.open(cuadro("k6623", 31.5, os.path.join(TMP, "alberca.jpg")))
im = tarjeta(W, H, "Más de 10 amenidades", "Para toda", "la familia",
             ["Alberca · Multicancha", "Gimnasio al aire libre · Calistenia", "Pista de jogging",
              "Zona Relax · Zona Lotus", "Family Zone · Juegos infantiles", "Caseta de seguridad"], fondo=fondo)
pie(ImageDraw.Draw(im), 7)
laminas.append(im)

# 08 Crédito
fondo = Image.open(cuadro("k6564", 41.0, os.path.join(TMP, "credito.jpg")))
im = tarjeta(W, H, "Crédito", "¿Te alcanza con", "tu Infonavit?",
             ["Infonavit · Fovissste · Bancario", "", "Escríbenos por WhatsApp", "y te precalificamos gratis hoy"],
             fondo=fondo, nota_txt=NOTA_PRECIO)
pie(ImageDraw.Draw(im), 8)
laminas.append(im)

# 09 Ubicación (distancias del brochure del desarrollador)
fondo = Image.open(cuadro("k6623", 18.0, os.path.join(TMP, "ubicacion.jpg")))
im = tarjeta(W, H, "Ubicación", "Av. Huayacán", "Cancún",
             ["Estación Tren Maya · 9.7 km", "Aeropuerto Internacional · 10 km", "Zona Hotelera · 12.5 km",
              "Playa Delfines · 29 km", "Supermercados, escuelas y hospitales cerca"], fondo=fondo)
pie(ImageDraw.Draw(im), 9)
laminas.append(im)

# 10 Cierre
im = Image.new("RGBA", (W, H), MARFIL + (255,))
d = ImageDraw.Draw(im)
lg = logo(240)
im.alpha_composite(lg, ((W - lg.width) // 2, 120))
d.line([(W / 2 - 40, 430), (W / 2 + 40, 430)], fill=ORO, width=2)
d.text((W / 2, 540), "Escríbenos por WhatsApp", font=fuente("cormorant", 82, "SemiBold"), fill=ESPRESSO, anchor="ms")
d.text((W / 2, 635), "te precalificamos gratis hoy", font=fuente("cormorant-it", 78, "SemiBold"), fill=ORO, anchor="ms")
texto_espaciado(d, (W / 2, 720), "DESDE $1,880,000 MXN · ENTREGA INMEDIATA", fuente("montserrat", 24, "SemiBold"), ESPRESSO, 0.15, "mm")
caja(im, 100, 790, W - 100, 1010, alfa=255, r=26)
d = ImageDraw.Draw(im)
texto_espaciado(d, (W / 2, 840), "WHATSAPP", fuente("montserrat", 22, "SemiBold"), ORO, 0.45, "mm")
d.text((W / 2, 915), WA, font=fuente("montserrat", 70, "Bold"), fill=MARFIL, anchor="mm")
d.text((W / 2, 975), WA2, font=fuente("montserrat", 34, "Medium"), fill=MARFIL, anchor="mm")
texto_espaciado(d, (W / 2, 1090), "@ALTAVIDAINMUEBLES", fuente("montserrat", 22, "SemiBold"), ESPRESSO, 0.35, "mm")
d.text((W / 2, 1180), "Precio según forma de pago y paquete. Sujeto a cambio sin previo aviso.",
       font=fuente("montserrat", 20, "Medium"), fill=ESPRESSO + (190,), anchor="mm")
d.text((W / 2, 1210), "Gastos de escrituración no incluidos.", font=fuente("montserrat", 20, "Medium"), fill=ESPRESSO + (190,), anchor="mm")
texto_espaciado(d, (W - 80, 1270), f"{N:02d} / {N:02d}", fuente("montserrat", 18, "Medium"), ESPRESSO, 0.25, "rm")
laminas.append(im)

for i, im in enumerate(laminas, 1):
    im.convert("RGB").save(f"{OUT}/carrusel_{i:02d}.jpg", quality=93, subsampling=0)
print(len(laminas), "láminas")
