from re import Pattern
from typing import Annotated

from fastapi import FastAPI
import jwt
from starlette.authentication import (AuthCredentials, AuthenticationBackend,
                                      AuthenticationError,
                                      UnauthenticatedUser, BaseUser)
from starlette.middleware.authentication import AuthenticationMiddleware
from auth_server.dtos.jwt_token import JWTToken
from auth_server.interfaces.user_authentication_provider import AuthUser
from auth_server.user_session_repository import UserSessionRepository
from app.user.repository import UserRepository

from nordic_realm.decorators.controller import Component
from nordic_realm.di.annotations import Config

@Component()
class OAuthSecurityMiddleware(AuthenticationBackend):
    
    user_repo : UserRepository
    user_session_repo : UserSessionRepository
    APP_SECRET_KEY : Annotated[str, Config("credentials.secret_app_key")]
    
    @staticmethod
    def install_middleware():
        from nordic_realm.application import ApplicationContext
        from nordic_realm.di.injector import DIInjector
        
        ApplicationContext.get().fastapi_app.add_middleware(
            AuthenticationMiddleware,
            backend=DIInjector().instance(OAuthSecurityMiddleware)
        )
    
    def _decode_token(self, jwt_encoded : str) -> JWTToken:
        try:
            return JWTToken(**jwt.decode(jwt=jwt_encoded, key=self.APP_SECRET_KEY, algorithms=["HS256"]))
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthenticationError("Expired access token. Use refresh token")
        except:
            raise AuthenticationError("Bad Authorization token")
            
    
    def _process_authorization(self, authorization_header : str | None, path_is_public : bool) -> tuple[AuthCredentials, BaseUser]:
        if authorization_header is None:
            return self._raise_error_or_return_unauthenticated("Missing Authorization header", path_is_public)
        
        auth_split = authorization_header.split(" ")
        if(len(auth_split) != 2 or auth_split[0] != "Bearer"):
            self._raise_error_or_return_unauthenticated("Bad Authorization header", path_is_public)
            
        token = self._decode_token(jwt_encoded=auth_split[1])
        session = self.user_session_repo.find_by_id(token.sid)
        if session is None:
            raise AuthenticationError("Session revoked")
        
        if session.access_token_tid != token.tid:
            raise AuthenticationError("Bad access_token_id")
        
        user = self.user_repo.get_by_id(session.user_id)

        return AuthCredentials([]), AuthUser(id=session.user_id, username=user.name)
    
    def _return_unauthenticated_credentials(self):
        return AuthCredentials([]), UnauthenticatedUser()
    
    def _raise_error_or_return_unauthenticated(self, error_msg : str, path_is_public : bool):
        if path_is_public:
            return self._return_unauthenticated_credentials()
        raise AuthenticationError(error_msg)

    
    async def authenticate(self, conn):
        app = conn.scope["app"] # type: FastAPI
        
        path = conn.scope["path"]
        slash_normalized_path : str
        if path.endswith("/"):
            slash_normalized_path = path.rstrip("/")
        else:
            slash_normalized_path = path + "/"
        
        path_is_public = False
        for _path_re in app._NR_public_paths: # type: ignore
            _path_re : Pattern
            if(_path_re.match(path) or _path_re.match(slash_normalized_path)):
                return self._return_unauthenticated_credentials()
        
        return self._process_authorization(conn.headers.get("Authorization", None), path_is_public)