export default function Filters({ onChange }) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    onChange((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="flex flex-wrap gap-3 mb-4">
      <select
        name="rarity"
        onChange={handleChange}
        className="nebula-panel p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">All Rarities</option>
        <option value="R">R</option>
        <option value="U">U</option>
        <option value="RR">RR</option>
        <option value="SR">SR</option>
      </select>

      <select
        name="feature"
        onChange={handleChange}
        className="nebula-panel p-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">All Features</option>
        <option value="Ultra Hero">Ultra Hero</option>
        <option value="Kaiju">Kaiju</option>
        <option value="Scene">Scene</option>
      </select>
    </div>
  );
}
