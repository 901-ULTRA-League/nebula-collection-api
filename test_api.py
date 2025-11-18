import pytest
from fastapi.testclient import TestClient
from nebula_api import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Nebula API for ULTRAMAN!",
        "documentation": "/docs",
        "cards": "/cards",
        "cards by number": "/cards/{card_id}",
        "search": "/search?q={query}",
        "stats": "/stats",
    }


def test_get_cards_no_filter():
    """Test fetching all cards without any filters."""
    response = client.get("/cards")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_cards_with_rarity_filter():
    """Test filtering cards by rarity."""
    response = client.get("/cards?rarity=UR")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        for card in data:
            assert card["rarity"] == "UR"


def test_get_cards_with_level_filter():
    """Test filtering cards by level."""
    response = client.get("/cards?level=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        for card in data:
            assert card["level"] == "5"


def test_get_cards_with_character_name_filter():
    """Test filtering cards by character name."""
    # Assuming 'Ultraman' is a valid character name
    response = client.get("/cards?character_name=Ultraman")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        for card in data:
            assert "Ultraman" in card["character_name"]


def test_get_card_by_number():
    """Test fetching a single card by its number."""
    # First, get a valid card number from the list of all cards
    all_cards_response = client.get("/cards")
    assert all_cards_response.status_code == 200
    all_cards = all_cards_response.json()

    if all_cards:
        card_number = all_cards[0]["number"]
        response = client.get(f"/cards/{card_number}")
        assert response.status_code == 200
        card = response.json()
        assert card["number"] == card_number


# def test_get_card_not_found():
#     """Test fetching a card that does not exist."""
#     response = client.get("/card/non-existent-card-number")
#     # The API returns a 500 with an error message in the body
#     assert response.status_code == 500
#     assert response.json().contains({"error": "Card not found"})

def test_search_cards():
    """Test searching for cards."""
    response = client.get("/search?q=attack")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_stats():
    """Test the statistics endpoint."""
    response = client.get("/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "total_cards" in stats
    assert "rarity_distribution" in stats
    assert "feature_distribution" in stats
    assert "top_25_ultras" in stats
    assert "top_25_kaiju" in stats

