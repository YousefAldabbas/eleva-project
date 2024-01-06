from fastapi import APIRouter, status

from app.api.v1.serializers import authorization as authorization_serializers
from app.api.v1.services import authorization as authorization_service
from app.core.utils import response_handler

router = APIRouter()


@router.post("/candidates/login", response_model=authorization_serializers.LoginOut)
async def candidate_login(payload: authorization_serializers.LoginFormSerializer):
    """
    API endpoint to login candidate.
    """
    return response_handler(
        data=await authorization_service.candidate_login(payload),
        status=status.HTTP_200_OK,
    )


@router.post("/users/login", response_model=authorization_serializers.LoginOut)
async def user_login(payload: authorization_serializers.LoginFormSerializer):
    """
    API endpoint to login user.
    """
    return response_handler(
        data=await authorization_service.user_login(payload), status=status.HTTP_200_OK
    )
