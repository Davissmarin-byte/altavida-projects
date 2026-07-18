import React from 'react';
import {Freeze, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {theme} from '../theme';

type Props = {
	src: string;
	durationInFrames: number;
	muted?: boolean;
	volume?: number;
	// Frame (relativo a esta Sequence) donde debe caer el punch-in. Omitir = sin punch-in.
	punchAtFrame?: number;
	// trimBefore está en FRAMES para OffthreadVideo (unidad confirmada: coincide con el
	// startFrom/endAt heredado, ver props.d.ts de remotion/dist/cjs/video/props.d.ts).
	trimBefore?: number;
	// Congela el video en este frame (propio del clip) y lo mantiene fijo el resto de la
	// Sequence — el zoom Ken Burns sigue animando sobre esa imagen fija. Útil para recortar
	// contenido que se ve mal más adelante en el clip (p. ej. el dron entrando en cuadro).
	freezeAtFrame?: number;
};

export const KenBurnsClip: React.FC<Props> = ({
	src,
	durationInFrames,
	muted = false,
	volume = 1,
	punchAtFrame,
	trimBefore,
	freezeAtFrame,
}) => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();

	const kenBurnsScale = interpolate(frame, [0, durationInFrames], theme.motion.kenBurnsScale, {
		extrapolateRight: 'clamp',
	});
	const kenBurnsX = interpolate(frame, [0, durationInFrames], [0, -30], {
		extrapolateRight: 'clamp',
	});

	let punchScale = 1;
	if (punchAtFrame !== undefined) {
		const punch = spring({
			frame: frame - punchAtFrame,
			fps,
			config: theme.motion.springSnappy,
			durationInFrames: 10,
		});
		punchScale = interpolate(punch, [0, 1], [1, theme.motion.punchInScale]);
	}

	const video = (
		<OffthreadVideo
			src={staticFile(src)}
			muted={muted}
			volume={volume}
			trimBefore={trimBefore}
			style={{objectFit: 'cover', width: '100%', height: '100%'}}
		/>
	);

	return (
		<div style={{overflow: 'hidden', width: '100%', height: '100%'}}>
			<div
				style={{
					width: '100%',
					height: '100%',
					transform: `scale(${kenBurnsScale * punchScale}) translateX(${kenBurnsX}px)`,
				}}
			>
				{freezeAtFrame !== undefined ? (
					<Freeze frame={freezeAtFrame} active={frame >= freezeAtFrame}>
						{video}
					</Freeze>
				) : (
					video
				)}
			</div>
		</div>
	);
};
