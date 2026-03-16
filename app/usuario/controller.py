from fastapi import Header

from app.impl.use_session import UseSession
from app.usuario.service import UsuarioService
from nordic_realm.decorators.controller import Controller, Get, Post
from nordic_realm.utils.default_base_model import DefaultBaseModel


class CreateUserRequest(DefaultBaseModel):
    nome: str
    sobrenome: str
    email: str
    senha_texto: str


class UsuarioDisconnectAllRequest(DefaultBaseModel):
    id: str


class UsuarioLoginRequest(DefaultBaseModel):
    usuario: str
    senha_texto: str


@Controller("/usuario")
class UsuarioController:
    usuario_service: UsuarioService

    @Post(path="/create", public=True)
    def create(self, payload: CreateUserRequest, user_agent: str = Header("NOT_SET")):
        return self.usuario_service.create(
            **payload.model_dump(), user_agent=user_agent
        )

    @Get("/me")
    def get_session_usuario_info(self, session: UseSession):
        return self.usuario_service.get_session_usuario_info(session.id)

    # @Post(path="/disconnect_all", public=True)
    # def disconnect_all(self, payload: UsuarioDisconnectAllRequest):
    #     return self.service.disconnect_all(**payload.model_dump())
