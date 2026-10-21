"""Motor de montaje: fotos reales con movimiento lento, títulos, subtítulos,
voz en off y música. Renderiza con ffmpeg (H.264).

Uso: python video.py reel|youtube|historias <carpeta_salida>
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageOps
sys.path.insert(0, os.path.dirname(__file__))
from marca import *

FPS = 30
MODO, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
AUD = os.path.join(S, "out", "audio")
VOZ = json.load(open(f"{AUD}/voz.json"))
JAIME = os.path.join(S, "jaime", "IMG_0386.jpg")
WA = "998 154 6066  ·  998 430 9472"


def foto(n):
    if n == "jaime":
        im = ImageOps.exif_transpose(Image.open(JAIME)).convert("RGB")
        # cuerpo superior, sin la mano ni el fondo
        w, h = im.size
        return gradar(im.crop((int(w * 0.45), int(h * 0.07), int(w * 0.98), int(h * 0.40))))
    return gradar(Image.open(f"{S}/photos/p{n:02d}.jpg"))


def base(seg, W, H, holgura=1.12):
    """Imagen base algo más grande que el cuadro para mover la cámara."""
    if isinstance(seg["img"], list):  # díptico editorial para 16:9
        a, b = seg["img"]
        bw, bh = int(W * holgura), int(H * holgura)
        g = int(18 * holgura)
        pw = (bw - g) // 2
        lienzo = Image.new("RGB", (bw, bh), ESPRESSO)
        lienzo.paste(cubrir(foto(a), pw, bh, *seg.get("f", (0.5, 0.5))), (0, 0))
        lienzo.paste(cubrir(foto(b), pw, bh, *seg.get("f2", (0.5, 0.5))), (pw + g, 0))
        return lienzo
    if seg["img"] == "cierre":
        return Image.new("RGB", (int(W * holgura), int(H * holgura)), MARFIL)
    return cubrir(foto(seg["img"]), int(W * holgura), int(H * holgura), *seg.get("f", (0.5, 0.5)))


def ease(t):
    return t * t * (3 - 2 * t)


def ventana(seg, bw, bh, W, H, t):
    """Rectángulo de recorte en el tiempo t (0..1) según el movimiento."""
    m = seg.get("mov", "in")
    e = ease(t)
    z0, z1 = {"in": (1.0, 1.10), "out": (1.10, 1.0)}.get(m, (1.06, 1.06))
    z = z0 + (z1 - z0) * e
    cw, ch = bw / z, bw / z * H / W
    if ch > bh:
        ch = bh / z
        cw = ch * W / H
    cx, cy = bw / 2, bh / 2
    dx, dy = bw - cw, bh - ch
    if m == "izq":
        cx = bw / 2 + dx * (0.45 - 0.9 * e) / 2
    elif m == "der":
        cx = bw / 2 - dx * (0.45 - 0.9 * e) / 2
    elif m == "sube":
        cy = bh / 2 + dy * (0.45 - 0.9 * e) / 2
    elif m == "baja":
        cy = bh / 2 - dy * (0.45 - 0.9 * e) / 2
    return (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)


# ---------------- capas de texto ----------------

def capa_titulo(seg, W, H, vertical):
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if not seg.get("titulo") and not seg.get("kicker"):
        return None
    d = ImageDraw.Draw(capa)
    if vertical:
        capa.alpha_composite(degradado(W, H, 0, 900, alfa_max=245, arriba=True))
        y = 380
        x = W / 2
        if seg.get("kicker"):
            texto_espaciado(d, (x, y - 95), seg["kicker"].upper(), fuente("montserrat", 26, "Medium"), ORO, 0.32, "mm")
        if seg.get("titulo"):
            d.text((x, y), seg["titulo"], font=fuente("cormorant", 86, "Light"), fill=MARFIL, anchor="ms")
        if seg.get("it"):
            fi = fuente("cormorant-it", 90, "Regular")
            d.text((x + 2, y + 97), seg["it"], font=fi, fill=(0, 0, 0, 150), anchor="ms")
            d.text((x, y + 95), seg["it"], font=fi, fill=ORO, anchor="ms")
    else:
        capa.alpha_composite(degradado(W, H, int(H * 0.55), H, alfa_max=190))
        x, y = 110, H - 210
        if seg.get("kicker"):
            texto_espaciado(d, (x, y - 70), seg["kicker"].upper(), fuente("montserrat", 22, "Medium"), ORO, 0.32)
        ft = fuente("cormorant", 74, "Light")
        d.text((x, y + 20), seg.get("titulo", ""), font=ft, fill=MARFIL, anchor="ls")
        if seg.get("it"):
            d.text((x + d.textlength(seg.get("titulo", "") + " ", font=ft), y + 20), seg["it"],
                   font=fuente("cormorant-it", 74, "Light"), fill=ORO, anchor="ls")
    return capa


def capa_jaime(W, H, vertical):
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    if vertical:
        capa.alpha_composite(degradado(W, H, int(H * 0.55), int(H * 0.8), alfa_max=220))
        y = 1300
        d.line([(W / 2 - 40, y - 70), (W / 2 + 40, y - 70)], fill=ORO, width=2)
        d.text((W / 2, y), "Jaime Marín", font=fuente("cormorant", 84, "Light"), fill=MARFIL, anchor="ms")
        texto_espaciado(d, (W / 2, y + 60), "DIRECTOR GENERAL, ALTA VIDA INMUEBLES",
                        fuente("montserrat", 24, "Medium"), ORO, 0.2, "mm")
    else:
        capa.alpha_composite(degradado(W, H, int(H * 0.5), H, alfa_max=200))
        d.line([(110, H - 250), (180, H - 250)], fill=ORO, width=2)
        d.text((108, H - 165), "Jaime Marín", font=fuente("cormorant", 80, "Light"), fill=MARFIL, anchor="ls")
        texto_espaciado(d, (110, H - 115), "DIRECTOR GENERAL, ALTA VIDA INMUEBLES",
                        fuente("montserrat", 22, "Medium"), ORO, 0.25)
    return capa


def capa_cierre(W, H, vertical):
    capa = Image.new("RGBA", (W, H), MARFIL + (255,))
    d = ImageDraw.Draw(capa)
    if vertical:
        lg = logo(300)
        capa.alpha_composite(lg, ((W - lg.width) // 2, 330))
        y0 = 830
    else:
        lg = logo(230)
        capa.alpha_composite(lg, ((W - lg.width) // 2, 90))
        y0 = 440
    d.text((W / 2, y0), "Agende su", font=fuente("cormorant", 88, "Light"), fill=ESPRESSO, anchor="ms")
    d.text((W / 2, y0 + 95), "visita privada", font=fuente("cormorant-it", 92, "Light"), fill=ORO, anchor="ms")
    texto_espaciado(d, (W / 2, y0 + 185), "$23,900,000 MXN", fuente("montserrat", 40, "Regular"), ESPRESSO, 0.1, "mm")
    bw = 860 if vertical else 900
    caja = Image.new("RGBA", (bw, 150), ESPRESSO + (255,))
    capa.alpha_composite(caja, ((W - bw) // 2, y0 + 250))
    texto_espaciado(d, (W / 2, y0 + 295), "WHATSAPP", fuente("montserrat", 20, "Medium"), ORO, 0.4, "mm")
    d.text((W / 2, y0 + 360), WA, font=fuente("montserrat", 36, "Regular"), fill=MARFIL, anchor="ms")
    texto_espaciado(d, (W / 2, y0 + 460), "@ALTAVIDAINMUEBLES", fuente("montserrat", 20, "Medium"), ESPRESSO, 0.3, "mm")
    return capa


def capa_sub(txt, W, H, vertical):
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    f = fuente("montserrat", 40 if vertical else 38, "Medium")
    maxw = W * (0.82 if vertical else 0.7)
    palabras, lineas, l = txt.split(), [], ""
    for p in palabras:
        if d.textlength((l + " " + p).strip(), font=f) > maxw:
            lineas.append(l); l = p
        else:
            l = (l + " " + p).strip()
    lineas.append(l)
    y = (1560 if vertical else H - 70) - (len(lineas) - 1) * 54
    anchos = [d.textlength(ln, font=f) for ln in lineas]
    pad = 26
    d.rounded_rectangle([W / 2 - max(anchos) / 2 - pad, y - 44, W / 2 + max(anchos) / 2 + pad,
                         y + (len(lineas) - 1) * 54 + 20], radius=10, fill=ESPRESSO + (165,))
    for ln in lineas:
        for dx, dy in ((2, 2), (0, 2), (2, 0)):
            d.text((W / 2 + dx, y + dy), ln, font=f, fill=(0, 0, 0, 170), anchor="ms")
        d.text((W / 2, y), ln, font=f, fill=MARFIL, anchor="ms")
        y += 54
    return capa


# ---------------- guiones de montaje ----------------
# vo: índices de líneas de voz; dur mínima en segundos

REEL = [
    dict(img=8, f=(0.5, 0.55), mov="in", vo=[0, 1], min=3.2, kicker="Lagos del Sol · Cancún", titulo="Vivir frente", it="al lago"),
    dict(img="jaime", f=(0.75, 0.15), mov="in", vo=[2], min=4.0, jaime=True),
    dict(img=1, f=(0.3, 0.5), mov="izq", vo=[3], min=3.5, kicker="Residencial", titulo="Lagos del Sol"),
    dict(img=4, mov="sube", vo=[4], min=3.5, kicker="Terraza", titulo="a doble altura"),
    dict(img=31, f=(0.5, 0.3), mov="in", vo=[5], min=3.5, kicker="Sala", titulo="a doble altura"),
    dict(img=5, mov="out", vo=[6], min=4.5, kicker="Alberca infinity", titulo="Acceso al lago"),
    dict(img=24, mov="der", vo=[7], min=4.0, kicker="4 recámaras · 4.5 baños", titulo="Vista al lago"),
    dict(img=26, mov="in", vo=[8], min=3.5),
    dict(img=20, mov="izq", vo=[9], min=4.5, kicker="570 m² construcción", titulo="550 m² terreno"),
    dict(img=6, mov="in", vo=[10], min=4.0),
    dict(img="cierre", mov="fijo", vo=[11], min=5.5, cierre=True),
]

YOUTUBE = [
    dict(img=8, mov="in", vo=[0, 1], min=9, kicker="Lagos del Sol · Cancún", titulo="Vivir frente", it="al lago"),
    dict(img="jaime_h", mov="fijo", vo=[2, 3], min=6, jaime=True),
    dict(img=46, mov="in", vo=[4], min=5, kicker="La llegada", titulo="Acceso", it="cubierto"),
    dict(img=1, mov="izq", vo=[5], min=6),
    dict(img=[45, 17], mov="in", vo=[6], min=8, kicker="550 m² · 570 m² · 4 estacionamientos", titulo="Residencia", it="frente al lago"),
    dict(img=[31, 9], f=(0.5, 0.4), mov="in", vo=[7], min=5, kicker="Planta baja", titulo="Sala a", it="doble altura"),
    dict(img=[32, 35], mov="out", vo=[8], min=8),
    dict(img=[9, 10], mov="in", vo=[9], min=5, kicker="Planta baja", titulo="Comedor"),
    dict(img=[2, 10], mov="izq", vo=[10], min=7, kicker="Cocina", titulo="y alacena"),
    dict(img=[4, 13], mov="in", vo=[11], min=7, kicker="Terraza techada", titulo="a doble", it="altura"),
    dict(img=[5, 6], mov="out", vo=[12], min=7, kicker="Jardín", titulo="Alberca", it="infinity"),
    dict(img=[8, 7], mov="in", vo=[13], min=6),
    dict(img=[44, 18], mov="der", vo=[14], min=6, kicker="Exterior", titulo="Acceso", it="al lago"),
    dict(img=19, mov="in", vo=[15], min=6, kicker="Planta alta", titulo="Family room"),
    dict(img=24, mov="izq", vo=[16], min=9, kicker="Planta alta", titulo="Recámara", it="principal"),
    dict(img=[26, 29], mov="in", vo=[], min=5, kicker="Recámara principal", titulo="Vestidor", it="y baño"),
    dict(img=[22, 33], mov="der", vo=[17], min=8, kicker="Recámaras 2 y 3", titulo="Vestidor y", it="baño completo"),
    dict(img=[38, 34], mov="in", vo=[18], min=6),
    dict(img=[27, 39], mov="out", vo=[19], min=5, kicker="4 recámaras", titulo="4.5", it="baños"),
    dict(img=21, mov="izq", vo=[20], min=5, kicker="Ubicación", titulo="Residencial", it="Lagos del Sol"),
    dict(img=20, mov="der", vo=[21], min=6, kicker="40 hectáreas de lagos", titulo="+30", it="amenidades"),
    dict(img=25, mov="in", vo=[22], min=6, kicker="Casa club · Parque del Lago", titulo="Gimnasio · SPA", it="· Ciclovía"),
    dict(img=[18, 25], mov="izq", vo=[23], min=5),
    dict(img=[5, 44], mov="in", vo=[24], min=7),
    dict(img="cierre", mov="fijo", vo=[25, 26], min=10, cierre=True),
]


def montar(guion, voz, W, H, vertical, musica, nombre, gap=0.55, pre=0.4, xf=0.6, cola=0.8):
    # 1) tiempos
    t = 0.0
    lineas_t = []  # (inicio, fin, texto, archivo)
    for s in guion:
        s["t0"] = t
        tt = t + pre
        for i in s["vo"]:
            v = voz[i]
            lineas_t.append((tt, tt + v["dur"], v["texto"], v["archivo"]))
            tt += v["dur"] + gap
        s["dur"] = max(s["min"], tt - t + 0.3)
        t += s["dur"]
    total = t + cola
    print(nombre, "duración", round(total, 1), "s")
    capitulos = [(round(s["t0"]), s.get("kicker", ""), s.get("titulo", "")) for s in guion]

    # 2) audio: voz + música con ducking
    sr = 24000
    vozpista = np.zeros(int(total * sr) + sr, np.float32)
    import soundfile as sf
    for a, b, txt, arch in lineas_t:
        x, _ = sf.read(arch, dtype="float32")
        i0 = int(a * sr)
        vozpista[i0:i0 + len(x)] += x
    sf.write(f"{OUT}/{nombre}_voz.wav", vozpista, sr)
    wav = f"{OUT}/{nombre}_mix.wav"
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/{nombre}_voz.wav", "-i", musica,
        "-filter_complex",
        "[0:a]aresample=48000,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=10:release=200,"
        "volume=1.6,asplit=2[v][sc];"
        f"[1:a]aresample=48000,atrim=0:{total},volume=0.32[m];"
        "[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=80:release=600[md];"
        f"[v][md]amix=inputs=2:normalize=0,afade=t=out:st={total - 1.5}:d=1.5,loudnorm=I=-14:TP=-1.5:LRA=9",
        "-ac", "2", wav], check=True)

    # 3) video
    for s in guion:
        img = s["img"]
        if img == "jaime_h":
            s["img"] = "jaime"
            s["_base"] = base_jaime_h(W, H)
        else:
            s["_base"] = base(s, W, H)
        s["_titulo"] = capa_jaime(W, H, vertical) if s.get("jaime") else capa_titulo(s, W, H, vertical)
        s["_cierre"] = capa_cierre(W, H, vertical) if s.get("cierre") else None
    subs = [(a, b, capa_sub(txt, W, H, vertical)) for a, b, txt, _ in lineas_t]

    mp4 = f"{OUT}/{nombre}.mp4"
    ff = subprocess.Popen([
        "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
        "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", "-shortest", mp4], stdin=subprocess.PIPE)
    vin = Image.new("RGBA", (W, H))
    vin = viñeta(W, H)
    nfr = int(total * FPS)
    for k in range(nfr):
        tk = k / FPS
        # segmento actual y siguiente (para disolvencia)
        idx = max(i for i, s in enumerate(guion) if s["t0"] <= tk) if tk < guion[-1]["t0"] + guion[-1]["dur"] else len(guion) - 1
        fr = cuadro(guion[idx], tk, W, H)
        nxt = guion[idx + 1] if idx + 1 < len(guion) else None
        if nxt and tk > nxt["t0"] - xf:
            a = (tk - (nxt["t0"] - xf)) / xf
            fr = Image.blend(fr, cuadro(nxt, tk, W, H), ease(a))
        fr = fr.convert("RGBA")
        if not guion[idx].get("cierre"):
            fr.alpha_composite(vin)
        for a, b, c in subs:
            if a - 0.15 <= tk <= b + 0.25:
                al = min(1, (tk - a + 0.15) / 0.2, (b + 0.25 - tk) / 0.2)
                fr.alpha_composite(alfa(c, al))
        if tk < 0.35:
            fr = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), fr, tk / 0.35)
        ff.stdin.write(fr.convert("RGB").tobytes())
    ff.stdin.close()
    ff.wait()
    return mp4, capitulos, lineas_t, total


def base_jaime_h(W, H):
    """16:9: retrato de Jaime a la izquierda sobre espresso."""
    lienzo = Image.new("RGB", (int(W * 1.04), int(H * 1.04)), ESPRESSO)
    retrato = cubrir(foto("jaime"), int(H * 1.04 * 0.75), int(H * 1.04), 0.5, 0.3)
    lienzo.paste(retrato, (int(W * 0.52), 0))
    return lienzo


_cache = {}


def cuadro(s, tk, W, H):
    b = s["_base"]
    u = min(1, max(0, (tk - s["t0"]) / (s["dur"] + 0.6)))
    if s.get("mov") == "fijo":
        caja = ventana(dict(mov="in"), b.width, b.height, W, H, u * 0.25)
    else:
        caja = ventana(s, b.width, b.height, W, H, u)
    fr = b.resize((W, H), Image.BICUBIC, box=caja).convert("RGBA")
    if s["_titulo"] is not None:
        a = min(1, max(0, (tk - s["t0"] - 0.5) / 0.6), max(0, (s["t0"] + s["dur"] - 0.2 - tk) / 0.5))
        if a > 0:
            fr.alpha_composite(alfa(s["_titulo"], a))
    if s["_cierre"] is not None:
        a = min(1, max(0, (tk - s["t0"]) / 0.8))
        fr = Image.blend(fr, s["_cierre"], a)
    return fr


def alfa(capa, a):
    if a >= 0.999:
        return capa
    key = (id(capa), round(a, 2))
    if key not in _cache:
        if len(_cache) > 400:
            _cache.clear()
        r, g, b_, al = capa.split()
        _cache[key] = Image.merge("RGBA", (r, g, b_, al.point(lambda v: int(v * a))))
    return _cache[key]


def viñeta(W, H):
    y, x = np.ogrid[:H, :W]
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    a = np.clip((r - 0.75) / 0.6, 0, 1) ** 2 * 110
    v = np.zeros((H, W, 4), np.uint8)
    v[..., :3] = ESPRESSO
    v[..., 3] = a.astype(np.uint8)
    return Image.fromarray(v, "RGBA")


def srt(lineas, ruta):
    def ts(x):
        h, r = divmod(x, 3600); m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"
    with open(ruta, "w") as f:
        for i, (a, b, t, _) in enumerate(lineas, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n")


if MODO == "reel":
    mp4, cap, lin, tot = montar(REEL, VOZ["reel"], 1080, 1920, True, f"{AUD}/musica_reel.wav", "reel_lagos_del_sol")
    srt(lin, f"{OUT}/reel_lagos_del_sol.srt")
elif MODO == "youtube":
    mp4, cap, lin, tot = montar(YOUTUBE, VOZ["youtube"], 1920, 1080, False, f"{AUD}/musica_youtube.wav",
                                "youtube_lagos_del_sol", gap=1.6, pre=1.2, xf=0.9, cola=1.5)
    srt(lin, f"{OUT}/youtube_lagos_del_sol.srt")
    json.dump(cap, open(f"{OUT}/youtube_capitulos.json", "w"), ensure_ascii=False)
