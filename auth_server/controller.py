import logging
from typing import Annotated

from auth_server.dtos.password_authentication_body import \
    PasswordAuthenticationBodyDto
from auth_server.service import AuthServerService
from fastapi import Body, Header
from nordic_realm.decorators.controller import Controller, Get, Post


@Controller("/auth")
class AuthServerController:
    auth_service: AuthServerService

    @Post("/login", public=True)
    def password_authentication(self, data: PasswordAuthenticationBodyDto, user_agent: Annotated[str, Header()]):
        return self.auth_service.authenticate_by_password(
            data.username,
            data.password,
            user_agent
        )

    @Post("/token/refresh", public=True)
    def refresh_token(self, refresh_token: Annotated[
        str, Body(embed=True, alias="refreshToken", validation_alias="refreshToken")]):
        return self.auth_service.use_refresh_token(
            refresh_token
        )

    @Post("/google", public=True)
    def google_oauth_code_exchange(self, code: Annotated[str, Body(embed=True)],
                                   user_agent: Annotated[str, Header()]):
        return self.auth_service.authenticate_by_google_sso(
            code,
            user_agent
        )

    @Get("/test")
    def test(self):
        return [name for name in logging.root.manager.loggerDict]
