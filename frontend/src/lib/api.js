// Si existe VITE_API_URL en tu .env, la usamos.
// Si no, por defecto apunta al backend en localhost:8000
const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function fetchModels() {
  const res = await fetch(`${BASE}/models/`); // 👈 importante: slash final
  if (!res.ok) {
    throw new Error(`Error fetching models: ${res.status}`);
  }
  return res.json(); // { models: [...] }
}

export async function sendChat({ model, prompt, docId }) {
  const res = await fetch(`${BASE}/chat/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model,
      prompt,
      doc_id: docId || null, // 👈 por si le mandás contexto PDF
    }),
  });
  if (!res.ok) {
    throw new Error(`Error sending chat: ${res.status}`);
  }
  return res.json(); // { message: { role, content }, ... }
}
