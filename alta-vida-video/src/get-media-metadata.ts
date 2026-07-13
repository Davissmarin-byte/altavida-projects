import { Input, ALL_FORMATS, UrlSource } from 'mediabunny';

export const getMediaMetadata = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src, { getRetryDelay: () => null }),
  });
  const durationInSeconds = await input.computeDuration();
  const videoTrack = await input.getPrimaryVideoTrack();
  if (!videoTrack) {
    throw new Error('No se encontro pista de video en ' + src);
  }
  return {
    durationInSeconds,
    dimensions: {
      width: videoTrack.displayWidth,
      height: videoTrack.displayHeight,
    },
  };
};
