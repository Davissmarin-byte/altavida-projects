// src/theme.ts — fuente única de verdad del look del video (ALTA VIDA Inmuebles)
export const theme = {
  colors: {
    accent: '#e8b763', // dorado — resaltado de subtítulos, barra, lower-third, CTA, cifras
    text: '#FFFFFF',
    textStroke: '#000000',
    bgIntro: '#0A0A0A',
  },
  fonts: {
    display: 'Montserrat',
  },
  caption: {
    fontSize: 72,
    fontWeight: 800,
    strokeWidth: 4,
    maxWordsPerPage: 5,
    safeBottomPct: 16,
    // Energía "redes": palabra por palabra, ritmo rápido.
    combineTokensWithinMilliseconds: 900,
  },
  motion: {
    springSmooth: { damping: 200 },
    springSnappy: { damping: 20, stiffness: 200 },
    springBouncy: { damping: 8 },
    kenBurnsScale: [1, 1.12] as [number, number],
    // Vibra energética: punch-ins más marcados y frecuentes que en un look "tranquilo".
    punchInScale: 1.08,
  },
  brand: {
    name: 'Jaime Marin',
    business: 'ALTA VIDA Inmuebles',
  },
  hook: 'Ahí está esta hermosa propiedad vacía, le faltas tú. Vive tu alta vida.',
  cta: 'Agenda tu llamada gratis o escríbenos por WhatsApp',
} as const;
