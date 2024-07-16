import re
from typing import List
import uuid
from datetime import UTC, datetime

from app.api.v1.serializers import users as users_serializers
from app.core.constants import USER_SUPPORTED_FILTERS
from app.core.exceptions import UserEmailAlreadyExists, UserNotFound
from app.core.helpers import hash_helper
from app.models import User


async def get_all_users(
    payload: users_serializers.UserSearchSerializer,
) -> list[users_serializers.User]:
    data = payload.model_dump(exclude_none=True)

    # Filter out unsupported filters
    query = {k: v for k, v in data.items() if k in USER_SUPPORTED_FILTERS}

    skip = (data["page"] - 1) * data["page_size"]
    limit = data["page_size"]
    sort_field = data.get("sort")
    order = data.get("order")

    if sort_field:
        sort_criteria = (sort_field, 1 if order == "asc" else -1)
    else:
        # Default sort criteria
        sort_criteria = ("created_at", -1)

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
        .sort(sort_criteria)  # type: ignore
        .skip(skip)
        .limit(limit)
        .to_list()
    )


async def get_user(user_uuid: str) -> users_serializers.User:
    user = await User.find_one(
        User.uuid == uuid.UUID(user_uuid), projection_model=users_serializers.User
    )
    if not user:
        raise UserNotFound
    return user


async def create_user(
    payload: users_serializers.RegisterUserSerializer,
) -> users_serializers.User:
    data = payload.model_dump()

    user = await User.find({"email": data["email"]}).first_or_none()
    if user:
        raise UserEmailAlreadyExists

    user = await User(**data).insert()

    return users_serializers.User(**user.model_dump())


async def update_user(
    user: User, payload: users_serializers.UpdateUserSerializer
) -> users_serializers.User:
    data = payload.model_dump(exclude_none=True)
    if data.get("password"):
        data["password"] = hash_helper.get_password_hash(payload.password)

    user = await user.update({"$set": data})

    return users_serializers.User(**user.model_dump())
