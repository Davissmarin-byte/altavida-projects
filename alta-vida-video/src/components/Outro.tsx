import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { theme } from '../theme';
import { fontFamily } from '../load-font';
import { brand, cta } from '../content';

export const Outro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const brandEnter = spring({ frame, fps, config: theme.motion.springSmooth, durationInFrames: 20 });
  const ctaEnter = spring({
    frame: frame - 8,
    fps,
    config: { damping: 12 },
    durationInFrames: 20,
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.colors.bgOutro,
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          fontFamily,
          fontWeight: 800,
          fontSize: 34,
          letterSpacing: 2,
          color: theme.colors.accent,
          opacity: brandEnter,
          transform: `translateY(${(1 - brandEnter) * 16}px)`,
          marginBottom: '2em',
          textTransform: 'uppercase',
        }}
      >
        {brand.name}
      </div>
      <div
        style={{
          fontFamily,
          fontWeight: 800,
          fontSize: 58,
          textAlign: 'center',
          padding: '0 10%',
          color: theme.colors.text,
          WebkitTextStroke: `2px ${theme.colors.textStroke}`,
          opacity: ctaEnter,
          transform: `scale(${0.9 + 0.1 * ctaEnter})`,
        }}
      >
        {cta.text}
      </div>
    </AbsoluteFill>
  );
};
