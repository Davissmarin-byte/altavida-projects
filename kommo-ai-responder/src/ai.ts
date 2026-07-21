import Anthropic from "@anthropic-ai/sdk";
import { config } from "./config.js";

const anthropic = new Anthropic({ apiKey: config.anthropicApiKey });

const DEFAULT_SYSTEM_PROMPT = `Eres el asistente de atención al cliente de Alta Vida Inmuebles, una inmobiliaria de lujo en Cancún.
Estás respondiendo a un lead que llegó desde un anuncio en Inmuebles24.
Responde en español, de forma breve, cálida y profesional (máximo 3-4 líneas).
Usa la información de la propiedad y del lead que se te da como contexto.
Tu objetivo es resolver la duda inicial y proponer agendar una llamada o visita.
No inventes precios, ubicaciones ni características que no te hayan dado en el contexto.`;

export interface LeadContext {
  leadId?: string | number;
  leadName?: string;
  contactName?: string;
  propertyTitle?: string;
  propertyUrl?: string;
  message: string;
}

export async function generateReply(context: LeadContext): Promise<string> {
  const contextLines = [
    context.leadId ? `ID de lead: ${context.leadId}` : null,
    context.leadName ? `Anuncio/lead: ${context.leadName}` : null,
    context.contactName ? `Nombre del contacto: ${context.contactName}` : null,
    context.propertyTitle ? `Propiedad: ${context.propertyTitle}` : null,
    context.propertyUrl ? `URL: ${context.propertyUrl}` : null,
  ].filter(Boolean);

  const userMessage = [...contextLines, "", `Mensaje del lead: ${context.message}`].join("\n");

  const response = await anthropic.messages.create({
    model: config.aiModel,
    max_tokens: 400,
    system: config.aiSystemPrompt ?? DEFAULT_SYSTEM_PROMPT,
    messages: [{ role: "user", content: userMessage }],
  });

  const textBlock = response.content.find((block) => block.type === "text");
  if (!textBlock || textBlock.type !== "text") {
    throw new Error("Claude no devolvió una respuesta de texto");
  }

  return textBlock.text.trim();
}
