/**
 * Alta Vida Inmuebles · Control de asistencia sin cámara
 *
 * Crea un Google Form (entrada / salida + checklist de apertura y cierre),
 * lo conecta a un Google Sheet y programa alertas automáticas:
 *   - Cada registro se clasifica (a tiempo / retardo) en la hoja "Control".
 *   - Si a las 08:15 no hay registro de entrada, avisa por correo a dirección.
 *   - Si 30 min después de la hora de salida no hay registro de salida, avisa.
 *
 * Uso: pega este archivo y appsscript.json en un proyecto de Apps Script,
 * ejecuta `instalar` una sola vez y autoriza los permisos.
 */

const CONFIG = {
  colaboradora: 'Alejandra Valle',
  puesto: 'Asistente de Dirección y Contenido Digital',
  horaEntrada: '08:00',
  horaSalida: '18:00',
  toleranciaMin: 10,
  // 1 = lunes … 6 = sábado, 7 = domingo
  diasLaborales: [1, 2, 3, 4, 5, 6],
  // Vacío = el correo de quien ejecuta `instalar` (dirección)
  correoDireccion: '',
  zonaHoraria: 'America/Cancun',
};

const TIPO_ENTRADA = 'Entrada';
const TIPO_SALIDA = 'Salida';
const TITULO_TIPO = 'Tipo de registro';

const CHECKLIST_APERTURA = [
  'Oficina ordenada y limpia (escritorios, sala de juntas, recepción)',
  'Insumos revisados: agua, café, papelería, folletos, tarjetas, plumas',
  'Equipo funcionando: computadora, internet, impresora, pantalla',
  'Aire acondicionado e iluminación listos para recibir clientes',
  'Agenda del día revisada (Calendar / CRM) y citas confirmadas',
  'WhatsApp de coordinación abierto y leads nuevos revisados',
];

const CHECKLIST_CIERRE = [
  'Leads y mensajes del día respondidos (WhatsApp, Instagram, Marketplace)',
  'Contenido del día publicado o programado',
  'Pendientes y avances registrados en CRM / Notion',
  'Oficina ordenada, equipo y aire acondicionado apagados',
  'Oficina cerrada con llave',
];

/** Ejecutar UNA sola vez. */
function instalar() {
  const props = PropertiesService.getScriptProperties();
  if (props.getProperty('FORM_ID')) {
    throw new Error('Ya está instalado. Usa `desinstalarTriggers` si necesitas reinstalar.');
  }

  const form = crearFormulario_();
  const ss = SpreadsheetApp.create('Alta Vida · Asistencia ' + CONFIG.colaboradora);
  ss.setSpreadsheetTimeZone(CONFIG.zonaHoraria);
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  crearHojaControl_(ss);

  props.setProperties({ FORM_ID: form.getId(), SHEET_ID: ss.getId() });
  crearTriggers_(form);

  const resumen = [
    'Formulario (link para Alejandra): ' + form.getPublishedUrl(),
    'Editar formulario: ' + form.getEditUrl(),
    'Hoja de registros (solo dirección): ' + ss.getUrl(),
    '',
    'PASO MANUAL: en el formulario, sección "Checklist de apertura", agrega una',
    'pregunta tipo "Subir archivo" llamada "Foto de la oficina abierta" (obligatoria,',
    'solo imágenes, 1 archivo, 10 MB). Google no permite crearla por script.',
  ].join('\n');
  Logger.log(resumen);
  MailApp.sendEmail(correoDireccion_(), 'Control de asistencia instalado', resumen);
}

