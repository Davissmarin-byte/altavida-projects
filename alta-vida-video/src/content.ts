// src/content.ts — guion en pantalla. El clip tiene voz real (persona hablando a camara),
// pero no se transcribio: huggingface.co (host del modelo de Whisper) esta bloqueado en
// este entorno. Ver nota en el PR. Este texto es marketing generico, no un subtitulo fiel
// a lo que se dice en el audio.
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
