from fastapi import APIRouter

from .authorization import router as authorization_router
from .candidates import router as candidate_router
from .health_check import router as health_check_router
from .users import router as user_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(user_router, prefix="/users", tags=["users"])
v1_router.include_router(candidate_router, prefix="/candidates", tags=["candidates"])
v1_router.include_router(health_check_router, prefix="/health", tags=["health check"])

v1_router.include_router(authorization_router, prefix="/auth", tags=["authorization"])
