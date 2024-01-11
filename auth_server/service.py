from datetime import timedelta
from os import name
from typing import Annotated

import httpx
import jwt
from starlette.authentication import AuthenticationError

from auth_server.dtos.auth_success_response import AuthSuccessResponse
from auth_server.dtos.jwt_token import JWTToken
from auth_server.dtos.open_id_profile import OpenIdProfile
from auth_server.interfaces.user_authentication_provider import (
    UserAuthenticationProvider, UserInterface)
from auth_server.user_session import UserSession
from auth_server.user_session_repository import UserSessionRepository
from app.user.service import UserService
from app.user.user import User
from nordic_realm.decorators.controller import Service
from nordic_realm.di.annotations import Config


@Service()
class AuthServerService:
    GOOGLE_AUTH_CODE_EXCHANGE_URL: Annotated[str, Config("credentials.oauth.google.code_exchange_url")]
    REDIRECT_URL: Annotated[str, Config("credentials.oauth.google.redirect_url")]
    GRANT_TYPE: Annotated[str, Config("credentials.oauth.google.grant_type")]
    CLIENT_ID: Annotated[str, Config("credentials.oauth.google.client_id")]
    CLIENT_SECRET: Annotated[str, Config("credentials.oauth.google.client_secret")]
    APP_SECRET_KEY: Annotated[str, Config("credentials.secret_app_key")]

    user_session_repo: UserSessionRepository
    user_auth_provider: UserAuthenticationProvider

    def create_access_token(self, user_session: UserSession) -> str:
        return jwt.encode(
            payload={
                "type": "access",
                "sid": str(user_session.id),
                "tid": user_session.access_token_tid,
                "exp": user_session.created_dt + timedelta(hours=1)
            },
            key=self.APP_SECRET_KEY,
            algorithm="HS256"
        )

    def create_refresh_token(self, user_session: UserSession) -> str:
        # The payload below is the same as JWTToken
        # it was used this way to avoid creating the object just to convert to dict
        return jwt.encode(
            payload={
                "type": "refresh",
                "sid": str(user_session.id),
                "tid": user_session.refresh_token_tid,
                "exp": user_session.expiry_dt
            },
            key=self.APP_SECRET_KEY,
            algorithm="HS256"
        )

    def create_session(self, user_id: str, user_agent: str):
        return self.user_session_repo.save(UserSession.create(user_id, user_agent))

    def google_auth_api_code_exchange(self, code: str) -> OpenIdProfile:
        request_data = {
            "code": code,
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "grant_type": self.GRANT_TYPE,
            "redirect_uri": self.REDIRECT_URL
        }

        response = httpx.post(
            url=self.GOOGLE_AUTH_CODE_EXCHANGE_URL,
            data=request_data
        )

        response_data = response.json()
        if "id_token" not in response_data:
            raise Exception(f"Request with Google API failed. Received data: {response_data}")

        profile = OpenIdProfile(**jwt.decode(
            jwt=response_data["id_token"],
            options={"verify_signature": False}
        )
                                )
        return profile

    def get_or_create_user_by_openid(self, profile: OpenIdProfile, login_method: str) -> UserInterface:
        user = self.user_auth_provider.get_user_by_email(profile.email)
        if user is None:
            return self.user_auth_provider.create_user(profile)
        return user

    def _decode_token(self, encoded_token: str) -> JWTToken:
        return JWTToken(**jwt.decode(
            jwt=encoded_token,
            key=self.APP_SECRET_KEY,
            algorithms=["HS256"]
        ))

    def use_refresh_token(self, encoded_refresh_token: str):
        try:
            jwt_token = self._decode_token(encoded_refresh_token)
            if jwt_token.type != "refresh":
                raise ValueError("Expected refresh token type")
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthenticationError("Expired token")
        except:
            raise AuthenticationError("Bad refresh token")

        session = self.user_session_repo.find_by_id(jwt_token.sid)
        if session is None:
            raise AuthenticationError("Revoked session")
        if jwt_token.tid != session.refresh_token_tid:
            raise AuthenticationError("Refresh token already used")

        session.generate_new_tokens()
        self.user_session_repo.save(session)

        new_access_token = self.create_access_token(session)
        new_refresh_token = self.create_refresh_token(session)

        return AuthSuccessResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )

    def authenticate_by_password(self, username: str, plaintext_password: str, user_agent: str):

        auth_user = self.user_auth_provider.authenticate_by_password(username, plaintext_password)

        user_session = self.create_session(auth_user.identity, user_agent)
        auth_jwt = self.create_access_token(user_session)
        refresh_jwt = self.create_refresh_token(user_session)

        return AuthSuccessResponse(
            access_token=auth_jwt,
            refresh_token=refresh_jwt
        )

    def _get_auth_success_response(self, user_session : UserSession):
        auth_jwt = self.create_access_token(user_session)
        refresh_jwt = self.create_refresh_token(user_session)

        return AuthSuccessResponse(
            access_token=auth_jwt,
            refresh_token=refresh_jwt
        )

    def authenticate_by_google_sso(self, code: str, user_agent: str):
        openid_profile = self.google_auth_api_code_exchange(code)
        user = self.get_or_create_user_by_openid(openid_profile, "google")

        user_session = self.create_session(user.id, user_agent)
        auth_jwt = self.create_access_token(user_session)
        refresh_jwt = self.create_refresh_token(user_session)

        return AuthSuccessResponse(
            access_token=auth_jwt,
            refresh_token=refresh_jwt
        )
