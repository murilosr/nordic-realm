from pydantic import BaseModel


class PasswordAuthenticationBodyDto(BaseModel):
    username: str
    password: str
