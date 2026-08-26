import React, {useCallback, useEffect, useMemo, useState} from 'react';
import {
	AbsoluteFill,
	cancelRender,
	continueRender,
	delayRender,
	staticFile,
	useCurrentFrame,
	useVideoConfig,
	spring,
} from 'remotion';
import {createTikTokStyleCaptions, type Caption, type TikTokPage} from '@remotion/captions';
import {useTheme} from './theme-context';

export const useCaptions = (jsonFileName: string): Caption[] | null => {
	const [captions, setCaptions] = useState<Caption[] | null>(null);
	const [handle] = useState(() => delayRender(`cargando-${jsonFileName}`));

	const load = useCallback(async () => {
		try {
			const res = await fetch(staticFile(jsonFileName));
			if (!res.ok) {
				// El archivo aún no fue generado por scripts/transcribir.mjs: seguimos sin subtítulos
				// en vez de romper el render (se regenerará cuando exista el JSON real).
				setCaptions([]);
				continueRender(handle);
				return;
			}
			const data = (await res.json()) as Caption[];
			setCaptions(data);
			continueRender(handle);
		} catch (e) {
			cancelRender(e);
		}
	}, [handle, jsonFileName]);

	useEffect(() => {
		load();
	}, [load]);

	return captions;
};

export const useTikTokPages = (captions: Caption[] | null): TikTokPage[] => {
	const theme = useTheme();
	return useMemo(() => {
		if (!captions || captions.length === 0) return [];
		const {pages} = createTikTokStyleCaptions({
			captions,
			combineTokensWithinMilliseconds: theme.caption.combineTokensWithinMilliseconds,
		});
		return pages;
	}, [captions, theme.caption.combineTokensWithinMilliseconds]);
};

export const CaptionPageView: React.FC<{page: TikTokPage}> = ({page}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const theme = useTheme();
	// Tiempo absoluto: token.fromMs/toMs son absolutos, frame es relativo a la Sequence de esta page.
	const absoluteTimeMs = page.startMs + (frame / fps) * 1000;
	const enter = spring({frame, fps, config: theme.motion.springSnappy, durationInFrames: 8});

	return (
		<AbsoluteFill
			style={{
				justifyContent: 'flex-end',
				alignItems: 'center',
				paddingBottom: `${theme.caption.safeBottomPct}%`,
			}}
		>
			<div
				style={{
					fontSize: theme.caption.fontSize,
					fontWeight: theme.caption.fontWeight,
					fontFamily: theme.fonts.display,
					textAlign: 'center',
					whiteSpace: 'pre-wrap',
					WebkitTextStroke: `${theme.caption.strokeWidth}px ${theme.colors.textStroke}`,
					padding: '0 6%',
					transform: `scale(${0.96 + 0.04 * enter})`,
					textShadow: '0 4px 16px rgba(0,0,0,0.55)',
				}}
			>
				{page.tokens.map((token) => {
					const active = token.fromMs <= absoluteTimeMs && token.toMs > absoluteTimeMs;
					return (
						<span
							key={token.fromMs}
							style={{
								color: active ? theme.colors.accent : theme.colors.text,
								display: 'inline-block',
								transform: active ? 'scale(1.12)' : 'scale(1)',
							}}
						>
							{token.text}
						</span>
					);
				})}
			</div>
		</AbsoluteFill>
	);
};
