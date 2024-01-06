from datetime import datetime
from typing import Annotated
from uuid import uuid4

from beanie import Document, Indexed
from bson import ObjectId
from pydantic import UUID4, EmailStr, Field


class User(Document):
    uuid: Annotated[UUID4, Indexed(unique=True)] = Field(default_factory=uuid4)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    email: Annotated[EmailStr, Indexed(unique=True)] = Field(max_length=255)
    password: str = Field(max_length=255)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "users"

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "uuid": "5f2f7b9f-0c5e-4d9e-9f2d-5b2f7b9f0c5e",
                "first_name": "Yousef",
                "last_name": "Aldabbas",
                "email": "YousefAldabbas0@dummy.com",
            }
        }

    async def update(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return await super().update(*args, **kwargs)
