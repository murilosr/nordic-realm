from app.usuario.repository import UsuarioRepository
from app.usuario.usuario import Usuario
from auth_server.dtos.auth_success_response import AuthSuccessResponse
from auth_server.interfaces.password_hash_provider import PasswordHashProvider
from auth_server.service import AuthServerService
from nordic_realm.decorators.controller import Service
from nordic_realm.utils import generate_id


@Service()
class UsuarioService:
    usuario_repo: UsuarioRepository
    password_hash_provider: PasswordHashProvider
    auth_service: AuthServerService

    def create(
        self, nome: str, email: str, senha_texto: str, user_agent: str, **kwargs
    ) -> AuthSuccessResponse:
        new_user = self.usuario_repo.save(
            Usuario(
                id=generate_id(),
                nome=nome,
                sobrenome="",
                email=email,
                senha=self.password_hash_provider.hash(senha_texto),
            )
        )

        session = self.auth_service.create_session(new_user.id, user_agent)

        return self.auth_service.create_token_pack(session)

    def login(
        self, username: str, plaintext_password: str, user_agent: str
    ) -> AuthSuccessResponse:
        return self.auth_service.authenticate_by_password(
            username=username,
            plaintext_password=plaintext_password,
            user_agent=user_agent,
        )

    def get_session_usuario_info(self, user_id: str) -> Usuario:
        return self.usuario_repo.get_by_id(user_id)
