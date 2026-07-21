# kommo-ai-responder

Servicio webhook que genera respuestas automáticas con IA (Claude) para leads
de Kommo que llegan desde anuncios de Inmuebles24.

No se conecta directamente a la cuenta de Kommo ni envía mensajes por sí
mismo: **Salesbot** (el motor de automatización de Kommo) llama a este
servicio con el contexto del lead, y este responde con el texto que Salesbot
debe enviar al contacto.

## Cómo funciona

```
Inmuebles24 → Kommo (lead nuevo) → Salesbot (trigger por pipeline/etapa)
   → paso "Enviar solicitud" (webhook) → este servicio → Claude
   → respuesta de texto → Salesbot → paso "Enviar mensaje" al contacto
```

## Configuración local

1. `cp .env.example .env` y completa:
   - `KOMMO_WEBHOOK_SECRET`: cualquier cadena aleatoria larga (ej. `openssl rand -hex 32`). Debe coincidir con el header que configures en Salesbot.
   - `ANTHROPIC_API_KEY`: tu API key de Anthropic ([console.anthropic.com](https://console.anthropic.com/settings/keys)).
2. `npm install`
3. `npm run dev` (con recarga automática) o `npm run build && npm start`.

## Endpoint

`POST /kommo/salesbot-reply`

Headers:
- `X-Webhook-Secret: <el mismo valor de KOMMO_WEBHOOK_SECRET>`

Body (JSON):
```json
{
  "lead_id": "12345",
  "lead_name": "Depto Zona Hotelera - Inmuebles24",
  "contact_name": "Juan Pérez",
  "property_title": "Depto 2 recámaras frente al mar",
  "property_url": "https://www.inmuebles24.com/propiedades/...",
  "message": "¿Sigue disponible? ¿Cuál es el precio?"
}
```

Respuesta:
```json
{ "text": "¡Hola Juan! Sí, el depto sigue disponible..." }
```

Solo `message` es obligatorio; el resto de campos son opcionales y mejoran el
contexto que recibe Claude.

## Cómo conectarlo en Kommo (Salesbot)

Esta parte se configura dentro de tu cuenta de Kommo — los nombres exactos de
menú pueden variar según la versión, pero el flujo es:

1. Ve al pipeline donde caen los leads de Inmuebles24 y abre el **Salesbot**.
2. Crea/edita el bot con disparador **"Cuando un lead entra a la etapa"** (la etapa donde llegan los leads de Inmuebles24).
3. Agrega el paso **"Enviar solicitud" / "Webhook"**:
   - Método: `POST`
   - URL: la URL pública donde despliegues este servicio, ej. `https://tu-dominio.com/kommo/salesbot-reply`
   - Header: `X-Webhook-Secret: <tu KOMMO_WEBHOOK_SECRET>`
   - Body: mapea los campos del lead/contacto/último mensaje entrante a los campos `lead_id`, `lead_name`, `contact_name`, `message`, etc. (Salesbot permite insertar variables del lead con `{{ }}`).
   - Guarda la respuesta (`text`) en una variable del bot.
4. Agrega el paso **"Enviar mensaje"** usando esa variable como contenido del mensaje.
5. Activa el bot y pruébalo con un lead de prueba antes de dejarlo en producción.

## Despliegue

Incluye un `Dockerfile` listo para desplegar en cualquier proveedor que corra
contenedores (Render, Railway, Fly.io, un VPS propio, etc.). El servicio
necesita:
- Un dominio/URL pública alcanzable por Kommo (HTTPS).
- Las variables de entorno `KOMMO_WEBHOOK_SECRET` y `ANTHROPIC_API_KEY` configuradas como secretos en la plataforma de hosting (nunca en el repo).

```bash
docker build -t kommo-ai-responder .
docker run -p 3000:3000 --env-file .env kommo-ai-responder
```
