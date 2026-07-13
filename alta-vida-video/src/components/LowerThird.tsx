import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { theme } from '../theme';
import { fontFamily } from '../load-font';

// `frame` es relativo a la Sequence que envuelve este componente.
export const LowerThird: React.FC<{ name: string; durationInFrames: number }> = ({
  name,
  durationInFrames,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const inAnimation = spring({ frame, fps, config: theme.motion.springSnappy, durationInFrames: 15 });
  const outAnimation = spring({
    frame: frame - (durationInFrames - 15),
    fps,
    config: theme.motion.springSnappy,
    durationInFrames: 15,
  });
  const progress = inAnimation - outAnimation;
  const translateX = interpolate(progress, [0, 1], [-40, 0]);

  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'flex-start' }}>
      <div
        style={{
          margin: `0 0 ${theme.caption.safeBottomPct}% 6%`,
          padding: '0.6em 1.1em',
          borderRadius: 8,
          background: 'rgba(10,10,10,0.55)',
          borderLeft: `4px solid ${theme.colors.accent}`,
          opacity: progress,
          transform: `translateX(${translateX}px)`,
        }}
      >
        <span
          style={{
            fontFamily,
            fontWeight: 800,
            fontSize: 30,
            color: theme.colors.text,
          }}
        >
          {name}
        </span>
      </div>
    </AbsoluteFill>
  );
};
