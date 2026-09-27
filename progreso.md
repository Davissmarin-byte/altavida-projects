# Progreso — Loop gerente Alta Vida

**Meta:** 1 video vertical (30–40 s) y 5 piezas de contenido listas para publicar, que vendan las propiedades de $10M a $24M MXN del inventario de Alta Vida.

**Vuelta:** 0 / 15

## Reglas del loop

- Una tarea por vuelta: siempre la primera de «Pendientes» que no esté bloqueada.
- Si una tarea necesita un dato que está en «Te necesito», se salta y se toma la siguiente. Si todas las que quedan están bloqueadas, el loop para.
- Nunca inventar precios, metros, nombres de residencial ni amenidades. Si no están en `contenido-lujo/propiedades.md`, se escribe `[PENDIENTE: dato]` y se anota en «Te necesito».
- Una tarea se da por buena solo si pasa todo lo que dice `revision.md`. Si falla 2 veces seguidas, pasa a «Te necesito» con el error exacto.

**Puede hacer sin preguntar** (supuesto: Jaime no lo ha confirmado, edítalo si no aplica):
crear y editar archivos en este repo, correr lint y render, commit y push a la rama `claude/self-managing-loop-setup-03kzff`, abrir un PR en borrador, redactar textos sin enviarlos.

**Tiene que buscar a Jaime** (supuesto, pendiente de confirmar):
publicar o enviar algo a un cliente real, gastar dinero (pauta de Meta, créditos de Higgsfield), usar datos de propiedades que no estén escritos, hacer merge a `main`.

## Pendientes

1. Crear `contenido-lujo/propiedades.md`: una tabla vacía con las columnas nombre, residencial/zona, precio MXN, m² terreno, m² construcción, recámaras, 3 amenidades, diferenciador y ruta de las fotos o clips. Anotar en «Te necesito» que Jaime la llene con 3 a 5 propiedades.
2. Crear `contenido-lujo/brief.md` con cliente objetivo (inversionista o empresario de 35 a 65 años con liquidez), 3 mensajes clave, tono, lista de palabras prohibidas, un CTA único (WhatsApp → visita privada) y los colores tomados de `alta-vida-video/src/theme.ts`.
3. Crear `contenido-lujo/plan.md` con una tabla de las 5 piezas (número, formato, canal, objetivo y propiedad). Propuesta: 1) carrusel de IG «3 propiedades de $10M a $24M»; 2) carrusel de IG con la ficha de la propiedad A; 3) post de Facebook/Marketplace con la propiedad B; 4) 3 historias de IG con encuesta; 5) mensaje de WhatsApp para cartera y referidos.
4. Crear `contenido-lujo/video/guion.md`: video vertical de 30 a 40 s, una tabla de escenas (segundo de inicio y fin, imagen, texto en pantalla), hook en los primeros 3 s y cierre con el CTA del brief.
5. Pieza 1: `contenido-lujo/piezas/01-carrusel-3-propiedades.md` (texto de cada slide y caption).
6. Pieza 2: `contenido-lujo/piezas/02-carrusel-ficha.md` (texto de cada slide y caption).
7. Pieza 3: `contenido-lujo/piezas/03-post-marketplace.md` (título, descripción y precio).
8. Pieza 4: `contenido-lujo/piezas/04-historias-ig.md` (3 frames, sticker de encuesta y CTA).
9. Pieza 5: `contenido-lujo/piezas/05-whatsapp-cartera.md` (mensaje de 90 palabras o menos y variante para referidos).
10. Crear `alta-vida-video/src/content-lujo.ts` con los textos del guion, con la misma forma que `content.ts`.
11. Registrar la composición `VideoLujo` (1080×1920) en `alta-vida-video/src/Root.tsx` reutilizando los componentes que ya existen, y pasar `npm run lint`.
12. Renderizar `alta-vida-video/out/video-lujo.mp4` y verificar que dure entre 30 y 40 s.
13. Crear `contenido-lujo/entrega.md` con el índice de los 6 entregables y sus rutas, y qué publicar, en qué canal y en qué día. Después, commit, push y PR en borrador.

## Hecho

_(vacío)_

## Te necesito

- **Confirmar permisos:** no contestaste las preguntas 2 y 3. El loop usa los supuestos de arriba; corrígelos aquí si algo no aplica.
- **Material del video:** clips o fotos de las propiedades de $10M a $24M. Súbelos a `alta-vida-video/public/lujo/`. Sin eso, el render de la tarea 12 usa `clip.mp4` como material provisional.
