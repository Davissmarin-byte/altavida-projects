"""Motor de montaje con tomas reales (ffmpeg + PIL).

Cada pieza es una lista de tomas (video real o tarjeta PIL), capas de texto con
tiempos y una mezcla de audio (música original + voz opcional con ducking).
Los videos fuente son proxys 1080×1920 / 1920×1080 a 30 fps en $CAMP_SRC/px.
"""
import json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from marca import S

FPS = 30
PX = os.path.join(S, "px")
GRADO = "eq=contrast=1.05:saturation=1.08:brightness=0.01,colorbalance=rm=0.02:bm=-0.02"


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(" ".join(cmd[:6]) + "\n" + r.stderr[-1500:])
    return r.stdout


def duracion(p):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).strip())


def toma(t, W, H, out):
    """Renderiza una toma a W×H (sin audio)."""
    dur = t["dur"]
    if "img" in t:  # tarjeta o foto fija
        p = out + ".png"
        im = t["img"]
        if isinstance(im, str):
            im = Image.open(im)
        im.convert("RGB").save(p)
        z0, z1 = t.get("zoom", (1.0, 1.0))
        vf = (f"scale={W}:{H},scale=w='trunc({W}*({z0}+({z1}-{z0})*t/{dur})/2)*2':h=-2:eval=frame,"
              f"crop={W}:{H},fps={FPS},format=yuv420p")
        sh(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", p,
            "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-r", str(FPS), out])
        return
    src = os.path.join(PX, t["src"] + ".mp4")
    vel = t.get("vel", 1.0)
    fx, fy = t.get("f", (0.5, 0.5))
    z0, z1 = t.get("zoom", (1.0, 1.06))
    cubrir = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}:(iw-ow)*{fx}:(ih-oh)*{fy},"
              f"scale=w='trunc({W}*({z0}+({z1}-{z0})*t/{dur})/2)*2':h=-2:eval=frame,crop={W}:{H}")
    base = f"setpts=(PTS-STARTPTS)/{vel},fps={FPS}"
    entra = ["-ss", str(t["ini"]), "-t", str(dur * vel + 0.1), "-i", src]
    vertical_en_horizontal = W > H and t.get("modo", "panel") == "panel"
    if vertical_en_horizontal:
        # video vertical dentro de 16:9: fondo desenfocado + video a la izquierda del panel de texto
        fw = int(H * 9 / 16) // 2 * 2
        x = t.get("x", 230)
        fc = (f"[0:v]{base},split[a][b];"
              f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=40,eq=brightness=-0.16:saturation=0.8[bg];"
              f"[b]scale={fw}:{H}:force_original_aspect_ratio=increase,crop={fw}:{H},"
              f"scale=w='trunc({fw}*({z0}+({z1}-{z0})*t/{dur})/2)*2':h=-2:eval=frame,crop={fw}:{H},{GRADO}[fg];"
              f"[bg][fg]overlay={x}:0,format=yuv420p[v]")
        sh(["ffmpeg", "-v", "error", "-y", *entra, "-filter_complex", fc, "-map", "[v]", "-t", str(dur),
            "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-r", str(FPS), out])
        return
    vf = f"{base},{cubrir},{GRADO},format=yuv420p"
    sh(["ffmpeg", "-v", "error", "-y", *entra, "-vf", vf, "-t", str(dur), "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-r", str(FPS), out])


def pista_voz(voces, total, sr=48000):
    """Coloca las líneas de voz [(wav, t)] en una pista mono."""
    pista = np.zeros(int((total + 1) * sr), np.float32)
    for wav, t in voces:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                             capture_output=True).stdout
        x = np.frombuffer(raw, np.float32)
        i0 = int(t * sr)
        n = min(len(x), len(pista) - i0)
        pista[i0:i0 + n] += x[:n]
    return pista


