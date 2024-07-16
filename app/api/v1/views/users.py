from typing import Any
from fastapi import APIRouter, Depends, status

from app.api.v1 import dependencies as deps
from app.api.v1.serializers import users as users_serializers
from app.api.v1.services import users as users_service
from app.core.constants import ResponseMessages
from app.core.utils import response_handler

router = APIRouter()


@router.get(
    path="",
    response_model=users_serializers.ListUserOut,
    # TODO use enum
    # dependencies=[Depends(deps.has_group("user"))],
)
async def get_all_users(
    payload: users_serializers.UserSearchSerializer = Depends(),
    msg: str = Depends(deps.message_locale(ResponseMessages.Retrieved)),
) :
    return response_handler(
        data=await users_service.get_all_users(payload),
        status=status.HTTP_200_OK,
        message=msg,
    )


@router.get("/me", response_model=users_serializers.UserOut)
async def get_user_profile(
    user: deps.AuthorizedUser,
    msg: str = Depends(deps.message_locale(ResponseMessages.Retrieved)),
) -> dict[str, Any]:
    return response_handler(
        data=users_serializers.User(**user.model_dump()),
        status=status.HTTP_200_OK,
        message=msg,
    )


@router.post("", response_model=users_serializers.UserOut)
async def create_user(
    payload: users_serializers.RegisterUserSerializer,
    msg: str = Depends(deps.message_locale(ResponseMessages.Created)),
) -> dict[str, Any]:
    return response_handler(
        data=await users_service.create_user(payload),
        status=status.HTTP_201_CREATED,
        message=msg,
    )


@router.patch("", response_model=users_serializers.UserOut)
async def update_user(
    user: deps.AuthorizedUser,
    paylaod: users_serializers.UpdateUserSerializer,
    msg: str = Depends(deps.message_locale(ResponseMessages.Updated)),
) -> dict[str, Any]:
    return response_handler(
        data=await users_service.update_user(user, paylaod),
        status=status.HTTP_202_ACCEPTED,
        message=msg,
    )


@router.get("/{user_uuid}", response_model=users_serializers.UserOut)
async def get_user(
    user_uuid: str,
    msg: str = Depends(deps.message_locale(ResponseMessages.Retrieved)),
) -> dict[str, Any]:
    return response_handler(
        data=await users_service.get_user(user_uuid),
        status=status.HTTP_200_OK,
        message=msg,
    )
