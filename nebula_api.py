from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import sqlite3
from typing import List, Optional
from pydantic import BaseModel, field_validator

# ======================================================
# Pydantic model for returning card data
# ======================================================
class Card(BaseModel):
    id: int
    name: str
    ruby: Optional[str]
    type_name: Optional[str]
    character_name: Optional[str]
    rarity: Optional[str]
    type: Optional[str]
    feature: Optional[str]
    level: Optional[str]
    @field_validator("level")
    def strip_decimal_level(cls, v): #pylint: disable=E0213
        return v[:-2] if isinstance(v, str) and v.endswith(".0") else v
    round: Optional[str]
    @field_validator("round")
    def strip_decimal_round(cls, v): #pylint: disable=E0213
        return v[:-2] if isinstance(v, str) and v.endswith(".0") else v
    battle_power_1: Optional[int]
    battle_power_2: Optional[int]
    battle_power_3: Optional[int]
    battle_power_4: Optional[int]
    battle_power_ex: Optional[int]
    effect: Optional[str]
    flavor_text: Optional[str]
    section: Optional[str]
    bundle_version: Optional[int]
    serial: Optional[int]
    branch: Optional[str]
    number: Optional[str]
    participating_works: Optional[str]
    participating_works_url: Optional[str]
    publication_year: Optional[int]
    illustrator_name: Optional[str]
    image_url: Optional[str]
    thumbnail_image_url: Optional[str]
    errata_enable: bool
    errata_url: Optional[str]


# ======================================================
# FastAPI app setup
# ======================================================
app = FastAPI(title="Nebula-API")

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
    ascii_art = r"""
      _   _      _ _         __        __         _     _ 
     | \ | |    | | |        \ \      / /        | |   | |
     |  \| | ___| | | ___     \ \ /\ / /__  _ __ | | __| |
     | . ` |/ _ \ | |/ _ \     \ V  V / _ \| '_ \| |/ _` |
     | |\  |  __/ | | (_) |     \_/\_/ (_) | | | | | (_| |
     |_| \_|\___|_|_|\___( )                 |_| |_|\__,_|
                         |/                                 
    """
    return {"message": "Welcome to the Nebula API for ULTRAMAN!",
            "documentation": "/docs",
            "cards": "/cards",
            "cards by number": "/cards/{card_id}",
            "search": "/search?q={query}",
            "stats": "/stats",
            "art": ascii_art
            }

@app.get("/favicon.png", include_in_schema=False)
async def redirect_favicon_png():
    return RedirectResponse(url="/favicon.ico", status_code=307)

@app.get("/vercel.svg", include_in_schema=False)
async def redirect_favicon_svg():
    return RedirectResponse(url="/favicon.ico", status_code=307)

@app.get("/cards", response_model=List[Card])
def get_cards(
    rarity: Optional[str] = Query(None),
    level: Optional[str] = Query(None),
    round: Optional[str] = Query(None), # pylint: disable=redefined-builtin
    character_name: Optional[str] = Query(None),
    feature: Optional[str] = Query(None),
    type: Optional[str] = Query(None), # pylint: disable=redefined-builtin
    publication_year: Optional[int] = Query(None),
    number: str = Query(None),
):
    """
    Fetch all cards or filter by rarity, level, character name, or feature (Ultra Hero, Kaiju, Scene)
    """
    query = "SELECT * FROM cards WHERE 1=1"
    params = []

    if rarity:
        query += " AND rarity LIKE ?"
        params.append(rarity)
    if level:
        query += " AND level LIKE ?"
        params.append(f"{level}%")
    if round:
        query += " AND round LIKE ?"
        params.append(f"{round}%")
    if character_name:
        query += " AND character_name LIKE ?"
        params.append(f"%{character_name}%")
    if feature:
        query += " AND feature LIKE ?"
        params.append(f"%{feature}%")
    if type:
        query += " AND type = ?"
        params.append(type)
    if publication_year:
        query += " AND publication_year = ?"
        params.append(publication_year)
    if number:
        query += " AND number LIKE ?"
        params.append(number)

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

    cursor.execute("SELECT character_name, COUNT(*) FROM cards WHERE character_name <> '-' AND feature = 'Ultra Hero' GROUP BY character_name ORDER BY COUNT(*) DESC LIMIT 25")
    top_ultras = {r: c for r, c in cursor.fetchall()}

    cursor.execute("SELECT character_name, COUNT(*) FROM cards WHERE character_name <> '-' AND feature = 'Kaiju' GROUP BY character_name ORDER BY COUNT(*) DESC LIMIT 25")
    top_kaiju = {r: c for r, c in cursor.fetchall()}

    conn.close()

    return {
        "total_cards": total,
        "rarity_distribution": rarity_counts,
        "feature_distribution": feature_counts,
        "top_25_ultras": top_ultras,
        "top_25_kaiju": top_kaiju,
    }
