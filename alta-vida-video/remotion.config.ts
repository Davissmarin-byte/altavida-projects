/**
 * Note: When using the Node.JS APIs, the config file
 * doesn't apply. Instead, pass options directly to the APIs.
 *
 * All configuration options: https://remotion.dev/docs/config
 */

import { Config } from "@remotion/cli/config";
import { enableTailwind } from '@remotion/tailwind-v4';

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
Config.overrideWebpackConfig(enableTailwind);

// Entorno sin acceso a remotion.media (host bloqueado): usamos el Chrome Headless Shell
// ya preinstalado para Playwright en este contenedor en vez de que Remotion descargue el suyo.
Config.setBrowserExecutable(
  "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
);
// El trafico sale por un proxy que re-termina TLS con su propia CA (ver /root/.ccr/README.md);
// Chromium no confia en esa CA por defecto, lo que rompe la carga de Google Fonts en el render.
Config.setChromiumIgnoreCertificateErrors(true);
