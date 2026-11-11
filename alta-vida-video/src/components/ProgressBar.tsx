import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { theme } from '../theme';

export const ProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const widthPct = interpolate(frame, [0, durationInFrames], [0, 100], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end' }}>
      <div style={{ height: 6, width: '100%', background: 'rgba(255,255,255,0.18)' }}>
        <div
          style={{
            height: '100%',
            width: `${widthPct}%`,
            background: theme.colors.accent,
            borderRadius: 999,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
