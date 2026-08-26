/**
 * Note: When using the Node.JS APIs, the config file
 * doesn't apply. Instead, pass options directly to the APIs.
 *
 * All configuration options: https://remotion.dev/docs/config
 */

import { existsSync } from 'fs';
import { Config } from "@remotion/cli/config";
import { enableTailwind } from '@remotion/tailwind-v4';

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
Config.overrideWebpackConfig(enableTailwind);

// Sandbox de desarrollo sin acceso a remotion.media (host bloqueado): usamos el Chrome
// Headless Shell ya preinstalado para Playwright en este contenedor en vez de que Remotion
// descargue el suyo, y desactivamos la validacion de certificados porque el trafico sale por
// un proxy que re-termina TLS con su propia CA (ver /root/.ccr/README.md), lo que rompe la
// carga de Google Fonts en el render. Ambos hacks solo se activan si ese binario existe, para
// que un render fuera de este sandbox use el Chromium normal de Remotion con TLS intacto.
const SANDBOX_CHROMIUM_PATH =
  "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell";
if (existsSync(SANDBOX_CHROMIUM_PATH)) {
  Config.setBrowserExecutable(SANDBOX_CHROMIUM_PATH);
  Config.setChromiumIgnoreCertificateErrors(true);
}
