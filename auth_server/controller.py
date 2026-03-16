from typing import Annotated

from fastapi import Body, Header

from auth_server.dtos.password_authentication_body import PasswordAuthenticationBodyDto
from auth_server.service import AuthServerService
from nordic_realm.decorators.controller import Controller, Post


@Controller("/auth")
class AuthServerController:
    auth_service: AuthServerService

    @Post("/login", public=True)
    def password_authentication(
        self, data: PasswordAuthenticationBodyDto, user_agent: Annotated[str, Header()]
    ):
        return self.auth_service.authenticate_by_password(
            data.usuario, data.senha_texto, user_agent
        )

    @Post("/token/refresh", public=True)
    async def refresh_token(
        self,
        refresh_token: Annotated[
            str, Body(embed=True, alias="refreshToken", validation_alias="refreshToken")
        ],
    ):
        # await asyncio.sleep(3.0)
        return self.auth_service.use_refresh_token(refresh_token)
