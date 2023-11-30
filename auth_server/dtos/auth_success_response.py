from pydantic import BaseModel


class AuthSuccessResponse(BaseModel):

    access_token : str
    refresh_token : str
    