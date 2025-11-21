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
                "name": "/cards?name={name} (e.g., Tiga)",
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

# @pytest.mark.parametrize("rarity, expected", [
#     ("C", True),
#     ("U", True),
#     ("R", True),
#     ("RR", True),
#     ("RRR", True),
#     ("RRRR", True),
#     ("SP", True),
#     ("SSSP", True),
#     ("UR", True),
#     ("ExP", True),
#     ("AP", True),
#     ("IR", False)
# ])
def test_get_cards_with_rarity_filter():
    """Test filtering cards by rarity."""
    choices = ["C", "U", "R", "RR", "RRR", "RRRR", "SP", "SSSP", "UR", "ExP", "AP"]
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

def test_get_cards_with_round_filter():
    """Test filtering cards by round."""
    choices = ["0","1", "2", "3", "4", "5", "6"]
    random_choice = random.choice(choices)
    response = client.get("/cards?round=" + random_choice)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        for card in data:
            assert card["round"] == random_choice


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


@pytest.mark.parametrize("feature, expected", [
    ("Ultra", True),
    ("Kaiju", True),
    ("Scene", True),
    ("InvalidFeature", False)
])
def test_get_cards_with_feature_filter(feature, expected):
    """Test filtering cards by feature for both valid and invalid features."""
    response = client.get(f"/cards?feature={feature}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    if expected:
        # If we expect results, assert that the list is not empty
        assert data, f"Expected results for feature '{feature}', but got none."
        # And assert that all returned cards have the correct feature
        for card in data:
            assert feature in card["feature"]
    else:
        # If we don't expect results, assert that the list is empty
        assert not data, f"Expected no results for feature '{feature}', but got some."


def test_get_cards_with_type_filter():
    """Test filtering cards by type."""
    choices = ["ARMED", "BASIC", "POWER", "SPEED", "DEVASTATION", "HAZARD", "METEO", "INVASION"]
    random_choice = random.choice(choices)
    response = client.get("/cards?type=" + random_choice)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        for card in data:
            assert random_choice in card["type"]


def test_get_cards_with_publication_year_filter():
    """Test filtering cards by publication year."""
    choices = [1966, 1967, 1996, 1997, 1998, 1999, 2004, 2006, 2009, 2010, 2013, 2014, 2015, 2016, 2017, 2018, 2020, 2021, 2022, 2023, 2024, 2025]
    random_choice = random.choice(choices)
    response = client.get(f"/cards?publication_year={random_choice}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        for card in data:
            assert card["publication_year"] == random_choice


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


def test_get_card_errata_enabled():
    """Test fetching cards with errata enabled."""
    response = client.get("/cards?errata_enable=true")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        for card in data:
            assert card["errata_enable"] is True


# def test_get_card_not_found():
#     """Test fetching a card that does not exist."""
#     response = client.get("/card/non-existent-card-number")
#     # The API returns a 500 with an error message in the body
#     assert response.status_code == 500
#     # assert response.json().contains({"error": "Card not found"})
#     # assert "error" in response.json()
#     # assert response.json()["input"][0]["error"] == "Card not found"


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

