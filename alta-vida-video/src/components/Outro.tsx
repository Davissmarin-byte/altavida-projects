import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {useTheme} from '../theme-context';

export const Outro: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const theme = useTheme();

	const brandEnter = spring({frame, fps, config: theme.motion.springSnappy, durationInFrames: 15});
	const ctaEnter = spring({
		frame: frame - 10,
		fps,
		config: theme.motion.springBouncy,
		durationInFrames: 18,
	});

	return (
		<AbsoluteFill
			style={{
				background: theme.colors.bgIntro,
				justifyContent: 'center',
				alignItems: 'center',
			}}
		>
			<div
				style={{
					opacity: interpolate(brandEnter, [0, 1], [0, 1]),
					transform: `translateY(${interpolate(brandEnter, [0, 1], [20, 0])}px)`,
					textAlign: 'center',
					marginBottom: 36,
				}}
			>
				<div
					style={{
						fontFamily: theme.fonts.display,
						fontWeight: 800,
						fontSize: 40,
						color: theme.colors.text,
					}}
				>
					{theme.brand.name}
				</div>
				<div
					style={{
						fontFamily: theme.fonts.display,
						fontWeight: 400,
						fontSize: 26,
						color: theme.colors.accent,
					}}
				>
					{theme.brand.business}
				</div>
			</div>
			<div
				style={{
					opacity: interpolate(ctaEnter, [0, 1], [0, 1]),
					transform: `scale(${interpolate(ctaEnter, [0, 1], [0.8, 1])})`,
					fontFamily: theme.fonts.display,
					fontWeight: 800,
					fontSize: 56,
					color: theme.colors.accent,
					textAlign: 'center',
					padding: '0 8%',
					lineHeight: 1.2,
					WebkitTextStroke: `2px ${theme.colors.textStroke}`,
				}}
			>
				{theme.cta}
			</div>
		</AbsoluteFill>
	);
};
