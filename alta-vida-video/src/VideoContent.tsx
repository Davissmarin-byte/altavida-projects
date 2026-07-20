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
import {agendaLlamadaTheme} from './theme';
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

export type VideoContentProps = {
	hookDurationInFrames: number;
	mainDurationInFrames: number;
	outroDurationInFrames: number;
	transitionDurationInFrames: number;
};

export const VideoContent: React.FC<VideoContentProps> = (props) => (
	<ThemeProvider value={agendaLlamadaTheme}>
		<VideoContentInner {...props} />
	</ThemeProvider>
);

const VideoContentInner: React.FC<VideoContentProps> = ({
	hookDurationInFrames,
	mainDurationInFrames,
	outroDurationInFrames,
	transitionDurationInFrames,
}) => {
	const {fps} = useVideoConfig();
	const theme = useTheme();
	useFontReady();
	const captionsA = useCaptions('captions-a.json');
	const pages = useTikTokPages(captionsA);

	// Punch-in justo cuando empieza a decir la cifra de comparación ("...ha alcanzado 25 30
	// millones de pesos"), tomado de public/captions-a.json (token " alcanz" en 21470ms).
	const punchAtFrame = Math.round((21470 / 1000) * fps);

	return (
		<TransitionSeries>
			<TransitionSeries.Sequence durationInFrames={hookDurationInFrames}>
				<AbsoluteFill>
					<KenBurnsClip
						src="clip-b.mp4"
						durationInFrames={hookDurationInFrames}
						muted
						volume={0}
						// El dron (visible en el propio plano, por ser un video generado por IA) entra en
						// cuadro pasado el frame ~24 (0.8s @30fps); congelamos justo antes en un fotograma
						// limpio de playa y mantenemos el Ken Burns sobre esa imagen fija.
						freezeAtFrame={20}
					/>
					<OnScreenText text={theme.hook} />
				</AbsoluteFill>
			</TransitionSeries.Sequence>

			<TransitionSeries.Transition
				presentation={slide({direction: 'from-right'})}
				timing={linearTiming({durationInFrames: transitionDurationInFrames})}
			/>

			<TransitionSeries.Sequence durationInFrames={mainDurationInFrames}>
				<AbsoluteFill>
					<KenBurnsClip
						src="clip-a.mp4"
						durationInFrames={mainDurationInFrames}
						punchAtFrame={punchAtFrame}
					/>
					<ProgressBar durationInFrames={mainDurationInFrames} />
					<LowerThird
						name={theme.brand.name}
						business={theme.brand.business}
						inAtFrame={Math.round(fps * 0.5)}
						outAtFrame={mainDurationInFrames - Math.round(fps * 1)}
					/>
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
					{/* Cifras reales mencionadas en el audio (public/captions-a.json), Paso 8. */}
					<Sequence from={Math.round((22300 / 1000) * fps)} durationInFrames={90} premountFor={fps}>
						<FigureHighlight text="$25–30M MXN" durationInFrames={90} />
					</Sequence>
					<Sequence from={Math.round((27500 / 1000) * fps)} durationInFrames={90} premountFor={fps}>
						<FigureHighlight text="Desde $4M MXN" durationInFrames={90} />
					</Sequence>
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
