import { timingSafeEqual } from "crypto";
import express from "express";
import { config } from "./config.js";
import { generateReply } from "./ai.js";

const app = express();
app.use(express.json());

function isValidWebhookSecret(provided: string | undefined): boolean {
  if (!provided) return false;
  const providedBuf = Buffer.from(provided);
  const expectedBuf = Buffer.from(config.webhookSecret);
  if (providedBuf.length !== expectedBuf.length) return false;
  return timingSafeEqual(providedBuf, expectedBuf);
}

app.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.post("/kommo/salesbot-reply", async (req, res) => {
  if (!isValidWebhookSecret(req.header("X-Webhook-Secret"))) {
    res.status(401).json({ error: "unauthorized" });
    return;
  }

  const { lead_id, lead_name, contact_name, property_title, property_url, message } = req.body ?? {};

  if (typeof message !== "string" || message.trim() === "") {
    res.status(400).json({ error: "falta el campo 'message'" });
    return;
  }

  try {
    const { text, priority, signals } = await generateReply({
      leadId: lead_id,
      leadName: lead_name,
      contactName: contact_name,
      propertyTitle: property_title,
      propertyUrl: property_url,
      message,
    });
    res.json({ text, priority, signals });
  } catch (error) {
    console.error("Error generando respuesta con IA:", error);
    res.status(502).json({ error: "no se pudo generar la respuesta" });
  }
});

app.listen(config.port, () => {
  console.log(`kommo-ai-responder escuchando en el puerto ${config.port}`);
});
