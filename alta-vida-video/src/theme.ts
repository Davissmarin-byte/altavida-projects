// src/theme.ts — fuente única de verdad del look de cada video (ALTA VIDA Inmuebles).
// Cada composición usa su propio Theme (ver Root.tsx) provisto vía ThemeContext,
// así varios videos pueden coexistir en el mismo proyecto sin pisarse colores/textos.
export type Theme = {
	colors: {
		accent: string; // resaltado de subtítulos, barra, lower-third, CTA, cifras
		text: string;
		textStroke: string;
		bgIntro: string;
	};
	fonts: {
		display: string;
	};
	caption: {
		fontSize: number;
		fontWeight: number;
		strokeWidth: number;
		maxWordsPerPage: number;
		safeBottomPct: number;
		combineTokensWithinMilliseconds: number;
	};
	motion: {
		springSmooth: {damping: number};
		springSnappy: {damping: number; stiffness: number};
		springBouncy: {damping: number};
		kenBurnsScale: [number, number];
		punchInScale: number;
	};
	brand: {
		name: string;
		business: string;
	};
	hook: string;
	cta: string;
};

// Motion/caption compartidos por defecto (vibra "energética/redes"): cortes rápidos,
// punch-ins marcados, resaltado palabra por palabra.
const energeticMotion: Theme['motion'] = {
	springSmooth: {damping: 200},
	springSnappy: {damping: 20, stiffness: 200},
	springBouncy: {damping: 8},
	kenBurnsScale: [1, 1.12],
	punchInScale: 1.08,
};

const energeticCaptionBase = {
	fontSize: 72,
	fontWeight: 800,
	strokeWidth: 4,
	maxWordsPerPage: 5,
	safeBottomPct: 16,
	combineTokensWithinMilliseconds: 900,
};

// Video 1: "agenda tu llamada" — departamentos frente al mar (dorado).
export const agendaLlamadaTheme: Theme = {
	colors: {
		accent: '#e8b763',
		text: '#FFFFFF',
		textStroke: '#000000',
		bgIntro: '#0A0A0A',
	},
	fonts: {display: 'Montserrat'},
	caption: energeticCaptionBase,
	motion: energeticMotion,
	brand: {
		name: 'Jaime Marin',
		business: 'ALTA VIDA Inmuebles',
	},
	hook: 'Ahí está esta hermosa propiedad vacía, le faltas tú. Vive tu alta vida.',
	cta: 'Agenda tu llamada gratis o escríbenos por WhatsApp',
};

// Video 2: "vender producto concreto" — plusvalía en Cancún (coral).
export const productoPlusvaliaTheme: Theme = {
	colors: {
		accent: '#e0795a',
		text: '#FFFFFF',
		textStroke: '#000000',
		bgIntro: '#0A0A0A',
	},
	fonts: {display: 'Montserrat'},
	caption: energeticCaptionBase,
	motion: energeticMotion,
	brand: {
		name: 'Jaime Marin',
		business: 'ALTA VIDA Inmuebles',
	},
	hook: 'Crecer tu capital en bienes raíces con ALTA VIDA Inmuebles es fácil',
	// No me dieron un CTA/enlace de producto exacto: propongo este. Cámbialo en una línea
	// si tienes el link de compra o un texto distinto.
	cta: 'Conoce la propiedad y aparta la tuya — escríbenos por WhatsApp',
};
