import "./index.css";
import React from "react";
import { Composition, staticFile } from "remotion";
import { VideoContent, type VideoContentProps } from "./VideoContent";
import { getMediaMetadata } from "./get-media-metadata";

const FPS = 30;
const HOOK_SECONDS = 3.2;
const OUTRO_SECONDS = 2.5;
const TRANSITION_FRAMES = 20;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="VideoVertical"
        component={VideoContent}
        width={1080}
        height={1920}
        fps={FPS}
        durationInFrames={FPS * 30} // placeholder; calculateMetadata calcula el valor real
        defaultProps={
          {
            hookDurationInFrames: FPS * 3,
            mainDurationInFrames: FPS * 20,
            outroDurationInFrames: FPS * 3,
            transitionDurationInFrames: TRANSITION_FRAMES,
          } satisfies VideoContentProps
        }
        calculateMetadata={async () => {
          const [clipA, clipB] = await Promise.all([
            getMediaMetadata(staticFile("clip-a.mp4")),
            getMediaMetadata(staticFile("clip-b.mp4")),
          ]);

          const hookDurationInFrames = Math.min(
            Math.round(HOOK_SECONDS * FPS),
            Math.round(clipB.durationInSeconds * FPS),
          );
          const mainDurationInFrames = Math.round(clipA.durationInSeconds * FPS);
          const outroDurationInFrames = Math.round(OUTRO_SECONDS * FPS);

          // Las transiciones solapan escenas: la duración total no es la suma de las Sequences.
          const durationInFrames =
            hookDurationInFrames + mainDurationInFrames + outroDurationInFrames - 2 * TRANSITION_FRAMES;

          const props: VideoContentProps = {
            hookDurationInFrames,
            mainDurationInFrames,
            outroDurationInFrames,
            transitionDurationInFrames: TRANSITION_FRAMES,
          };

          return { durationInFrames, fps: FPS, props };
        }}
      />
    </>
  );
};
