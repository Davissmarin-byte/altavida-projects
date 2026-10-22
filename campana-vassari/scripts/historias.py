"""Seis historias 9:16: MP4 de 7 s con video real en movimiento + JPG (cuadro fijo).

Uso: python historias.py <carpeta_salida>
La historia 6 deja libre la franja 820–1180 px para el sticker de encuesta y el enlace a WhatsApp.
"""
import os, subprocess, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from capas import *
from montaje import render, cuadro

W, H, DUR = 1080, 1920, 7.0
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
MUS = os.path.join(S, "audio", "musica_historia.wav")
CUADRO_JPG = {2: 0.8}  # segundo del MP4 que se usa como JPG (por defecto 3.5)


def cta_encuesta():
    c = lienzo(W, H)
    c.alpha_composite(Image.new("RGBA", (W, H), ESPRESSO + (170,)))
    d = ImageDraw.Draw(c)
    d.text((W / 2, 560), "¿Ya quieres", font=fuente("cormorant", 120, "SemiBold"), fill=MARFIL, anchor="ms")
    d.text((W / 2, 690), "dejar de rentar?", font=fuente("cormorant-it", 124, "SemiBold"), fill=ORO, anchor="ms")
    # franja libre 820–1180 para la encuesta de Instagram
    caja(c, 100, 1250, W - 100, 1470, color=MARFIL, alfa=255, r=26)
    d = ImageDraw.Draw(c)
    texto_espaciado(d, (W / 2, 1300), "WHATSAPP · PRECALIFICACIÓN GRATIS", fuente("montserrat", 24, "SemiBold"), ESPRESSO, 0.25, "mm")
    d.text((W / 2, 1375), WA, font=fuente("montserrat", 72, "Bold"), fill=ESPRESSO, anchor="mm")
    d.text((W / 2, 1440), WA2, font=fuente("montserrat", 36, "Medium"), fill=ESPRESSO, anchor="mm")
    texto_espaciado(d, (W / 2, 1540), "@ALTAVIDAINMUEBLES", fuente("montserrat", 24, "SemiBold"), MARFIL, 0.35, "mm")
    return c


HISTORIAS = [
    # (fuente, inicio, capas)
    ("w4", 0.0, [gancho(W, H, "Nuevo en Av. Huayacán", "Mira lo que te alcanza", "con tu Infonavit", y=420),
                 subtitulo(W, H, "Sigue viendo  →", y=1450, tam=48)]),
    ("k6564", 0.0, [firma(W, H), etiqueta(W, H, NOTA_MUESTRA, 312, tam=18),
                    subtitulo(W, H, "3 recámaras · 2 baños · cocina incluida", oro=("3", "2", "cocina", "incluida"), y=1250, tam=64)]),
    ("k6564", 44.0, [firma(W, H), etiqueta(W, H, NOTA_MUESTRA, 312, tam=18),
                     gancho(W, H, "3 recámaras", "Un cuarto", "para cada quien", y=520)]),
    ("k6623", 26.0, [firma(W, H), subtitulo(W, H, "Alberca, multicancha y +10 amenidades", oro=("alberca,", "+10"), y=1250, tam=64)]),
    ("k6564", 12.0, [firma(W, H), precio(W, H), nota(W, H, NOTA_PRECIO, y=1420)]),
    ("k6564", 39.0, [cta_encuesta()]),
]

for i, (src, ini, capas_h) in enumerate(HISTORIAS, 1):
    mp4 = os.path.join(OUT, f"historia_{i:02d}.mp4")
    lento = 0.75 if i in (5, 6) else 1.0
    render(mp4, W, H, [dict(src=src, ini=ini, dur=DUR, vel=lento, zoom=(1.0, 1.06))],
           [(c, 0.0, DUR) for c in capas_h], MUS, mus_ini=(i - 1) * 6.0)
    # JPG: un cuadro del MP4 (ya trae los rótulos)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(CUADRO_JPG.get(i, 3.5)), "-i", mp4, "-frames:v", "1", "-q:v", "2",
                    os.path.join(OUT, f"historia_{i:02d}.jpg")], check=True)
    print("historia", i)
