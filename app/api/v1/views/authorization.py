from fastapi import APIRouter, status
from app.api.v1.serializers import authorization as authorization_serializers
from app.api.v1.services import authorization as authorization_service
from app.core.constants.responses import ResponseMessages
from app.core.utils import response_handler

router = APIRouter()

@router.post("/login", response_model=authorization_serializers.LoginOut)
async def user_login(payload: authorization_serializers.LoginFormSerializer):
    """
    API endpoint to login user.
    """
    return response_handler(
        data=await authorization_service.user_login(payload),
        status=status.HTTP_200_OK,
        message=ResponseMessages.Retrieved,
    )


@router.post("/refresh", response_model=authorization_serializers.RefreshTokenOut)
async def refresh_token(paylaod: authorization_serializers.RefreshTokenSerializer):
    """
    API endpoint to refresh token.
    """
    return response_handler(
        data=await authorization_service.refresh_token(paylaod),
        status=status.HTTP_200_OK,
        message=ResponseMessages.Retrieved,
    )
