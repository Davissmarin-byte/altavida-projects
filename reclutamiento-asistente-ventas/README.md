# Reclutamiento: Asistente de Ventas — ALTA VIDA Inmuebles

Paquete completo para contratar al Asistente de Ventas de ALTA VIDA Inmuebles: perfil, esquema
de compensación, mensaje de contacto y creativo para redes sociales.

## Contenido

- **`propuesta-asistente-ventas.pdf`** — Documento completo: perfil del puesto, condiciones
  laborales y periodo de evaluación (15–20 días), esquema de compensación con benchmark de
  mercado (OCC, Computrabajo, Indeed, Glassdoor) y nota legal (salario mínimo 2026 y Art. 39-A
  LFT), plan de desarrollo/capacitación y proceso de selección.
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
| Evaluación (día 1–15/20) | $10,000 MXN | $500–$1,000 MXN (bono de arranque) | $10,500–$11,000 MXN |
| Formalización (día 15/21+) | $10,000 MXN (se mantiene) | $2,000 MXN + comisión/bono por volumen | $12,000 MXN + comisiones |

El sueldo base no baja de $10,000 porque, desde el 1 de enero de 2026, el salario mínimo
general en México es de $9,582.47 MXN/mes (DOF/CONASAMI) — $8,000 u $9,000 quedarían por
debajo del piso legal, y el periodo de prueba no exime del salario mínimo. La ventana de
evaluación se fijó en 15–20 días (no 30–60) porque el Art. 39-A de la LFT topa el periodo de
prueba en 30 días para puestos operativos como este. La palanca de motivación para formalizar
se mueve al bono, que sí es flexible. Ver el PDF para el detalle completo y las fuentes de
benchmark de mercado.

## Regenerar el banner

El banner se genera con Python + Pillow a partir de `scripts/make_banner.py` (fuentes
Cormorant Garamond y Montserrat instanciadas como estáticas en `scripts/fonts/static/`).
El PDF se genera con `scripts/make_pdf.py` (reportlab).
