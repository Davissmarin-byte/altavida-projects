#!/usr/bin/env python3
"""PreToolUse: nunca editar ni borrar archivos .env (sí se permite .env.example)."""
import json, os, re, sys

data = json.load(sys.stdin)
tool = data.get("tool_name", "")
inp = data.get("tool_input", {}) or {}

def is_env(path):
    name = os.path.basename(str(path))
    return name == ".env" or (name.startswith(".env.") and name != ".env.example")

blocked = False
if tool in ("Edit", "Write", "NotebookEdit", "MultiEdit"):
    blocked = is_env(inp.get("file_path") or inp.get("notebook_path") or "")
elif tool == "Bash":
    cmd = str(inp.get("command", ""))
    mentions = re.search(r"(^|[\s/'\"=])\.env(\.(?!example\b)[\w-]+)?(?=$|[\s'\";|&>)])", cmd)
    writes = re.search(r"\b(rm|mv|cp|tee|truncate|shred|unlink|chmod|dd)\b|sed\s+-i|>{1,2}|perl\s+-[a-z]*i", cmd)
    blocked = bool(mentions and writes)

if blocked:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Regla de Alta Vida: nunca editar ni borrar archivos .env (guardan las claves del respondedor de Kommo)."}}, ensure_ascii=False))
sys.exit(0)
