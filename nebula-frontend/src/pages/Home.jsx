import { useState, useEffect } from "react";
import { fetchCards, searchCards } from "../api";
import CardGrid from "../components/CardGrid";
import Filters from "../components/Filters";

export default function Home() {
  const [cards, setCards] = useState([]);
  const [filters, setFilters] = useState({});
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    (async () => {
      if (searchTerm) {
        setCards(await searchCards(searchTerm));
      } else {
        setCards(await fetchCards(filters));
      }
    })();
  }, [filters, searchTerm]);

  return (
    <div>
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
        <Filters onChange={setFilters} />
        <input
          type="text"
          placeholder="Search cards..."
          className="p-2 rounded bg-gray-800 text-white"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>
      <CardGrid cards={cards} />
    </div>
  );
}
