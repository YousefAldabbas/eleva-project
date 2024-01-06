from app.api.v1.serializers import authorization as authorization_serializers
from app.core.enums.group import Group
from app.core.exceptions import InvalidCredentials, UserNotFound
from app.core.helpers import hash_helper, jwt_helper
from app.models import Candidate, User


async def _login(
    payload: authorization_serializers.LoginFormSerializer, model: User | Candidate
):
    user = await model.find(model.email == str(payload.email)).first_or_none()

    if not user:
        raise UserNotFound

    if not hash_helper.verify_password(payload.password, user.password):
        raise InvalidCredentials

    group = Group.USER if isinstance(user, User) else Group.CANDIDATE
    return {
        "access_token": jwt_helper.create_access_token(user, group),
        "refresh_token": jwt_helper.create_refresh_token(user, group),
    }


async def candidate_login(payload: authorization_serializers.LoginFormSerializer):
    return await _login(payload, Candidate)


async def user_login(payload: authorization_serializers.LoginFormSerializer):
    return await _login(payload, User)


async def get_access_token_from_refresh_token(token: str):
    payload = jwt_helper.decode_token(token)
    return jwt_helper.create_access_token(payload, Group(payload.get("group")))
