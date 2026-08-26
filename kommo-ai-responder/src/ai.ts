import Anthropic from "@anthropic-ai/sdk";
import { config } from "./config.js";

const anthropic = new Anthropic({ apiKey: config.anthropicApiKey });

const DEFAULT_SYSTEM_PROMPT = `Eres el asistente de atención al cliente de ALTA VIDA Inmuebles, agencia de bienes raíces de lujo en Cancún especializada en propiedades entre $3,000,000 y $23,000,000 MXN.
Estás respondiendo a un lead que llegó por un anuncio (Meta Ads, Inmuebles24 u otro canal).
Responde en español, breve (máximo 4-5 líneas), cálido, sofisticado y cercano — nunca genérico ni de call center.
Usa la información de la propiedad y del lead que se te da como contexto.

En cada conversación, sin sonar a cuestionario, busca entender estos tres puntos a lo largo del chat:
- Rango de presupuesto o si ya tiene un monto en mente.
- Forma de pago: contado o crédito/financiamiento.
- Plazo: si busca comprar pronto o está explorando.
Si el lead no mencionó ninguno de estos puntos todavía, incluye UNA sola pregunta natural sobre el más relevante según lo que haya escrito, nunca una lista de preguntas.

Tu objetivo principal es agendar una llamada o visita con un asesor humano, no cerrar la venta por chat.
No inventes precios, ubicaciones ni características que no te hayan dado en el contexto.
Nunca uses lenguaje que suene a plantilla automática; el lead debe sentir que le escribe alguien que entiende propiedades de alto nivel.`;

export interface LeadContext {
  leadId?: string | number;
  leadName?: string;
  contactName?: string;
  propertyTitle?: string;
  propertyUrl?: string;
  message: string;
}

export interface LeadReply {
  text: string;
  priority: "alta" | "normal";
  signals: string[];
}

const HIGH_VALUE_PATTERNS: Array<{ signal: string; pattern: RegExp }> = [
  { signal: "monto_alto", pattern: /\$?\s*\d{1,3}(?:[.,]\d{3})*(?:\.\d+)?\s*(?:mdp|mill?ones?|m\.?d\.?p\.?)/i },
  { signal: "monto_alto", pattern: /(?:usd|dólares|dolares|us\$)\s*\d/i },
  { signal: "forma_de_pago", pattern: /\b(contado|efectivo|cr[eé]dito|financiamiento|hipoteca|enganche)\b/i },
  { signal: "urgencia", pattern: /\b(urgente|hoy mismo|esta semana|lo antes posible|cuanto antes|ya tengo el dinero|list[oa] para comprar)\b/i },
  { signal: "quiere_visita", pattern: /\b(visita|cita|conocer la propiedad|ver la propiedad en persona|agendar)\b/i },
];

export function assessLeadPriority(message: string): { priority: "alta" | "normal"; signals: string[] } {
  const signals = [...new Set(
    HIGH_VALUE_PATTERNS.filter(({ pattern }) => pattern.test(message)).map(({ signal }) => signal),
  )];
  return { priority: signals.length > 0 ? "alta" : "normal", signals };
}

export async function generateReply(context: LeadContext): Promise<LeadReply> {
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

  const { priority, signals } = assessLeadPriority(context.message);

  return { text: textBlock.text.trim(), priority, signals };
}
