from typing import TypeAlias

from app.usuario.usuario import Usuario
from auth_server.fastapi.dependencies import AbstractUseSession

UseSession: TypeAlias = AbstractUseSession[Usuario]
