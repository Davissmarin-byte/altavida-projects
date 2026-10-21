#!/usr/bin/env bash
# Inserta el vuelo aéreo (recreación IA de Gemini) en el Reel y en YouTube.
# Entradas en el directorio actual: aereo.mp4, reel.mp4, yt.mp4, Montserrat-Medium.ttf
# Requiere ffmpeg y sox.
set -e
F=$PWD/Montserrat-Medium.ttf
LBL="Recreación ilustrativa generada con IA"
BOX="shadowcolor=black@0.6:shadowx=2:shadowy=2:box=1:boxcolor=0x1C1510@0.55"
GRADO="eq=saturation=0.92:contrast=1.04,colorbalance=rh=0.03:bh=-0.03"
# pad musical suave (síntesis propia) para el tramo aéreo
sox -n -r 48000 -c 2 pad.wav synth 5 sine 130.81 sine 196.0 sine 246.94 sine 329.63 remix 1-4 1-4 gain -14 fade q 1.2 5 1.5

# REEL 9:16: vuelo de 3.5 s al inicio + Reel original (disolvencia de 0.5 s)
ffmpeg -v error -y -ss 1.0 -t 4.0 -i aereo.mp4 -vf "fps=30,scale=-2:1920:flags=lanczos,crop=1080:1920:x='(iw-1080)*(0.15+0.5*t/4)':y=0,$GRADO,drawtext=fontfile=$F:text='$LBL':fontsize=26:fontcolor=0xFDFCF8@0.9:$BOX:boxborderw=14:x=(w-tw)/2:y=250,drawtext=fontfile=$F:text='LAGOS DEL SOL · CANCÚN':fontsize=30:fontcolor=0xC9A96E:$BOX:boxborderw=14:x=(w-tw)/2:y=330,format=yuv420p" -an -c:v libx264 -crf 17 -preset medium aer_v.mp4
ffmpeg -v error -y -i aer_v.mp4 -i reel.mp4 -i pad.wav -filter_complex "[0:v]setpts=PTS-STARTPTS,settb=AVTB[a];[1:v]fps=30,setpts=PTS-STARTPTS,settb=AVTB[b];[a][b]xfade=transition=fade:duration=0.5:offset=3.5,format=yuv420p[v];[2:a]atrim=0:4,asetpts=PTS-STARTPTS[p];[p][1:a]acrossfade=d=0.5[au]" -map "[v]" -map "[au]" -c:v libx264 -crf 18 -preset medium -profile:v high -c:a aac -b:a 192k -movflags +faststart reel_lagos_del_sol_v2.mp4

# YOUTUBE 16:9: vuelo de 4 s insertado en el segundo 22.6 (después de Jaime, antes de la llegada)
ffmpeg -v error -y -ss 1.0 -t 4.6 -i aereo.mp4 -vf "fps=30,scale=1920:1080:flags=lanczos,zoompan=z='1+0.0008*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30,$GRADO,drawtext=fontfile=$F:text='$LBL':fontsize=22:fontcolor=0xFDFCF8@0.9:$BOX:boxborderw=10:x=w-tw-40:y=h-th-36,drawtext=fontfile=$F:text='LAGOS DEL SOL · CANCÚN':fontsize=28:fontcolor=0xC9A96E:$BOX:boxborderw=12:x=110:y=h-150,format=yuv420p" -an -c:v libx264 -crf 17 -preset medium aer_h.mp4
ffmpeg -v error -y -i yt.mp4 -i aer_h.mp4 -i pad.wav -filter_complex "[0:v]trim=0:22.6,setpts=PTS-STARTPTS,settb=AVTB[A];[0:v]trim=start=22.6,setpts=PTS-STARTPTS,settb=AVTB[B];[1:v]setpts=PTS-STARTPTS,settb=AVTB[X];[A][X]xfade=transition=fade:duration=0.6:offset=22.0[AX];[AX][B]xfade=transition=fade:duration=0.6:offset=25.4,format=yuv420p[v];[0:a]atrim=0:22.6,asetpts=PTS-STARTPTS[a1];[0:a]atrim=start=22.6,asetpts=PTS-STARTPTS[a2];[2:a]atrim=0:4.0,asetpts=PTS-STARTPTS[p];[a1][p]acrossfade=d=0.6[ap];[ap][a2]acrossfade=d=0.6[au]" -map "[v]" -map "[au]" -c:v libx264 -crf 20 -preset medium -profile:v high -c:a aac -b:a 192k -movflags +faststart youtube_lagos_del_sol_v2.mp4
