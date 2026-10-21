"""Escribe título, descripción SEO con capítulos y etiquetas para YouTube."""
import json, sys

cap = json.load(open(sys.argv[1]))
out = sys.argv[2]

nombres = {0: "El lago", 1: "Presentación", 2: "La llegada", 5: "Sala a doble altura", 7: "Comedor y cocina",
           9: "Terraza, jardín y alberca infinity", 12: "Acceso al lago", 13: "Planta alta",
           14: "Recámara principal", 16: "Recámaras", 19: "Residencial Lagos del Sol", 24: "Precio y visita privada"}


def mmss(s):
    return f"{s // 60}:{s % 60:02d}"


lineas = [(0 if i == 0 else cap[i][0], n) for i, n in nombres.items()]
if len(sys.argv) > 3:  # versión con vuelo aéreo insertado tras la presentación
    lineas.append((int(sys.argv[3]), "Vuelo sobre Lagos del Sol (recreación IA)"))
capitulos = "\n".join(f"{mmss(t)} {n}" for t, n in sorted(lineas))

txt = f"""# YouTube · metadatos

**Título**
Casa frente al lago en Lagos del Sol, Cancún | Alberca infinity y acceso al lago | $23.9 MDP

**Descripción**

Recorrido por una residencia frente al lago en Residencial Lagos del Sol, Cancún, presentada por ALTA VIDA Inmuebles.

Alberca infinity que se funde con el lago, acceso propio al agua, sala a doble altura y 4 recámaras, cada una con vestidor y baño completo.

· Terreno: 550 m² · Construcción: 570 m²
· 4 recámaras · 4.5 baños · 4 estacionamientos
· Planta baja: acceso cubierto, sala a doble altura, comedor con vista al lago, cocina y alacena, medio baño de visitas, recámara de visitas con vestidor y baño completo, terraza techada a doble altura, jardín, alberca infinity, baño exterior, acceso al lago, cuarto de servicio con baño completo y cuarto de lavado
· Planta alta: sala de TV o family room, recámara principal con vestidor y baño completo, recámaras 2 y 3 con vestidor y baño completo, closet de blancos
· Residencial: más de 30 amenidades, 40 hectáreas de lagos, casa club, Parque del Lago, cafetería, albercas, gimnasio, SPA, canchas deportivas, ciclovía, skate park y parque de mascotas

Precio: $23,900,000 MXN

Visitas privadas con cita por WhatsApp: 998 154 6066 · 998 430 9472
Instagram: @altavidainmuebles

Capítulos
{capitulos}

Imágenes: fotografía real de la propiedad. La toma aérea del residencial es una recreación ilustrativa generada con IA. Voz en off sintética.

#LagosDelSol #CasasEnCancun #CancunRealEstate

**Etiquetas**
Lagos del Sol, casa frente al lago Cancún, casas en venta Cancún, residencial Lagos del Sol, casa con alberca infinity, bienes raíces Cancún, casas de lujo Cancún, Cancun real estate, inversión inmobiliaria Cancún, ALTA VIDA Inmuebles, casa en venta Quintana Roo, lake house Cancun

**Configuración**
Categoría: Viajes y eventos (o Personas y blogs) · No es contenido para niños · Declarar «contenido alterado o sintético»: sí (voz) · Miniatura: `youtube_miniatura.jpg`
"""
open(out, "w").write(txt)
print(capitulos)
