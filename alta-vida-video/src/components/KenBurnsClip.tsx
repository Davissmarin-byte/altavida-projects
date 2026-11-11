import { AbsoluteFill, OffthreadVideo, interpolate, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { theme } from '../theme';

// El clip fuente (public/clip.mp4) es vertical (1080x1920, confirmado con ffprobe).
// En el formato horizontal no se recorta el contenido: se agrega una capa de fondo
// desenfocada y ampliada del mismo clip para llenar el marco (efecto "pillarbox" con blur),
// y el video nitido se centra con objectFit: 'contain'.
export const KenBurnsClip: React.FC<{ format: 'vertical' | 'horizontal' }> = ({ format }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const [scaleFrom, scaleTo] = theme.motion.kenBurnsScale;
  const scale = interpolate(frame, [0, durationInFrames], [scaleFrom, scaleTo], {
    extrapolateRight: 'clamp',
  });

  const sharpVideo = (
    <div
      style={{
        width: '100%',
        height: '100%',
        overflow: 'hidden',
        transform: `scale(${scale})`,
      }}
    >
      <OffthreadVideo
        src={staticFile('clip.mp4')}
        style={{
          width: '100%',
          height: '100%',
          objectFit: format === 'vertical' ? 'cover' : 'contain',
        }}
      />
    </div>
  );

  if (format === 'vertical') {
    return <AbsoluteFill style={{ backgroundColor: '#000' }}>{sharpVideo}</AbsoluteFill>;
  }

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      <AbsoluteFill style={{ overflow: 'hidden' }}>
        <OffthreadVideo
          src={staticFile('clip.mp4')}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            filter: 'blur(60px) brightness(0.55)',
            transform: 'scale(1.2)',
          }}
        />
      </AbsoluteFill>
      {sharpVideo}
    </AbsoluteFill>
  );
};
