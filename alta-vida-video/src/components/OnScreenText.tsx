import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {theme} from '../theme';

type Props = {
	text: string;
	// Posición vertical del bloque de texto.
	position?: 'center' | 'top';
	fontSize?: number;
};

// Texto grande de gancho/CTA: entra con carácter (spring rebotado), legible sin sonido.
export const OnScreenText: React.FC<Props> = ({text, position = 'center', fontSize = 84}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const enter = spring({frame, fps, config: theme.motion.springBouncy, durationInFrames: 18});
	const scale = interpolate(enter, [0, 1], [0.7, 1]);
	const opacity = interpolate(enter, [0, 1], [0, 1]);

	return (
		<AbsoluteFill
			style={{
				justifyContent: position === 'center' ? 'center' : 'flex-start',
				alignItems: 'center',
				paddingTop: position === 'top' ? '14%' : 0,
			}}
		>
			<div
				style={{
					fontFamily: theme.fonts.display,
					fontWeight: 800,
					fontSize,
					color: theme.colors.text,
					WebkitTextStroke: `${theme.caption.strokeWidth}px ${theme.colors.textStroke}`,
					textAlign: 'center',
					padding: '0 8%',
					lineHeight: 1.15,
					textShadow: '0 6px 20px rgba(0,0,0,0.6)',
					transform: `scale(${scale})`,
					opacity,
				}}
			>
				{text}
			</div>
		</AbsoluteFill>
	);
};
