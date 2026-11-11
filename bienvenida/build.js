// Genera las presentaciones de bienvenida. Uso: node build.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const SKILL = process.env.PPTX_SKILL_DIR || "/root/.claude/skills/synced/800045a2-c963-469a-bd59-3509d6447a9f_a92b681b-8ae2-459e-b230-2a60c022f0f3/pptx";
const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js"));
const A = (f) => path.join(__dirname, "assets", f);

const THEME = {
  name: "Alta Vida Inmuebles",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "000000", lt1: "FFFFFF", dk2: "17171C", lt2: "D9D9DC",
    accent1: "C99A2E", accent2: "F3D774", accent3: "B8541C",
    accent4: "9A9AA0", accent5: "E6B94A", accent6: "FF5500",
    hlink: "F3D774", folHlink: "9A9AA0",
  },
};

async function build(person, file) {
  const N = person.name;
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  pres.title = `Bienvenida a Alta Vida Inmuebles – ${N}`;
  pres.author = "Alta Vida Inmuebles";
  pres.company = "Alta Vida Inmuebles";
  const C = pres.SchemeColor;

  pres.defineSlideMaster({
    title: "FULL", background: { color: "000000" }, objects: [],
  });
  pres.defineSlideMaster({
    title: "CONTENIDO", background: { color: "000000" },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.4, w: 12.1, h: 0.95, fontSize: 34, bold: true, color: C.background1, align: "left", valign: "middle", margin: 0 }, text: "" } },
      { image: { path: A("logo_glyph.png"), x: 0.6, y: 6.93, w: 0.42, h: 0.286 } },
      { text: { text: "ALTA VIDA INMUEBLES", options: { x: 1.15, y: 6.93, w: 4, h: 0.3, fontSize: 10, color: C.accent4, charSpacing: 3, valign: "middle", margin: 0 } } },
    ],
    slideNumber: { x: 12.2, y: 6.93, w: 0.5, h: 0.3, color: C.accent4, fontSize: 10, align: "right" },
  });

  const card = (s, x, y, w, h, name) =>
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: C.text2 }, line: { color: C.accent1, width: 0.75, transparency: 55 }, objectName: name });
  const circle = (s, x, y, d, label, size, name) => {
    s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: C.accent1 }, line: { color: C.accent2, width: 1 }, objectName: name + " círculo" });
    s.addText(label, { x, y, w: d, h: d, align: "center", valign: "middle", fontSize: size, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: name });
  };
  const txt = (s, t, o) => s.addText(t, Object.assign({ isTextBox: true, margin: 0 }, o));

  // ---------- 1. Portada
  let s = pres.addSlide({ masterName: "FULL" });
  s.addImage({ path: A("wheel.png"), x: 6.9, y: 0.55, w: 6.0, h: 6.0, objectName: "Rueda de la fortuna", altText: "Rueda de la fortuna dorada" });
  s.addImage({ path: A("logo_full.png"), x: 0.7, y: 0.5, w: 1.5, h: 1.283, objectName: "Logo Alta Vida Inmuebles", altText: "Logotipo de Alta Vida Inmuebles" });
  txt(s, "EQUIPO DE VENTAS  ·  BIENVENIDA", { x: 0.7, y: 2.3, w: 6, h: 0.4, fontSize: 14, bold: true, color: C.accent1, charSpacing: 4, objectName: "Etiqueta" });
  txt(s, [
    { text: "Te damos la bienvenida,", options: { color: C.background1, breakLine: true } },
    { text: N, options: { color: C.accent2 } },
  ], { x: 0.7, y: 2.8, w: 6.1, h: 2.5, fontSize: 52, bold: true, valign: "top", objectName: "Título", fontFace: "Cambria" });
  txt(s, "Empieza un viaje extraordinario.", { x: 0.7, y: 5.6, w: 6, h: 0.5, fontSize: 22, color: C.background2, objectName: "Subtítulo" });
  s.addNotes(`Apertura. Léela despacio: "${N}, hoy empieza algo distinto. No es un trabajo más: es un viaje." Deja un silencio de tres segundos antes de pasar a la siguiente lámina.`);

  // ---------- 2. Foto con Jaime y Kenia
  s = pres.addSlide({ masterName: "FULL" });
  s.addImage({ path: A("jaime_kenia_corporativa.jpg"), x: 0, y: 0, w: 7.2, h: 7.5, objectName: "Jaime Marin y Kenia Acosta", altText: "Jaime Marin y la Lic. Kenia Acosta Aguilera, Alta Vida Inmuebles" });
  txt(s, "EL EQUIPO QUE TE RECIBE", { x: 7.8, y: 0.8, w: 4.9, h: 0.35, fontSize: 12, bold: true, color: C.accent1, charSpacing: 4, objectName: "Etiqueta" });
  txt(s, `Hoy ${N} se suma a un equipo extraordinario`, { x: 7.8, y: 1.25, w: 4.9, h: 2.5, fontSize: 34, bold: true, color: C.background1, valign: "top", fontFace: "Cambria", objectName: "Título" });
  txt(s, [
    { text: "Jaime Marin", options: { fontSize: 20, bold: true, color: C.background1, breakLine: true } },
    { text: "Dueño de Alta Vida Inmuebles desde 2011", options: { fontSize: 14, color: C.background2 } },
  ], { x: 7.8, y: 4.0, w: 4.9, h: 0.8, valign: "top", objectName: "Jaime" });
  txt(s, [
    { text: "Lic. Kenia Acosta Aguilera", options: { fontSize: 20, bold: true, color: C.background1, breakLine: true } },
    { text: "Experta inmobiliaria · más de 24 años en Cancún", options: { fontSize: 14, color: C.background2 } },
  ], { x: 7.8, y: 5.0, w: 4.9, h: 0.8, valign: "top", objectName: "Kenia" });
  txt(s, "Aquí nadie sube solo.", { x: 7.8, y: 6.2, w: 4.9, h: 0.5, fontSize: 22, italic: true, color: C.accent2, fontFace: "Cambria", objectName: "Frase" });
  s.addNotes("Presenta a quienes lo reciben. Jaime: dueño desde 2011. Kenia: más de 24 años de trayectoria en Cancún. El mensaje: el nuevo integrante entra a un equipo que lo acompaña.");

  // ---------- 3. Rueda de la fortuna
  s = pres.addSlide({ masterName: "CONTENIDO" });
  s.addText("Una rueda de la fortuna de emociones", { placeholder: "title" });
  s.addImage({ path: A("wheel.png"), x: 0.6, y: 1.5, w: 5.1, h: 5.1, objectName: "Rueda de la fortuna", altText: "Rueda de la fortuna dorada" });
  const rows = [
    ["Subes", "La emoción", "El primer sí de un cliente se siente como llegar a la cima."],
    ["Giras", "La adrenalina", "Ciclos de venta de 2 a 4 semanas: todo se mueve rápido."],
    ["Bajas", "El reto", "Habrá noes y citas que se caen. Se aprende y se vuelve a subir."],
    ["Disfrutas", "La vista", "Entregar una llave y ver a una familia estrenar su patrimonio."],
  ];
  rows.forEach((r, i) => {
    const y = 1.5 + i * 1.3;
    card(s, 6.2, y, 6.5, 1.1, "Tarjeta " + r[0]);
    circle(s, 6.4, y + 0.2, 0.7, String(i + 1), 20, "Número " + (i + 1));
    txt(s, [
      { text: `${r[0]} — ${r[1]}`, options: { fontSize: 20, bold: true, color: C.accent2, breakLine: true } },
      { text: r[2], options: { fontSize: 14, color: C.background1 } },
    ], { x: 1.0 + 6.2, y: y + 0.1, w: 5.4, h: 0.9, valign: "middle", objectName: "Texto " + r[0] });
  });
  s.addNotes("La metáfora: una rueda de la fortuna. Hay emoción al subir, adrenalina al girar, retos al bajar y una vista increíble desde arriba. Quien se sube con ganas, disfruta cada vuelta.");

  // ---------- 4. Saltos cuánticos
  s = pres.addSlide({ masterName: "CONTENIDO" });
  s.addText("Un viaje de saltos cuánticos", { placeholder: "title" });
  const q = [
    ["Superposición", "Hasta que respondes, cada prospecto puede ser comprador, inversionista o tu próximo referido. Tu rapidez decide cuál se hace realidad."],
    ["Entrelazamiento", "Cliente, desarrollador, notario y banco están conectados. Cuando mueves uno, avanzan todos."],
    ["Salto cuántico", "Un salto de nivel no pide años de espera. Aquí ya se han cerrado ventas de $14.5M y $17.5M."],
  ];
  q.forEach((c, i) => {
    const x = 0.6 + i * 4.1;
    card(s, x, 1.6, 3.9, 5.0, "Tarjeta " + c[0]);
    const cx = x + 1.95, cy = 2.55;
    [0, 60, 120].forEach((rot) => s.addShape(pres.shapes.OVAL, { x: cx - 0.85, y: cy - 0.3, w: 1.7, h: 0.6, rotate: rot, fill: { type: "none" }, line: { color: C.accent1, width: 1.5 }, objectName: `Órbita ${rot} ${c[0]}` }));
    s.addShape(pres.shapes.OVAL, { x: cx - 0.12, y: cy - 0.12, w: 0.24, h: 0.24, fill: { color: C.accent2 }, line: { color: C.accent2, width: 0.5 }, objectName: "Núcleo " + c[0] });
    txt(s, c[0], { x: x + 0.3, y: 3.65, w: 3.3, h: 0.5, fontSize: 24, bold: true, color: C.accent2, fontFace: "Cambria", objectName: "Título " + c[0] });
    txt(s, c[1], { x: x + 0.3, y: 4.25, w: 3.3, h: 2.2, fontSize: 18, color: C.background1, valign: "top", objectName: "Texto " + c[0] });
  });
  s.addNotes("Aquí está el lado cuántico del viaje: cada lead es un abanico de posibilidades hasta que lo atiendes; todo está entrelazado; y los saltos de nivel ocurren sin pasos intermedios. Ventas cerradas de $14.5M y $17.5M respaldan que se puede.");

  // ---------- 5. Números
  s = pres.addSlide({ masterName: "CONTENIDO" });
  s.addText("Los números del viaje", { placeholder: "title" });
  const st = [["$4.7M", "ticket promedio de nuestras ventas (MXN)"], ["50%", "de las ventas llega por referido"], ["2–4 sem", "ciclo típico de una venta"], ["+24 años", "de trayectoria de Kenia en Cancún"]];
  st.forEach((c, i) => {
    const x = 0.6 + i * 3.08;
    card(s, x, 1.6, 2.86, 3.0, "Tarjeta " + c[0]);
    txt(s, c[0], { x: x + 0.15, y: 1.95, w: 2.56, h: 1.1, fontSize: 40, bold: true, color: C.accent2, align: "center", valign: "middle", fontFace: "Cambria", objectName: "Cifra " + c[0] });
    txt(s, c[1], { x: x + 0.25, y: 3.2, w: 2.36, h: 1.1, fontSize: 16, color: C.background1, align: "center", valign: "top", objectName: "Descripción " + c[0] });
  });
  card(s, 0.6, 4.95, 12.1, 1.5, "Meta");
  txt(s, "Tu meta: sumar tus propias ventas a esta historia.", { x: 0.9, y: 4.95, w: 11.5, h: 1.5, fontSize: 28, italic: true, color: C.background1, align: "center", valign: "middle", fontFace: "Cambria", objectName: "Texto meta" });
  s.addNotes("Cifras del negocio (Alta Vida Inmuebles): ticket promedio $4.7M MXN, la mitad de las ventas por referido, ciclo de 2 a 4 semanas, más de 24 años de trayectoria de Kenia en Cancún.");

  // ---------- 6. Tres retos
  s = pres.addSlide({ masterName: "CONTENIDO" });
  s.addText("Tus tres retos", { placeholder: "title" });
  const rt = [
    ["Clientes nuevos", "Atender cada lead en minutos, desde Inmuebles24, Marketplace, WhatsApp y redes."],
    ["Cerrar prospectos", "Dar seguimiento a quienes ya levantaron la mano y a la cartera: convertir conversaciones en citas y cierres."],
    ["Más referidos", "La mitad de nuestras ventas llega por referido. Cada cliente bien cuidado abre la puerta a otros."],
  ];
  rt.forEach((c, i) => {
    const x = 0.6 + i * 4.1;
    card(s, x, 1.6, 3.9, 4.9, "Tarjeta reto " + (i + 1));
    circle(s, x + 0.35, 1.95, 0.9, String(i + 1), 30, "Número reto " + (i + 1));
    txt(s, c[0], { x: x + 0.35, y: 3.1, w: 3.2, h: 0.6, fontSize: 24, bold: true, color: C.accent2, fontFace: "Cambria", objectName: "Título reto " + (i + 1) });
    txt(s, c[1], { x: x + 0.35, y: 3.85, w: 3.2, h: 2.4, fontSize: 20, color: C.background1, valign: "top", objectName: "Texto reto " + (i + 1) });
  });
  s.addNotes("Los tres retos, en orden de prioridad: 1) clientes nuevos, 2) cerrar prospectos nuevos y de cartera, 3) más referidos.");

  // ---------- 7. Canales (Inmuebles24)
  s = pres.addSlide({ masterName: "CONTENIDO" });
  s.addText("Dónde sucede la magia", { placeholder: "title" });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.6, w: 5.6, h: 1.9, rectRadius: 0.12, fill: { color: C.background1 }, line: { color: C.accent6, width: 1.5 }, objectName: "Insignia Inmuebles24" });
  s.addImage({ path: A("i24_logo.png"), x: 1.2, y: 1.95, w: 4.4, h: 1.05, objectName: "Logo Inmuebles24", altText: "Logotipo de Inmuebles24" });
  txt(s, "Aquí nacen conversaciones con prospectos que ya levantaron la mano.", { x: 0.6, y: 3.7, w: 5.6, h: 0.9, fontSize: 16, color: C.background2, valign: "top", objectName: "Texto Inmuebles24" });
  txt(s, "Quien responde primero, cierra primero.", { x: 0.6, y: 4.8, w: 5.6, h: 1.7, fontSize: 32, bold: true, color: C.accent2, valign: "middle", fontFace: "Cambria", objectName: "Frase velocidad" });
  const ch = [
    ["Inmuebles24", "Publicación y atención inmediata de cada lead"],
    ["WhatsApp", "Respuestas rápidas, guiones listos y seguimiento"],
    ["Marketplace", "Conversaciones nuevas con compradores"],
    ["Referidos", "La mitad de nuestras ventas"],
    ["Redes y web", "Instagram, Facebook, TikTok, YouTube y nuestro sitio"],
  ];
  ch.forEach((c, i) => {
    const y = 1.6 + i * 0.98;
    card(s, 6.6, y, 6.1, 0.84, "Canal " + c[0]);
    s.addShape(pres.shapes.OVAL, { x: 6.85, y: y + 0.3, w: 0.24, h: 0.24, fill: { color: i === 0 ? C.accent6 : C.accent1 }, line: { color: C.accent2, width: 0.5 }, objectName: "Punto " + c[0] });
    txt(s, [
      { text: c[0], options: { fontSize: 18, bold: true, color: C.background1, breakLine: true } },
      { text: c[1], options: { fontSize: 14, color: C.background2 } },
    ], { x: 7.3, y: y + 0.05, w: 5.2, h: 0.74, valign: "middle", objectName: "Texto " + c[0] });
  });
  s.addNotes("Inmuebles24 es uno de nuestros canales de captación. Lo que más valora el cliente es la velocidad: cada lead se atiende en minutos. Marca y logotipo de Inmuebles24 usados solo para identificar el portal donde publicamos.");

  // ---------- 8. Lo que valora el cliente
  s = pres.addSlide({ masterName: "CONTENIDO" });
  s.addText("Lo que más valora quien nos compra", { placeholder: "title" });
  const v = [
    ["Velocidad", "Respuesta y trámites en tiempos cortos"],
    ["Atención profesional", "Trato cercano y preparado en cada recorrido"],
    ["Precio", "Información clara y datos exactos de cada ficha"],
    ["Marca", "Alta Vida: trayectoria impecable en Cancún"],
    ["Ubicación segura", "Zonas de plusvalía con amenidades de primer mundo"],
  ];
  v.forEach((c, i) => {
    const x = 0.6 + i * 2.45;
    card(s, x, 1.6, 2.25, 3.5, "Tarjeta " + c[0]);
    circle(s, x + 0.2, 1.85, 0.6, String(i + 1), 20, "Número " + c[0]);
    txt(s, c[0], { x: x + 0.2, y: 2.65, w: 1.85, h: 0.9, fontSize: 20, bold: true, color: C.accent2, valign: "top", fontFace: "Cambria", objectName: "Título " + c[0] });
    txt(s, c[1], { x: x + 0.2, y: 3.55, w: 1.85, h: 1.4, fontSize: 14, color: C.background1, valign: "top", objectName: "Texto " + c[0] });
  });
  card(s, 0.6, 5.4, 12.1, 1.2, "Cierre valores");
  txt(s, "Tu trabajo: convertir cada uno de estos cinco valores en una experiencia.", { x: 0.9, y: 5.4, w: 11.5, h: 1.2, fontSize: 24, italic: true, color: C.background1, align: "center", valign: "middle", fontFace: "Cambria", objectName: "Texto cierre valores" });
  s.addNotes("Lo que más valora nuestro cliente: velocidad, atención profesional, precio, marca y una ubicación segura con amenidades de primer mundo.");

  // ---------- 9. Primera vuelta
  s = pres.addSlide({ masterName: "CONTENIDO" });
  s.addText("Tu primera vuelta a la rueda: 4 semanas", { placeholder: "title" });
  s.addShape(pres.shapes.LINE, { x: 1.4, y: 2.2, w: 10.5, h: 0, line: { color: C.accent1, width: 2.5 }, objectName: "Línea de ruta" });
  const wk = [
    ["Semana 1", "Conoce", "Inventario, desarrollos y zonas de plusvalía. Estudia cada ficha."],
    ["Semana 2", "Acompaña", "Recorridos y citas junto a Kenia y Jaime."],
    ["Semana 3", "Presenta", "Tu primer cliente: atiendes el lead y llevas la cita."],
    ["Semana 4", "Cierra", "Seguimiento, trámites y crédito hasta la firma."],
  ];
  wk.forEach((c, i) => {
    const x = 0.6 + i * 3.08;
    circle(s, x + 1.08, 1.85, 0.7, String(i + 1), 20, "Nodo " + (i + 1));
    card(s, x, 2.9, 2.86, 3.6, "Tarjeta " + c[0]);
    txt(s, c[0].toUpperCase(), { x: x + 0.25, y: 3.1, w: 2.4, h: 0.35, fontSize: 12, bold: true, color: C.accent1, charSpacing: 3, objectName: "Etiqueta " + c[0] });
    txt(s, c[1], { x: x + 0.25, y: 3.5, w: 2.4, h: 0.6, fontSize: 26, bold: true, color: C.accent2, fontFace: "Cambria", objectName: "Título " + c[0] });
    txt(s, c[2], { x: x + 0.25, y: 4.25, w: 2.4, h: 2.0, fontSize: 18, color: C.background1, valign: "top", objectName: "Texto " + c[0] });
  });
  s.addNotes("Propuesta de primer ciclo (ajustable por Jaime): conocer inventario, acompañar recorridos, presentar al primer cliente y cerrar. El ciclo de venta típico es de 2 a 4 semanas.");

  // ---------- 10. Cierre
  s = pres.addSlide({ masterName: "FULL" });
  s.addImage({ path: A("wheel.png"), x: 7.1, y: 0.7, w: 5.8, h: 5.8, transparency: 35, objectName: "Rueda de la fortuna", altText: "Rueda de la fortuna dorada" });
  s.addImage({ path: A("logo_full.png"), x: 0.7, y: 0.5, w: 1.5, h: 1.283, objectName: "Logo Alta Vida Inmuebles", altText: "Logotipo de Alta Vida Inmuebles" });
  txt(s, [
    { text: "Sube.", options: { color: C.background1, breakLine: true } },
    { text: "La vista desde arriba es otra.", options: { color: C.accent2 } },
  ], { x: 0.7, y: 2.4, w: 6.3, h: 2.6, fontSize: 48, bold: true, valign: "top", fontFace: "Cambria", objectName: "Título" });
  txt(s, `${N}, esto apenas comienza.`, { x: 0.7, y: 5.2, w: 6.3, h: 0.55, fontSize: 24, color: C.background1, objectName: "Mensaje" });
  txt(s, "Jaime Marin  ·  Lic. Kenia Acosta Aguilera  ·  Alta Vida Inmuebles", { x: 0.7, y: 6.2, w: 6.3, h: 0.7, fontSize: 14, color: C.accent4, valign: "top", objectName: "Firma" });
  s.addNotes("Cierre. Invita a subir: la rueda empieza a girar hoy. Termina con un apretón de manos o un abrazo del equipo.");

  const out = path.join(__dirname, file);
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("OK", out);
}

(async () => {
  await build({ name: "Juli Pastrana" }, "Bienvenida_Juli_Pastrana.pptx");
  await build({ name: "Gaby Luna" }, "Bienvenida_Gaby_Luna.pptx");
})();
