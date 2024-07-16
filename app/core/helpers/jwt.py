import uuid
from datetime import UTC, datetime, timedelta

from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt

from app.core.enums import Group, Token
from app.core import exceptions as exc
from app.core.settings import Settings
from app.models import Candidate, User


class JWTHelper:
    def decode_token(self, token):
        return jwt.decode(
            token=token,
            key=Settings.JWT.SECRET_KEY,
            algorithms=[Settings.JWT.ALGORITHM],
        )

    def create_access_token(self, user: User | Candidate, group: Group = Group.USER):
        return self._genereate_token(user, group)

    def create_refresh_token(self, user: User | Candidate, group: Group = Group.USER):
        return self._genereate_token(user, group, timedelta(days=7))

    def _genereate_token(
        self,
        user: User | Candidate,
        group: Group,
        expires_delta: timedelta | None = None,
    ):
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(
                minutes=Settings.JWT.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode = {
            "uuid": user.uuid,
            "group": group.value,
            "scope": Token.REFRESH.value if expires_delta else Token.ACCESS.value,
            "exp": int(expire.timestamp()),
        }
        to_encode = jsonable_encoder(to_encode)
        return jwt.encode(
            to_encode,
            Settings.JWT.SECRET_KEY,
            algorithm=Settings.JWT.ALGORITHM,
        )

    async def get_user_from_token(self, token: str, group: str = Group.USER.value):
        try:
            payload = self.decode_token(token)
            self._check_user_group(payload, group)
            user_uuid = payload.get("uuid")

            if user_uuid is None:
                raise exc.InvalidTokenPayload

            if payload["scope"] != Token.ACCESS.value:
                raise exc.InvalidToken

            obj = (
                await User.find_one(User.uuid == uuid.UUID(user_uuid))
                if group == Group.USER
                else await Candidate.find_one(Candidate.uuid == uuid.UUID(user_uuid))
            )
            if not obj:
                raise exc.UserNotFound if group == Group.USER else exc.CandidateNotFound
            return obj
        except (exc.InvalidTokenPayload, exc.UserNotFound, exc.CandidateNotFound) as e:
            raise e
        except JWTError as e:
            raise exc.Unauthorized

    def _check_user_group(self, token_payload: dict, group: str):
        if token_payload["group"] != group:
            raise exc.Unauthorized

    def create_access_token_from_refresh_token(self, payload: dict):
        to_encode = {
            "uuid": payload["uuid"],
            "group": payload["group"],
            "scope": Token.ACCESS,
            "exp": int(datetime.now(UTC) + timedelta(minutes=930).timestamp()),
        }
        to_encode = jsonable_encoder(to_encode)
        return jwt.encode(
            to_encode,
            Settings.JWT.SECRET_KEY,
            algorithm=Settings.JWT.ALGORITHM,
        )

    def get_access_token_from_refresh_token(self, token: str):

        payload = self.decode_token(token)
        return self.create_access_token_from_refresh_token(payload)

    def get_expiration_time(self):

        return datetime.now(UTC) + timedelta(
            minutes=Settings.JWT.ACCESS_TOKEN_EXPIRE_MINUTES
        )


jwt_helper = JWTHelper()
