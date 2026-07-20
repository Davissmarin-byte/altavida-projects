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
}) => {
	const {fps} = useVideoConfig();
	const theme = useTheme();
	useFontReady();
	const captions = useCaptions(captionsFile);
	const pages = useTikTokPages(captions);

	// Punch-in a mitad del clip principal, coincide con un cambio de idea (ajustable con datos
	// reales de la transcripción una vez esté disponible).
	const punchAtFrame = Math.round(mainDurationInFrames / 2);
	const hookFadeOutStartFrame = hookOverlayDurationInFrames - Math.round(fps * 0.5);

	return (
		<TransitionSeries>
			<TransitionSeries.Sequence durationInFrames={mainDurationInFrames}>
				<AbsoluteFill>
					<KenBurnsClip src={clipSrc} durationInFrames={mainDurationInFrames} punchAtFrame={punchAtFrame} />
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
