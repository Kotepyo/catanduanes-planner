import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.db import engine

app = FastAPI(title="Catanduanes Planner API")

frontend_origin = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/places")
def list_places():
    query = text(
        """
        SELECT id, name, municipality, category, latitude, longitude,
               description, estimated_cost_php, opening_hours,
               how_to_get_there, best_time, tags
        FROM places
        ORDER BY id
        """
    )
    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()
    return [dict(row) for row in rows]