function crearFormulario_() {
  const form = FormApp.create('Alta Vida · Registro de asistencia');
  form.setDescription(
    CONFIG.colaboradora + ' · ' + CONFIG.puesto + '\n' +
    'Registra tu ENTRADA al llegar (horario ' + CONFIG.horaEntrada + ') y tu SALIDA al terminar (' +
    CONFIG.horaSalida + '). La hora se guarda automáticamente.'
  );
  try {
    form.setEmailCollectionType(FormApp.EmailCollectionType.VERIFIED);
  } catch (e) {
    form.setCollectEmail(true);
  }
  form.setAllowResponseEdits(false);
  form.setLimitOneResponsePerUser(false);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage('Registro guardado con hora automática. ¡Gracias!');

  const tipo = form.addMultipleChoiceItem().setTitle(TITULO_TIPO).setRequired(true);

  const paginaApertura = form.addPageBreakItem()
    .setTitle('Checklist de apertura')
    .setHelpText('Revisa cada punto antes de marcarlo. Después sube la foto de la oficina lista.');
  form.addCheckboxItem()
    .setTitle('Apertura completada')
    .setChoiceValues(CHECKLIST_APERTURA)
    .setValidation(FormApp.createCheckboxValidation()
      .setHelpText('Debes completar todos los puntos de apertura.')
      .requireSelectExactly(CHECKLIST_APERTURA.length)
      .build())
    .setRequired(true);
  form.addParagraphTextItem()
    .setTitle('Insumos faltantes o incidencias')
    .setHelpText('Ej.: "Se acabó el agua", "impresora sin tóner". Deja vacío si todo está bien.');

  const paginaCierre = form.addPageBreakItem()
    .setTitle('Checklist de cierre')
    .setHelpText('Antes de irte, confirma el cierre del día.');
  form.addCheckboxItem()
    .setTitle('Cierre completado')
    .setChoiceValues(CHECKLIST_CIERRE)
    .setValidation(FormApp.createCheckboxValidation()
      .setHelpText('Debes completar todos los puntos de cierre.')
      .requireSelectExactly(CHECKLIST_CIERRE.length)
      .build())
    .setRequired(true);
  form.addParagraphTextItem()
    .setTitle('Resumen del día')
    .setHelpText('3 líneas: qué publicaste, qué leads atendiste, qué queda pendiente para mañana.')
    .setRequired(true);

  // setGoToPage aplica al terminar la sección ANTERIOR a este salto:
  // al terminar la apertura se envía, sin pasar por la sección de cierre.
  paginaCierre.setGoToPage(FormApp.PageNavigationType.SUBMIT);

  tipo.setChoices([
    tipo.createChoice(TIPO_ENTRADA, paginaApertura),
    tipo.createChoice(TIPO_SALIDA, paginaCierre),
  ]);
  return form;
}

function crearHojaControl_(ss) {
  const hoja = ss.insertSheet('Control');
  hoja.appendRow(['Fecha', 'Hora', 'Tipo', 'Correo', 'Estado', 'Minutos de diferencia', 'Incidencias / resumen']);
  hoja.setFrozenRows(1);
  hoja.getRange('A1:G1').setFontWeight('bold').setBackground('#0f2a3d').setFontColor('#ffffff');
  // Evidencia laboral: solo la persona dueña del archivo puede editar esta hoja.
  const proteccion = hoja.protect().setDescription('Solo dirección');
  proteccion.removeEditors(proteccion.getEditors());
  if (proteccion.canDomainEdit()) proteccion.setDomainEdit(false);
}

function crearTriggers_(form) {
  ScriptApp.newTrigger('alEnviar').forForm(form).onFormSubmit().create();
  const [hE, mE] = CONFIG.horaEntrada.split(':').map(Number);
  const [hS, mS] = CONFIG.horaSalida.split(':').map(Number);
  const alertaEntrada = hE * 60 + mE + 15;
  const alertaSalida = hS * 60 + mS + 30;
  ScriptApp.newTrigger('revisarEntrada').timeBased()
    .atHour(Math.floor(alertaEntrada / 60)).nearMinute(alertaEntrada % 60)
    .everyDays(1).inTimezone(CONFIG.zonaHoraria).create();
  ScriptApp.newTrigger('revisarSalida').timeBased()
    .atHour(Math.floor(alertaSalida / 60)).nearMinute(alertaSalida % 60)
    .everyDays(1).inTimezone(CONFIG.zonaHoraria).create();
}

