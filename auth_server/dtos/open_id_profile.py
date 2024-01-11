from pydantic import BaseModel


class OpenIdProfile(BaseModel):
    email: str
    email_verified: bool
    name: str
    picture: str
    locale: str
