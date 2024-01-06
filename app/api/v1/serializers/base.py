from pydantic import BaseModel, EmailStr, Field


class BaseUserSerializer(BaseModel):
    """Base User Serializer"""

    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
