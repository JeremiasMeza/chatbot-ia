import { useEffect, useState } from "react";
import ModelSelector from "./components/ModelSelector";
import ChatBox from "./components/ChatBox";
import { fetchModels } from "./lib/api";

export default function App() {
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState("");
  const [docId, setDocId] = useState("");       // 👈 nuevo
  const [uploading, setUploading] = useState(false);
  const [uploadMsg, setUploadMsg] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const data = await fetchModels();
        setModels(data?.models || []);
        if (data?.models?.length) setSelectedModel(data.models[0].name);
      } catch {}
    })();
  }, []);

  const onUploadPdf = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    setUploadMsg("");
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch(`${import.meta.env.VITE_API_URL || "/api"}/upload/`, {
        method: "POST",
        body: form,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.detail || "Error al subir PDF");
      setDocId(data.doc_id);
      setUploadMsg(`PDF indexado: ${data.filename} (${data.upserted} chunks)`);
    } catch (err) {
      setUploadMsg("Error al subir/indexar el PDF.");
      console.error(err);
    } finally {
      setUploading(false);
      e.target.value = ""; // reset input
    }
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Ollama Panel</h1>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Modelo</label>
        <ModelSelector models={models} onSelect={setSelectedModel} />
      </div>

      <div className="mb-4 flex items-center gap-3">
        <input type="file" accept="application/pdf" onChange={onUploadPdf} />
        {uploading && <span className="text-gray-600">Indexando…</span>}
        {uploadMsg && <span className="text-sm text-gray-700">{uploadMsg}</span>}
      </div>

      <ChatBox model={selectedModel} docId={docId} /> {/* 👈 pasa docId */}
    </div>
  );
}
