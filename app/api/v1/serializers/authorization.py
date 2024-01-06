from pydantic import BaseModel, EmailStr, Field

from app.core.utils import ResponseModel


class LoginFormSerializer(BaseModel):
    """Login Form Serializer"""

    email: EmailStr = Field(max_length=255)
    password: str = Field(max_length=255)


class RefreshTokenSerializer(BaseModel):
    """Refresh Token Serializer"""

    refresh_token: str


class LoginResponseSerializer(BaseModel):
    """Login Response Serializer"""

    access_token: str
    refresh_token: str
    exp: int

class RefreshTokenResponseSerializer(BaseModel):
    """Refresh Token Response Serializer"""

    access_token: str
    exp: int

class LoginOut(ResponseModel):
    """Login Response"""

    data: LoginResponseSerializer


class RefreshTokenOut(ResponseModel):
    """Refresh Token Response"""

    data: RefreshTokenResponseSerializer