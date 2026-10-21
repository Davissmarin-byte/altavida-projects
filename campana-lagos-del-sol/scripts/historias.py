"""Historias 1080×1920: JPG + MP4 de 7 s con movimiento lento y música."""
import os, subprocess, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from marca import *

W, H, FPS, DUR = 1080, 1920, 30, 7
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
MUS = os.path.join(S, "out", "audio", "musica_historia.wav")
WA = "998 154 6066  ·  998 430 9472"


def fondo(n, fx=0.5, fy=0.5):
    return cubrir(gradar(Image.open(f"{S}/photos/p{n:02d}.jpg")), int(W * 1.1), int(H * 1.1), fx, fy)


def capa_texto(kicker, titulo, it, sub=None, y=1470):
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c.alpha_composite(degradado(W, H, int(H * 0.38), int(H * 0.72), alfa_max=240))
    d = ImageDraw.Draw(c)
    texto_espaciado(d, (W / 2, y - 120), kicker.upper(), fuente("montserrat", 28, "Medium"), ORO, 0.32, "mm")
    d.text((W / 2, y), titulo, font=fuente("cormorant", 100, "Light"), fill=MARFIL, anchor="ms")
    if it:
        d.text((W / 2, y + 110), it, font=fuente("cormorant-it", 104, "Light"), fill=ORO, anchor="ms")
    if sub:
        d.text((W / 2, y + 210), sub, font=fuente("montserrat", 32, "Light"), fill=MARFIL, anchor="ms")
    return c


def marca_sup(c):
    c.alpha_composite(degradado(W, H, 0, 420, alfa_max=150, arriba=True))
    d = ImageDraw.Draw(c)
    texto_espaciado(d, (W / 2, 250), "ALTA VIDA INMUEBLES", fuente("montserrat", 22, "Medium"), MARFIL, 0.4, "mm")
    return c


historias = []
historias.append((fondo(8, 0.5, 0.55), capa_texto("Lagos del Sol · Cancún", "Vivir frente", "al lago", "Muy pronto, todos los detalles.")))
historias.append((fondo(31, 0.5, 0.3), capa_texto("Planta baja", "Sala a", "doble altura")))
historias.append((fondo(5), capa_texto("Jardín", "Alberca infinity", "y acceso al lago")))
historias.append((fondo(24), capa_texto("Planta alta", "Amanecer", "frente al agua", "4 recámaras con vestidor y baño")))

# precio
c = capa_texto("Casa frente al lago", "$23,900,000", "MXN", None, y=1330)
d = ImageDraw.Draw(c)
datos = [("550", "m² terreno"), ("570", "m² constr."), ("4", "recámaras"), ("4.5", "baños")]
for i, (v, t) in enumerate(datos):
    x = 150 + i * 260
    d.text((x, 1600), v, font=fuente("cormorant", 70, "Regular"), fill=MARFIL, anchor="ms")
    d.text((x, 1650), t, font=fuente("montserrat", 22, "Regular"), fill=ORO, anchor="ms")
historias.append((fondo(1, 0.3, 0.5), c))

# CTA con espacio para encuesta / pregunta de Instagram
c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
c.alpha_composite(Image.new("RGBA", (W, H), ESPRESSO + (205,)))
d = ImageDraw.Draw(c)
d.text((W / 2, 560), "¿Le gustaría", font=fuente("cormorant", 104, "Light"), fill=MARFIL, anchor="ms")
d.text((W / 2, 680), "conocerla?", font=fuente("cormorant-it", 110, "Light"), fill=ORO, anchor="ms")
d.line([(W / 2 - 40, 760), (W / 2 + 40, 760)], fill=ORO, width=2)
# zona libre 820–1180 para el sticker de encuesta en Instagram
caja = Image.new("RGBA", (880, 170), MARFIL + (255,))
c.alpha_composite(caja, (100, 1300))
texto_espaciado(d, (W / 2, 1350), "WHATSAPP · VISITA PRIVADA", fuente("montserrat", 22, "Medium"), ESPRESSO, 0.3, "mm")
d.text((W / 2, 1420), WA, font=fuente("montserrat", 38, "Regular"), fill=ESPRESSO, anchor="ms")
texto_espaciado(d, (W / 2, 1560), "@ALTAVIDAINMUEBLES", fuente("montserrat", 22, "Medium"), MARFIL, 0.3, "mm")
historias.append((fondo(6), c))

for i, (bg, capa) in enumerate(historias, 1):
    marca_sup(capa)
    # JPG
    fr = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width + W) // 2, (bg.height + H) // 2)).convert("RGBA")
    fr.alpha_composite(capa)
    fr.convert("RGB").save(f"{OUT}/historia_{i:02d}.jpg", quality=93, subsampling=0)
    # MP4
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-ss", str((i - 1) * DUR % 30), "-i", MUS,
                           "-filter_complex", f"[1:a]volume=0.8,afade=t=in:d=0.6,afade=t=out:st={DUR - 0.8}:d=0.8[a]",
                           "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-crf", "19", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "160k", "-t", str(DUR), "-movflags", "+faststart",
                           f"{OUT}/historia_{i:02d}.mp4"], stdin=subprocess.PIPE)
    n = DUR * FPS
    for k in range(n):
        u = k / n
        u = u * u * (3 - 2 * u)
        z = 1.0 + 0.08 * u
        cw, ch = bg.width / 1.1 / z * 1.0, bg.height / 1.1 / z
        cx, cy = bg.width / 2, bg.height / 2
        f = bg.resize((W, H), Image.BICUBIC, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)).convert("RGBA")
        a = min(1, k / (0.7 * FPS))
        if a < 1:
            r, g, b, al = capa.split()
            f.alpha_composite(Image.merge("RGBA", (r, g, b, al.point(lambda v: int(v * a)))))
        else:
            f.alpha_composite(capa)
        ff.stdin.write(f.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait()
print(len(historias), "historias")
