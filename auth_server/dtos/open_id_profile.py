from pydantic import BaseModel


class OpenIdProfile(BaseModel):
    email: str
    email_verified: bool
    name: str
    given_name: str | None
    family_name: str | None
    picture: str
    locale: str
