import './index.css';
import { Composition, staticFile } from 'remotion';
import type { CalculateMetadataFunction } from 'remotion';
import { getMediaMetadata } from './get-media-metadata';
import { VideoContent, TRANSITION_DURATION_IN_FRAMES, OUTRO_DURATION_IN_SECONDS } from './VideoContent';

const FPS = 30;

type Props = {
  src: string;
  clipDurationInFrames: number;
};

const calculateMetadata: CalculateMetadataFunction<Props> = async ({ props }) => {
  const { durationInSeconds } = await getMediaMetadata(props.src);
  const clipDurationInFrames = Math.ceil(durationInSeconds * FPS);
  const outroDurationInFrames = Math.round(FPS * OUTRO_DURATION_IN_SECONDS);
  const durationInFrames =
    clipDurationInFrames + outroDurationInFrames - TRANSITION_DURATION_IN_FRAMES;

  return {
    durationInFrames,
    fps: FPS,
    props: { ...props, clipDurationInFrames },
  };
};

const VideoVertical: React.FC<Props> = ({ clipDurationInFrames }) => (
  <VideoContent format="vertical" clipDurationInFrames={clipDurationInFrames} />
);

const VideoHorizontal: React.FC<Props> = ({ clipDurationInFrames }) => (
  <VideoContent format="horizontal" clipDurationInFrames={clipDurationInFrames} />
);

const defaultProps: Props = { src: staticFile('clip.mp4'), clipDurationInFrames: 0 };

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="VideoVertical"
        component={VideoVertical}
        fps={FPS}
        width={1080}
        height={1920}
        durationInFrames={150}
        defaultProps={defaultProps}
        calculateMetadata={calculateMetadata}
      />
      <Composition
        id="VideoHorizontal"
        component={VideoHorizontal}
        fps={FPS}
        width={1920}
        height={1080}
        durationInFrames={150}
        defaultProps={defaultProps}
        calculateMetadata={calculateMetadata}
      />
    </>
  );
};
