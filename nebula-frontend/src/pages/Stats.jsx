import { useEffect, useState } from "react";
import { fetchStats } from "../api";

export default function Stats() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchStats().then(setStats);
  }, []);

  if (!stats) return <p>Loading stats...</p>;

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Card Database Stats</h2>
      <p>Total Cards: {stats.total_cards}</p>

      <div>
        <h3 className="text-xl font-semibold mb-2">Rarity Distribution</h3>
        <ul>
          {Object.entries(stats.rarity_distribution).map(([r, c]) => (
            <li key={r}>{r || "Unknown"}: {c}</li>
          ))}
        </ul>
      </div>

      <div>
        <h3 className="text-xl font-semibold mb-2">Feature Distribution</h3>
        <ul>
          {Object.entries(stats.feature_distribution).map(([r, c]) => (
            <li key={r}>{r || "Unknown"}: {c}</li>
          ))}
        </ul>
      </div>

      <div>
        <h3 className="text-xl font-semibold mb-2">Top 25 Characters</h3>
        <ul>
          {Object.entries(stats.top_25_characters).map(([n, c]) => (
            <li key={n}>{n}: {c}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
