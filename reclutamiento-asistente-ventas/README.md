# Reclutamiento: Asistente de Ventas — ALTA VIDA Inmuebles

Paquete completo para contratar al Asistente de Ventas de ALTA VIDA Inmuebles: perfil, esquema
de compensación, mensaje de contacto y creativo para redes sociales.

## Contenido

- **`propuesta-asistente-ventas.pdf`** — Documento completo (6 páginas): perfil del puesto,
  condiciones laborales y periodo de prueba, esquema de compensación con benchmark de mercado
  (OCC, Computrabajo, Indeed, Glassdoor), plan de desarrollo/capacitación y proceso de selección.
- **`mensaje-whatsapp.md`** — Mensaje listo para enviar a candidatas/os por WhatsApp (versión
  larga y versión corta).
- **`publicidad-redes-sociales.md`** — Tres variantes de copy para Instagram/Facebook (feed,
  tono aspiracional y versión corta para Stories/Reels).
- **`banner/banner-asistente-ventas.png`** — Arte para publicar en redes (1080×1350, formato
  feed/IG), inspirado en el estilo de anuncios de reclutamiento inmobiliario de la referencia
  adjunta, adaptado a la identidad de marca de ALTA VIDA (paleta `#FDFCF8 / #C9A96E / #1C1510 /
  #F5EFE6`, tipografías Cormorant Garamond + Montserrat).

## Resumen de la propuesta de compensación

| Etapa | Sueldo base | Bono | Total potencial |
|---|---|---|---|
| Prueba (día 1–30/60) | $10,000 MXN | hasta $2,000 MXN (KPIs) | $12,000 MXN |
| Formalización (día 31/61+) | $10,000 MXN (se mantiene) | $2,000 MXN + comisión por cierre | $12,000 MXN + comisiones |

Se recomienda **mantener el bono variable de $2,000** en lugar de subir el fijo a $12,000,
para preservar el vínculo entre pago y desempeño. Ver el PDF para el detalle completo y las
fuentes de benchmark de mercado.

## Regenerar el banner

El banner se genera con Python + Pillow a partir de `scripts/make_banner.py` (fuentes
Cormorant Garamond y Montserrat instanciadas como estáticas en `scripts/fonts/static/`).
El PDF se genera con `scripts/make_pdf.py` (reportlab).
