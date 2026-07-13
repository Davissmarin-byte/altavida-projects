# Guía de Configuración — Sistema IA Alta Vida Inmuebles

## Componentes del sistema

| Componente | Archivo | Estado |
|-----------|---------|--------|
| Prompt de Avi (Claude) | `avi-system-prompt.txt` | ✅ Listo |
| Descripción Instagram AI | `avi-instagram-description.txt` | ✅ Listo |
| Make.com — Respuestas WA entrantes | `make-whatsapp-ai-blueprint.json` | ✅ Listo (necesita API key) |
| Kommo SalesBot | `kommo-salesbot-config.json` | ✅ Listo (configurar en UI) |

---

## PASO 1 — Obtén tu Anthropic API Key

1. Ve a: **console.anthropic.com**
2. Inicia sesión con el mismo email que usas en Claude.ai
3. Sidebar izquierdo → **API Keys** → **Create Key**
4. Ponle nombre: `altavida-whatsapp`
5. Copia la clave (empieza con `sk-ant-...`)
6. Guárdala — solo se muestra una vez

> ⚠️ Claude.ai (chat) y la API son cuentas separadas. Necesitas agregar un método de pago en console.anthropic.com. El modelo `claude-haiku-4-5` cuesta ~$0.25 por millón de tokens de entrada — muy económico para mensajes de WhatsApp.

---

## PASO 2 — Configura "Avi" en Instagram AI Studio

1. Abre Instagram → Tu perfil `@altavidainmuebles`
2. Ve al enlace de "Avi tu asistente AltaVida 24/7" que ya creaste
3. En **"Describe tu IA"**, reemplaza el texto actual con el contenido de `avi-instagram-description.txt`
4. En **"Configuración avanzada"**, pega las instrucciones del mismo archivo
5. Publica los cambios

---

## PASO 3 — Crea el escenario de WhatsApp entrante en Make.com

1. Ve a: **us2.make.com** → Crear nuevo escenario
2. Agrega módulo **Custom Webhook** (copia la URL del webhook)
3. En 360dialog: **Configuración → Webhooks → Agregar** la URL del webhook de Make
4. Importa el blueprint `make-whatsapp-ai-blueprint.json`
5. Reemplaza en el módulo Claude (id 3):
   - `REEMPLAZAR_CON_TU_ANTHROPIC_API_KEY` → tu clave de Anthropic
6. Reemplaza en los módulos de Kommo (id 5 y 6):
   - `REEMPLAZAR_CON_KOMMO_TOKEN` → el Bearer token de Kommo
7. Activa el escenario

---

## PASO 4 — Configura el SalesBot en Kommo

1. Ve a: **davissmarin.kommo.com/settings/salesbot/**
2. Crea un nuevo bot llamado "Avi - Alta Vida 24/7"
3. Para cada etapa del pipeline, crea los pasos según `kommo-salesbot-config.json`
4. Conecta el bot al pipeline principal de leads
5. Asegúrate de que el canal de WhatsApp (360dialog) está conectado en Kommo

---

## PASO 5 — Configura el pipeline en Kommo

Crea estas etapas en **davissmarin.kommo.com/settings/pipelines/**:

1. 🔵 **Nuevo Lead** — entrada automática desde Meta Ads
2. 📞 **Primer Contacto** — WhatsApp enviado, esperando respuesta
3. ✅ **Calificado** — tiene presupuesto e interés confirmado
4. 📅 **Visita Agendada** — cita con asesor programada
5. 📄 **Propuesta Enviada** — ficha o cotización enviada
6. 💬 **Negociación** — en proceso de cierre
7. 🏡 **Cierre Exitoso** — ¡vendido!
8. ❌ **No Interesado** — lead perdido (con motivo)

---

## Flujo completo una vez configurado

```
Lead Meta Ads
     ↓
Make.com Webhook (escenario existente 4885612)
     ↓
Google Sheets ← registro automático
     ↓
WhatsApp 360dialog ← mensaje de bienvenida Avi
     ↓
Kommo CRM ← lead creado con contacto, teléfono y email
     ↓
SalesBot Kommo ← secuencia de seguimiento automatizada
     ↓
Si cliente responde por WhatsApp:
     ↓
Make.com escenario NUEVO (entrante) ← este archivo
     ↓
Claude API (Avi) ← genera respuesta personalizada
     ↓
360dialog ← envía respuesta
     ↓
Kommo ← nota registrada en el lead
```

---

## Costo estimado mensual

| Servicio | Costo approx. |
|---------|--------------|
| Anthropic Claude Haiku | $5-15 USD/mes (500-1500 conversaciones) |
| Make.com (operaciones) | Según plan actual |
| 360dialog WhatsApp | Según conversaciones activas |

---

## Próximos pasos recomendados

1. **Agregar catálogo completo** de propiedades al system prompt de Avi
2. **Conectar Google Sheets** con inventario de propiedades actualizado en tiempo real
3. **Configurar Avi en WhatsApp Business** con mensaje de bienvenida automático
4. **Integrar Meta Ads Lead Forms** directamente en el pipeline de Kommo
5. **Dashboard de conversiones** en Google Sheets o Notion
