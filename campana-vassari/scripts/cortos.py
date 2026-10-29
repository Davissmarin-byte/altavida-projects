"""Tres Reels cortos 9:16, sin voz, cortados al ritmo (112 bpm → 1.07 s = 2 tiempos).

Uso: python cortos.py rentar|faq|amenidades <salida.mp4>
Cada uno tiene un estilo distinto para no repetir el Reel principal:
  rentar      POV con Kenia abriendo la puerta y cortes rápidos con rótulos grandes
  faq         tarjetas de pregunta + respuesta sobre el recorrido
  amenidades  montaje exterior rápido y lista de amenidades del brochure
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from capas import *
from montaje import render

W, H = 1080, 1920
B2 = 60 / 112 * 2
PIEZA, OUT = sys.argv[1], sys.argv[2]
MUS = os.path.join(S, "audio", "musica_corto.wav")


def grande(txt, oro=()):
    return subtitulo(W, H, txt, oro=oro, y=1240, tam=74)


if PIEZA == "rentar":
    corte = [("k6564", 0.2), ("k6564", 9.0), ("k6564", 5.2), ("k6564", 6.6), ("k6564", 31.0),
             ("k6564", 47.0), ("k6564", 65.0), ("k6564", 24.5), ("k6564", 40.3)]
    tomas = [dict(src="w4", ini=0.0, dur=3.2, zoom=(1.0, 1.04))]
    tomas += [dict(src=s, ini=i, dur=round(B2, 3), zoom=(1.08, 1.0) if n % 2 else (1.0, 1.08)) for n, (s, i) in enumerate(corte)]
    t0 = 3.2
    tf = t0 + 9 * B2
    tomas += [dict(src="k6564", ini=1.0, dur=3.0, vel=0.6, zoom=(1.0, 1.08)), dict(img=cierre(W, H), dur=2.8)]
    capas = [
        (gancho(W, H, "POV", "Dejaste de rentar", "y estrenaste depa"), 0.0, 3.2),
        (grande("Sala y comedor"), t0, t0 + 2 * B2),
        (grande("Cocina incluida", ("cocina", "incluida")), t0 + 2 * B2, t0 + 4 * B2),
        (grande("3 recámaras", ("3",)), t0 + 4 * B2, t0 + 7 * B2),
        (grande("2 baños completos", ("2",)), t0 + 7 * B2, t0 + 8 * B2),
        (grande("Entrega inmediata", ("inmediata",)), t0 + 8 * B2, tf),
        (etiqueta(W, H, NOTA_MUESTRA, 312, tam=18), t0, tf),
        (firma(W, H), t0, tf),
        (precio(W, H), tf, tf + 3.0),
        (etiqueta(W, H, "TU DEPA CON INFONAVIT EN CANCÚN", 740, oro=True, tam=26), tf, tf + 3.0),
        (nota(W, H, NOTA_PRECIO, y=1420), tf, tf + 3.0),
    ]
    titulo = "POV: dejaste de rentar · ALTA VIDA Inmuebles"

elif PIEZA == "faq":
    tomas, capas, t = [], [], 0.0
    pares = [
        ("¿Me alcanza con mi Infonavit?", "k6564", 39.5, "Te precalificamos GRATIS por WhatsApp y te decimos hoy", ("gratis", "hoy")),
        ("¿Cuándo me lo entregan?", "k6564", 0.5, "Entrega inmediata: 30 días después de firmar escrituras", ("inmediata:", "30")),
        ("¿Aceptan Fovissste o crédito bancario?", "w4", 3.5, "Sí: Infonavit, Fovissste y bancario", ("infonavit,", "fovissste", "bancario")),
    ]
    for n, (q, src, ini, r, oro) in enumerate(pares, 1):
        tomas.append(dict(img=pregunta(W, H, q, n), dur=1.8, zoom=(1.0, 1.04)))
        tomas.append(dict(src=src, ini=ini, dur=2.8))
        capas.append((respuesta(W, H, r, oro), t + 1.8, t + 4.6))
        capas.append((firma(W, H), t + 1.8, t + 4.6))
        t += 4.6
    tomas.append(dict(img=pregunta(W, H, "¿Y cuánto cuesta?", 4), dur=1.6, zoom=(1.0, 1.04)))
    tomas.append(dict(src="k6564", ini=62.0, dur=3.2, vel=0.7))
    t += 1.6
    capas += [(precio(W, H), t, t + 3.2), (nota(W, H, NOTA_PRECIO, y=1420), t, t + 3.2)]
    tomas.append(dict(img=cierre(W, H), dur=3.2))
    titulo = "¿Me alcanza con mi Infonavit? · ALTA VIDA Inmuebles"

elif PIEZA == "amenidades":
    corte = [("k6623", 26.5, "Alberca"), ("k6623", 12.0, "Terraza junto a la alberca"), ("k6624a", 1.0, "Áreas verdes"),
             ("k6623", 18.0, "Áreas comunes"), ("k6623", 31.0, "Alberca"), ("k6564", 0.5, "Entrega inmediata")]
    tomas = [dict(src="k6623", ini=29.0, dur=round(2 * B2, 3), zoom=(1.0, 1.08))]
    capas = [(gancho(W, H, "Amenidades", "Así se vive", "en Huayacán"), 0.0, 2 * B2)]
    t = 2 * B2
    for n, (s, i, txt) in enumerate(corte):
        tomas.append(dict(src=s, ini=i, dur=round(B2, 3), zoom=(1.08, 1.0) if n % 2 else (1.0, 1.08)))
        capas.append((grande(txt), t, t + B2))
        t += B2
    capas.append((firma(W, H), 2 * B2, t))
    tomas.append(dict(src="k6623", ini=30.0, dur=4.2, vel=0.6, zoom=(1.0, 1.08)))
    capas.append((lista(W, H, "+10 amenidades", ["Alberca", "Multicancha", "Gimnasio al aire libre y calistenia",
                                                  "Pista de jogging", "Zona Relax y Zona Lotus", "Family Zone y juegos infantiles",
                                                  "Caseta de seguridad"], kicker="Para toda la familia", y=480), t, t + 4.2))
    tomas.append(dict(img=cierre(W, H), dur=3.0))
    titulo = "Amenidades · departamentos en Huayacán · ALTA VIDA Inmuebles"

print(PIEZA, render(OUT, W, H, tomas, capas, MUS, titulo=titulo))
