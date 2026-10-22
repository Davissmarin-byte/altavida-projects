# Campaña orgánica · Departamentos de 3 recámaras en Av. Huayacán, Cancún · desde $1,880,000

ALTA VIDA Inmuebles · lanzamiento jueves 22 de octubre de 2026, 08:30 (Cancún)

> Regla de Jaime: **las piezas públicas no mencionan el nombre del residencial ni del desarrollador**, para que el cliente nos escriba directo. Se descartaron todas las tomas donde se lee el letrero del club o la placa del desarrollador, y se quitó el audio original de los videos.

## Piezas (ligas en `salidas/enlaces.md`)

| Pieza | Formato | Estilo |
|---|---|---|
| Reel principal | 9:16 · 36 s | Kenia abre la puerta y recorre el depa; voz en off, subtítulos, precio y CTA |
| Reel POV «Dejaste de rentar» | 9:16 · 18.6 s | Tendencia POV, cortes al ritmo |
| Reel FAQ «¿Me alcanza con mi Infonavit?» | 9:16 · 21.8 s | Tarjetas de pregunta y respuesta |
| Reel Amenidades | 9:16 · 15.8 s | Montaje exterior + lista del brochure |
| Carrusel | 10 láminas 1080×1350 | Cuadros 4K del recorrido real |
| Historias | 6 × (MP4 7 s + JPG) + ZIP | Video real en movimiento; H6 con franja para encuesta |
| YouTube | 16:9 · 3:01 + miniatura | Recorrido completo, paneles por espacio, «Así se entrega» |

## Textos (`copy/`)

1. `01_concepto_y_guiones.md`: datos verificados, ángulos y guion del Reel principal
2. `02_copys_por_red.md`: copys de IG/FB, TikTok, Threads, YouTube Shorts, LinkedIn y stickers
3. `03_calendario_y_pendientes.md`: calendario programado en Metricool y lo que se hace a mano
4. `04_youtube_metadatos.md`: título, descripción SEO, capítulos y etiquetas
5. `05_whatsapp.md`: difusión a la cartera, estados y respuestas rápidas
6. `06_estrategia.md`: horarios, KPIs, portales y recomendación de pauta

## Cómo regenerar (sandbox de Higgsfield)

Material en `$CAMP_SRC`: `raw/` (originales de Drive), `px/` (proxys 1080p a 30 fps), `raw4k/` (enlaces a los .MOV 4K), `voz/T0…T4.wav`, `audio/` (música) y `fonts/` (Cormorant Garamond, Montserrat y el logo ALTAVIDA® de Drive).

```bash
export CAMP_SRC=~/v
python scripts/musica.py $CAMP_SRC/audio
python scripts/reel.py salidas/reel_principal.mp4
python scripts/cortos.py rentar|faq|amenidades salidas/reel_corto_X.mp4
python scripts/carrusel.py salidas/carrusel
python scripts/historias.py salidas/historias
PRESET=fast python scripts/youtube.py salidas/youtube_recorrido.mp4 salidas/youtube_miniatura.jpg
```

`montaje.py` es el motor: corta las tomas reales, aplica rótulos con fundido (cada rótulo solo existe en su ventana de tiempo) y mezcla música, voz y ducking. `capas.py` contiene los rótulos de marca (espresso #1C1510, oro #C9A96E, marfil #FDFCF8).

## Material usado

- Recorridos de Kenia Acosta (Drive «VASSARI CAMPAÑA – MATERIAL»): IMG_6564 (depa muestra, 70 s, 4K), IMG_6623 (áreas comunes), IMG_6620/6624 (alberca y jardín) y los videos de WhatsApp (Kenia abriendo la puerta; departamento entregado sin muebles).
- Lista de precios actualizada al 21/10/2026 y brochure del desarrollador (solo como fuente de datos; no se usa su logo).
- Voz «Marisol» (Higgsfield Seed Audio). Los créditos se agotaron después de 5 líneas.
