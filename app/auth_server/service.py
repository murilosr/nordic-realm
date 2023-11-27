from datetime import datetime
from uuid import uuid4
from app.auth_server.auth_token import AuthToken
from app.auth_server.auth_token_repository import AuthTokenRepository
from nordic_realm.decorators.controller import Service


@Service()
class AuthServerService:
    repo : AuthTokenRepository
    
    def new_tokens(self, user_id : str):
        return self.repo.save(AuthToken(_id = uuid4().hex + uuid4().hex, user_id=user_id))
    
    def get(self):
        return self.repo.get_all()