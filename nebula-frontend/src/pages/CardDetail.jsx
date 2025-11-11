import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchCard } from "../api";

export default function CardDetail() {
  const { number } = useParams();
  const [card, setCard] = useState(null);

  useEffect(() => {
    fetchCard(number).then(setCard);
  }, [number]);

  if (!card) return <p>Loading card data...</p>;

  return (
    <div className="nebula-panel p-6 max-w-4xl mx-auto">
      <div className="flex flex-col md:flex-row gap-6">
        <img
          src={card.image_url}
          alt={card.name}
          className="rounded-xl card-glow w-full md:w-1/2 object-contain"
        />
        <div className="space-y-2 md:w-1/2">
          <h2 className="text-3xl font-bold text-blue-400">{card.name}</h2>
          <p className="text-gray-400">{card.number}</p>
          <div className="grid grid-cols-2 gap-y-1 text-sm">
            <span className="text-gray-400">Rarity:</span><span>{card.rarity}</span>
            <span className="text-gray-400">Feature:</span><span>{card.feature}</span>
            <span className="text-gray-400">Level:</span><span>{card.level}</span>
            <span className="text-gray-400">Character:</span><span>{card.character_name}</span>
          </div>
          <div className="mt-3">
            <h3 className="font-semibold text-blue-300">Effect</h3>
            <p>{card.effect || "No special effect."}</p>
          </div>
          <p className="italic text-gray-400 mt-2">{card.flavor_text || "No flavor text."}</p>
          <p className="text-sm text-gray-500 mt-3">
            Illustrated by {card.illustrator_name || "Unknown"} ({card.publication_year || "—"})
          </p>
        </div>
      </div>
      <div className="mt-6 text-right">
        <Link to="/" className="btn">← Back to Collection</Link>
      </div>
    </div>
  );
}
