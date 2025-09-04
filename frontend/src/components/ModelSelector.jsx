export default function ModelSelector({ models, onSelect }) {
  return (
    <select
      className="border p-2 mb-4 rounded"
      onChange={(e) => onSelect(e.target.value)}
      defaultValue=""
    >
      <option value="" disabled>-- Selecciona un modelo --</option>
      {Array.isArray(models) && models.map((m) => (
        <option key={m.name} value={m.name}>{m.name}</option>
      ))}
    </select>
  );
}
