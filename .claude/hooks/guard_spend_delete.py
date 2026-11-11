#!/usr/bin/env python3
"""PreToolUse: pide confirmación de Jaime antes de gastar en pauta o borrar datos."""
import json, sys

data = json.load(sys.stdin)
tool = data.get("tool_name", "")
inp = data.get("tool_input", {}) or {}

AD_CONNECTORS = {"facebook", "google_ads", "tiktok", "linkedin", "bing", "amazon_ads"}
DELETE_TOOLS = {
    "mcp__Notion__notion-delete-pages": "borrar páginas de Notion",
    "mcp__Notion__notion-delete-databases": "borrar bases de datos de Notion",
    "mcp__Google_Drive__trash_file": "mandar un archivo de Drive a la papelera",
    "mcp__Google_Sheets__batch_clear_values": "vaciar celdas de Google Sheets",
}

reason = None
if tool == "mcp__Windsor_ai__execute_action":
    connector = str(inp.get("connector", "")).lower()
    if connector in AD_CONNECTORS:
        reason = f"Cambio en pauta pagada ({connector}, acción {inp.get('action')}). Regla: no gastar presupuesto sin autorización de Jaime."
elif tool in DELETE_TOOLS:
    reason = f"Voy a {DELETE_TOOLS[tool]}. Regla: no borrar datos sin preguntar a Jaime."

if reason:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason}}, ensure_ascii=False))
sys.exit(0)
