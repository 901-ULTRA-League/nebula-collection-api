import pytest
from fastapi.exceptions import ResponseValidationError
from fastapi.testclient import TestClient
from nebula_api import app

client = TestClient(app)
KNOWN_CHARACTER_NAMES = [
    "AGUL", "ALIEN BALTAN", "ALIEN METRON", "ARC", "BAZANGA", "BELIAL",
    "BEMULAR", "BLAZAR", "BLU", "C.O.V.", "DARK LUGIEL", "DARK MEPHISTO",
    "DARKLOPS ZERO", "DECKER", "DESTROYER", "DINOZOLE", "DUGRID", "DYNA",
    "ELEKING", "EMI", "FIVE KING", "GAIA", "GAIGARAID", "GALACTRON",
    "GARGORGON", "GATANOTHOR", "GEBALGA", "GEED", "GENEGARG", "GIGANTRON",
    "GINGA", "GIVAS", "GOLBA", "GOLZA", "GOMORA", "GRAIM", "GREGORE",
    "GRIGIO BONE", "GUIL ARC", "HAYAO SATO", "HIKARI", "IZAC",
    "JUGGLUS JUGGLER", "KEN SATO", "KING OF MONS", "KUTUURA", "KYRIELOID",
    "MEBIUS", "NEO DARAMBIA", "NEXUS", "OMEGA", "ORB", "PAZUZU",
    "PEDANIUM ZETTON", "REKINESS", "ROSSO", "SATAN BIZOR", "SHAGONG",
    "SHEPHERDON", "SKULL GOMORA", "SPHERESAURUS", "TERRAPHASER",
    "THUNDER KILLER", "TIGA", "TRIGARON", "TRIGGER", "VALGENESS", "VICTORY",
    "X", "Z", "ZADIME", "ZAMSHER", "ZERO", "ZETTON", "ZOVARAS",
]


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
                "errata_enable": "/cards?errata_enable=true",
                "limit": "/cards?limit={limit} (e.g., 25)"
                }, 
            "card by number": "/card/{number}",
            "search": "/search?q={query}",
            "stats": "/stats",
            "copyright": "901 ULTRA League"
            }


