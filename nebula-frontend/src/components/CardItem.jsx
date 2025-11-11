import { Link } from "react-router-dom";

export default function CardItem({ card }) {
  return (
    <Link to={`/card/${card.number}`}>
      <div className="nebula-panel overflow-hidden transform hover:-translate-y-1 transition duration-200 hover:shadow-blue-600/30 hover:shadow-lg">
        <img
          src={card.thumbnail_image_url}
          alt={card.name}
          className="rounded-t-xl object-cover w-full"
        />
        <div className="p-3">
          <h2 className="text-lg font-semibold text-blue-400 truncate">{card.name}</h2>
          <p className="text-sm text-gray-400">{card.rarity} • {card.feature}</p>
        </div>
      </div>
    </Link>
  );
}
