import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise SystemExit("DATABASE_URL is missing. Check backend/.env")

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';"
        )
        print(cur.fetchone())