import React from 'react';
import {AbsoluteFill, Sequence, useVideoConfig} from 'remotion';
import {TransitionSeries, linearTiming} from '@remotion/transitions';
import {slide} from '@remotion/transitions/slide';
import {KenBurnsClip} from './components/KenBurnsClip';
import {ProgressBar} from './components/ProgressBar';
import {LowerThird} from './components/LowerThird';
import {OnScreenText} from './components/OnScreenText';
import {Outro} from './components/Outro';
import {CaptionPageView, useCaptions, useTikTokPages} from './Captions';
import {useFontReady} from './load-font';
import {theme} from './theme';

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

export const VideoContent: React.FC<VideoContentProps> = ({
	hookDurationInFrames,
	mainDurationInFrames,
	outroDurationInFrames,
	transitionDurationInFrames,
}) => {
	const {fps} = useVideoConfig();
	useFontReady();
	const captionsA = useCaptions('captions-a.json');
	const pages = useTikTokPages(captionsA);

	// Punch-in a mitad del clip principal, coincide con un cambio de idea (ajustable con datos reales
	// de captions-a.json una vez esté disponible la transcripción).
	const punchAtFrame = Math.round(mainDurationInFrames / 2);

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
