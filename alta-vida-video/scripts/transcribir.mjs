import {
  installWhisperCpp,
  downloadWhisperModel,
  transcribe,
  toCaptions,
} from '@remotion/install-whisper-cpp';
import fs from 'node:fs';
import path from 'node:path';

// Versión única de Whisper.cpp usada en toda la instalación y en la transcripción.
const WHISPER_VERSION = '1.5.5';
const WHISPER_PATH = path.join(process.cwd(), 'whisper.cpp');
const MODEL = 'medium';

const inputs = [
  { audio: path.join(process.cwd(), 'public/audio-a.wav'), out: 'public/captions-a.json' },
  { audio: path.join(process.cwd(), 'public/audio-b.wav'), out: 'public/captions-b.json' },
];

const main = async () => {
  console.log('Instalando whisper.cpp...');
  await installWhisperCpp({ to: WHISPER_PATH, version: WHISPER_VERSION });

  console.log(`Descargando modelo ${MODEL}...`);
  await downloadWhisperModel({ model: MODEL, folder: WHISPER_PATH });

  for (const { audio, out } of inputs) {
    console.log(`Transcribiendo ${audio}...`);
    const { transcription } = await transcribe({
      model: MODEL,
      whisperPath: WHISPER_PATH,
      whisperCppVersion: WHISPER_VERSION,
      inputPath: audio,
      tokenLevelTimestamps: true,
      language: 'es',
    });

    const { captions } = toCaptions({ whisperCppOutput: transcription });
    fs.writeFileSync(out, JSON.stringify(captions, null, 2));
    console.log(`Escrito ${out} (${captions.length} captions)`);
    console.log('Primeros 2 captions:', JSON.stringify(captions.slice(0, 2), null, 2));
  }
};

main().catch((err) => {
  console.error('Error en la transcripción:', err);
  process.exit(1);
});
