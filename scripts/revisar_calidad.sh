#!/usr/bin/env bash
# Revisa la calidad de un video ANTES de editarlo o gastar créditos.
# Uso: scripts/revisar_calidad.sh video.mp4 [video2.mov ...]
#   APTO     lado corto >= 1080 px y >= 4 Mbps de video
#   REVISAR  lado corto 720-1079 px o 2-4 Mbps: se escala y se mira un fotograma a tamaño completo antes de usarlo
#   NO USAR  lado corto < 720 px o < 2 Mbps: no se edita; se pide el original o mejora con IA solo si Jaime la autoriza
for f in "$@"; do
  ffprobe -v error -select_streams v:0 -show_entries stream=width,height,bit_rate,r_frame_rate:format=duration,size -of json "$f" | python3 -c "
import json,sys
d=json.load(sys.stdin); s=d['streams'][0]; fm=d['format']
w,h=s['width'],s['height']; br=s.get('bit_rate')
br=float(br) if br not in (None,'N/A') else float(fm['size'])*8/float(fm['duration'])
short=min(w,h); n,dd=s['r_frame_rate'].split('/'); fps=round(int(n)/int(dd))
v='APTO' if short>=1080 and br>=4e6 else ('NO USAR' if short<720 or br<2e6 else 'REVISAR')
print(f'{v} | {w}x{h} | {br/1e6:.1f} Mbps | {fps} fps | $f')"
done
