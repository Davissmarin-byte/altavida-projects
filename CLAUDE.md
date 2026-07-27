# CLAUDE.md

## Herramientas de gstack disponibles

Este proyecto tiene instalado [G Stack](https://github.com/garrytan/gstack) en `~/.claude/skills/gstack`. Se invoca a través del skill router `gstack` (por ejemplo, pidiendo "/autoplan" o describiendo la tarea), que despacha al subcomando correspondiente:

| Comando | Qué hace |
|---|---|
| `/autoplan` | Pipeline de auto-revisión: corre en secuencia las revisiones de CEO, diseño, ingeniería y DX con decisiones automáticas |
| `/benchmark` | Detección de regresiones de performance usando el daemon de browse |
| `/benchmark-models` | Benchmark cruzado entre modelos para los skills de gstack |
| `/browse` | Navegador headless rápido para QA y probar el sitio |
| `/canary` | Monitoreo post-deploy (canary) |
| `/careful` | Guardrails de seguridad para comandos destructivos |
| `/codex` | Wrapper de OpenAI Codex CLI (tres modos) |
| `/connect-chrome`, `/open-gstack-browser` | Lanza GStack Browser (Chromium controlado por IA con extensión sidebar) |
| `/context-save` / `/context-restore` | Guardar y restaurar contexto de trabajo |
| `/cso` | Modo "Chief Security Officer" (seguridad) |
| `/design-consultation` | Propone un sistema de diseño completo (estética, tipografía, color, layout, motion) |
| `/design-html` | Genera HTML/CSS de producción para el diseño finalizado |
| `/design-review` | QA visual: inconsistencias, espaciado, jerarquía, "AI slop" |
| `/design-shotgun` | Genera múltiples variantes de diseño para comparar |
| `/devex-review` | Auditoría en vivo de developer experience |
| `/diagram` | Convierte una descripción (o mermaid) en un diagrama editable (.excalidraw) |
| `/document-generate` | Genera documentación faltante desde cero |
| `/document-release` | Actualiza documentación después de un ship |
| `/freeze` / `/unfreeze` | Restringe (o libera) ediciones a un directorio específico durante la sesión |
| `/gstack-upgrade` | Actualiza gstack a la última versión |
| `/guard` | Modo seguridad completo: warnings de comandos destructivos + ediciones acotadas por directorio |
| `/health` | Dashboard de calidad de código |
| `/investigate` | Debugging sistemático con investigación de causa raíz |
| `/ios-clean`, `/ios-design-review`, `/ios-fix`, `/ios-qa`, `/ios-sync` | Suite de QA/debug/diseño para apps iOS |
| `/land-and-deploy` | Flujo de merge + deploy |
| `/landing-report` | Dashboard de cola (solo lectura) para ship por workspace |
| `/learn` | Administra los "learnings" del proyecto |
| `/make-pdf` | Convierte un markdown en PDF de calidad de publicación |
| `/office-hours` | "YC Office Hours" — feedback de producto en dos modos |
| `/pair-agent` | Empareja un agente de IA remoto con tu navegador |
| `/plan-ceo-review` | Revisión de plan en modo CEO/founder |
| `/plan-design-review` | Revisión de plan desde la óptica de diseño |
| `/plan-devex-review` | Revisión interactiva de plan desde developer experience |
| `/plan-eng-review` | Revisión de plan en modo eng manager |
| `/plan-tune` | Auto-ajuste de sensibilidad de preguntas de gstack |
| `/qa` | Testea sistemáticamente una web app y arregla los bugs encontrados |
| `/qa-only` | QA en modo solo-reporte (sin arreglar) |
| `/retro` | Retrospectiva semanal de ingeniería |
| `/review` | Revisión de PR antes de mergear |
| `/scrape` | Extrae datos de una página web |
| `/setup-browser-cookies` | Importa cookies de tu navegador real al browse headless |
| `/setup-deploy` | Configura el deploy para `/land-and-deploy` |
| `/setup-gbrain` | Instala y configura gbrain (memoria/índice del repo) |
| `/ship` | Flujo de ship: merge, tests, revisión de diff, versión, changelog, commit, push, PR |
| `/skillify` | Convierte el último `/scrape` exitoso en un browser-skill permanente |
| `/spec` | Convierte una intención vaga en una spec ejecutable en cinco fases |
| `/sync-gbrain` | Mantiene gbrain sincronizado con el repo |

**Nota:** la función `/browse` (y todo lo que dependa de Chromium vía Playwright) puede no funcionar en este entorno: la instalación falló al descargar el binario de Chromium porque el proxy de red del sandbox bloquea `cdn.playwright.dev`. El resto de los skills no depende de esa descarga.
