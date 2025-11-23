import sqlite3
import pandas as pd

# === CONFIGURATION ===
CSV_FILE = "ultraman_cards.csv"       # Update this if the file name changes
DB_FILE = "ultraman_cards.db"             # Output database file name

# === LOAD CSV ===
print(f"Loading CSV: {CSV_FILE}")
df = pd.read_csv(CSV_FILE)

# === CLEAN DATA ===
# Replace NaN / Null values in all battle_power columns with 0, cast as int
# battle_cols = ['battle_power_1', 'battle_power_2', 'battle_power_3', 'battle_power_4' 'battle_power_ex']
# for col in battle_cols:
#     if col in df.columns:
#         df[col] = df[col].fillna(0).astype(int)

# # Convert key numeric columns to integers where possible
# numeric_cols = ['level', 'bundle_version', 'publication_year']
# for col in numeric_cols:
#     if col in df.columns:
#         df[col] = df[col].fillna(0).astype(int)

# === CREATE DATABASE ===
print(f"Creating database: {DB_FILE}")
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Drop and recreate table
cursor.execute("DROP TABLE IF EXISTS cards")

cursor.execute("""
CREATE TABLE cards (
    id INTEGER PRIMARY KEY,
    name TEXT,
    ruby TEXT,
    type_name TEXT,
    character_name TEXT,
    rarity TEXT,
    type TEXT,
    feature TEXT,
    level TEXT,
    round TEXT,
    battle_power_1 INTEGER,
    battle_power_2 INTEGER,
    battle_power_3 INTEGER,
    battle_power_4 INTEGER,
    battle_power_ex INTEGER,
    effect TEXT,
    flavor_text TEXT,
    section TEXT,
    bundle_version TEXT,
    serial TEXT,
    branch TEXT,
    number TEXT,
    participating_works TEXT,
    participating_works_url TEXT,
    publication_year INTEGER,
    illustrator_name TEXT,
    image_url TEXT,
    thumbnail_image_url TEXT,
    errata_enable BOOLEAN,
    errata_url TEXT
);
""")

# === INSERT DATA ===
print("Inserting card records...")
df.to_sql('cards', conn, if_exists='append', index=False)

conn.commit()
conn.close()

print(f"Database '{DB_FILE}' successfully rebuilt and populated with {len(df)} cards.")
