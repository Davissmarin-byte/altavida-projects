import os
# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, NextPageTemplate, PageBreak, KeepTogether, ListFlowable, ListItem
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

FDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "static")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "propuesta-asistente-ventas.pdf")

# ---- Brand palette ----
DARK = colors.Color(28/255, 21/255, 16/255)
GOLD = colors.Color(201/255, 169/255, 110/255)
GOLD_DIM = colors.Color(150/255, 126/255, 82/255)
CREAM = colors.Color(253/255, 252/255, 248/255)
CREAM2 = colors.Color(245/255, 239/255, 230/255)
INK = colors.Color(35/255, 30/255, 25/255)
LINE = colors.Color(214/255, 200/255, 176/255)

# ---- Fonts ----
pdfmetrics.registerFont(TTFont("CG-SemiBold", f"{FDIR}/CormorantGaramond-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("CG-Medium", f"{FDIR}/CormorantGaramond-Medium.ttf"))
pdfmetrics.registerFont(TTFont("CG-Italic", f"{FDIR}/CormorantGaramond-Italic.ttf"))
pdfmetrics.registerFont(TTFont("CG-Light", f"{FDIR}/CormorantGaramond-Light.ttf"))
pdfmetrics.registerFont(TTFont("Mont-Light", f"{FDIR}/Montserrat-Light.ttf"))
pdfmetrics.registerFont(TTFont("Mont-Regular", f"{FDIR}/Montserrat-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Mont-Medium", f"{FDIR}/Montserrat-Medium.ttf"))
pdfmetrics.registerFont(TTFont("Mont-SemiBold", f"{FDIR}/Montserrat-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("Mont-Bold", f"{FDIR}/Montserrat-Bold.ttf"))

PAGE_W, PAGE_H = letter
MARGIN = 22 * mm

# ---- Paragraph styles ----
styles = {
    "h1": ParagraphStyle("h1", fontName="CG-SemiBold", fontSize=25, leading=29, textColor=DARK, spaceAfter=4),
    "h1sub": ParagraphStyle("h1sub", fontName="Mont-Medium", fontSize=10.5, leading=14, textColor=GOLD_DIM, spaceAfter=14, tracking=1),
    "h2": ParagraphStyle("h2", fontName="CG-SemiBold", fontSize=17, leading=20, textColor=DARK, spaceBefore=2, spaceAfter=8),
    "label": ParagraphStyle("label", fontName="Mont-SemiBold", fontSize=8.6, leading=12, textColor=GOLD_DIM, spaceAfter=6),
    "body": ParagraphStyle("body", fontName="Mont-Light", fontSize=9.6, leading=14.5, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6),
    "bodytight": ParagraphStyle("bodytight", fontName="Mont-Light", fontSize=9.6, leading=14.5, textColor=INK, alignment=TA_LEFT, spaceAfter=4),
    "bullet": ParagraphStyle("bullet", fontName="Mont-Light", fontSize=9.6, leading=14.5, textColor=INK, alignment=TA_LEFT, spaceAfter=5, leftIndent=0),
    "quote": ParagraphStyle("quote", fontName="CG-Italic", fontSize=13, leading=18, textColor=GOLD_DIM, alignment=TA_LEFT, spaceAfter=10),
    "tcell": ParagraphStyle("tcell", fontName="Mont-Regular", fontSize=8.6, leading=12, textColor=INK),
    "tcellB": ParagraphStyle("tcellB", fontName="Mont-SemiBold", fontSize=8.6, leading=12, textColor=DARK),
    "thead": ParagraphStyle("thead", fontName="Mont-SemiBold", fontSize=8.4, leading=11, textColor=CREAM),
    "footer": ParagraphStyle("footer", fontName="Mont-Regular", fontSize=7.6, leading=10, textColor=GOLD_DIM),
    "small": ParagraphStyle("small", fontName="Mont-Light", fontSize=8.6, leading=13, textColor=INK, alignment=TA_LEFT),
}

def tracked(s, n=1):
    return (" " * 0).join(list(s)) if n else s

def sp(s):
    return (" ").join(list(s))

# ================= COVER PAGE =================
def draw_cover(c, doc):
    c.saveState()
    c.setFillColor(DARK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # soft gold corner rules
    c.setStrokeColor(GOLD_DIM)
    c.setLineWidth(0.6)
    m = 16*mm
    c.line(m, PAGE_H-m, m+22*mm, PAGE_H-m)
    c.line(m, PAGE_H-m, m, PAGE_H-m-22*mm)
    c.line(PAGE_W-m, m, PAGE_W-m-22*mm, m)
    c.line(PAGE_W-m, m, PAGE_W-m, m+22*mm)

    cx = PAGE_W/2
    # diamond
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.1)
    dsize = 3.6*mm
    dy = PAGE_H - 62*mm
    c.line(cx-dsize, dy, cx, dy+dsize)
    c.line(cx, dy+dsize, cx+dsize, dy)
    c.line(cx+dsize, dy, cx, dy-dsize)
    c.line(cx, dy-dsize, cx-dsize, dy)

    c.setFillColor(CREAM)
    c.setFont("CG-SemiBold", 30)
    c.drawCentredString(cx, PAGE_H-78*mm, "A L T A   V I D A")
    c.setFont("Mont-Regular", 9.5)
    c.setFillColor(GOLD)
    c.drawCentredString(cx, PAGE_H-84*mm, "I N M U E B L E S")

    c.setStrokeColor(GOLD_DIM)
    c.setLineWidth(0.5)
    c.line(cx-16*mm, PAGE_H-90*mm, cx+16*mm, PAGE_H-90*mm)

    c.setFont("Mont-SemiBold", 10)
    c.setFillColor(GOLD)
    c.drawCentredString(cx, PAGE_H-104*mm, "P R O P U E S T A   D E   C O N T R A T A C I Ó N")

    c.setFont("CG-SemiBold", 40)
    c.setFillColor(CREAM)
    c.drawCentredString(cx, PAGE_H-122*mm, "Asistente de Ventas")
    c.setFont("CG-Italic", 24)
    c.setFillColor(GOLD)
    c.drawCentredString(cx, PAGE_H-133*mm, "Perfil, compensación y plan de crecimiento")

    c.setFont("Mont-Light", 9)
    c.setFillColor(CREAM2)
    c.drawCentredString(cx, PAGE_H-176*mm, "Documento interno  ·  Preparado para David Marín  ·  ALTA VIDA Inmuebles")
    c.setFont("Mont-Light", 9)
    c.drawCentredString(cx, PAGE_H-182*mm, "Cancún, Quintana Roo · Julio 2026")
    c.restoreState()

# ================= INNER PAGES (header/footer) =================
PAGE_TITLE = "PROPUESTA DE CONTRATACIÓN · ASISTENTE DE VENTAS"

def draw_inner(c, doc):
    c.saveState()
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # header rule
    c.setStrokeColor(GOLD_DIM)
    c.setLineWidth(0.6)
    c.line(MARGIN, PAGE_H-16*mm, PAGE_W-MARGIN, PAGE_H-16*mm)
    c.setFont("Mont-SemiBold", 7.6)
    c.setFillColor(GOLD_DIM)
    c.drawString(MARGIN, PAGE_H-13.5*mm, "ALTA VIDA INMUEBLES")
    c.drawRightString(PAGE_W-MARGIN, PAGE_H-13.5*mm, PAGE_TITLE)
    # footer
    c.line(MARGIN, 14*mm, PAGE_W-MARGIN, 14*mm)
    c.setFont("Mont-Regular", 7.6)
    c.drawString(MARGIN, 10.5*mm, "Cancún, Quintana Roo · México")
    c.drawRightString(PAGE_W-MARGIN, 10.5*mm, f"{doc.page - 1}")
    c.restoreState()

doc = BaseDocTemplate(OUT, pagesize=letter,
                       leftMargin=MARGIN, rightMargin=MARGIN,
                       topMargin=24*mm, bottomMargin=20*mm)

frame_cover = Frame(0, 0, PAGE_W, PAGE_H, id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
frame_inner = Frame(MARGIN, 18*mm, PAGE_W-2*MARGIN, PAGE_H-24*mm-18*mm, id="inner")

doc.addPageTemplates([
    PageTemplate(id="Cover", frames=[frame_cover], onPage=draw_cover),
    PageTemplate(id="Inner", frames=[frame_inner], onPage=draw_inner),
])

def hr(color=LINE, thickness=0.6, space_before=4, space_after=10):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceBefore=space_before, spaceAfter=space_after)

def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(it, styles["bullet"]), bulletColor=GOLD, value="•") for it in items],
        bulletType="bullet", start="•", leftIndent=12, bulletFontSize=9, spaceBefore=1, spaceAfter=4,
    )

from reportlab.platypus import Spacer as _Spacer

story = [_Spacer(1, 1)]
story.append(NextPageTemplate("Inner"))
story.append(PageBreak())

# ================= SECTION 1: PERFIL DEL PUESTO =================
story.append(Paragraph("01 · Perfil del puesto", styles["h1"]))
story.append(Paragraph("ASISTENTE DE VENTAS INMOBILIARIO", styles["h1sub"]))
story.append(hr())

story.append(Paragraph(
    "ALTA VIDA Inmuebles busca incorporar a una persona joven, con un nivel de energía muy alto y "
    "auténtica actitud de aprendizaje, para acompañar el proceso comercial de la agencia: atención a "
    "prospectos, seguimiento en CRM, coordinación de citas y soporte directo al cierre de operaciones. "
    "No se busca experiencia previa como requisito — se busca potencial, disciplina y hambre de crecer.",
    styles["body"]))

story.append(Paragraph("PERFIL IDEAL", styles["label"]))
story.append(bullets([
    "Edad: 19 a 27 años (rango preferente).",
    "Energía y actitud por encima de experiencia: proactiva, positiva, con ganas genuinas de aprender.",
    "Enfoque a resultados: cómoda con metas, seguimiento de indicadores y retroalimentación constante.",
    "Facilidad de palabra y trato cercano; capacidad de generar confianza rápidamente con prospectos.",
    "Organización, disciplina y orden en el manejo de agenda, CRM y reportes.",
    "Apertura real a la capacitación constante y adaptación a la tecnología (CRM, IA y herramientas digitales que ALTA VIDA está implementando).",
    "Interés genuino por aprender de negociación, inversión inmobiliaria, finanzas personales y escalamiento profesional.",
    "Transporte propio: deseable, no excluyente.",
]))

story.append(Paragraph("PRINCIPALES RESPONSABILIDADES", styles["label"]))
story.append(bullets([
    "Atención y calificación de prospectos por WhatsApp, teléfono y redes sociales.",
    "Registro y actualización disciplinada de leads en el CRM (Kommo).",
    "Agendamiento y confirmación de citas / visitas a desarrollos.",
    "Seguimiento puntual a la cartera de prospectos en cada etapa del embudo.",
    "Apoyo en la elaboración de cotizaciones, fichas técnicas y material de apoyo para cierre.",
    "Reporte semanal de actividad y resultados al responsable comercial.",
]))

story.append(PageBreak())

# ================= SECTION 2: CONDICIONES LABORALES =================
story.append(Paragraph("02 · Condiciones laborales", styles["h1"]))
story.append(Paragraph("HORARIO, MODALIDAD Y PERIODO DE EVALUACIÓN", styles["h1sub"]))
story.append(hr())

story.append(Paragraph("HORARIO RECOMENDADO", styles["label"]))
story.append(Paragraph(
    "Lunes a viernes de 9:00 a 18:00 h, sábados de 10:00 a 14:00 h (medio día). Es el estándar del "
    "sector inmobiliario en Cancún, que exige disponibilidad los fines de semana por la naturaleza de las "
    "visitas y cierres. Se recomienda además una ventana de atención flexible por WhatsApp en horario "
    "extendido razonable, para no perder prospectos calientes fuera de oficina.",
    styles["body"]))

story.append(Paragraph("MODALIDAD Y PERIODO DE EVALUACIÓN", styles["label"]))
story.append(Paragraph(
    "Presencial, en oficina. Ventana de evaluación de 15 a 20 días, suficiente para observar actitud, "
    "energía, puntualidad y disciplina en un puesto de asistente — no se necesita un ciclo de venta "
    "completo (que en proyectos desde $2.5 MDP es naturalmente largo) para ver si el perfil es el correcto.",
    styles["body"]))

story.append(Table(
    [[Paragraph("Checkpoint", styles["thead"]), Paragraph("Día", styles["thead"]), Paragraph("Qué se evalúa", styles["thead"])],
     [Paragraph("Primer corte", styles["tcell"]), Paragraph("Día 7–8", styles["tcellB"]), Paragraph("Actitud, puntualidad, disposición a aprender, manejo básico del CRM.", styles["tcell"])],
     [Paragraph("Decisión", styles["tcell"]), Paragraph("Día 15–20", styles["tcellB"]), Paragraph("Curva de aprendizaje, disciplina de seguimiento, primeras citas generadas → formalización.", styles["tcell"])],
     ],
    colWidths=[28*mm, 20*mm, None],
    style=TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK),
        ("BACKGROUND", (0,1), (-1,-1), CREAM2),
        ("GRID", (0,0), (-1,-1), 0.4, LINE),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ])
))

