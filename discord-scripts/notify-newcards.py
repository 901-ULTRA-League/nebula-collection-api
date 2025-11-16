import json
import os
import requests

API_URL = "https://nebula-collection-api.vercel.app/cards"
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
CACHE_FILE = "discord-scripts/last_cards.json"


def load_previous_ids():
    if not os.path.exists(CACHE_FILE):
        return set()
    with open(CACHE_FILE, "r") as f:
        return set(json.load(f))


def save_current_ids(ids):
    with open(CACHE_FILE, "w") as f:
        json.dump(list(ids), f)


def send_discord_notification(card):
    image_url = card.get("image_url")
    # message = {
    #     "content": f"🆕 **New Card Added:**\n"+
    #     f"{card['name']} (ID: {card['number']})\n"+
    #     f"Rarity: {card.get('rarity')}\n"+
    #     f"Type: {card.get('type')}\n"
    # }
    embed = {
        "title": f"🆕 New Card Added: {card['name']}",
        "description": (
            f"**Number:** {card['number']}\n"
            f"**Rarity:** {card['rarity']}\n"
            f"**Feature:** {card['feature']}\n"
            # f"**Type:** {card['type']}"
        ),
        "color": 0x3498db,  # blue
    }

    if image_url:
        embed["image"] = {"url": image_url}

    payload = {
        "embeds": [embed]
    }
    requests.post(WEBHOOK_URL, json=payload)


def main():
    response = requests.get(API_URL)
    response.raise_for_status()
    cards = response.json()

    current_ids = {c["id"] for c in cards}
    previous_ids = load_previous_ids()

    new_ids = current_ids - previous_ids
    if not new_ids:
        print("No new cards detected.")
        return

    # Notify for each new card
    for card in cards:
        if card["id"] in new_ids:
            send_discord_notification(card)

    # Update cache
    save_current_ids(current_ids)
    print(f"Sent notifications for {len(new_ids)} new cards.")


if __name__ == "__main__":
    main()
