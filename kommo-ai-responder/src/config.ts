import "dotenv/config";

function required(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Falta la variable de entorno requerida: ${name}`);
  }
  return value;
}

export const config = {
  port: Number(process.env.PORT ?? 3000),
  webhookSecret: required("KOMMO_WEBHOOK_SECRET"),
  anthropicApiKey: required("ANTHROPIC_API_KEY"),
  aiModel: process.env.AI_MODEL ?? "claude-sonnet-5",
  aiSystemPrompt: process.env.AI_SYSTEM_PROMPT || undefined,
};
