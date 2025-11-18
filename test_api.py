# TODO: Write additional tests for other filters and edge cases

import random
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
            "API_docs": "/docs",
            "cards": "/cards",
            "filters": {
                "rarity": "/cards?rarity={rarity} (C,U,R)",
                "level": "/cards?level={level} (1,3,7)",
                "round": "/cards?round={round} (1,2,3)",
                "character_name": "/cards?character_name={character_name} (Tiga,Zero,Dyna)",
                "feature": "/cards?feature={feature} (Ultra,Kaiju,Scene)",
                "type": "/cards?type={type} (Speed,Power,Basic)",
                "publication_year": "/cards?publication_year={year} (1996,1997,2004)",
                "number": "/cards?number={number} (BP01-001, e.g.)",
                "errata_enable": "/cards?errata_enable=true"
                }, 
            "card by number": "/card/{number}",
            "search": "/search?q={query}",
            "stats": "/stats"
            }


def test_get_cards_no_filter():
    """Test fetching all cards without any filters."""
    response = client.get("/cards")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_cards_with_rarity_filter():
    """Test filtering cards by rarity."""
    choices = ["C", "U", "R", "RR", "RRR", "RRRR", "SP", "SSSP", "UR", "ExP"]
    random_choice = random.choice(choices)
    response = client.get("/cards?rarity=" + random_choice)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        for card in data:
            assert card["rarity"] == random_choice


def test_get_cards_with_level_filter():
    """Test filtering cards by level."""
    choices = ["1", "2", "3", "4", "5", "6", "7"]
    random_choice = random.choice(choices)
    response = client.get("/cards?level=" + random_choice)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        for card in data:
            assert card["level"] == random_choice


def test_get_cards_with_character_name_filter():
    """Test filtering cards by character name."""
    choices = ["TIGA", "DYNA", "ZERO", "Z", "GAIA", "BELIAL", "GOMORA", "ZETTON", "REKINESS", "ELEKING"]
    random_choice = random.choice(choices)
    response = client.get("/cards?character_name=" + random_choice)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        for card in data:
            assert random_choice in card["character_name"]


def test_get_card_by_number():
    """Test fetching a single card by its number."""
    # First, get a valid card number from the list of all cards
    all_cards_response = client.get("/cards")
    assert all_cards_response.status_code == 200
    all_cards = all_cards_response.json()

    if all_cards:
        card_number = all_cards[0]["number"]
        response = client.get(f"/card/{card_number}")
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

