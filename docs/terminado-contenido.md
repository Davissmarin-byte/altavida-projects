# Terminado: contenido que vende de una propiedad

Tarea: crear reel, carrusel e historia de una propiedad, subirlos a Drive y programarlos en Metricool.
Cada punto se contesta con sí o no.

1. Los datos coinciden con la fuente: precio, m², recámaras y baños salen de la ficha, carpeta o anuncio, y cito cuál.
   Revisión: comparo cada cifra del copy y de las imágenes contra la fuente citada.
2. No aparece ninguna dirección exacta, número de casa ni dato personal, ni en el texto ni en las imágenes.
   Revisión: `grep -nE '[A-Za-z]+ [0-9]{1,4}\b|#[0-9]+' copy.txt` y reviso fotogramas del reel con `ffmpeg -ss <s> -i reel.mp4 -frames:v 1 f.jpg`.
3. Los formatos son correctos: reel 1080x1920 mp4 de 10 a 60 s y menos de 3 MB (el conector de Drive no deja subir archivos más pesados); carrusel 1080x1350; historia 1080x1920.
   Revisión: `ffprobe -v error -show_entries stream=width,height:format=duration,size -of csv=p=0 reel.mp4` y `identify -format '%f %wx%h\n' *.jpg`.
   Calidad: miro un fotograma a tamaño completo; si se ve pixelado o borroso, no pasa.
4. Cada pieza lleva logo de Alta Vida y la última lámina o escena trae WhatsApp 998 154 6066 y 998 430 9472.
   Revisión: miro la última lámina y el último fotograma del reel.
5. El copy trae llamado a la acción a WhatsApp, las 6 cuentas de Instagram del CLAUDE.md, de 8 a 12 hashtags y un primer comentario con pregunta y WhatsApp.
   Revisión: `grep -c '998 154 6066' copy.txt`, `grep -o '@[a-z._]*' copy.txt | sort -u | wc -l` (6) y `grep -o '#[A-Za-z]*' copy.txt | wc -l` (8 a 12).
6. Todo está en Drive, en la carpeta con la fecha dentro de "Alta Vida – Contenido diario", y la copia descargada es idéntica al original.
   Revisión: bajo un archivo de Drive y comparo `sha256sum` contra el local.
7. Cada pieza está programada en Metricool en las redes que tocan, como publicación orgánica, sin pauta pagada.
   Revisión: getScheduledPosts muestra cada publicación en PENDING, con la fecha correcta y sin boost.
8. El resumen para Jaime dice a qué cliente va cada pieza, qué resultado se espera (mensajes, citas o leads) y cómo se mide.
   Revisión: el resumen tiene esos tres datos por pieza.