story.append(Spacer(1, 10))
story.append(Paragraph("MARCO LEGAL (por qué 15–20 días y no 30–60)", styles["label"]))
story.append(Paragraph(
    "El Art. 39-A de la Ley Federal del Trabajo topa el periodo de prueba en <b>30 días</b> para puestos "
    "operativos (los 180 días aplican solo a puestos directivos, gerenciales o técnico-especializados, "
    "no a un asistente de ventas). Evaluar y decidir en 15–20 días, en lugar de estirar hasta 30 o más, "
    "deja margen dentro del tope legal y evita operar en una zona ambigua de \"prueba extendida\" que la "
    "ley no reconoce para este puesto.",
    styles["body"]))

story.append(PageBreak())

# ================= SECTION 3: COMPENSACIÓN =================
story.append(Paragraph("03 · Esquema de compensación", styles["h1"]))
story.append(Paragraph("BENCHMARK DE MERCADO Y PROPUESTA ALTA VIDA", styles["h1sub"]))
story.append(hr())

story.append(Paragraph("REFERENCIA DE MERCADO (México / Cancún, 2026)", styles["label"]))
story.append(Table(
    [[Paragraph("Perfil", styles["thead"]), Paragraph("Rango mensual de mercado", styles["thead"])],
     [Paragraph("Asistente / auxiliar de ventas (cualquier sector)", styles["tcell"]), Paragraph("$8,000 – $10,700 MXN", styles["tcellB"])],
     [Paragraph("Ejecutivo de ventas junior, sector inmobiliario", styles["tcell"]), Paragraph("$8,000 – $15,000 MXN base + comisiones sin tope", styles["tcellB"])],
     [Paragraph("Agente / asesor inmobiliario (promedio nacional)", styles["tcell"]), Paragraph("~$13,700 MXN/mes (con comisión)", styles["tcellB"])],
     ],
    colWidths=[None, 62*mm],
    style=TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK),
        ("BACKGROUND", (0,1), (-1,-1), CREAM2),
        ("GRID", (0,0), (-1,-1), 0.4, LINE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ])
))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Fuentes: OCC Mundial, Computrabajo México, Indeed México y Glassdoor México (consulta julio 2026). "
    "La mayoría de las vacantes juniors en el sector no ofrecen sueldo base garantizado competitivo — "
    "dependen casi enteramente de comisión, lo que expulsa talento joven sin colchón financiero antes de "
    "que pueda desarrollar su curva de aprendizaje.",
    styles["small"]))

