// src/theme.ts — fuente unica de verdad del look del video (Alta Vida Inmuebles)
export const theme = {
  colors: {
    accent: '#e8b763', // dorado — resaltado de texto, barra, lower-third, CTA
    text: '#FFFFFF',
    textStroke: '#000000',
    bgOutro: '#0A0A0A',
  },
  fonts: {
    display: 'Montserrat',
  },
  caption: {
    fontSize: 64,
    fontWeight: 800,
    strokeWidth: 3,
    safeBottomPct: 14,
  },
  hook: {
    fontSize: 72,
  },
  motion: {
    // Verificado: spring({config}) acepta damping/stiffness/mass, ver remotion.dev/docs/spring
    springSmooth: { damping: 200 }, // reveals suaves — ritmo "tranquila/elegante"
    springSnappy: { damping: 20, stiffness: 200 },
    kenBurnsScale: [1, 1.1] as const, // zoom muy lento y sutil (vibra tranquila)
  },
} as const;
