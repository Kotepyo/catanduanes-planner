# Catanduanes Planner

An AI travel planner for Catanduanes, Philippines. It builds a 1 to 3 day itinerary from a curated list of local places.

**Status:** in development. Backend and frontend skeletons are running locally.

## Tech stack

- Frontend: React, TypeScript, Vite
- Backend: FastAPI (Python)

## Run locally

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend (in a second terminal):

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173
