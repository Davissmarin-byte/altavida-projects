# Revisión — qué tiene que pasar una tarea para darse por buena

Hay que correr cada comprobación que aplique a la tarea y anotar en «Hecho» de `progreso.md` el resultado de cada una (✅ o ❌ con el motivo). Si una falla, la tarea no está terminada.

## 1. El archivo existe y tiene sus partes
El archivo que pide la tarea existe en la ruta exacta y tiene todas las secciones o campos que la tarea menciona.
```bash
test -s <ruta> && grep -c '^#' <ruta>
```
Falla si el archivo está vacío o si falta alguna sección que la tarea nombra (por ejemplo, «caption» en un carrusel).

## 2. Cero datos inventados
Todo precio, metraje o nombre de residencial que aparezca en `contenido-lujo/` tiene que estar también en `contenido-lujo/propiedades.md`. Si falta, va `[PENDIENTE: …]` y ese pendiente tiene que estar en «Te necesito».
```bash
grep -rhoE '\$[0-9][0-9,.]*( ?(M|MDP|millones))?' contenido-lujo/ --exclude=propiedades.md | sort -u
# cada resultado debe aparecer con grep -F en contenido-lujo/propiedades.md
grep -rn 'PENDIENTE' contenido-lujo/
```
Falla si aparece un precio que no está en `propiedades.md`, o si un `[PENDIENTE]` no está anotado en «Te necesito».

## 3. Rango y CTA correctos
Todo precio mencionado está entre $10,000,000 y $24,000,000 MXN. Cada pieza tiene exactamente un CTA y ese CTA es el que define `brief.md` (WhatsApp → visita privada).
```bash
grep -ciE 'whatsapp|agenda|visita privada' contenido-lujo/piezas/<pieza>.md
```
Falla si hay 0 CTA, si hay 2 CTA distintos o si algún precio queda fuera del rango.

## 4. Límites de longitud
- Hook del video y títulos de slide: 10 palabras o menos.
- Caption de Instagram: 2,200 caracteres o menos.
- Mensaje de WhatsApp: 90 palabras o menos.
```bash
wc -w <archivo o fragmento>   # palabras
wc -m <archivo o fragmento>   # caracteres
```

## 5. El código compila
Aplica solo a las tareas que tocan `alta-vida-video/`.
```bash
cd alta-vida-video && npm install --no-audit --no-fund && npm run lint
```
Falla si `npm run lint` (eslint + tsc) no termina con exit 0.

## 6. El video renderiza y dura lo correcto
Aplica solo a la tarea 12.
```bash
cd alta-vida-video && npx remotion render VideoLujo out/video-lujo.mp4 \
  && npx remotion ffprobe -v error -show_entries format=duration -of csv=p=0 out/video-lujo.mp4
```
Falla si el render no termina con exit 0 o si la duración queda fuera de 30 a 40 segundos.
