from pydantic import BaseModel


class PasswordAuthenticationBodyDto(BaseModel):
    usuario: str
    senha_texto: str
