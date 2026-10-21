#!/usr/bin/env bash
# Mezcla final v3 (en el sandbox de Higgsfield):
#  - Reel: coloca las líneas de voz de Marisol (f_L*.wav) en sus tiempos (reel_v3_lineas.json),
#    baja la música bajo la voz y antepone el vuelo aéreo.
#  - YouTube: película sin narración; inserta el vuelo aéreo después del primer plano.
# Entradas: reel_v3.mp4, yt_v3.mp4, reel_v3_lineas.json, f_L*.wav, aereo.mp4, Montserrat-Medium.ttf
set -e
F=$PWD/Montserrat-Medium.ttf
LBL="Recreación ilustrativa generada con IA"
BOX="shadowcolor=black@0.6:shadowx=2:shadowy=2:box=1:boxcolor=0x1C1510@0.55"
GRADO="eq=saturation=0.92:contrast=1.04,colorbalance=rh=0.03:bh=-0.03"
YT_CORTE=${YT_CORTE:-6.6}

# 1) pista de voz del Reel
python3 - <<'EOF'
import json, subprocess, numpy as np
R = 48000
lin = json.load(open("reel_v3_lineas.json"))
claves = ["L00", "L01", "L02", "L03", "L04", "L05", "L07", "L08", "L09", "L11"]
fin = lin[-1][1] + 3
pista = np.zeros(int(fin * R) + R, np.float32)
for (a, b, t), k in zip(lin, claves):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"f_{k}.wav", "-ac", "1", "-ar", str(R), "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)
    i0 = int(a * R)
    pista[i0:i0 + len(x)] += x
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(R), "-ac", "1", "-i", "-", "voz_reel.wav"], input=pista.tobytes(), check=True)
EOF

# 2) Reel con voz: música del video bajo la voz (ducking) + normalización
ffmpeg -v error -y -i reel_v3.mp4 -i voz_reel.wav -filter_complex \
 "[1:a]highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=10:release=200,volume=1.5,asplit=2[v][sc];[0:a]volume=0.35[m];[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=80:release=600[md];[v][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest reel_v3_voz.mp4

sox -n -r 48000 -c 2 pad.wav synth 5 sine 130.81 sine 196.0 sine 246.94 sine 329.63 remix 1-4 1-4 gain -14 fade q 1.2 5 1.5

# 3) Reel: vuelo aéreo de 3.5 s al inicio
ffmpeg -v error -y -ss 1.0 -t 4.0 -i aereo.mp4 -vf "fps=30,scale=-2:1920:flags=lanczos,crop=1080:1920:x='(iw-1080)*(0.15+0.5*t/4)':y=0,$GRADO,drawtext=fontfile=$F:text='$LBL':fontsize=26:fontcolor=0xFDFCF8@0.9:$BOX:boxborderw=14:x=(w-tw)/2:y=250,drawtext=fontfile=$F:text='LAGOS DEL SOL · CANCÚN':fontsize=30:fontcolor=0xC9A96E:$BOX:boxborderw=14:x=(w-tw)/2:y=330,format=yuv420p" -an -c:v libx264 -crf 17 -preset medium aer_v.mp4
ffmpeg -v error -y -i aer_v.mp4 -i reel_v3_voz.mp4 -i pad.wav -filter_complex "[0:v]setpts=PTS-STARTPTS,settb=AVTB[a];[1:v]fps=30,setpts=PTS-STARTPTS,settb=AVTB[b];[a][b]xfade=transition=fade:duration=0.5:offset=3.5,format=yuv420p[v];[2:a]atrim=0:4,asetpts=PTS-STARTPTS[p];[p][1:a]acrossfade=d=0.5[au]" -map "[v]" -map "[au]" -c:v libx264 -crf 18 -preset medium -profile:v high -c:a aac -b:a 192k -movflags +faststart reel_lagos_del_sol_v3_final.mp4

# 4) YouTube: vuelo aéreo de 4 s después del primer plano
ffmpeg -v error -y -ss 1.0 -t 4.6 -i aereo.mp4 -vf "fps=30,scale=1920:1080:flags=lanczos,zoompan=z='1+0.0008*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30,$GRADO,drawtext=fontfile=$F:text='$LBL':fontsize=22:fontcolor=0xFDFCF8@0.9:$BOX:boxborderw=10:x=w-tw-40:y=h-th-36,drawtext=fontfile=$F:text='LAGOS DEL SOL · CANCÚN':fontsize=28:fontcolor=0xC9A96E:$BOX:boxborderw=12:x=110:y=h-150,format=yuv420p" -an -c:v libx264 -crf 17 -preset medium aer_h.mp4
O1=$(python3 -c "print(round($YT_CORTE-0.6,3))"); O2=$(python3 -c "print(round($YT_CORTE-0.6+4.0-0.6,3))")
ffmpeg -v error -y -i yt_v3.mp4 -i aer_h.mp4 -i pad.wav -filter_complex "[0:v]trim=0:$YT_CORTE,setpts=PTS-STARTPTS,settb=AVTB[A];[0:v]trim=start=$YT_CORTE,setpts=PTS-STARTPTS,settb=AVTB[B];[1:v]setpts=PTS-STARTPTS,settb=AVTB[X];[A][X]xfade=transition=fade:duration=0.6:offset=$O1[AX];[AX][B]xfade=transition=fade:duration=0.6:offset=$O2,format=yuv420p[v];[0:a]atrim=0:$YT_CORTE,asetpts=PTS-STARTPTS[a1];[0:a]atrim=start=$YT_CORTE,asetpts=PTS-STARTPTS[a2];[2:a]atrim=0:4.0,asetpts=PTS-STARTPTS[p];[a1][p]acrossfade=d=0.6[ap];[ap][a2]acrossfade=d=0.6[au]" -map "[v]" -map "[au]" -c:v libx264 -crf 20 -preset medium -profile:v high -c:a aac -b:a 192k -movflags +faststart youtube_lagos_del_sol_v3_final.mp4
for f in reel_lagos_del_sol_v3_final.mp4 youtube_lagos_del_sol_v3_final.mp4; do ffprobe -v error -show_entries format=duration,size -of csv=p=0 $f; done
echo HECHO
