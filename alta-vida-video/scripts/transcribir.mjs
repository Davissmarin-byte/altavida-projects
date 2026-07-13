import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import {
  installWhisperCpp,
  downloadWhisperModel,
  transcribe,
  toCaptions,
} from '@remotion/install-whisper-cpp';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.join(__dirname, '..');

const WHISPER_VERSION = '1.5.5';
const WHISPER_PATH = path.join(projectRoot, 'whisper.cpp');
const MODEL = 'medium';

async function main() {
  console.log('Instalando whisper.cpp version', WHISPER_VERSION);
  await installWhisperCpp({ to: WHISPER_PATH, version: WHISPER_VERSION });

  console.log('Descargando modelo', MODEL);
  await downloadWhisperModel({ model: MODEL, folder: WHISPER_PATH });

  console.log('Transcribiendo audio...');
  const { transcription } = await transcribe({
    model: MODEL,
    whisperPath: WHISPER_PATH,
    whisperCppVersion: WHISPER_VERSION,
    inputPath: path.join(projectRoot, 'public', 'audio.wav'),
    tokenLevelTimestamps: true,
    language: 'es',
  });

  const { captions } = toCaptions({ whisperCppOutput: transcription });

  const outPath = path.join(projectRoot, 'public', 'captions.json');
  fs.writeFileSync(outPath, JSON.stringify(captions, null, 2));
  console.log('Guardado en', outPath);
  console.log('Total captions:', captions.length);
  console.log('Primeros 2:', JSON.stringify(captions.slice(0, 2), null, 2));
}

main().catch((e) => {
  console.error('ERROR en transcripcion:', e);
  process.exit(1);
});
