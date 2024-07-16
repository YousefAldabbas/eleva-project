from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from app.core.constants import group_maper
from app.core.enums.group import Group
from app.core.exceptions import Unauthorized
from app.core.helpers import jwt_helper
from app.models import Candidate, User

oauth2_scheme = APIKeyHeader(name="Authorization")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current user from token"""
    user = await jwt_helper.get_user_from_token(token, Group.USER)
    if user is None:
        raise Unauthorized
    return user


async def get_current_candidate(token: str = Depends(oauth2_scheme)) -> Candidate:
    """Get current candidate from token"""
    candidate = await jwt_helper.get_user_from_token(token, Group.CANDIDATE)
    if candidate is None:
        raise Unauthorized
    return candidate


def has_group(group: str):
    """Check if user has group"""

    async def _has_group(user: User | Candidate = Depends(get_current_user)):
        if not isinstance(user, group_maper[group]):
            raise Unauthorized
        return user

    return _has_group


AuthorizedUser = Annotated[User, Depends(get_current_user)]
AuthorizedCandidate = Annotated[Candidate, Depends(get_current_candidate)]
