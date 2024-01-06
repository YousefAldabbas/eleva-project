import uuid
from datetime import datetime, timedelta

from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt

from app.core.enums import Group, Token
from app.core.exceptions import (
    CandidateNotFound,
    InvalidToken,
    InvalidTokenPayload,
    Unauthorized,
    UserNotFound,
)
from app.core.settings import AppSettings, get_settings
from app.models import Candidate, User


class JWTHelper:
    """
    Helper class for JWT operations
    """

    def decode_token(self, token):
        """
        Decode token
        :param token:
        :return: token payload
        """
        return jwt.decode(
            token,
            get_settings(AppSettings).SECRET_KEY,
            algorithms=[get_settings(AppSettings).ALGORITHM],
        )

    def create_access_token(self, user: User | Candidate, group: Group = Group.USER):
        """
        Create access token
        :param user:
        :param group:
        """
        return self._genereate_token(user, group)

    def create_refresh_token(self, user: User | Candidate, group: Group = Group.USER):
        """ "
        Create refresh token
        :param user:
        :param group:
        """
        return self._genereate_token(user, group, timedelta(days=7))

    def _genereate_token(
        self,
        user: User | Candidate,
        group: Group,
        expires_delta: timedelta = None,
    ):
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=930)
        to_encode = {
            "uuid": user.uuid,
            "group": group.value,
            "scope": Token.ACCESS.value if not expires_delta else Token.REFRESH.value,
            "exp": int(expire.timestamp()),
        }
        to_encode = jsonable_encoder(to_encode)
        encoded_jwt = jwt.encode(
            to_encode,
            get_settings(AppSettings).SECRET_KEY,
            algorithm=get_settings(AppSettings).ALGORITHM,
        )
        return encoded_jwt

    async def get_user_from_token(self, token: str, group: str = Group.USER.value):
        """
        Get user from token
        :param token:
        :param group:
        :return: User | Candidate

        this method will raise AuthorizationException if token is invalid or user not found
        """
        try:
            payload = self.decode_token(token)
            self._check_user_group(payload, group)
            user_uuid: str = payload.get("uuid")

            if user_uuid is None:
                raise InvalidTokenPayload

            if payload["scope"] != Token.ACCESS.value:
                raise InvalidToken

            obj = (
                await User.find_one(User.uuid == uuid.UUID(user_uuid))
                if group == Group.USER
                else await Candidate.find_one(Candidate.uuid == uuid.UUID(user_uuid))
            )
            if not obj:
                raise UserNotFound if group == Group.USER else CandidateNotFound
            return obj
        except (InvalidTokenPayload, UserNotFound, CandidateNotFound) as e:
            raise e
        except JWTError as e:
            raise Unauthorized

    def _check_user_group(self, token_payload: dict, group: str):
        """
        Check if user has group
        :param token_payload:
        :param group:

        this method will raise InvalidTokenPayload if user has no group
        """
        if token_payload["group"] != group:
            raise Unauthorized

    def create_access_token_from_refresh_token(self, payload: dict):
        """
        Create access token from refresh token
        :param payload:
        :return: access token
        """
        to_encode = {
            "uuid": payload["uuid"],
            "group": payload["group"],
            "scope": Token.ACCESS,
            "exp": int(datetime.utcnow() + timedelta(minutes=930).timestamp()),
        }
        to_encode = jsonable_encoder(to_encode)
        encoded_jwt = jwt.encode(
            to_encode,
            get_settings(AppSettings).SECRET_KEY,
            algorithm=get_settings(AppSettings).ALGORITHM,
        )
        return encoded_jwt

    def get_access_token_from_refresh_token(self, token: str):
        """
        Get access token from refresh token
        :param token:
        :return: access token
        """
        payload = self.decode_token(token)
        return self.create_access_token_from_refresh_token(payload)


jwt_helper = JWTHelper()
