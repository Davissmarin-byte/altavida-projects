# Campaña orgánica · Casa frente al lago · Lagos del Sol · $23,900,000 MXN

ALTA VIDA Inmuebles · octubre de 2026

## Piezas listas (`salidas/`)

| Pieza | Archivo | Formato |
|---|---|---|
| Carrusel IG/FB | `salidas/carrusel/carrusel_01…12.jpg` | 12 láminas, 1080×1350 |
| Reel / TikTok / FB Reels | `salidas/reel/reel_lagos_del_sol.mp4` (+ `.srt`) | 9:16, 1080×1920, 57 s, voz + subtítulos + música |
| YouTube | `salidas/youtube/youtube_lagos_del_sol.mp4` (+ `.srt`, `youtube_miniatura.jpg`) | 16:9, 1920×1080, 3:04 |
| Historias | `salidas/historias/historia_01…06.jpg` y `.mp4` | 9:16, MP4 de 7 s |
| ZIP para WhatsApp | `salidas/historias_whatsapp.zip` | 6 JPG + 6 MP4 |
| Muestras de voz | `salidas/muestras_voz/A_masculina_principal.m4a`, `B_masculina_alterna.m4a`, `C_femenina.m4a` | ~15 s |

## Textos (`copy/`)

1. `01_concepto_y_guion.md`: concepto «El lago como horizonte» y guiones del Reel y de YouTube
2. `02_copys_publicaciones.md`: copys, hashtags, menciones, stickers y mensaje para la cartera de WhatsApp
3. `03_calendario_y_pendientes.md`: calendario con los mejores horarios de Metricool y checklist
4. `04_youtube_metadatos.md`: título, descripción SEO con capítulos y etiquetas

## Reglas aplicadas

- Solo fotos reales de la propiedad; ninguna persona ficticia. La única persona que aparece es Jaime Marín, con su foto real (IMG_2630).
- Solo los datos de la ficha técnica. No se menciona arquitecto ni plusvalía.
- Logo ALTAVIDA® oficial (`ALTA VIDA PNG .png`) sin modificar, solo en el cierre y sobre fondo marfil.
- El vuelo aéreo IA (Gemini) **no se usó**, porque no se pudo verificar su fidelidad.
- La voz en off es sintética (Kokoro, voz masculina en español). Al publicar el Reel, el TikTok y el video de YouTube hay que activar la etiqueta de IA.
- La música es original, sintetizada en `scripts/voz.py`, sin derechos de terceros.

## Cómo regenerar

Requiere Python con `pillow`, `numpy`, `soundfile`, `kokoro-onnx` y `ffmpeg`. El material fuente (fotos, logo, fuentes y modelo de voz) va en `$CAMP_SRC`.

```bash
CAMP_SRC=/ruta/material python scripts/voz.py $CAMP_SRC/out/audio em_alex
CAMP_SRC=/ruta/material python scripts/carrusel.py salidas/carrusel
CAMP_SRC=/ruta/material python scripts/historias.py salidas/historias
CAMP_SRC=/ruta/material python scripts/video.py reel salidas/reel
CAMP_SRC=/ruta/material python scripts/video.py youtube salidas/youtube
CAMP_SRC=/ruta/material python scripts/miniatura.py salidas/youtube/youtube_miniatura.jpg
```

Para cambiar la voz por el clon de Jaime, sustituye los WAV en `$CAMP_SRC/out/audio/` (mismos nombres) y vuelve a correr `video.py`.
