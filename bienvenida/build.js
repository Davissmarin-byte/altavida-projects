// Genera las bienvenidas verticales (historia 9:16 y feed 4:5). Uso: node build.js [carpeta_salida_feed]
const path = require("path");
const pptxgen = require("pptxgenjs");
const SKILL = process.env.PPTX_SKILL_DIR || "/root/.claude/skills/synced/800045a2-c963-469a-bd59-3509d6447a9f_a92b681b-8ae2-459e-b230-2a60c022f0f3/pptx";
const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js"));
const A = (f) => path.join(__dirname, "assets", f);

const THEME = {
  name: "Alta Vida Inmuebles", headFontFace: "Cambria", bodyFontFace: "Calibri",
  colors: { dk1: "000000", lt1: "FFFFFF", dk2: "17171C", lt2: "D9D9DC", accent1: "C99A2E", accent2: "F3D774", accent3: "B8541C", accent4: "9A9AA0", accent5: "E6B94A", accent6: "FF5500", hlink: "F3D774", folHlink: "9A9AA0" },
};
// 7.5 in de ancho = 1080 px a 144 dpi. Historia 1080x1920 (zona segura ~250 px arriba y abajo); feed 1080x1350.
const FORMATS = {
  story: { h: 13.333, logo: { y: 1.85, w: 1.15 }, label: 3.05, phrase: { y: 3.5, h: 1.7, size: 38 }, name: 5.3, panel: { y: 5.95, h: 6.0, img: "equipo_story.jpg" }, cap: 10.5, handle: 11.3 },
  feed:  { h: 9.375, logo: { y: 0.45, w: 0.9 }, label: 1.55, phrase: { y: 1.95, h: 1.4, size: 34 }, name: 3.35, panel: { y: 3.9, h: 5.23, img: "equipo_feed.jpg" }, cap: 7.95, handle: 8.8 },
};

async function build(name, fmt, out) {
  const F = FORMATS[fmt];
  const pres = new pptxgen();
  pres.defineLayout({ name: "VERT", width: 7.5, height: F.h });
  pres.layout = "VERT";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  pres.title = `Bienvenida a Alta Vida Inmuebles – ${name}`;
  pres.author = "Alta Vida Inmuebles";
  pres.company = "Alta Vida Inmuebles";
  const C = pres.SchemeColor;
  pres.defineSlideMaster({ title: "BIENVENIDA", background: { color: "000000" }, objects: [] });
  const txt = (s, t, o) => s.addText(t, Object.assign({ isTextBox: true, margin: 0, align: "center" }, o));
  const s = pres.addSlide({ masterName: "BIENVENIDA" });
  s.addImage({ path: A(F.panel.img), x: 0, y: F.panel.y, w: 7.5, h: F.panel.h, objectName: "Jaime Marin y Kenia Acosta", altText: "Jaime Marin y Kenia Acosta, Alta Vida Inmuebles" });
  const lh = F.logo.w * 0.856;
  s.addImage({ path: A("logo_full.png"), x: (7.5 - F.logo.w) / 2, y: F.logo.y, w: F.logo.w, h: lh, objectName: "Logo Alta Vida Inmuebles", altText: "Logotipo de Alta Vida Inmuebles" });
  txt(s, "BIENVENIDA  ·  EQUIPO DE VENTAS", { x: 0.5, y: F.label, w: 6.5, h: 0.35, fontSize: 13, bold: true, color: C.accent1, charSpacing: 4, objectName: "Etiqueta" });
  txt(s, [{ text: "Hoy empieza tu viaje", options: { breakLine: true } }, { text: "extraordinario." }], { x: 0.5, y: F.phrase.y, w: 6.5, h: F.phrase.h, fontSize: F.phrase.size, bold: true, color: C.background1, valign: "top", fontFace: "Cambria", objectName: "Frase" });
  txt(s, name, { x: 0.5, y: F.name, w: 6.5, h: 0.6, fontSize: 28, color: C.accent2, fontFace: "Cambria", objectName: "Nombre" });
  txt(s, [{ text: "Jaime Marin", options: { fontSize: 16, bold: true, color: C.background1, breakLine: true } }, { text: "SH y Líder de Ventas", options: { fontSize: 14, color: C.accent2 } }], { x: 1.15, y: F.cap, w: 2.5, h: 0.7, valign: "top", objectName: "Jaime Marin" });
  txt(s, [{ text: "Kenia Acosta", options: { fontSize: 16, bold: true, color: C.background1, breakLine: true } }, { text: "Socia y Vendedora", options: { fontSize: 14, color: C.accent2 } }], { x: 3.85, y: F.cap, w: 2.5, h: 0.7, valign: "top", objectName: "Kenia Acosta" });
  txt(s, "@altavidainmuebles", { x: 0.5, y: F.handle, w: 6.5, h: 0.35, fontSize: 14, color: C.accent4, objectName: "Cuenta" });
  s.addNotes(`Bienvenida a ${name}: "Hoy empieza tu viaje extraordinario."`);
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("OK", out);
}

(async () => {
  const feedDir = process.argv[2] || __dirname;
  for (const [name, slug] of [["Juli Pastrana", "Juli_Pastrana"], ["Gaby Luna", "Gaby_Luna"]]) {
    await build(name, "story", path.join(__dirname, `Bienvenida_${slug}_historia.pptx`));
    await build(name, "feed", path.join(feedDir, `Bienvenida_${slug}_feed.pptx`));
  }
})();
