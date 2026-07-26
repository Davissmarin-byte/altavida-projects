# ALTAVIDA — Make.com Automation Fix

Escenario Make.com ID: **4885612**  
Flujo: Meta Ads Webhook → Google Sheets → WhatsApp (360dialog) → Kommo CRM

## Bugs corregidos

### Bug 1 — Módulo 7 (Kommo): error 400 `NotSupportedChoice`
**Causa:** `PHONE` y `EMAIL` estaban en `custom_fields_values` del lead.  
Esos campos pertenecen al **contacto**, no al lead.

**Antes (roto):**
```json
[{"name":"Lead ALTAVIDA - {{1.nombre}}",
  "custom_fields_values":[
    {"field_code":"PHONE","values":[{"value":"{{1.telefono}}"}]},
    {"field_code":"EMAIL","values":[{"value":"{{1.email}}"}]}
  ]}]
```

**Después (correcto):**
```json
[{"name":"Lead ALTAVIDA - {{1.nombre}}",
  "_embedded":{"contacts":[{
    "name":"{{1.nombre}}",
    "custom_fields_values":[
      {"field_code":"PHONE","values":[{"value":"{{1.telefono}}","enum_code":"MOB"}]},
      {"field_code":"EMAIL","values":[{"value":"{{1.email}}","enum_code":"WORK"}]}
    ]
  }]}}]
```

### Bug 2 — Módulo 3 (WhatsApp 360dialog): error 400 `Invalid parameter`
**Causa:** El número usaba prefijo `521{{1.telefono}}`. El `1` es redundante.  
360dialog v2 requiere formato E.164: código de país + número (sin el 1 extra para México).

**Antes:** `"to":"521{{1.telefono}}"` → resultado: `5219984894142` (13 dígitos, inválido)  
**Después:** `"to":"52{{1.telefono}}"` → resultado: `529984894142` (12 dígitos, correcto)

### Bug 3 — Módulo 12 (Kommo nativo sin OAuth)
No aparece en el blueprint activo — fue eliminado previamente. ✓

---

## Aplicar el fix

### Opción A — Script automático (recomendado)

1. Obtén tu API key en: **Make.com → Perfil → API**
2. Ejecuta:
```bash
export MAKE_API_KEY="tu-api-key"
python3 apply-make-fix.py
```

### Opción B — Manual en Make.com UI

**Módulo 3 (WhatsApp):**
1. Abre el escenario en `us2.make.com/2213687/scenarios/4885612/edit`
2. Haz clic en el módulo 3 (HTTP WhatsApp)
3. En el campo **Body**, cambia `521{{1.telefono}}` por `52{{1.telefono}}`

**Módulo 7 (Kommo):**
1. Haz clic en el módulo 7 (HTTP Kommo)
2. Reemplaza el contenido de **Body** con:
```json
[{"name":"Lead ALTAVIDA - {{1.nombre}}","_embedded":{"contacts":[{"name":"{{1.nombre}}","custom_fields_values":[{"field_code":"PHONE","values":[{"value":"{{1.telefono}}","enum_code":"MOB"}]},{"field_code":"EMAIL","values":[{"value":"{{1.email}}","enum_code":"WORK"}]}]}]}}]
```
3. Guarda el escenario

### Opción C — Importar blueprint desde archivo

El archivo `make-blueprint-corrected.json` contiene el blueprint validado completo.

---

## Verificación

Enviar lead de prueba al webhook:
```bash
curl -X POST https://hook.us2.make.com/tmn161mw17n3ipiwp28irr0pgebvf3gf \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test Claude Code","telefono":"9984894142","email":"test@altavida.mx","canal":"Meta Ads","propiedad":"Aqua Residencial"}'
```

Confirmar en: https://davissmarin.kommo.com/leads

---

## Notas técnicas

- **Token Kommo** expira: 2030-05-09 (vigente)
- **Escenario activo:** `isActive: true` ✓
- **Blueprint validado** por Make MCP schema validator ✓
