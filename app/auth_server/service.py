from typing import Annotated, ClassVar
import httpx

from app.auth_server.auth_token import AuthToken
from app.auth_server.auth_token_repository import AuthTokenRepository
from nordic_realm.application.context import ApplicationContext
from nordic_realm.decorators.controller import Service
from nordic_realm.di.annotations import Config

@Service()
class AuthServerService:

    GOOGLE_AUTH_CODE_EXCHANGE_URL : Annotated[str, Config("credentials.oauth.google.code_exchange_url")]
    REDIRECT_URL : Annotated[str, Config("credentials.oauth.google.redirect_url")]
    GRANT_TYPE : Annotated[str, Config("credentials.oauth.google.grant_type")]
    CLIENT_ID : Annotated[str, Config("credentials.oauth.google.client_id")]
    CLIENT_SECRET : Annotated[str, Config("credentials.oauth.google.client_secret")]

    auth_token_repo : AuthTokenRepository
    
    def new_tokens(self, user_id : str):
        return self.auth_token_repo.save(AuthToken.create(user_id))
    
    def get(self):
        return self.auth_token_repo.get_all()
    
    def google_auth_api_code_exchange(self, code : str):
        data = {
            "code" : code,
            "client_id" : self.CLIENT_ID,
            "client_secret" : self.CLIENT_SECRET,
            "grant_type" : self.GRANT_TYPE,
            "redirect_uri" : self.REDIRECT_URL
        }

        response = httpx.post(
            url=self.GOOGLE_AUTH_CODE_EXCHANGE_URL,
            data=data
        )

        _r = response.json()
        print(_r)
        print(response.json())