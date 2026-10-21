"""Miniatura YouTube 1280×720."""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from marca import *

W, H = 1280, 720
im = cubrir(gradar(Image.open(f"{S}/photos/p08.jpg")), W, H, 0.5, 0.3).convert("RGBA")
capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(capa)
for x in range(W):
    a = int(235 * max(0, 1 - x / 820) ** 1.3)
    d.line([(x, 0), (x, H)], fill=ESPRESSO + (a,))
im.alpha_composite(capa)
d = ImageDraw.Draw(im)
texto_espaciado(d, (70, 150), "LAGOS DEL SOL · CANCÚN", fuente("montserrat", 26, "SemiBold"), ORO, 0.3)
d.text((64, 300), "Frente", font=fuente("cormorant", 150, "Regular"), fill=MARFIL, anchor="ls")
d.text((64, 440), "al lago", font=fuente("cormorant-it", 160, "Regular"), fill=ORO, anchor="ls")
d.text((70, 530), "$23.9 MDP", font=fuente("montserrat", 54, "SemiBold"), fill=MARFIL, anchor="ls")
texto_espaciado(d, (70, 600), "ALBERCA INFINITY · ACCESO AL LAGO", fuente("montserrat", 22, "Medium"), MARFIL, 0.2)
badge = Image.new("RGBA", (170, 170), MARFIL + (255,))
lg = logo(130)
badge.alpha_composite(lg, ((170 - lg.width) // 2, 20))
im.alpha_composite(badge, (W - 200, H - 200))
im.convert("RGB").save(sys.argv[1], quality=92)