story.append(Spacer(1, 8))
story.append(Paragraph("NOTA LEGAL — POR QUÉ NO SE BAJA EL SUELDO BASE", styles["label"]))
story.append(Paragraph(
    "El salario mínimo general subió el 1 de enero de 2026 a <b>$315.04/día = $9,582.47 MXN/mes</b> "
    "(incremento del 13%, publicado en el DOF / CONASAMI). Cancún no está en la Zona Libre de la Frontera "
    "Norte, así que aplica este mínimo general. Un sueldo de $8,000 u $9,000 queda por debajo del piso "
    "legal — el periodo de prueba no exime del salario mínimo, son dos figuras distintas en la ley. Por "
    "eso el sueldo base se mantiene en $10,000 (con colchón de ~$417 sobre el mínimo) y la palanca de "
    "motivación se mueve al bono, que sí es enteramente flexible.",
    styles["body"]))

story.append(Spacer(1, 8))
story.append(Paragraph("PROPUESTA ALTA VIDA — ETAPA 1: EVALUACIÓN (Día 1 a 15/20)", styles["label"]))
story.append(Table(
    [[Paragraph("Concepto", styles["thead"]), Paragraph("Monto mensual", styles["thead"])],
     [Paragraph("Sueldo base", styles["tcell"]), Paragraph("$10,000 MXN", styles["tcellB"])],
     [Paragraph("Bono de arranque (asistencia, puntualidad, disciplina básica de CRM)", styles["tcell"]), Paragraph("$500 – $1,000 MXN", styles["tcellB"])],
     [Paragraph("Total potencial", styles["tcellB"]), Paragraph("$10,500 – $11,000 MXN", styles["tcellB"])],
     ],
    colWidths=[None, 45*mm],
    style=TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK),
        ("BACKGROUND", (0,1), (-1,-2), CREAM2),
        ("BACKGROUND", (0,-1), (-1,-1), GOLD),
        ("GRID", (0,0), (-1,-1), 0.4, LINE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ])
))

