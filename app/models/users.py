from pydantic import Field

from .common import Person


class User(Person):
    password: str = Field(max_length=255)

    class Settings:
        collection = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "uuid": "5f2f7b9f-0c5e-4d9e-9f2d-5b2f7b9f0c5e",
                "first_name": "Yousef",
                "last_name": "Aldabbas",
                "email": "YousefAldabbas0@dummy.com",
            }
        }

    async def insert(self):
        # Avoid circular import
        from app.core.helpers import hash_helper

        self.password = hash_helper.get_password_hash(self.password)
        return await super().insert()
