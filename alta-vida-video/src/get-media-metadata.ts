import {Input, ALL_FORMATS, UrlSource} from 'mediabunny';

// Forma esperada por calculateMetadata() en Root.tsx.
export type MediaMetadata = {
	durationInSeconds: number;
	dimensions: {width: number; height: number};
};

export const getMediaMetadata = async (src: string): Promise<MediaMetadata> => {
	const input = new Input({
		formats: ALL_FORMATS,
		source: new UrlSource(src, {getRetryDelay: () => null}),
	});

	const durationInSeconds = await input.computeDuration();
	const videoTrack = await input.getPrimaryVideoTrack();
	if (!videoTrack) {
		throw new Error(`No se encontró pista de video en ${src}`);
	}

	return {
		durationInSeconds,
		dimensions: {
			width: videoTrack.displayWidth,
			height: videoTrack.displayHeight,
		},
	};
};
