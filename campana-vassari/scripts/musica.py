"""Música original con ritmo (síntesis propia, sin derechos de terceros).

Estilo tropical-house suave: bombo a negras, palmas en 2 y 4, hi-hat,
bajo y acordes tipo marimba. Pensada para Reels de vivienda familiar.

Uso: python musica.py <salida_dir>
Genera musica_reel.wav (75 s, 104 bpm), musica_corto.wav (30 s, 112 bpm),
musica_youtube.wav (200 s, 96 bpm, sin bombo en la intro) y musica_historia.wav (45 s).
"""
import os, sys, wave
import numpy as np

SR = 44100
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env_ad(n, a, d):
    t = np.arange(n) / SR
    return np.clip(t / a, 0, 1) * np.exp(-t / d)


def bombo():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 50 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def palma():
    n = int(0.22 * SR)
    r = rng.standard_normal(n)
    r = np.convolve(r, [1, -0.9], "same")
    e = np.zeros(n)
    for k in (0, 0.012, 0.024):
        i = int(k * SR)
        e[i:] += np.exp(-np.arange(n - i) / SR * 28)
    return r * e * 0.5


def hat(abierto=False):
    n = int((0.18 if abierto else 0.05) * SR)
    r = rng.standard_normal(n)
    r = r - np.convolve(r, np.ones(6) / 6, "same")
    return r * np.exp(-np.arange(n) / SR * (14 if abierto else 70)) * 0.35


def marimba(f, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 18)
    return s * env_ad(n, 0.004, 0.32)


def bajo(f, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return s * env_ad(n, 0.01, 0.5) * np.clip((dur - t) / 0.05, 0, 1)


def pad(fs, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.004 * t) for f in fs) / len(fs)
    return s * np.clip(t / 0.4, 0, 1) * np.clip((dur - t) / 0.4, 0, 1)


def poner(pista, x, t0, g=1.0):
    i = int(t0 * SR)
    if i >= len(pista):
        return
    x = x[: len(pista) - i]
    pista[i:i + len(x)] += g * x


def tema(seg, bpm, intro_sin_bombo=0):
    """Progresión I–V–vi–IV en La mayor (A–E–F#m–D), un acorde por compás."""
    beat = 60 / bpm
    comp = 4 * beat
    acordes = [(57, [57, 61, 64, 69]), (52, [56, 59, 64, 68]), (54, [57, 61, 66, 69]), (50, [57, 62, 66, 69])]
    L = np.zeros(int(seg * SR) + SR)
    D, P, B, H, M = (np.zeros_like(L) for _ in range(5))
    k_b, k_p = bombo(), palma()
    patron = [0, 2, 3, 5, 7, 8, 10, 13]  # semicorcheas del arpegio, sincopado
    c = 0
    while c * comp < seg:
        t0 = c * comp
        raiz, notas = acordes[c % 4]
        poner(P, pad([hz(m) for m in notas], comp + 0.3), t0, 0.22)
        for b in range(4):
            tb = t0 + b * beat
            if tb >= intro_sin_bombo:
                poner(D, k_b, tb, 0.9)
                if b in (1, 3):
                    poner(D, k_p, tb, 0.55)
            poner(H, hat(), tb + beat / 2, 0.8 if tb >= intro_sin_bombo else 0.4)
            poner(H, hat(), tb + beat / 4 * 3, 0.35)
        for q in (0, 1.5, 2.5, 3):  # bajo sincopado
            poner(B, bajo(hz(raiz - 12), beat * 0.9), t0 + q * beat, 0.55)
        for j, s16 in enumerate(patron):
            nota = notas[(j * 3) % len(notas)] + (12 if j % 4 == 3 else 0)
            poner(M, marimba(hz(nota), 0.6), t0 + s16 * beat / 4, 0.28)
        c += 1
    mezcla = D * 0.9 + P + B + H * 0.6 + M
    mezcla = mezcla[: int(seg * SR)]
    t = np.arange(len(mezcla)) / SR
    mezcla *= np.clip(t / 0.3, 0, 1) * np.clip((seg - t) / 2.0, 0, 1)
    mezcla /= np.abs(mezcla).max() + 1e-9
    izq = mezcla * 0.85 + 0.15 * np.roll(M[: len(mezcla)], 220) / (np.abs(M).max() + 1e-9)
    der = mezcla * 0.85 + 0.15 * np.roll(H[: len(mezcla)], 330) / (np.abs(H).max() + 1e-9)
    st = np.stack([izq, der], 1)
    return (st / (np.abs(st).max() + 1e-9) * 0.8).astype(np.float32)


def guardar(nombre, a):
    with wave.open(os.path.join(OUT, nombre), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((a * 32767).astype("<i2").tobytes())


guardar("musica_reel.wav", tema(75, 104))
guardar("musica_corto.wav", tema(30, 112))
guardar("musica_youtube.wav", tema(200, 96, intro_sin_bombo=8))
guardar("musica_historia.wav", tema(45, 104))
print("ok")
