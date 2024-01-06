import functools
from typing import TypeVar

import dotenv
from pydantic_settings import BaseSettings


class MongoDbSettings(BaseSettings):
    HOST: str
    PORT: int
    USERNAME: str
    PASSWORD: str
    DATABASE: str

    @property
    def uri(self):
        return f"mongodb://{self.HOST}:{self.PORT}/{self.DATABASE}"

    class Config:
        env_file = ".env"
        env_prefix = "MONGO_DB_"
        case_sensitive = True


class AppSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


TSettings = TypeVar("TSettings", bound=BaseSettings)


def get_settings(cls: type[TSettings]) -> TSettings:
    dotenv.load_dotenv()
    return cls()


get_settings = functools.lru_cache(get_settings)  # Mypy moment