def test_get_cards_no_filter():
    """Test fetching all cards without any filters."""
    response = client.get("/cards")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_cards_with_limit_filter():
    """Test limiting the number of returned cards."""
    limit = 5
    response = client.get(f"/cards?limit={limit}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= limit

@pytest.mark.parametrize(
    "rarity, expected_results",
    [
        ("C", True),
        ("U", True),
        ("R", True),
        ("RR", True),
        ("RRR", True),
        ("RRRR", True),
        ("SP", True),
        ("SSSP", True),
        ("UR", True),
        ("ExP", True),
        ("AP", True),
        ("INVALID_RARITY", False),
    ],
)
def test_get_cards_with_rarity_filter(rarity, expected_results):
    """Valid rarities should return results; invalid should return empty list."""
    response = client.get(f"/cards?rarity={rarity}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if expected_results:
        assert data, f"Expected results for rarity {rarity}"
        assert all(card["rarity"] == rarity for card in data)
    else:
        assert not data


@pytest.mark.parametrize(
    "level, expected_results",
    [("1", True), ("3", True), ("7", True), ("9", False)],
)
def test_get_cards_with_level_filter(level, expected_results):
    """Levels that exist should return results; unexpected ones should not."""
    response = client.get(f"/cards?level={level}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if expected_results:
        assert data, f"Expected results for level {level}"
        assert all(card["level"] == level for card in data)
    else:
        assert not data

@pytest.mark.parametrize(
    "round_value, expected_results",
    [("0", True), ("1", True), ("4", True), ("9", False)],
)
def test_get_cards_with_round_filter(round_value, expected_results):
    """Rounds that exist should return results; unexpected ones should not."""
    response = client.get(f"/cards?round={round_value}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if expected_results:
        assert data, f"Expected results for round {round_value}"
        assert all(card["round"] == round_value for card in data)
    else:
        assert not data


@pytest.mark.parametrize("character_name", KNOWN_CHARACTER_NAMES)
def test_get_cards_with_character_name_filter(character_name):
    """Ensure every known character name filter returns matching cards."""
    response = client.get(f"/cards?character_name={character_name}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data, f"No cards returned for character {character_name}"
    for card in data:
        assert character_name in card["character_name"]


@pytest.mark.parametrize("character_name", ["UNKNOWN", "12345", "not-a-character"])
def test_get_cards_with_character_name_filter_invalid(character_name):
    """Invalid character names should return an empty list."""
    response = client.get(f"/cards?character_name={character_name}")
    assert response.status_code == 200
    assert response.json() == []


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


@pytest.mark.parametrize(
    "type_value, expected_results",
    [
        ("ARMED", True),
        ("BASIC", True),
        ("POWER", True),
        ("SPEED", True),
        ("DEVASTATION", True),
        ("HAZARD", True),
        ("METEO", True),
        ("INVASION", True),
        ("FLYING", False),
    ],
)
def test_get_cards_with_type_filter(type_value, expected_results):
    """Valid types should return results; invalid types should not."""
    response = client.get(f"/cards?type={type_value}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if expected_results:
        assert data, f"Expected results for type {type_value}"
        assert all(type_value in card["type"] for card in data)
    else:
        assert not data


@pytest.mark.parametrize(
    "year, expected_results",
    [(1966, True), (2018, True), (2025, True), (1800, False)],
)
def test_get_cards_with_publication_year_filter(year, expected_results):
    """Publication years in the dataset should return data; out-of-range years should not."""
    response = client.get(f"/cards?publication_year={year}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if expected_results:
        assert data, f"Expected results for publication year {year}"
        assert all(card["publication_year"] == year for card in data)
    else:
        assert not data


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


def test_get_cards_number_filter_returns_expected_card():
    """Use a concrete card number to verify field normalization and errata flag."""
    response = client.get("/cards?number=BP04-031")
    assert response.status_code == 200
    data = response.json()
    assert data, "Expected at least one card for BP04-031"
    card = data[0]
    assert card["number"] == "BP04-031"
    assert card["name"] == "Ultraman Z"
    assert card["feature"] == "Ultra Hero"
    assert card["type"] == "SPEED"
    assert card["rarity"] == "U"
    assert card["level"] == "3"
    assert card["publication_year"] == 2020
    assert card["errata_enable"] is True


def test_get_cards_combined_filters_and_limit():
    """Ensure multiple filters and limit work together."""
    response = client.get("/cards?feature=Ultra Hero&rarity=R&limit=3")
    assert response.status_code == 200
    cards = response.json()
    assert cards and len(cards) <= 3
    for card in cards:
        assert card["feature"] == "Ultra Hero"
        assert card["rarity"] == "R"


def test_get_cards_limit_validation_error():
    """Invalid limit should be rejected by FastAPI validation."""
    response = client.get("/cards?limit=0")
    assert response.status_code == 422


def test_get_card_not_found_returns_error_payload():
    """
    Unexpected card ids currently trigger a FastAPI response validation error due to the response model.
    Capture that behavior explicitly so regressions are visible.
    """
    with pytest.raises(ResponseValidationError):
        client.get("/card/DOES-NOT-EXIST-999")


def test_publication_year_type_validation_error():
    """Non-integer publication year should trigger validation."""
    response = client.get("/cards?publication_year=not-a-number")
    assert response.status_code == 422


def test_search_matches_effect_text():
    """Search should inspect effect text, not just names."""
    response = client.get("/search?q=draw two cards")
    assert response.status_code == 200
    cards = response.json()
    numbers = {card["number"] for card in cards}
    assert "BP01-010" in numbers


def test_stats_totals_match_database_snapshot():
    """Verify stats payload matches expected dataset snapshot values."""
    response = client.get("/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_cards"] == 872
    assert stats["feature_distribution"].get("Ultra Hero") == 630
