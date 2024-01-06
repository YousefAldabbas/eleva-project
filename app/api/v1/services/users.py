import re
import uuid
from datetime import datetime

from app.api.v1.serializers import users as users_serializers
from app.core.constants import USER_SUPPORTED_FILTERS
from app.core.exceptions import UserEmailAlreadyExists, UserNotFound
from app.core.helpers import hash_helper
from app.models import User


async def get_all_users(payload: users_serializers.UserSearchSerializer):
    """
    Async function to get all users base on the provided search criteria.

    :param payload: UserSearchSerializer
    :return: list of users
    """
    payload = payload.model_dump(exclude_none=True)

    # Filter out unsupported filters
    query = {k: v for k, v in payload.items() if k in USER_SUPPORTED_FILTERS}

    skip = (payload["page"] - 1) * payload["page_size"]
    limit = payload["page_size"]
    sort_field = payload.get("sort")
    order = payload.get("order")

    if sort_field:
        sort_criteria = [(sort_field, 1 if order == "asc" else -1)]
    else:
        # Default sort criteria
        sort_criteria = [("created_at", -1)]

    # Regex search for first_name and last_name
    # it will be case insensitive and will match any string that contains the provided value
    for key, value in query.items():
        if key in {"first_name", "last_name"}:
            query[key] = (
                {"$regex": re.escape(value), "$options": "i"} if value else None
            )
        else:
            query[key] = value

    return (
        await User.find(query, projection_model=users_serializers.User)
        .sort(sort_criteria)
        .skip(skip)
        .limit(limit)
        .to_list()
    )


async def get_user(user_uuid: str):
    """
    Async function to get user by uuid.

    :param user_uuid: user uuid
    :return: user
    """
    user = await User.find_one(
        User.uuid == uuid.UUID(user_uuid), projection_model=users_serializers.User
    )
    if not user:
        raise UserNotFound
    return user


async def create_user(payload: users_serializers.RegisterUserSerializer) -> User:
    """
    Async function to create user.

    :param payload: RegisterUserSerializer
    :return: user
    """
    data = payload.model_dump()

    user = await User.find({"email": data["email"]}).first_or_none()
    if user:
        raise UserEmailAlreadyExists

    data["password"] = hash_helper.get_password_hash(data["password"])
    user = await User(**data).insert()

    return users_serializers.User(**user.model_dump())


async def update_user(
    user: User, payload: users_serializers.UpdateUserSerializer
) -> User:
    """
    Async function to update user.

    :param user: User
    :param payload: UpdateUserSerializer
    :return: user
    """
    data = payload.model_dump(exclude_none=True)
    if data.get("password"):
        data["password"] = hash_helper.get_password_hash(payload.password)

    data["updated_at"] = datetime.utcnow()
    user = await user.update({"$set": data})

    return users_serializers.User(**user.model_dump())