story.append(Spacer(1, 6))
story.append(Paragraph(
    "El bono de arranque se mantiene deliberadamente chico frente al de la etapa formal: es una prueba de "
    "disciplina básica (asistencia, puntualidad, registro de leads el mismo día, primeras citas agendadas), "
    "no de resultados de venta. El salto real de bono llega al formalizar — ahí es donde se siente que "
    "vale la pena quedarse.",
    styles["body"]))

story.append(Paragraph("PROPUESTA ALTA VIDA — ETAPA 2: FORMALIZACIÓN (a partir de día 15/21)", styles["label"]))
story.append(Paragraph(
    "Al comprobar el perfil, se recomienda <b>mantener la estructura de $10,000 base + $2,000 de bono de "
    "productividad</b>, en lugar de subir el fijo a $12,000. Razón: preserva el vínculo directo entre pago y "
    "desempeño, mantiene la motivación activa después de la evaluación, y evita el riesgo — ya vivido "
    "por ALTA VIDA en una contratación anterior — de formalizar un sueldo fijo alto antes de confirmar que "
    "la persona realmente está para el puesto y no solo de paso.",
    styles["body"]))
story.append(bullets([
    "Contrato formal con prestaciones de ley (IMSS, aguinaldo, vacaciones).",
    "Se mantiene: $10,000 base + $2,000 bono de productividad (techo $12,000/mes).",
    "Al asignarle atención directa a clientes de proyectos desde $2.5 MDP, se agregan bonos adicionales por volumen y comisión por cierre de operación, a definir % según política comercial vigente.",
    "Revisión de desempeño y compensación a los 90 días, con posibilidad de ajuste de base conforme a resultados sostenidos.",
]))
story.append(PageBreak())

