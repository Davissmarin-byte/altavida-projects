import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {theme} from '../theme';

type Props = {
	name: string;
	business: string;
	// Frame (relativo a la Sequence) en que entra.
	inAtFrame: number;
	// Frame (relativo a la Sequence) en que empieza a salir.
	outAtFrame: number;
};

// Colocado arriba a la izquierda para no chocar con los subtítulos (zona segura inferior).
export const LowerThird: React.FC<Props> = ({name, business, inAtFrame, outAtFrame}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const inAnim = spring({
		frame: frame - inAtFrame,
		fps,
		config: theme.motion.springSnappy,
		durationInFrames: 15,
	});
	const outAnim = spring({
		frame: frame - outAtFrame,
		fps,
		config: theme.motion.springSnappy,
		durationInFrames: 15,
	});
	const progress = inAnim - outAnim;
	const translateY = interpolate(progress, [0, 1], [-40, 0]);
	const opacity = interpolate(progress, [0, 1], [0, 1]);

	return (
		<div
			style={{
				position: 'absolute',
				top: '8%',
				left: '6%',
				opacity,
				transform: `translateY(${translateY}px)`,
			}}
		>
			<div
				style={{
					background: 'rgba(0,0,0,0.55)',
					borderLeft: `4px solid ${theme.colors.accent}`,
					padding: '10px 18px',
					borderRadius: 6,
				}}
			>
				<div
					style={{
						fontFamily: theme.fonts.display,
						fontWeight: 800,
						fontSize: 26,
						color: theme.colors.text,
					}}
				>
					{name}
				</div>
				<div
					style={{
						fontFamily: theme.fonts.display,
						fontWeight: 400,
						fontSize: 18,
						color: theme.colors.accent,
					}}
				>
					{business}
				</div>
			</div>
		</div>
	);
};
