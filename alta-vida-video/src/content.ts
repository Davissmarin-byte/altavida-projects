// src/content.ts — guion en pantalla (no hay narracion en el clip: video de dron sin dialogo,
// ver nota en el PR sobre por que no se uso transcripcion por voz).
export const brand = {
  name: 'Alta Vida Inmuebles',
};

export const hook = {
  text: 'El mejor momento para crecer tu patrimonio es ahora',
  startSec: 0,
  durationSec: 3,
};

export const midTexts = [
  {
    text: 'Propiedades de alta plusvalia',
    startSec: 6.5,
    durationSec: 2.6,
  },
  {
    text: 'Para familias e inversionistas',
    startSec: 12.5,
    durationSec: 2.6,
  },
] as const;

export const lowerThird = {
  startSec: hook.startSec + hook.durationSec + 0.3,
  // se oculta un poco antes del final del clip principal, calculado en la composicion
  endOffsetFromClipEndSec: 1.2,
};

export const cta = {
  text: 'Agenda tu visita privada hoy',
};
