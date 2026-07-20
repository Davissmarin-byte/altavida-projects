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

// Solo audio-a: es la única pista que se usa en el video (clip-b se muteó en ambas
// composiciones, así que transcribirlo no serviría de nada).
const inputs = [
  { audio: path.join(process.cwd(), 'public/audio-a.wav'), out: 'public/captions-a.json' },
];

const main = async () => {
  console.log('Instalando whisper.cpp...');
  await installWhisperCpp({ to: WHISPER_PATH, version: WHISPER_VERSION });

  console.log(`Descargando modelo ${MODEL}...`);
  await downloadWhisperModel({ model: MODEL, folder: WHISPER_PATH });

  for (const { audio, out } of inputs) {
    console.log(`Transcribiendo ${audio}...`);
    // transcribe() devuelve el JSON completo de whisper.cpp (con su propio campo
    // `.transcription` adentro) — NO desestructurar aquí; toCaptions espera ese objeto
    // completo como `whisperCppOutput` (verificado leyendo to-captions.js instalado).
    const whisperCppOutput = await transcribe({
      model: MODEL,
      whisperPath: WHISPER_PATH,
      whisperCppVersion: WHISPER_VERSION,
      inputPath: audio,
      tokenLevelTimestamps: true,
      language: 'es',
    });

    const { captions } = toCaptions({ whisperCppOutput });

    // whisper.cpp a veces "alucina" una etiqueta de no-habla al final de un silencio
    // (p. ej. "[AUDIO_EN_BLANCO]") con un timestamp que excede la duración real del audio.
    // No es diálogo real: cortamos el array en el primer token "[" literal.
    const bracketIndex = captions.findIndex((c) => c.text.trim() === '[');
    const cleanCaptions = bracketIndex === -1 ? captions : captions.slice(0, bracketIndex);

    fs.writeFileSync(out, JSON.stringify(cleanCaptions, null, 2));
    console.log(`Escrito ${out} (${cleanCaptions.length} captions, ${captions.length - cleanCaptions.length} descartados por alucinación de silencio)`);
    console.log('Primeros 2 captions:', JSON.stringify(cleanCaptions.slice(0, 2), null, 2));
    console.log('Últimos 2 captions:', JSON.stringify(cleanCaptions.slice(-2), null, 2));
  }
};

main().catch((err) => {
  console.error('Error en la transcripción:', err);
  process.exit(1);
});
