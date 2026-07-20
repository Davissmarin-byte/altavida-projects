import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {useTheme} from '../theme-context';

type Props = {
	text: string;
	// Duración de la Sequence que envuelve este componente (relativo a ella misma), para
	// calcular el fundido de salida antes de que la Sequence termine.
	durationInFrames: number;
};

// "Sello" de cifra/dato real mencionado en el audio (Paso 8: la prueba visible vende).
export const FigureHighlight: React.FC<Props> = ({text, durationInFrames}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const theme = useTheme();

	const enter = spring({frame, fps, config: theme.motion.springBouncy, durationInFrames: 12});
	const scale = interpolate(enter, [0, 1], [0.6, 1]);
	const enterOpacity = interpolate(enter, [0, 1], [0, 1]);
	const exitOpacity = interpolate(frame, [durationInFrames - 10, durationInFrames], [1, 0], {
		extrapolateLeft: 'clamp',
		extrapolateRight: 'clamp',
	});

	return (
		<AbsoluteFill style={{justifyContent: 'flex-start', alignItems: 'center', paddingTop: '23%'}}>
			<div
				style={{
					background: theme.colors.accent,
					color: theme.colors.bgIntro,
					fontFamily: theme.fonts.display,
					fontWeight: 800,
					fontSize: 46,
					padding: '14px 36px',
					borderRadius: 16,
					textAlign: 'center',
					boxShadow: '0 8px 24px rgba(0,0,0,0.35)',
					transform: `scale(${scale})`,
					opacity: enterOpacity * exitOpacity,
				}}
			>
				{text}
			</div>
		</AbsoluteFill>
	);
};
