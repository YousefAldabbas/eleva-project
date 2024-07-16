import functools

import dotenv
from pydantic_settings import BaseSettings

dotenv.load_dotenv()
class MongoDBSettings(BaseSettings):

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
        extra = "ignore"


class JWTSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


class Settings:
    MONGO_DB = MongoDBSettings() # type: ignore
    JWT = JWTSettings() # type: ignore
