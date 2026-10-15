import json
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
PLACES_FILE = BACKEND_DIR.parent / "data" / "places.json"

load_dotenv(BACKEND_DIR / ".env")

database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise SystemExit("DATABASE_URL is missing. Check backend/.env")

with open(PLACES_FILE, encoding="utf-8") as f:
    places = json.load(f)

COLUMNS = [
    "id",
    "name",
    "municipality",
    "category",
    "latitude",
    "longitude",
    "description",
    "estimated_cost_php",
    "opening_hours",
    "how_to_get_there",
    "best_time",
    "tags",
]

UPSERT_SQL = """
INSERT INTO places (
    id, name, municipality, category, latitude, longitude, description,
    estimated_cost_php, opening_hours, how_to_get_there, best_time, tags
)
VALUES (
    %(id)s, %(name)s, %(municipality)s, %(category)s, %(latitude)s,
    %(longitude)s, %(description)s, %(estimated_cost_php)s, %(opening_hours)s,
    %(how_to_get_there)s, %(best_time)s, %(tags)s::text[]
)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    municipality = EXCLUDED.municipality,
    category = EXCLUDED.category,
    latitude = EXCLUDED.latitude,
    longitude = EXCLUDED.longitude,
    description = EXCLUDED.description,
    estimated_cost_php = EXCLUDED.estimated_cost_php,
    opening_hours = EXCLUDED.opening_hours,
    how_to_get_there = EXCLUDED.how_to_get_there,
    best_time = EXCLUDED.best_time,
    tags = EXCLUDED.tags;
"""

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        for place in places:
            params = {column: place.get(column) for column in COLUMNS}
            if params["tags"] is None:
                params["tags"] = []
            cur.execute(UPSERT_SQL, params)
        cur.execute("SELECT count(*) FROM places;")
        total = cur.fetchone()[0]

print(f"Loaded {len(places)} place(s). Total rows in places: {total}")