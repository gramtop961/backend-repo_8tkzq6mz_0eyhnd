from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from schemas import Lead
from database import create_document, get_documents, get_db

app = FastAPI(title="Software Company API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Health(BaseModel):
    status: str


@app.get("/", response_model=Health)
async def root() -> Health:
    return Health(status="ok")


@app.get("/test", response_model=dict)
async def test_db():
    # just try to access db name to validate connection
    db = get_db()
    return {"database": str(db.name)}


@app.post("/leads", response_model=dict)
async def create_lead(lead: Lead):
    try:
        saved = await create_document("lead", lead.model_dump())
        return {"success": True, "lead": saved}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/leads", response_model=dict)
async def list_leads(limit: int = 50):
    try:
        items = await get_documents("lead", limit=limit)
        return {"success": True, "items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
