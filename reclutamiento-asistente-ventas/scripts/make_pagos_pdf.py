# -*- coding: utf-8 -*-
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY

FDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "static")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "esquema-pagos-asistente-ventas.pdf")

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
pdfmetrics.registerFont(TTFont("CG-Italic", f"{FDIR}/CormorantGaramond-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Mont-Light", f"{FDIR}/Montserrat-Light.ttf"))
pdfmetrics.registerFont(TTFont("Mont-Regular", f"{FDIR}/Montserrat-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Mont-Medium", f"{FDIR}/Montserrat-Medium.ttf"))
pdfmetrics.registerFont(TTFont("Mont-SemiBold", f"{FDIR}/Montserrat-SemiBold.ttf"))

PAGE_W, PAGE_H = letter
MARGIN = 20 * mm

styles = {
    "h1": ParagraphStyle("h1", fontName="CG-SemiBold", fontSize=22, leading=26, textColor=DARK, spaceAfter=2),
    "h1sub": ParagraphStyle("h1sub", fontName="Mont-Medium", fontSize=10, leading=14, textColor=GOLD_DIM, spaceAfter=10),
    "h2": ParagraphStyle("h2", fontName="CG-SemiBold", fontSize=15, leading=18, textColor=DARK, spaceBefore=4, spaceAfter=4),
    "label": ParagraphStyle("label", fontName="Mont-SemiBold", fontSize=8.4, leading=11, textColor=GOLD_DIM, spaceAfter=4),
    "body": ParagraphStyle("body", fontName="Mont-Light", fontSize=9.3, leading=13.5, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6),
    "bullet": ParagraphStyle("bullet", fontName="Mont-Light", fontSize=9.3, leading=13.5, textColor=INK, alignment=TA_LEFT, spaceAfter=3),
    "tcell": ParagraphStyle("tcell", fontName="Mont-Regular", fontSize=8.6, leading=12, textColor=INK),
    "tcellB": ParagraphStyle("tcellB", fontName="Mont-SemiBold", fontSize=8.6, leading=12, textColor=DARK),
    "thead": ParagraphStyle("thead", fontName="Mont-SemiBold", fontSize=8.2, leading=11, textColor=CREAM),
    "quote": ParagraphStyle("quote", fontName="CG-Italic", fontSize=11.5, leading=15.5, textColor=GOLD_DIM, alignment=TA_LEFT, spaceAfter=6),
    "small": ParagraphStyle("small", fontName="Mont-Light", fontSize=7.8, leading=11.5, textColor=INK, alignment=TA_LEFT),
}

def hr(color=LINE, thickness=0.6, space_before=2, space_after=8):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceBefore=space_before, spaceAfter=space_after)

def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(it, styles["bullet"]), bulletColor=GOLD, value="•") for it in items],
        bulletType="bullet", start="•", leftIndent=12, bulletFontSize=8.5, spaceBefore=1, spaceAfter=4,
    )

def comp_table(rows):
    data = [[Paragraph("Etapa", styles["thead"]), Paragraph("Sueldo base", styles["thead"]),
             Paragraph("Bono", styles["thead"]), Paragraph("Total potencial", styles["thead"])]]
    for r in rows:
        data.append([Paragraph(r[0], styles["tcell"]), Paragraph(r[1], styles["tcellB"]),
                     Paragraph(r[2], styles["tcellB"]), Paragraph(r[3], styles["tcellB"])])
    t = Table(data, colWidths=[46*mm, 30*mm, 40*mm, None], style=TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK),
        ("BACKGROUND", (0,1), (-1,-1), CREAM2),
        ("GRID", (0,0), (-1,-1), 0.4, LINE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 5.5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5.5),
        ("LEFTPADDING", (0,0), (-1,-1), 7),
    ]))
    return t