/** Trigger: cada envío del formulario. */
function alEnviar(e) {
  const resp = e.response;
  const fecha = resp.getTimestamp();
  const tipo = valor_(resp, TITULO_TIPO);
  const esperado = tipo === TIPO_ENTRADA ? CONFIG.horaEntrada : CONFIG.horaSalida;
  const diff = minutosDesde_(fecha, esperado);

  let estado;
  if (tipo === TIPO_ENTRADA) {
    estado = diff <= CONFIG.toleranciaMin ? 'A tiempo' : 'RETARDO';
  } else {
    estado = diff >= 0 ? 'Salida completa' : 'SALIDA ANTICIPADA';
  }
  const notas = valor_(resp, 'Insumos faltantes o incidencias') || valor_(resp, 'Resumen del día') || '';

  hojaControl_().appendRow([
    Utilities.formatDate(fecha, CONFIG.zonaHoraria, 'yyyy-MM-dd'),
    Utilities.formatDate(fecha, CONFIG.zonaHoraria, 'HH:mm:ss'),
    tipo,
    resp.getRespondentEmail(),
    estado,
    diff,
    notas,
  ]);

  if (estado === 'RETARDO' || estado === 'SALIDA ANTICIPADA' || (tipo === TIPO_ENTRADA && notas)) {
    MailApp.sendEmail(correoDireccion_(),
      'Asistencia ' + CONFIG.colaboradora + ': ' + estado,
      tipo + ' a las ' + Utilities.formatDate(fecha, CONFIG.zonaHoraria, 'HH:mm') +
      ' (' + diff + ' min vs ' + esperado + ').' + (notas ? '\nNotas: ' + notas : ''));
  }
}

/** Trigger diario 15 min después de la hora de entrada. */
function revisarEntrada() {
  if (!esDiaLaboral_()) return;
  if (!hayRegistroHoy_(TIPO_ENTRADA)) {
    MailApp.sendEmail(correoDireccion_(),
      'SIN REGISTRO DE ENTRADA: ' + CONFIG.colaboradora,
      'A las ' + Utilities.formatDate(new Date(), CONFIG.zonaHoraria, 'HH:mm') +
      ' no hay registro de entrada. Horario: ' + CONFIG.horaEntrada + '.');
  }
}

/** Trigger diario 30 min después de la hora de salida. */
function revisarSalida() {
  if (!esDiaLaboral_()) return;
  if (hayRegistroHoy_(TIPO_ENTRADA) && !hayRegistroHoy_(TIPO_SALIDA)) {
    MailApp.sendEmail(correoDireccion_(),
      'SIN REGISTRO DE SALIDA: ' + CONFIG.colaboradora,
      'Hubo entrada hoy pero no hay registro de salida.');
  }
}

/** Utilidad: borra los triggers (para reinstalar o pausar). */
function desinstalarTriggers() {
  ScriptApp.getProjectTriggers().forEach(function (t) { ScriptApp.deleteTrigger(t); });
  PropertiesService.getScriptProperties().deleteAllProperties();
}

function hayRegistroHoy_(tipo) {
  const form = FormApp.openById(PropertiesService.getScriptProperties().getProperty('FORM_ID'));
  return form.getResponses(inicioDelDia_()).some(function (r) { return valor_(r, TITULO_TIPO) === tipo; });
}

function valor_(resp, titulo) {
  const item = resp.getItemResponses().find(function (ir) { return ir.getItem().getTitle() === titulo; });
  return item ? item.getResponse() : null;
}

function minutosDesde_(fecha, hhmm) {
  const [h, m] = hhmm.split(':').map(Number);
  const hora = Number(Utilities.formatDate(fecha, CONFIG.zonaHoraria, 'H'));
  const min = Number(Utilities.formatDate(fecha, CONFIG.zonaHoraria, 'm'));
  return (hora * 60 + min) - (h * 60 + m);
}

function inicioDelDia_() {
  const hoy = Utilities.formatDate(new Date(), CONFIG.zonaHoraria, "yyyy-MM-dd'T'00:00:00XXX");
  return new Date(hoy);
}

function esDiaLaboral_() {
  const dia = Number(Utilities.formatDate(new Date(), CONFIG.zonaHoraria, 'u'));
  return CONFIG.diasLaborales.indexOf(dia) !== -1;
}

function hojaControl_() {
  return SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty('SHEET_ID'))
    .getSheetByName('Control');
}

function correoDireccion_() {
  return CONFIG.correoDireccion || Session.getEffectiveUser().getEmail();
}
