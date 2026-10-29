"""Video YouTube 16:9 (~3:10) con el recorrido completo de Kenia, sin narración.

Video vertical a la izquierda sobre fondo desenfocado y panel de texto a la derecha.
Uso: python youtube.py <salida.mp4> <miniatura.jpg>
"""
import json, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from capas import *
from montaje import render, cuadro

W, H = 1920, 1080
OUT, MINI = sys.argv[1], sys.argv[2]
tmp = os.path.dirname(os.path.abspath(OUT))

tomas, capas, capitulos = [], [], []
t = 0.0


def bloque(toma, titulo_cap, panel_args=None, extra=()):
    global t
    capitulos.append((round(t), titulo_cap))
    tomas.append(toma)
    if panel_args:
        capas.append((panel(W, H, *panel_args), t, t + toma["dur"]))
    for c, a, b in extra:
        capas.append((c, t + a, t + b))
    capas.append((firma(W, H), t, t + toma["dur"]))
    t += toma["dur"]


bloque(dict(src="w4", ini=0.0, dur=6.0), "Llegada",
       ("ALTA VIDA Inmuebles presenta", "Departamento de 3 recámaras", "con tu Infonavit", ["Av. Huayacán, Cancún", "Entrega inmediata"]))
bloque(dict(src="k6623", ini=17.0, dur=3.0), "Áreas comunes",
       ("Desarrollo nuevo", "Áreas comunes", None, ["Alberca y jardines"]))
# recorrido completo del depto muestra, con paneles por espacio
k0 = t
bloque(dict(src="k6564", ini=0.0, dur=69.6, zoom=(1.0, 1.03)), "Recorrido del departamento")
for a, b, args in [
    (0, 5, ("Planta", "Sala", None, ["Espacio para convivir"])),
    (5, 11, ("Cocina incluida", "Cocina", "lista para estrenar", ["Incluida en todos los paquetes"])),
    (11, 22, ("Planta", "Sala y comedor", None, ["Luz natural"])),
    (22, 28, ("Baño completo", "Baño", None, ["2 baños completos"])),
    (28, 40, ("Recámara 2", "Recámara", "o estudio", ["Espacio para escritorio"])),
    (40, 43, ("Pasillo", "Distribución", None, ["Recorrido con Kenia Acosta"])),
    (43, 57, ("Recámara 3", "Un cuarto", "para cada quien", [])),
    (57, 69.6, ("Recámara principal", "Recámara", "principal", ["Paquete Master: clósets incluidos"])),
]:
    capas.append((panel(W, H, *args), k0 + a, k0 + b))
    capitulos.append((round(k0 + a), args[1] + (" " + args[2] if args[2] else "")))
capitulos.remove((round(k0), "Recorrido del departamento"))
capas.append((nota(W, H, "Departamento muestra: muebles y decoración no incluidos."), k0, k0 + 69.6))

bloque(dict(src="w2", ini=15.0, dur=9.0), "Área de servicio",
       ("Área de servicio", "Área", "de servicio", []))
bloque(dict(src="w1", ini=0.0, dur=41.5, vel=1.5), "Así se entrega tu departamento",
       ("Así se entrega", "Tu departamento", "tal cual", ["Sin muebles ni decoración", "Cocina incluida", "Listo para habitar"]))
bloque(dict(src="k6623", ini=10.2, dur=24.3), "Amenidades",
       ("Más de 10 amenidades", "Vive", "en comunidad", ["Alberca · Multicancha", "Calistenia · Gimnasio al aire libre",
                                                         "Zona Relax · Zona Lotus", "Family Zone · Juegos infantiles",
                                                         "Caseta de seguridad"]))
bloque(dict(src="k6624a", ini=0.0, dur=4.5, modo="lleno"), "Jardines")
bloque(dict(img=tarjeta(W, H, "Ubicación", "Av. Huayacán, Cancún", None,
                        ["Estación Tren Maya · 9.7 km", "Aeropuerto Internacional · 10 km",
                         "Zona Hotelera · 12.5 km", "Playa Delfines · 29 km"]), dur=8.0, zoom=(1.0, 1.03)), "Ubicación")
bloque(dict(img=tarjeta(W, H, "Precio y crédito", "Desde $1,880,000 MXN", "entrega inmediata",
                        ["Infonavit · Fovissste · Crédito bancario", "Te precalificamos gratis por WhatsApp"],
                        nota_txt=NOTA_PRECIO), dur=8.0, zoom=(1.0, 1.03)), "Precio y crédito")
bloque(dict(img=cierre(W, H), dur=7.0), "Contacto")

total = render(OUT, W, H, tomas, capas, os.path.join(S, "audio", "musica_youtube.wav"), vol_musica=0.6,
               titulo="Departamento de 3 recámaras con Infonavit en Cancún · Av. Huayacán")
# YouTube exige capítulos de 10 s o más: se fusionan los más cortos con el anterior
capitulos.sort()
limpios = []
for i, (s_, c_) in enumerate(capitulos):
    sig = capitulos[i + 1][0] if i + 1 < len(capitulos) else total
    if limpios and (sig - s_ < 10 or s_ - limpios[-1][0] < 10):
        continue
    limpios.append((s_, c_))
capitulos = limpios
json.dump(capitulos, open(os.path.join(tmp, "youtube_capitulos.json"), "w"), ensure_ascii=False, indent=1)
print("youtube", total)
for s_, c_ in capitulos:
    print(f"{s_ // 60}:{s_ % 60:02d} {c_}")

# miniatura 1280×720
im = Image.open(cuadro("k6564", 0.3, os.path.join(tmp, "mini_src.jpg")))
mini = cubrir(gradar(im), 1280, 720, 0.5, 0.45).convert("RGBA")
mini.alpha_composite(Image.new("RGBA", (1280, 720), ESPRESSO + (0,)))
capa = lienzo(1280, 720)
ImageDraw.Draw(capa).rectangle((0, 0, 700, 720), fill=ESPRESSO + (225,))
mini.alpha_composite(capa)
d = ImageDraw.Draw(mini)
texto_espaciado(d, (60, 120), "CANCÚN · AV. HUAYACÁN", fuente("montserrat", 26, "SemiBold"), ORO, 0.3, "lm")
d.text((56, 250), "3 recámaras", font=fuente("cormorant", 110, "Bold"), fill=MARFIL, anchor="ls")
d.text((56, 360), "con Infonavit", font=fuente("cormorant-it", 104, "Bold"), fill=ORO, anchor="ls")
d.text((60, 450), "Desde $1,880,000", font=fuente("montserrat", 54, "Bold"), fill=MARFIL, anchor="ls")
mini.alpha_composite(etiqueta(1280, 720, "ENTREGA INMEDIATA", 540, x=60, oro=True, tam=28))
d = ImageDraw.Draw(mini)
texto_espaciado(d, (60, 660), "ALTA VIDA INMUEBLES", fuente("montserrat", 22, "SemiBold"), MARFIL, 0.4, "lm")
mini.convert("RGB").save(MINI, quality=92)
