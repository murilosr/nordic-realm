from datetime import timedelta
from os import name
from typing import Annotated

import httpx
import jwt
from app.auth_server.dtos.jwt_token import JWTToken
from app.auth_server.dtos.open_id_profile import OpenIdProfile
from app.auth_server.interfaces.password_authentication_provider import AuthUser

from app.auth_server.user_session import UserSession
from app.auth_server.user_session_repository import UserSessionRepository
from app.user.service import UserService
from app.user.user import User
from nordic_realm.decorators.controller import Service
from nordic_realm.di.annotations import Config


@Service()
class AuthServerService:

    GOOGLE_AUTH_CODE_EXCHANGE_URL : Annotated[str, Config("credentials.oauth.google.code_exchange_url")]
    REDIRECT_URL : Annotated[str, Config("credentials.oauth.google.redirect_url")]
    GRANT_TYPE : Annotated[str, Config("credentials.oauth.google.grant_type")]
    CLIENT_ID : Annotated[str, Config("credentials.oauth.google.client_id")]
    CLIENT_SECRET : Annotated[str, Config("credentials.oauth.google.client_secret")]
    APP_SECRET_KEY : Annotated[str, Config("credentials.secret_app_key")]

    user_session_repo : UserSessionRepository
    user_service : UserService
    
    def create_access_token(self, user_session : UserSession) -> str:
        return jwt.encode(
            payload={
                "type" : "access",
                "sid" : str(user_session.id),
                "tid" : user_session.access_token_tid,
                "exp" : user_session.created_dt + timedelta(hours=1)
            },
            key=self.APP_SECRET_KEY,
            algorithm="HS256"
        )
    
    def create_refresh_token(self, user_session : UserSession) -> str:
        # The payload below is the same as JWTToken
        # it was used this way to avoid creating the object just to convert to dict
        return jwt.encode(
            payload={
                "type" : "refresh",
                "sid" : str(user_session.id),
                "tid" : user_session.access_token_tid,
                "exp" : user_session.expiry_dt
            },
            key=self.APP_SECRET_KEY,
            algorithm="HS256"
        )
    
    def create_session(self, user_id : str, user_agent : str):
        return self.user_session_repo.save(UserSession.create(user_id, user_agent))
    
    def google_auth_api_code_exchange(self, code : str) -> OpenIdProfile:
        request_data = {
            "code" : code,
            "client_id" : self.CLIENT_ID,
            "client_secret" : self.CLIENT_SECRET,
            "grant_type" : self.GRANT_TYPE,
            "redirect_uri" : self.REDIRECT_URL
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

    def get_or_create_user_by_openid(self, profile : OpenIdProfile, login_method : str) -> User:
        user = self.user_service.find_user_by_email(profile.email)
        if user is None:
            return self.user_service.create(profile.name, profile.email)
        return user
    

