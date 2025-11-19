from __future__ import annotations

import os
from typing import Any, Dict, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "flames_app")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db


async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = get_db()
    from datetime import datetime

    data_to_insert = {
        **data,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    result = await db[collection_name].insert_one(data_to_insert)
    inserted = await db[collection_name].find_one({"_id": result.inserted_id})
    if inserted and "_id" in inserted:
        inserted["id"] = str(inserted.pop("_id"))
    return inserted or {}


async def get_documents(
    collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50
) -> list[Dict[str, Any]]:
    db = get_db()
    filter_dict = filter_dict or {}
    cursor = db[collection_name].find(filter_dict).limit(limit)
    docs = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        docs.append(doc)
    return docs
