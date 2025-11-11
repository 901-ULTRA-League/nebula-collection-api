import CardItem from "./CardItem";

export default function CardGrid({ cards }) {
  if (!cards.length) return <p>No cards found.</p>;

  return (
    <div className="grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {cards.map((card) => (
        <CardItem key={card.number} card={card} />
      ))}
    </div>
  );
}
