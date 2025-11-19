from __future__ import annotations

from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class Lead(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    company: Optional[str] = Field(None, max_length=150)
    message: Optional[str] = Field(None, max_length=2000)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jane@company.com",
                "company": "Acme Corp",
                "message": "We need a modern SaaS website and mobile app."
            }
        }
