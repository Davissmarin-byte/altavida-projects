"""Genera las líneas de voz en off (Kokoro, español) y la música ambiental original.

Uso: python voz.py <salida> <voz>   (voz: em_alex | em_santa | ef_dora)
"""
import json, os, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

S = os.environ["CAMP_SRC"]
OUT, VOZ = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
SR = 24000

REEL = [
    "Hay casas que se recorren.", "Y hay casas que se sienten.",
    "ALTA VIDA Inmuebles le presenta una residencia frente al lago.",
    "Residencial Lagos del Sol. Cancún.",
    "Una terraza a doble altura, abierta al jardín.",
    "Interiores que dejan entrar la luz... y el agua.",
    "Una alberca infinity que se funde con el lago, y un acceso propio, directo al agua.",
    "Cuatro recámaras, cada una con su vestidor y su baño completo.",
    "Materiales nobles. Madera, piedra y cristal.",
    "Quinientos setenta metros de construcción, sobre un terreno de quinientos cincuenta.",
    "Un patrimonio para vivirse hoy... y heredarse mañana.",
    "Veintitrés millones novecientos mil pesos. Agende su visita privada.",
]

YOUTUBE = [
    "Hay casas que se recorren. Y hay casas que se sienten desde el primer paso.",
    "Esta es una de ellas.",
    "ALTA VIDA Inmuebles le presenta una residencia frente al lago, en Lagos del Sol, Cancún.",
    "Acompáñenos hasta el final.",
    "La llegada es serena.",
    "Un acceso cubierto, líneas limpias, madera cálida sobre piedra.",
    "Quinientos cincuenta metros de terreno, quinientos setenta de construcción, y cuatro estacionamientos.",
    "Al entrar, el espacio se abre hacia arriba.",
    "La sala a doble altura recibe la luz desde el lago, y la escalera flota sobre cristal.",
    "El comedor mira al agua.",
    "A un lado, la cocina con alacena, pensada para recibir sin prisa.",
    "Afuera, la terraza techada a doble altura da paso al jardín.",
    "Y a una alberca infinity que se funde con el lago.",
    "Aquí, el horizonte es parte de la casa.",
    "Y un acceso propio lo lleva directo al agua.",
    "Arriba, una sala de televisión para la familia.",
    "La recámara principal amanece frente al lago, con su vestidor y su baño completo.",
    "Las recámaras dos y tres tienen, cada una, su vestidor y su baño completo.",
    "En planta baja, una recámara de visitas con el mismo cuidado.",
    "Cuatro recámaras. Cuatro baños y medio.",
    "Alrededor, Residencial Lagos del Sol.",
    "Cuarenta hectáreas de lagos, y más de treinta amenidades.",
    "Casa club, Parque del Lago, gimnasio, spa y ciclovía.",
    "Un entorno privado, seguro y tranquilo.",
    "Un patrimonio para vivirse hoy... y heredarse mañana.",
    "Veintitrés millones novecientos mil pesos.",
    "Agende su visita privada con ALTA VIDA Inmuebles.",
]

MUESTRA = ("Hay casas que se recorren. Y hay casas que se sienten desde el primer paso. "
           "Frente al lago, en Residencial Lagos del Sol, Cancún. "
           "Agende su visita privada con ALTA VIDA Inmuebles.")

k = Kokoro(f"{S}/tts/kokoro-v1.0.onnx", f"{S}/tts/voices.npz")


def decir(txt, voz=VOZ):
    a, sr = k.create(txt.replace("ALTA VIDA", "Alta Vida"), voice=voz, speed=0.86, lang="es")
    assert sr == SR
    # recorta silencios de los bordes
    idx = np.where(np.abs(a) > 0.01)[0]
    return a[max(0, idx[0] - 600): idx[-1] + 2400].astype(np.float32)


meta = {}
for nombre, lineas in (("reel", REEL), ("youtube", YOUTUBE)):
    meta[nombre] = []
    for i, t in enumerate(lineas):
        a = decir(t)
        p = f"{OUT}/{nombre}_{i:02d}.wav"
        sf.write(p, a, SR)
        meta[nombre].append({"texto": t, "archivo": p, "dur": len(a) / SR})
json.dump(meta, open(f"{OUT}/voz.json", "w"), ensure_ascii=False, indent=1)

# muestras de 15 s para elegir voz
os.makedirs(f"{OUT}/muestras", exist_ok=True)
for v in ("em_alex", "em_santa", "ef_dora"):
    sf.write(f"{OUT}/muestras/muestra_{v}.wav", decir(MUESTRA, v), SR)


# música ambiental original (síntesis propia, sin derechos de terceros)
def musica(seg, sr=44100):
    t = np.arange(int(seg * sr)) / sr
    acordes = [[48, 55, 59, 64, 67], [45, 52, 57, 60, 64], [41, 48, 53, 57, 64], [43, 50, 55, 59, 62]]
    dur_ac = 8.0
    out = np.zeros_like(t)
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    for j in range(int(seg // dur_ac) + 1):
        ac = acordes[j % 4]
        t0 = j * dur_ac
        m = (t >= t0 - 2) & (t < t0 + dur_ac + 2)
        tt = t[m] - t0
        env = np.clip((tt + 2) / 3, 0, 1) * np.clip((dur_ac + 2 - tt) / 3, 0, 1)
        for n in ac:
            f = hz(n)
            out[m] += env * (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.003 * tt)
                             + 0.18 * np.sin(2 * np.pi * 2 * f * tt)) / len(ac)
        # campana suave: arpegio lento
        for q, n in enumerate(ac[1:] + [ac[2] + 12]):
            tn = tt - q * 1.6 - 0.4
            mm = tn >= 0
            out[m] += mm * 0.22 * np.exp(-np.clip(tn, 0, None) * 1.1) * np.sin(2 * np.pi * hz(n + 12) * tn) * (tn < 6)
    out = np.convolve(out, np.ones(8) / 8, mode="same")
    out *= np.clip(t / 3, 0, 1) * np.clip((seg - t) / 4, 0, 1)
    out /= np.abs(out).max() + 1e-9
    return (out * 0.6).astype(np.float32), sr


for nombre, seg in (("reel", 70), ("youtube", 260), ("historia", 40)):
    a, sr = musica(seg)
    sf.write(f"{OUT}/musica_{nombre}.wav", np.stack([a, np.roll(a, 300)], 1), sr)
print(json.dumps({k2: round(sum(x["dur"] for x in v), 1) for k2, v in meta.items()}))
