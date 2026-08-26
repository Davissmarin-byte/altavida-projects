import React from 'react';
import {AbsoluteFill, Sequence, useVideoConfig} from 'remotion';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {slide} from '@remotion/transitions/slide';
import {KenBurnsClip} from './components/KenBurnsClip';
import {ProgressBar} from './components/ProgressBar';
import {LowerThird} from './components/LowerThird';
import {OnScreenText} from './components/OnScreenText';
import {FigureHighlight} from './components/FigureHighlight';
import {Outro} from './components/Outro';
import {CaptionPageView, useCaptions, useTikTokPages} from './Captions';
import {useFontReady} from './load-font';
import type {Theme} from './theme';
import {ThemeProvider, useTheme} from './theme-context';

// Música: por ahora no hay pista. Cuando tengas un .mp3, pégalo en public/music.mp3,
// importa { Audio } from '@remotion/media' y descomenta el bloque de abajo dentro de <AbsoluteFill>:
//
// import {Audio} from '@remotion/media';
// import {staticFile, interpolate} from 'remotion';
// <Audio
//   src={staticFile('music.mp3')}
//   loop
//   loopVolumeCurveBehavior="extend"
//   volume={(f) =>
//     interpolate(f, [0, fps, durationInFrames - fps, durationInFrames], [0, 0.12, 0.12, 0], {
//       extrapolateLeft: 'clamp',
//       extrapolateRight: 'clamp',
//     })
//   }
// />

export type FigureHighlightSpec = {
	text: string;
	// Momento (ms, dentro del audio/clip) en que aparece el "sello" con la cifra.
	atMs: number;
	durationInFrames: number;
};

export type SingleClipVideoContentProps = {
	theme: Theme;
	clipSrc: string;
	captionsFile: string;
	mainDurationInFrames: number;
	outroDurationInFrames: number;
	transitionDurationInFrames: number;
	// Cuánto tiempo se mantiene el gancho superpuesto sobre el propio clip antes de desvanecerse
	// (aquí no hay un clip B separado: el gancho es texto encima del inicio del clip principal).
	hookOverlayDurationInFrames: number;
	// Frame (relativo al clip principal) donde cae el punch-in. Por defecto, la mitad del clip.
	punchAtFrame?: number;
	// Cifras/datos reales mencionados en el audio para resaltar en pantalla (Paso 8).
	figureHighlights?: FigureHighlightSpec[];
};

export const SingleClipVideoContent: React.FC<SingleClipVideoContentProps> = ({theme, ...props}) => (
	<ThemeProvider value={theme}>
		<SingleClipVideoContentInner {...props} />
	</ThemeProvider>
);

const SingleClipVideoContentInner: React.FC<Omit<SingleClipVideoContentProps, 'theme'>> = ({
	clipSrc,
	captionsFile,
	mainDurationInFrames,
	outroDurationInFrames,
	transitionDurationInFrames,
	hookOverlayDurationInFrames,
	punchAtFrame,
	figureHighlights = [],
}) => {
	const {fps} = useVideoConfig();
	const theme = useTheme();
	useFontReady();
	const captions = useCaptions(captionsFile);
	const pages = useTikTokPages(captions);

	// Punch-in: usa el frame real pasado por props (ideal, anclado a un momento de la
	// transcripción) o, si no se especifica, la mitad del clip.
	const resolvedPunchAtFrame = punchAtFrame ?? Math.round(mainDurationInFrames / 2);
	const hookFadeOutStartFrame = hookOverlayDurationInFrames - Math.round(fps * 0.5);

	return (
		<TransitionSeries>
			<TransitionSeries.Sequence durationInFrames={mainDurationInFrames}>
				<AbsoluteFill>
					<KenBurnsClip
						src={clipSrc}
						durationInFrames={mainDurationInFrames}
						punchAtFrame={resolvedPunchAtFrame}
					/>
					<ProgressBar durationInFrames={mainDurationInFrames} />
					<LowerThird
						name={theme.brand.name}
						business={theme.brand.business}
						inAtFrame={hookOverlayDurationInFrames + Math.round(fps * 0.3)}
						outAtFrame={mainDurationInFrames - Math.round(fps * 1)}
					/>
					<Sequence durationInFrames={hookOverlayDurationInFrames} premountFor={fps}>
						<OnScreenText text={theme.hook} position="top" fadeOutAfterFrame={hookFadeOutStartFrame} />
					</Sequence>
					{pages.map((page) => {
						const startFrame = Math.round((page.startMs / 1000) * fps);
						const durationInFrames = Math.round((page.durationMs / 1000) * fps);
						if (durationInFrames <= 0) return null;
						return (
							<Sequence
								key={page.startMs}
								from={startFrame}
								durationInFrames={durationInFrames}
								premountFor={fps}
							>
								<CaptionPageView page={page} />
							</Sequence>
						);
					})}
					{figureHighlights.map((figure) => (
						<Sequence
							key={figure.atMs}
							from={Math.round((figure.atMs / 1000) * fps)}
							durationInFrames={figure.durationInFrames}
							premountFor={fps}
						>
							<FigureHighlight text={figure.text} durationInFrames={figure.durationInFrames} />
						</Sequence>
					))}
				</AbsoluteFill>
			</TransitionSeries.Sequence>

			<TransitionSeries.Transition
				presentation={slide({direction: 'from-right'})}
				timing={linearTiming({durationInFrames: transitionDurationInFrames})}
			/>

			<TransitionSeries.Sequence durationInFrames={outroDurationInFrames}>
				<Outro />
			</TransitionSeries.Sequence>
		</TransitionSeries>
	);
};