def draw_page(c, doc):
    c.saveState()
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # header
    cx = MARGIN
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.1)
    dsize = 2.6*mm
    dcx, dcy = MARGIN + dsize, PAGE_H - 18*mm
    c.line(dcx-dsize, dcy, dcx, dcy+dsize)
    c.line(dcx, dcy+dsize, dcx+dsize, dcy)
    c.line(dcx+dsize, dcy, dcx, dcy-dsize)
    c.line(dcx, dcy-dsize, dcx-dsize, dcy)
    c.setFont("CG-SemiBold", 15)
    c.setFillColor(DARK)
    c.drawString(dcx + 7*mm, dcy - 2*mm, "ALTA VIDA")
    c.setFont("Mont-Regular", 7.5)
    c.setFillColor(GOLD_DIM)
    c.drawString(dcx + 7*mm, dcy - 6.5*mm, "INMUEBLES")
    c.setFont("Mont-Regular", 7.5)
    c.setFillColor(GOLD_DIM)
    c.drawRightString(PAGE_W - MARGIN, dcy - 2*mm, "ESQUEMA DE PAGOS · ASISTENTE DE VENTAS")
    c.setStrokeColor(GOLD_DIM)
    c.setLineWidth(0.6)
    c.line(MARGIN, PAGE_H - 24*mm, PAGE_W - MARGIN, PAGE_H - 24*mm)
    # footer
    c.line(MARGIN, 14*mm, PAGE_W - MARGIN, 14*mm)
    c.setFont("Mont-Regular", 7.6)
    c.setFillColor(GOLD_DIM)
    c.drawString(MARGIN, 10.5*mm, "ALTA VIDA Inmuebles · Cancún, Quintana Roo · WhatsApp 998 489 4142")
    c.drawRightString(PAGE_W - MARGIN, 10.5*mm, f"{doc.page}")
    c.restoreState()

doc = BaseDocTemplate(OUT, pagesize=letter,
                       leftMargin=MARGIN, rightMargin=MARGIN,
                       topMargin=27*mm, bottomMargin=18*mm)
frame = Frame(MARGIN, 18*mm, PAGE_W - 2*MARGIN, PAGE_H - 27*mm - 18*mm, id="main")
doc.addPageTemplates([PageTemplate(id="Main", frames=[frame], onPage=draw_page)])

story = []
story.append(Paragraph("Esquema de Pagos", styles["h1"]))
story.append(Paragraph("ASISTENTE DE VENTAS · DOS RUTAS SEGÚN DISPONIBILIDAD", styles["h1sub"]))
story.append(hr())

story.append(Paragraph(
    "Dos formas de incorporarse al puesto, según el tiempo disponible de la persona candidata. Ambas "
    "rutas convergen en el mismo esquema al formalizar el contrato.",
    styles["body"]))

story.append(Spacer(1, 6))
story.append(Paragraph("OPCIÓN A · TIEMPO COMPLETO", styles["h2"]))
story.append(Paragraph(
    "Horario: lunes a viernes 9:00–18:00 h, sábados 10:00–14:00 h, desde el día 1.",
    styles["small"]))
story.append(Spacer(1, 4))
story.append(comp_table([
    ("Evaluación (día 1–15/20)", "$10,000", "$500 – $1,000<br/>(bono de arranque)", "$10,500 – $11,000"),
    ("Formalización (día 15/21+)", "$10,000", "$2,000<br/>(productividad)", "$12,000"),
]))

story.append(Spacer(1, 10))
story.append(Paragraph("OPCIÓN B · MEDIO TIEMPO", styles["h2"]))
story.append(Paragraph(
    "Horario: 4 horas de oficina (mañana o tarde, con espacio para comer) + tarea de campo breve y "
    "verificable el resto del día (visitas, llamadas de seguimiento, registro de aprendizajes). Al "
    "formalizar, se pasa a jornada completa y al esquema de la Opción A.",
    styles["small"]))
story.append(Spacer(1, 4))
story.append(comp_table([
    ("Evaluación (día 1–15/20)", "$5,000 – $5,500", "$300 – $500<br/>(bono de arranque)", "$5,300 – $6,000"),
    ("Formalización → tiempo completo", "$10,000", "$2,000<br/>(productividad)", "$12,000"),
]))

story.append(Spacer(1, 12))
story.append(Paragraph("EN AMBAS OPCIONES", styles["label"]))
story.append(bullets([
    "Bono sorpresa si participa en cerrar una renta o venta durante la etapa de evaluación.",
    "Al confirmar el perfil y asumir atención directa a clientes de proyectos desde $2.5 MDP, se agregan bonos por volumen y comisión por cierre de operación.",
    "Contrato formal con prestaciones de ley (IMSS, aguinaldo, vacaciones) al formalizar.",
    "Revisión de desempeño y compensación a los 90 días de formalizado.",
]))

story.append(Spacer(1, 8))
story.append(Paragraph(
    "El sueldo base no baja de estos montos porque, desde el 1 de enero de 2026, el salario mínimo "
    "general en México es de $9,582.47 MXN/mes ($315.04/día, DOF/CONASAMI) — proporcional a $4,791.24 "
    "para una jornada de 4 horas. El periodo de evaluación se fija en 15–20 días, dentro del tope de 30 "
    "días que marca el Art. 39-A de la Ley Federal del Trabajo para puestos operativos.",
    styles["quote"]))

doc.build(story)
print("PDF built:", OUT)
