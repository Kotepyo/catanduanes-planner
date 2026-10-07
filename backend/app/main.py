from fastapi import FastAPI

app = FastAPI(title="Catanduanes Planner API")


@app.get("/health")
def health():
    return {"status": "ok"}