def render(salida, W, H, tomas, capas, musica, voces=(), vol_musica=0.55, titulo=None, mus_ini=0.0):
    """tomas: lista de dicts; capas: lista de (Image, t0, t1); voces: [(wav, t)]."""
    tmp = tempfile.mkdtemp(prefix="mont_")
    segs = []
    for i, t in enumerate(tomas):
        p = os.path.join(tmp, f"s{i:03d}.mp4")
        toma(t, W, H, p)
        segs.append(p)
    with open(os.path.join(tmp, "lista.txt"), "w") as f:
        f.writelines(f"file '{p}'\n" for p in segs)
    base = os.path.join(tmp, "base.mp4")
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "lista.txt"), "-c", "copy", base])
    total = round(sum(t["dur"] for t in tomas), 3)

    # capas de texto con fundidos
    entradas, fc, prev = ["-i", base], [], "0:v"
    for k, (im, t0, t1) in enumerate(capas, 1):
        p = os.path.join(tmp, f"c{k:03d}.png")
        im.save(p)
        # la capa solo existe en su ventana (itsoffset): mucho más rápido en videos largos
        entradas += ["-itsoffset", str(t0), "-loop", "1", "-framerate", str(FPS), "-t", str(round(t1 - t0, 3)), "-i", p]
        fi = min(0.18, (t1 - t0) / 4)
        fc.append(f"[{k}:v]format=rgba,fade=t=in:st={t0}:d={fi}:alpha=1,fade=t=out:st={t1 - fi}:d={fi}:alpha=1[o{k}]")
        fc.append(f"[{prev}][o{k}]overlay=0:0:eof_action=pass:enable='between(t,{t0},{t1})'[v{k}]")
        prev = f"v{k}"

    # audio: música + voz con ducking + normalización
    a_idx = len(capas) + 1
    entradas += ["-i", musica]
    if voces:
        vp = os.path.join(tmp, "voz.wav")
        x = pista_voz(voces, total)
        sh_in = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", "48000", "-ac", "1", "-i", "-", vp],
                               input=x.tobytes(), capture_output=True)
        entradas += ["-i", vp]
        fc.append(f"[{a_idx}:a]atrim={mus_ini}:{mus_ini + total},asetpts=PTS-STARTPTS,volume={vol_musica}[m]")
        fc.append(f"[{a_idx + 1}:a]atrim=0:{total},highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=10:release=200,"
                  f"volume=1.6,aformat=channel_layouts=stereo,asplit=2[vz][sc]")
        fc.append("[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=60:release=500[md]")
        fc.append(f"[vz][md]amix=inputs=2:normalize=0,afade=t=out:st={total - 1.2}:d=1.2,loudnorm=I=-14:TP=-1.5:LRA=9[a]")
    else:
        fc.append(f"[{a_idx}:a]atrim={mus_ini}:{mus_ini + total},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={total - 1.2}:d=1.2,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    vmap = f"[{prev}]" if capas else "0:v"
    meta = ["-metadata", f"title={titulo}"] if titulo else []
    sh(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", ";".join(fc), "-map", vmap, "-map", "[a]",
        "-t", str(total), "-c:v", "libx264", "-preset", os.environ.get("PRESET", "medium"), "-crf", "19", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", *meta, salida])
    return total


def nitidez(p):
    """Varianza de bordes: más alto = cuadro más nítido."""
    from PIL import ImageFilter
    g = np.asarray(Image.open(p).convert("L").resize((270, 480)).filter(ImageFilter.FIND_EDGES), np.float32)
    return float(g.var())


def cuadro(src, t, out, ventana=0.6):
    """Extrae el cuadro más nítido en t±ventana, del original 4K si existe (para carrusel y fotos)."""
    cand = [round(max(0, t + d / 10), 2) for d in range(int(-ventana * 10), int(ventana * 10) + 1, 2)]
    prueba = []
    for c in cand:
        q = f"{out}.{c}.jpg"
        sh(["ffmpeg", "-v", "error", "-y", "-ss", str(c), "-i", os.path.join(PX, src + ".mp4"), "-frames:v", "1", q])
        prueba.append((nitidez(q), c))
        os.remove(q)
    mejor = max(prueba)[1]
    raw = os.path.join(S, "raw4k", src + ".MOV")
    p = raw if os.path.exists(raw) else os.path.join(PX, src + ".mp4")
    sh(["ffmpeg", "-v", "error", "-y", "-ss", str(mejor), "-i", p, "-frames:v", "1", "-q:v", "2", out])
    return out
