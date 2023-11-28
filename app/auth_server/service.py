from datetime import datetime
from uuid import uuid4

import httpx
from app.auth_server.auth_token import AuthToken
from app.auth_server.auth_token_repository import AuthTokenRepository
from nordic_realm.decorators.controller import Service

GOOGLE_AUTH_CODE_EXCHANGE_URL = "https://oauth2.googleapis.com/token"
REDIRECT_URL = "http://localnet.thorson.tech:3000/auth/google"
GRANT_TYPE = "authorization_code"
CLIENT_ID = ""
CLIENT_SECRET = ""

@Service()
class AuthServerService:
    repo : AuthTokenRepository
    
    def new_tokens(self, user_id : str):
        return self.repo.save(AuthToken.create(user_id))
    
    def get(self):
        return self.repo.get_all()
    
    def google_auth_api_code_exchange(self, code : str):
        data = {
            "code" : code,
            "client_id" : CLIENT_ID,
            "client_secret" : CLIENT_SECRET,
            "grant_type" : GRANT_TYPE,
            "redirect_uri" : REDIRECT_URL
        }

        response = httpx.post(
            url=GOOGLE_AUTH_CODE_EXCHANGE_URL,
            data=data
        )

        _r = response.json()
        print(_r)
        print(response.json()["id_token"])