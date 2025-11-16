import feedparser
import requests
import json
import os

# -------------------------------------
# CONFIG
# -------------------------------------
RSS_FEED_URL = "https://www.ultramanconnection.com/feed/"
DISCORD_WEBHOOK_URL = os.environ.get("NEWS_WEBHOOK")
if DISCORD_WEBHOOK_URL:
    print("DISCORD_WEBHOOK_URL detected.")
else:
    print("DISCORD_WEBHOOK_URL not found. Please set the NEWS_WEBHOOK environment variable.")
    exit(1)
STATE_FILE = "last_rss_uc_item.json"
# -------------------------------------


def load_last_item():
    """Load the last processed RSS item GUID or published time."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                data = json.load(f)
                return data.get("last_item")
            except Exception:
                return None
    return None


def save_last_item(value):
    """Save the latest processed item GUID."""
    with open(STATE_FILE, "w") as f:
        json.dump({"last_item": value}, f, indent=2)


def send_to_discord(title, link, summary=None, image_url=None):
    """Send a formatted message to Discord via webhook."""
    data = {
        "embeds": [
            {
                "title": title,
                "url": link,
                "description": summary or "",
                "color": 0x2ECC71  # optional
            }
        ]
    }

    if image_url:
        data["embeds"][0]["image"] = {"url": image_url}

    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    response.raise_for_status()


def extract_image(entry):
    """Try to extract first image (if RSS feed includes one)."""
    if "media_content" in entry and entry.media_content:
        return entry.media_content[0].get("url")

    if "links" in entry:
        for link in entry.links:
            if link.get("type", "").startswith("image/"):
                return link.get("href")

    return None


def process_feed():
    feed = feedparser.parse(RSS_FEED_URL)
    if feed.bozo:
        print(f"Feed error: {feed.bozo_exception}")
        return

    last_item = load_last_item()
    new_items = []

    for entry in feed.entries:
        guid = entry.get("id") or entry.get("link")
        if guid == last_item:
            break
        new_items.append(entry)

    # Process newest → oldest
    for entry in reversed(new_items):
        title = entry.get("title", "No title")
        link = entry.get("link", "")
        summary = entry.get("summary", "")
        image_url = extract_image(entry)

        send_to_discord(title, link, summary, image_url)
        print(f"Sent: {title}")

    # Update state
    if new_items:
        latest_guid = new_items[0].get("id") or new_items[0].get("link")
        save_last_item(latest_guid)


if __name__ == "__main__":
    process_feed()
