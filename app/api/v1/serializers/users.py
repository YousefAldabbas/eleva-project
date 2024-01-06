from typing import List, Optional
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, EmailStr, field_validator

from app.core.constants import USER_SUPPORTED_FILTERS
from app.core.enums import Order
from app.core.utils import ResponseModel

from .base import BaseUserSerializer


class RegisterUserSerializer(BaseUserSerializer):
    """Register User Serializer"""

    ...


class UserSearchSerializer(BaseModel):
    """User Search Serializer"""

    page: int = Query(1, ge=1)
    page_size: int = Query(10, ge=1, le=100)

    sort: Optional[str] = Query(None)
    order: Optional[Order] = Query(default=Order.ASC)
    first_name: Optional[str] = Query(None)
    last_name: Optional[str] = Query(None)

    @field_validator("sort")
    @classmethod
    def validate_sort(cls, v):
        """
        Validate sort field to be one of user fields
        """
        if v and v not in USER_SUPPORTED_FILTERS:
            raise ValueError("Invalid sort field")
        return v


class UpdateUserSerializer(BaseModel):
    """Update User Serializer"""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(BaseModel):
    """
    User pydantic model to be used in query projection
    """

    uuid: UUID
    first_name: str
    last_name: str
    email: str


class ListUserOut(ResponseModel):
    """List User Out Serializer to be used in response"""

    data: List[User]


class UserOut(ResponseModel):
    """User Out Serializer to be used in response"""

    data: User
