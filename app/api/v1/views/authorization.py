from typing import Any
from fastapi import APIRouter, Depends, status
from app.api.v1 import dependencies as deps
from app.api.v1.serializers import authorization as authorization_serializers
from app.api.v1.services import authorization as authorization_service
from app.core.constants.responses import ResponseMessages
from app.core.utils import response_handler

router = APIRouter()


@router.post("/login", response_model=authorization_serializers.LoginOut)
async def user_login(
    payload: authorization_serializers.LoginFormSerializer,
    msg: str = Depends(deps.message_locale(ResponseMessages.Retrieved)),
) -> dict[str, Any]:
    return response_handler(
        data=await authorization_service.user_login(payload),
        status=status.HTTP_200_OK,
        message=msg,
    )


@router.post("/refresh", response_model=authorization_serializers.RefreshTokenOut)
async def refresh_token(
    paylaod: authorization_serializers.RefreshTokenSerializer,
    msg: str = Depends(deps.message_locale(ResponseMessages.Retrieved)),
) -> dict[str, Any]:
    return response_handler(
        data=await authorization_service.refresh_token(paylaod),
        status=status.HTTP_200_OK,
        message=msg,
    )
