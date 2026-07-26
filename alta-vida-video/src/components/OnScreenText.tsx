import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { theme } from '../theme';
import { fontFamily } from '../load-font';

// Texto grande, animado palabra por palabra (entrada escalonada con spring), pensado para
// leerse sin sonido. `frame` es relativo a la Sequence que envuelve este componente.
export const OnScreenText: React.FC<{
  text: string;
  fontSize: number;
  durationInFrames: number;
  highlightLastWords?: number;
  position?: 'center' | 'lower-center';
}> = ({ text, fontSize, durationInFrames, highlightLastWords = 0, position = 'center' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = text.split(' ');

  const exitStart = durationInFrames - Math.round(fps * 0.5);
  const exitProgress = interpolate(frame, [exitStart, durationInFrames], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: position === 'center' ? 'center' : 'flex-end',
        alignItems: 'center',
        paddingBottom: position === 'lower-center' ? '32%' : 0,
      }}
    >
      <div
        style={{
          fontFamily,
          fontWeight: 800,
          fontSize,
          textAlign: 'center',
          padding: '0 8%',
          lineHeight: 1.25,
          opacity: exitProgress,
        }}
      >
        {words.map((word, i) => {
          const enter = spring({
            frame: frame - i * 3,
            fps,
            config: theme.motion.springSmooth,
            durationInFrames: 18,
          });
          const isHighlighted = i >= words.length - highlightLastWords;
          return (
            <span
              key={i}
              style={{
                display: 'inline-block',
                marginRight: '0.3em',
                color: isHighlighted ? theme.colors.accent : theme.colors.text,
                WebkitTextStroke: `${theme.caption.strokeWidth}px ${theme.colors.textStroke}`,
                textShadow: '0 4px 20px rgba(0,0,0,0.6)',
                opacity: enter,
                transform: `translateY(${interpolate(enter, [0, 1], [24, 0])}px)`,
              }}
            >
              {word}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
