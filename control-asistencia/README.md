# Control de asistencia sin cámara · Alta Vida Inmuebles

Google Form con hora automática para entrada y salida, checklist de apertura y cierre, foto de la oficina y alertas por correo a dirección. Primer uso: **Alejandra Valle**, Asistente de Dirección y Contenido Digital.

## Archivos

| Archivo | Para quién | Qué es |
|---|---|---|
| `Instructivo-Asistencia-Alejandra-Valle.pdf` / `.docx` | Alejandra | Instructivo para imprimir y firmar (acuse de recibo) |
| `apps-script/Code.gs` + `appsscript.json` | Dirección | Script que crea el formulario, la hoja y las alertas |

## Configuración (15 minutos, una sola vez)

1. Entra a <https://script.google.com> con la cuenta de Alta Vida → **Nuevo proyecto**. Nómbralo "Asistencia Alta Vida".
2. Borra el contenido de `Código.gs` y pega todo `apps-script/Code.gs`.
3. **Configuración del proyecto** (engrane) → activa "Mostrar el archivo de manifiesto appsscript.json" → pega `apps-script/appsscript.json`.
4. Si hace falta, ajusta `CONFIG` al inicio del script: hora de entrada (`08:00`), salida (`18:00`), tolerancia (10 min), días laborales (lunes a sábado) y correo de dirección (vacío = tu cuenta).
5. Selecciona la función `instalar` → **Ejecutar** → autoriza los permisos.
6. Te llega un correo con 3 links: formulario, edición del formulario y hoja de registros.
7. **Paso manual (Google no permite hacerlo por script):** abre el link de edición → sección "Checklist de apertura" → agrega una pregunta **Subir archivo** llamada "Foto de la oficina abierta": obligatoria, solo imágenes, 1 archivo, máximo 10 MB.
8. Envía a Alejandra **solo el link del formulario** por WhatsApp. **No** le compartas la hoja.
9. Haz una prueba con ella el primer día (entrada y salida) y revisa que aparezcan en la hoja "Control".

## Qué pasa automáticamente

- Cada registro se guarda con hora exacta y correo verificado de Google (no se puede escribir la hora a mano).
- En la hoja **Control** cada registro se marca como `A tiempo`, `RETARDO`, `Salida completa` o `SALIDA ANTICIPADA`, con los minutos de diferencia.
- Correo a dirección cuando hay retardo, salida anticipada o incidencia de insumos.
- **08:15** – si no hay entrada, correo "SIN REGISTRO DE ENTRADA".
- **18:30** – si hubo entrada pero no salida, correo "SIN REGISTRO DE SALIDA".
- Las fotos se guardan en tu Google Drive, en una carpeta del formulario.

Para pausar o reinstalar: ejecuta `desinstalarTriggers`.

## Para que sirva como evidencia laboral

- **Que firme el acuse** (página 3 del instructivo) y guarda el original. Escanéalo a Drive.
- La hoja y el formulario son solo tuyos: no le des permisos de edición. La pestaña "Control" está protegida.
- No borres respuestas. Si algo se corrige, hazlo con una nota aparte, no editando el registro.
- Conserva los registros durante toda la relación laboral y al menos 1 año después de que termine (LFT art. 804). En un juicio la carga de la prueba sobre la jornada es del patrón (LFT art. 784).
- Menciona este método de control en su contrato o en el reglamento interior. Pide a tu abogado laboral o contador que lo valide antes de usarlo como única prueba.
