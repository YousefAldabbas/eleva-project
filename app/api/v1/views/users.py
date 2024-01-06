from fastapi import APIRouter, Depends, status

from app.api.v1.dependancies.validate_authorization import AuthorizedUser
from app.api.v1.serializers import users as users_serializers
from app.api.v1.services import users as users_service
from app.core.utils import response_handler

router = APIRouter()


@router.get("", response_model=users_serializers.ListUserOut)
async def get_all_users(payload: users_serializers.UserSearchSerializer = Depends()):
    """
    API endpoint to get all users based on the provided search criteria.
    """

    return response_handler(
        data=await users_service.get_all_users(payload), status=status.HTTP_200_OK
    )


@router.get("/me", response_model=users_serializers.UserOut)
async def get_current_user(user: AuthorizedUser):
    """
    API endpoint to get current user information.
    """

    return response_handler(data=user, status=status.HTTP_200_OK)


@router.post("", response_model=users_serializers.UserOut)
async def create_user(payload: users_serializers.RegisterUserSerializer):
    """
    API endpoint to create new user.
    """

    return response_handler(
        data=await users_service.create_user(payload), status=status.HTTP_201_CREATED
    )


@router.patch("", response_model=users_serializers.UserOut)
async def update_user(
    user: AuthorizedUser, paylaod: users_serializers.UpdateUserSerializer
):
    """
    API endpoint to update user information.
    """
    return response_handler(
        data=await users_service.update_user(user, paylaod),
        status=status.HTTP_202_ACCEPTED,
    )


@router.get("/{user_uuid}", response_model=users_serializers.UserOut)
async def get_user(user_uuid: str):
    """
    API endpoint to get user information by uuid.
    """
    return response_handler(
        data=await users_service.get_user(user_uuid), status=status.HTTP_200_OK
    )
