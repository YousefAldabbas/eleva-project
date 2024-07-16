from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.settings import Settings
from app.core.utils import logger
from app.models import Candidate, User


async def check_mongo_connection():
    try:
        client = AsyncIOMotorClient(Settings.MONGO_DB.uri)
        # ping mongo server
        await client.server_info()
        return True
    except Exception as e:
        logger.exception(f"MongoDB connection error: {e}", exc_info=False)
        raise e


async def init_database_connection(app: FastAPI) -> None:
    app.db = AsyncIOMotorClient(Settings.MONGO_DB.uri).get_database()  # type: ignore[attr-defined]
    await app.db.command("ping") # type: ignore[attr-defined]

    await init_beanie(app.db, document_models=[User, Candidate]) # type: ignore[arg-type]
    logger.info("Database connection established")
