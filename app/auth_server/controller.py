from typing import Annotated

from fastapi import Query
from app.auth_server.dtos.password_authentication_body import \
    PasswordAuthenticationBodyDto
from app.auth_server.interfaces.password_authentication_provider import \
    PasswordAuthenticationProvider
from app.auth_server.service import AuthServerService
from app.user.service import UserService
from nordic_realm.decorators.controller import Controller, Get, Post


@Controller("/auth")
class AuthServerController:
    pass_auth_provider : PasswordAuthenticationProvider
    service : AuthServerService
    user_service : UserService
    
    @Post("/login", public=True)
    def password_authentication(self, data : PasswordAuthenticationBodyDto):
        self.pass_auth_provider.authenticate(data.username, data.password)
        return {"uname" : self.pass_auth_provider.authenticate(data.username, data.password)}
    
    @Get("/google", public=True)
    def google_oauth_code_exchange(self, code : Annotated[str, Query()]):
        self.service.google_auth_api_code_exchange(code)
        return {}
    