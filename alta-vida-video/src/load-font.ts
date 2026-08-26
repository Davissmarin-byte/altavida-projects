import {useEffect, useState} from 'react';
import {continueRender, delayRender, staticFile} from 'remotion';

// La fuente está autoalojada en public/fonts/ (mismo woff2 variable que sirve
// @remotion/google-fonts para Montserrat, subset latin) porque este entorno bloquea el
// acceso de Chromium a fonts.gstatic.com durante el render (Node sí puede alcanzarlo).
// Se carga con la FontFace API + staticFile() en vez de @font-face en CSS porque el
// bundler de Remotion no resuelve rutas de public/ dentro de url() en archivos .css.
export const fontFamily = 'Montserrat';

// Bloquea el render hasta que la fuente terminó de cargar (evita flash de fuente por defecto).
export const useFontReady = () => {
	const [handle] = useState(() => delayRender('cargando-fuente-montserrat'));

	useEffect(() => {
		const font = new FontFace(
			fontFamily,
			`url(${staticFile('fonts/Montserrat-Variable-latin.woff2')})`,
			{weight: '100 900', style: 'normal'},
		);
		font.load().then((loaded) => {
			document.fonts.add(loaded);
			continueRender(handle);
		});
	}, [handle]);
};