# ================= SECTION 4: PLAN DE CRECIMIENTO =================
story.append(Paragraph("04 · Plan de desarrollo y crecimiento", styles["h1"]))
story.append(Paragraph("CAPACITACIÓN CONTINUA COMO PARTE DE LA OFERTA", styles["h1sub"]))
story.append(hr())

story.append(Paragraph(
    "Más allá del sueldo, la propuesta de valor para este perfil es el desarrollo: alguien de 19 a 27 años que "
    "busca crecer se queda por la curva de aprendizaje, no solo por el pago. ALTA VIDA ofrece una ruta de "
    "formación constante en:",
    styles["body"]))
story.append(bullets([
    "Negociación y cierre de ventas de alto valor.",
    "Fundamentos de inversión inmobiliaria y análisis de plusvalía.",
    "Finanzas personales y escalamiento financiero.",
    "Uso de CRM (Kommo), IA y herramientas digitales aplicadas a ventas.",
    "Comunicación, imagen profesional y crecimiento de estatus dentro del sector.",
]))
story.append(Paragraph(
    "Se recomienda comunicar esta ruta desde la entrevista y reforzarla en cada checkpoint del periodo de "
    "evaluación: no es solo un empleo de asistente, es la puerta de entrada a una carrera comercial en bienes "
    "raíces de lujo.",
    styles["body"]))

story.append(Spacer(1, 8))
story.append(Paragraph("LECCIÓN APLICADA", styles["label"]))
story.append(Paragraph(
    "Una experiencia previa de contratación para un puesto de mayor rango no prosperó porque el perfil no "
    "correspondía al puesto y la energía no era la esperada para el rol. Este proceso corrige el enfoque: "
    "puesto de entrada, edad objetivo más joven, expectativas explícitas desde el día 1 y evaluación real "
    "antes de formalizar cualquier compromiso.",
    styles["body"]))

story.append(PageBreak())

# ================= SECTION 5: PRÓXIMOS PASOS =================
story.append(Paragraph("05 · Próximos pasos", styles["h1"]))
story.append(Paragraph("PROCESO DE SELECCIÓN", styles["h1sub"]))
story.append(hr())
story.append(bullets([
    "Difusión de la vacante: WhatsApp directo a candidatas/os identificados + publicación en redes sociales (arte adjunto) + bolsas de trabajo (OCC, Computrabajo, Indeed).",
    "Primer contacto y filtro por WhatsApp: energía, disponibilidad de horario, interés real en aprender.",
    "Entrevista presencial breve en oficina.",
    "Inicio de periodo de evaluación (15–20 días) con corte intermedio en día 7–8 y decisión en día 15–20.",
    "Formalización de contrato al confirmar el perfil.",
]))
story.append(Spacer(1, 10))
story.append(Paragraph(
    "Este documento acompaña el mensaje de WhatsApp para candidatas y el arte para redes sociales, "
    "preparados en conjunto como parte de esta misma propuesta.",
    styles["quote"]))

doc.build(story)
print("PDF built:", OUT)
