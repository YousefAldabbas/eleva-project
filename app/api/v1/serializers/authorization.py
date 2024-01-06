from pydantic import BaseModel, EmailStr, Field

from app.core.utils import ResponseModel


class LoginFormSerializer(BaseModel):
    """Login Form Serializer"""

    email: EmailStr = Field(max_length=255)
    password: str = Field(max_length=255)


class LoginResponseSerializer(BaseModel):
    """Login Response Serializer"""

    access_token: str
    refresh_token: str


class LoginOut(ResponseModel):
    """Login Response"""

    data: LoginResponseSerializer
