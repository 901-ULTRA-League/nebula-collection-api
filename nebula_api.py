from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List, Optional
from pydantic import BaseModel

# ======================================================
# Pydantic model for returning card data
# ======================================================
class Card(BaseModel):
    id: int
    name: str
    type_name: Optional[str]
    character_name: Optional[str]
    rarity: Optional[str]
    type: Optional[str]
    feature: Optional[str]
    level: Optional[int]
    battle_power_1: Optional[int]
    battle_power_2: Optional[int]
    battle_power_3: Optional[int]
    battle_power_ex: Optional[int]
    effect: Optional[str]
    flavor_text: Optional[str]
    section: Optional[str]
    bundle_version: Optional[int]
    serial: Optional[int]
    branch: Optional[str]
    number: Optional[str]
    participating_works: Optional[str]
    publication_year: Optional[int]
    illustrator_name: Optional[str]
    image_url: Optional[str]
    thumbnail_image_url: Optional[str]


# ======================================================
# FastAPI app setup
# ======================================================
app = FastAPI(title="Nebula API")

# Enable CORS (so your frontend can connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======================================================
# Database helper
# ======================================================
DB_PATH = "ultraman_cards.db"

def query_db(query: str, params: tuple = ()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ======================================================
# Endpoints
# ======================================================

@app.get("/")
def read_root():
    return {"message": "Welcome to the Nebula API for ULTRAMAN!"}

@app.get("/cards", response_model=List[Card])
def get_cards(
    rarity: Optional[str] = Query(None),
    level: Optional[int] = Query(None),
    character_name: Optional[str] = Query(None),
    feature: Optional[str] = Query(None),
):
    """
    Fetch all cards or filter by rarity, level, character name, or feature (Ultra Hero, Kaiju, Scene)
    """
    query = "SELECT * FROM cards WHERE 1=1"
    params = []

    if rarity:
        query += " AND rarity = ?"
        params.append(rarity)
    if level is not None:
        query += " AND level = ?"
        params.append(level)
    if character_name:
        query += " AND character_name LIKE ?"
        params.append(f"%{character_name}%")
    if feature:
        query += " AND feature LIKE ?"
        params.append(f"%{feature}%")

    return query_db(query, tuple(params))


@app.get("/cards/{card_id}", response_model=Card)
def get_card(card_id: str):
    """Fetch a single card by Number"""
    result = query_db("SELECT * FROM cards WHERE number = ?", (card_id,))
    if not result:
        return {"error": "Card not found"}
    return result[0]


@app.get("/search", response_model=List[Card])
def search_cards(q: str):
    """Search by card name or effect text"""
    query = """
        SELECT * FROM cards
        WHERE name LIKE ? OR effect LIKE ? OR flavor_text LIKE ?
    """
    like = f"%{q}%"
    return query_db(query, (like, like, like))


@app.get("/stats")
def get_stats():
    """Return database statistics like total card count and counts by rarity/type"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM cards")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT rarity, COUNT(*) FROM cards GROUP BY rarity")
    rarity_counts = {r: c for r, c in cursor.fetchall()}

    cursor.execute("SELECT feature, COUNT(*) FROM cards GROUP BY feature")
    feature_counts = {r: c for r, c in cursor.fetchall()}

    cursor.execute("SELECT character_name, COUNT(*) FROM cards WHERE character_name <> '-' GROUP BY character_name ORDER BY COUNT(*) DESC LIMIT 25")
    top_characters = {r: c for r, c in cursor.fetchall()}

    conn.close()

    return {
        "total_cards": total,
        "rarity_distribution": rarity_counts,
        "feature_distribution": feature_counts,
        "top_25_characters": top_characters,
    }
