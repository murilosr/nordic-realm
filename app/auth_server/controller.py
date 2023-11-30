from typing import Annotated

from fastapi import Header, Query
from app.auth_server.dtos.auth_success_response import AuthSuccessResponse
from app.auth_server.dtos.password_authentication_body import \
    PasswordAuthenticationBodyDto
from app.auth_server.interfaces.password_authentication_provider import \
    PasswordAuthenticationProvider
from app.auth_server.service import AuthServerService
from app.user.service import UserService
from nordic_realm.decorators.controller import Controller, Get, Post
import logging

@Controller("/auth")
class AuthServerController:
    pass_auth_provider : PasswordAuthenticationProvider
    auth_service : AuthServerService
    user_service : UserService
    
    @Post("/login", public=True)
    def password_authentication(self, data : PasswordAuthenticationBodyDto, user_agent : Annotated[str, Header()]):
        auth_user = self.pass_auth_provider.authenticate(data.username, data.password)
        
        user_session = self.auth_service.create_session(auth_user.identity, user_agent)
        auth_jwt = self.auth_service.create_access_token(user_session)
        refresh_jwt = self.auth_service.create_refresh_token(user_session)

        return AuthSuccessResponse(
            access_token=auth_jwt,
            refresh_token=refresh_jwt
        )
    
    @Get("/google", public=True)
    def google_oauth_code_exchange(self, code : Annotated[str, Query()], user_agent : Annotated[str, Header()]):
        openid_profile = self.auth_service.google_auth_api_code_exchange(code)
        user = self.auth_service.get_or_create_user_by_openid(openid_profile, "google")
        
        user_session = self.auth_service.create_session(user.id, user_agent)
        auth_jwt = self.auth_service.create_access_token(user_session)
        refresh_jwt = self.auth_service.create_refresh_token(user_session)

        print(AuthSuccessResponse(
            access_token=auth_jwt,
            refresh_token=refresh_jwt
        ))
        return AuthSuccessResponse(
            access_token=auth_jwt,
            refresh_token=refresh_jwt
        )
    
    @Get("/test", public=True)
    def test(self):
        return [name for name in logging.root.manager.loggerDict]
    