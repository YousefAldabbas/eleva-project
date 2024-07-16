from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from beanie import Document, Indexed
from bson import ObjectId
from pydantic import UUID4, EmailStr, Field


def get_datetime_utc_now():
    return datetime.now(UTC)


class Person(Document):
    uuid: Annotated[UUID4, Indexed(unique=True)] = Field(default_factory=uuid4)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    email: Annotated[EmailStr, Indexed(unique=True)] = Field(max_length=255)

    created_at: datetime = Field(default_factory=get_datetime_utc_now)
    updated_at: datetime = Field(default_factory=get_datetime_utc_now)

    class Settings:
        is_root = True

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

    async def update(self, *args, **kwargs):
        self.updated_at = datetime.now(UTC)
        return await super().update(*args, **kwargs)

