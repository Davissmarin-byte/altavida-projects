// Genera las bienvenidas de una sola lámina. Uso: node build.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const SKILL = process.env.PPTX_SKILL_DIR || "/root/.claude/skills/synced/800045a2-c963-469a-bd59-3509d6447a9f_a92b681b-8ae2-459e-b230-2a60c022f0f3/pptx";
const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js"));
const A = (f) => path.join(__dirname, "assets", f);

const THEME = {
  name: "Alta Vida Inmuebles", headFontFace: "Cambria", bodyFontFace: "Calibri",
  colors: { dk1: "000000", lt1: "FFFFFF", dk2: "17171C", lt2: "D9D9DC", accent1: "C99A2E", accent2: "F3D774", accent3: "B8541C", accent4: "9A9AA0", accent5: "E6B94A", accent6: "FF5500", hlink: "F3D774", folHlink: "9A9AA0" },
};

async function build(name, file) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  pres.title = `Bienvenida a Alta Vida Inmuebles – ${name}`;
  pres.author = "Alta Vida Inmuebles";
  pres.company = "Alta Vida Inmuebles";
  const C = pres.SchemeColor;
  pres.defineSlideMaster({ title: "BIENVENIDA", background: { color: "000000" }, objects: [] });
  const txt = (s, t, o) => s.addText(t, Object.assign({ isTextBox: true, margin: 0 }, o));

  const s = pres.addSlide({ masterName: "BIENVENIDA" });
  s.addImage({ path: A("equipo_jaime_kenia.jpg"), x: 6.73, y: 0, w: 6.6, h: 7.5, objectName: "Jaime Marin y Kenia Acosta", altText: "Jaime Marin y Kenia Acosta, Alta Vida Inmuebles" });
  s.addImage({ path: A("logo_full.png"), x: 0.8, y: 0.7, w: 1.2, h: 1.027, objectName: "Logo Alta Vida Inmuebles", altText: "Logotipo de Alta Vida Inmuebles" });
  txt(s, "BIENVENIDA  ·  EQUIPO DE VENTAS", { x: 0.8, y: 2.45, w: 5.6, h: 0.35, fontSize: 13, bold: true, color: C.accent1, charSpacing: 4, objectName: "Etiqueta" });
  txt(s, [{ text: "Hoy empieza tu viaje", options: { breakLine: true } }, { text: "extraordinario." }], { x: 0.8, y: 2.95, w: 6.0, h: 1.8, fontSize: 40, bold: true, color: C.background1, valign: "top", fontFace: "Cambria", objectName: "Frase" });
  txt(s, name, { x: 0.8, y: 4.95, w: 5.6, h: 0.6, fontSize: 28, color: C.accent2, fontFace: "Cambria", objectName: "Nombre" });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.8, y: 6.45, w: 1.8, h: 0.5, rectRadius: 0.08, fill: { color: C.background1 }, line: { color: C.background1, width: 0.5 }, objectName: "Insignia Inmuebles24" });
  s.addImage({ path: A("i24_logo.png"), x: 0.92, y: 6.53, w: 1.56, h: 0.372, objectName: "Logo Inmuebles24", altText: "Logotipo de Inmuebles24" });
  txt(s, [
    { text: "Jaime Marin", options: { fontSize: 16, bold: true, color: C.background1, breakLine: true } },
    { text: "SH y Líder de Ventas", options: { fontSize: 14, color: C.accent2 } },
  ], { x: 6.95, y: 5.7, w: 2.7, h: 0.7, valign: "top", objectName: "Jaime Marin" });
  txt(s, [
    { text: "Kenia Acosta", options: { fontSize: 16, bold: true, color: C.background1, breakLine: true } },
    { text: "Socia y Vendedora", options: { fontSize: 14, color: C.accent2 } },
  ], { x: 9.9, y: 5.7, w: 2.9, h: 0.7, valign: "top", objectName: "Kenia Acosta" });
  s.addNotes(`Bienvenida a ${name}: "Hoy empieza tu viaje extraordinario." Cada vuelta de la rueda te lleva más alto; aquí no subes solo.`);

  const out = path.join(__dirname, file);
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("OK", out);
}

(async () => {
  await build("Juli Pastrana", "Bienvenida_Juli_Pastrana.pptx");
  await build("Gaby Luna", "Bienvenida_Gaby_Luna.pptx");
})();
