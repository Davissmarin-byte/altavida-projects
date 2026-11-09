#!/usr/bin/env python3
"""Stop: si en este turno se generó un video o imagen, exige un enlace de Google Drive en la respuesta."""
import json, re, sys

data = json.load(sys.stdin)
path = data.get("transcript_path")
if not path:
    sys.exit(0)

entries = []
with open(path, encoding="utf-8") as f:
    for line in f:
        try:
            entries.append(json.loads(line))
        except Exception:
            pass

def content(e):
    c = (e.get("message") or {}).get("content")
    return c if isinstance(c, list) else ([{"type": "text", "text": c}] if isinstance(c, str) else [])

# Inicio del turno: último mensaje del usuario que no sea solo resultado de herramientas.
start = 0
for i, e in enumerate(entries):
    if e.get("type") == "user" and any(b.get("type") == "text" for b in content(e)):
        start = i

MEDIA_EXT = r"\.(mp4|mov|webm|m4v|png|jpe?g|webp|gif)\b"
MEDIA_TOOLS = re.compile(r"^mcp__(Higgsfield__(generate_(image|video)(_batch)?|upscale_(image|video)|outpaint_image|reframe)"
                         r"|Canva__(export-design|generate-design|create-video)|HyperFrames_by_HeyGen__render_video)$")
made_media = False
last_text = ""
for e in entries[start:]:
    if e.get("type") != "assistant":
        continue
    texts = [b.get("text", "") for b in content(e) if b.get("type") == "text"]
    if texts:
        last_text = "\n".join(texts)
    for b in content(e):
        if b.get("type") != "tool_use":
            continue
        name, inp = b.get("name", ""), b.get("input") or {}
        if MEDIA_TOOLS.match(name):
            made_media = True
        elif name == "Bash":
            cmd = str(inp.get("command", ""))
            if re.search(r"remotion\s+(render|still)|ffmpeg\b|npm\s+run\s+render", cmd):
                made_media = True
        elif name == "Write" and re.search(MEDIA_EXT, str(inp.get("file_path", "")), re.I):
            made_media = True

has_link = re.search(r"https://(drive|docs)\.google\.com/", last_text)
if made_media and not has_link:
    if data.get("stop_hook_active"):
        print(json.dumps({"systemMessage": "Aviso: se generó contenido y no quedó enlace de Google Drive. Revísalo antes de compartirlo."}, ensure_ascii=False))
    else:
        print(json.dumps({"decision": "block", "reason": (
            "Regla de Alta Vida: generaste un video o imagen en este turno y tu respuesta no trae enlace de Google Drive. "
            "Súbelo a la carpeta 'Alta Vida – Contenido diario', comprueba que descarga y da el enlace a Jaime. "
            "Si no puedes subirlo, dilo claramente.")}, ensure_ascii=False))
sys.exit(0)
