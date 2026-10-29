"""Reel principal 9:16 (36 s): recorrido real con Kenia, voz en off, subtítulos y CTA."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from capas import *
from montaje import render

W, H = 1080, 1920
V = os.path.join(S, "voz")
OUT = sys.argv[1]

tomas = [
    dict(src="w4", ini=0.2, dur=3.2, zoom=(1.0, 1.05)),          # Kenia abre la puerta
    dict(src="k6564", ini=0.0, dur=2.0),                          # sala
    dict(src="k6564", ini=8.6, dur=1.6),                          # comedor
    dict(src="k6564", ini=5.6, dur=1.6, zoom=(1.06, 1.0)),        # cocina
    dict(src="k6564", ini=13.0, dur=1.8),                         # sala con ventana
    dict(src="k6564", ini=40.0, dur=1.6, zoom=(1.0, 1.0)),        # Kenia en el pasillo
    dict(src="k6564", ini=30.0, dur=1.4),                         # recámara 2
    dict(src="k6564", ini=46.0, dur=1.2),                         # recámara 3
    dict(src="k6564", ini=24.2, dur=1.2, zoom=(1.06, 1.0)),       # baño
    dict(src="k6564", ini=65.0, dur=1.4),                         # recámara principal
    dict(src="k6623", ini=28.0, dur=1.6),                         # alberca desde terraza
    dict(src="k6623", ini=24.5, dur=1.4),                         # terraza hacia la alberca
    dict(src="k6623", ini=11.0, dur=1.2),                         # área de convivencia
    dict(src="k6624a", ini=0.5, dur=1.2, f=(0.5, 0.5)),           # jardín
    dict(src="k6623", ini=30.5, dur=2.0),                         # alberca
    dict(src="k6623", ini=32.0, dur=2.6, zoom=(1.08, 1.0)),       # alberca, toma abierta
    dict(src="k6564", ini=15.5, dur=4.5, vel=0.6, zoom=(1.0, 1.1)),  # fondo del precio
    dict(img=cierre(W, H), dur=4.5, zoom=(1.0, 1.03)),
]

voces = [(f"{V}/T0.wav", 0.3), (f"{V}/T1.wav", 5.2), (f"{V}/T2.wav", 10.3), (f"{V}/T3.wav", 15.7), (f"{V}/T4.wav", 22.2)]

capas = [
    (gancho(W, H, "Entrega inmediata · Cancún", "3 recámaras", "con tu Infonavit"), 0.0, 3.2),
    (subtitulo(W, H, "Así es un depa de 3 recámaras con tu Infonavit en Cancún", oro=("3", "infonavit")), 0.3, 5.0),
    (firma(W, H), 3.2, 27.0),
    (etiqueta(W, H, NOTA_MUESTRA, 312, tam=18), 3.2, 15.6),
    (subtitulo(W, H, "Sala y comedor con luz natural, y cocina incluida", oro=("cocina", "incluida")), 5.2, 10.1),
    (subtitulo(W, H, "3 recámaras, 2 baños completos y 80 m² de construcción", oro=("3", "2", "80", "m²")), 10.3, 15.5),
    (subtitulo(W, H, "Afuera: alberca, multicancha y gimnasio al aire libre", oro=("alberca,", "alberca")), 15.7, 18.8),
    (subtitulo(W, H, "pista para correr y juegos para los niños", oro=("niños",)), 18.8, 22.0),
    (subtitulo(W, H, "Sobre Av. Huayacán, a 10 km del aeropuerto", oro=("huayacán,", "10", "km")), 22.2, 27.0),
    (etiqueta(W, H, "ZONA HOTELERA 12.5 KM · TREN MAYA 9.7 KM", 1200, tam=22), 23.0, 27.0),
    (precio(W, H), 27.0, 31.5),
    (etiqueta(W, H, "DEPARTAMENTO NUEVO · 3 REC · 2 BAÑOS", 740, oro=True, tam=26), 27.0, 31.5),
    (nota(W, H, NOTA_PRECIO, y=1420), 27.0, 31.5),
]

t = render(OUT, W, H, tomas, capas, os.path.join(S, "audio", "musica_reel.wav"), voces, vol_musica=0.5,
           titulo="Departamento 3 recámaras con Infonavit · Cancún · ALTA VIDA Inmuebles")
print("reel", t)
