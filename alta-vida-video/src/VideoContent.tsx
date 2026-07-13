import { Sequence, useVideoConfig } from 'remotion';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
// Musica de fondo: por ahora no hay .mp3 (segun tu configuracion). Cuando tengas uno:
// 1) Pega el archivo en public/music.mp3
// 2) Descomenta este import:
// import { Audio } from '@remotion/media';
// import { staticFile, interpolate } from 'remotion';
import { KenBurnsClip } from './components/KenBurnsClip';
import { OnScreenText } from './components/OnScreenText';
import { LowerThird } from './components/LowerThird';
import { ProgressBar } from './components/ProgressBar';
import { Outro } from './components/Outro';
import { hook, midTexts, lowerThird, brand } from './content';
import { theme } from './theme';

export const TRANSITION_DURATION_IN_FRAMES = 20;
export const OUTRO_DURATION_IN_SECONDS = 3;

export const VideoContent: React.FC<{
  format: 'vertical' | 'horizontal';
  clipDurationInFrames: number;
}> = ({ format, clipDurationInFrames }) => {
  const { fps } = useVideoConfig();
  const outroDurationInFrames = Math.round(fps * OUTRO_DURATION_IN_SECONDS);
  const sec = (s: number) => Math.round(s * fps);

  const lowerThirdStart = sec(lowerThird.startSec);
  const lowerThirdEnd = clipDurationInFrames - sec(lowerThird.endOffsetFromClipEndSec);
  const lowerThirdDuration = Math.max(0, lowerThirdEnd - lowerThirdStart);

  return (
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={clipDurationInFrames}>
        {/*
          Bloque de audio (musica de fondo) — listo para activar, hoy sin musica:
          <Audio
            src={staticFile('music.mp3')}
            loop
            loopVolumeCurveBehavior="extend"
            volume={(f) =>
              interpolate(
                f,
                [0, fps, clipDurationInFrames - fps, clipDurationInFrames],
                [0, 0.12, 0.12, 0],
                { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
              )
            }
          />
        */}
        <KenBurnsClip format={format} />
        <ProgressBar />
        <Sequence from={sec(hook.startSec)} durationInFrames={sec(hook.durationSec)} layout="none">
          <OnScreenText
            text={hook.text}
            fontSize={theme.hook.fontSize}
            durationInFrames={sec(hook.durationSec)}
            highlightLastWords={1}
            position="center"
          />
        </Sequence>
        {midTexts.map((block, i) => (
          <Sequence
            key={i}
            from={sec(block.startSec)}
            durationInFrames={sec(block.durationSec)}
            layout="none"
          >
            <OnScreenText
              text={block.text}
              fontSize={theme.caption.fontSize}
              durationInFrames={sec(block.durationSec)}
              position="lower-center"
            />
          </Sequence>
        ))}
        {lowerThirdDuration > 0 && (
          <Sequence from={lowerThirdStart} durationInFrames={lowerThirdDuration} layout="none">
            <LowerThird name={brand.name} durationInFrames={lowerThirdDuration} />
          </Sequence>
        )}
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition
        timing={linearTiming({ durationInFrames: TRANSITION_DURATION_IN_FRAMES })}
        presentation={fade()}
      />
      <TransitionSeries.Sequence durationInFrames={outroDurationInFrames}>
        <Outro />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
