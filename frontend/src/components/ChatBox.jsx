import { useState } from "react";

export default function ChatBox({ model, docId }) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const push = (m) => setMessages((prev) => [...prev, m]);

  const onSend = async () => {
    if (!input.trim() || !model) return;
    const userMsg = { role: "user", content: input };
    push(userMsg);
    setInput("");
    setLoading(true);
    try {
      const base = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const res = await fetch(`${base}/chat/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model,
          prompt: userMsg.content,
          doc_id: docId || null, // si no hay PDF subido, va null
        }),
      });
      const data = await res.json();
      const reply =
        data?.message?.content ??
        data?.message ??
        JSON.stringify(data);
      push({ role: "ai", content: reply });
    } catch (e) {
      console.error(e);
      push({ role: "ai", content: "⚠️ Error al consultar el modelo." });
    } finally {
      setLoading(false);
    }
  };

  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div>
      <div className="border rounded p-3 mb-3 h-72 overflow-y-auto flex flex-col">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`rounded-lg px-3 py-2 mb-2 ${
              msg.role === "user" ? "bg-blue-600 text-white ml-auto" : "bg-gray-100 text-gray-900 mr-auto"
            }`}
          >
            <b>{msg.role === "user" ? "Tú" : "AI"}:</b> {msg.content}
          </div>
        ))}
        {loading && <div className="text-sm text-gray-500">Generando respuesta…</div>}
      </div>

      <div className="flex gap-2">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKeyDown}
          className="border rounded flex-1 p-2 min-h-12"
          placeholder={model ? "Escribe tu consulta…" : "Selecciona un modelo primero"}
        />
        <button
          onClick={onSend}
          disabled={loading || !model}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white px-4 py-2 rounded font-medium"
        >
          Enviar
        </button>
      </div>
    </div>
  );
}
