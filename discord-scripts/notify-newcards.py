import json
import os
import requests

API_URL = "https://nebula-collection-api.vercel.app/cards"
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
if WEBHOOK_URL:
    print("WEBHOOK_URL detected.")
else:
    print("WEBHOOK_URL not found. Please set the DISCORD_WEBHOOK_URL environment variable.")
    exit(1)
CACHE_FILE = "discord-scripts/last_cards.json"
ERRATA_CACHE = "discord-scripts/errata_cards.json"


def load_previous_ids():
    if not os.path.exists(CACHE_FILE):
        return set()
    with open(CACHE_FILE, "r") as f:
        return set(json.load(f))
    
def load_previous_erratas():
    if not os.path.exists(ERRATA_CACHE):
        return set()
    with open(ERRATA_CACHE, "r") as f:
        return set(json.load(f))


def save_current_ids(ids):
    with open(CACHE_FILE, "w") as f:
        json.dump(list(ids), f)

def save_current_errata_ids(ids):
    with open(ERRATA_CACHE, "w") as f:
        json.dump(list(ids), f)


def send_discord_notification(card):
    image_url = card.get("image_url")
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

def send_errata_notification(card):
    image_url = card.get("image_url")
    embed = {
        "title": f"🆕 New Errata Added: {card['name']}",
        "description": (
            f"**Number:** {card['number']}\n"
            f"**Feature:** {card['feature']}\n"
            f"**Errata URL:** {card['errata_url']}\n"
            f"**Corrected Effect:** {card['effect']}"

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

    current_ids = {c["number"] for c in cards}
    previous_ids = load_previous_ids()
    current_errata_ids = {c["number"] for c in cards if c["errata_enable"]}
    previous_errata_ids = load_previous_erratas()

    new_ids = current_ids - previous_ids
    new_errata_ids = current_errata_ids - previous_errata_ids

    if not new_ids:
        print("No new cards detected.")
    if not new_errata_ids:
        print("No new errata detected.")
        return

    # Notify for each new card
    for card in cards:
        if card["number"] in new_ids:
            send_discord_notification(card)
        if card["number"] in new_errata_ids:
            send_errata_notification(card)

    # Update cache
    save_current_ids(current_ids)
    save_current_errata_ids(current_errata_ids)
    print(f"Sent notifications for {len(new_ids)} new cards.")
    print(f"Sent notifications for {len(new_errata_ids)} new errata.")


if __name__ == "__main__":
    main()
