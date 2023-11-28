from app.auth_server.interfaces.password_authentication_provider import AuthUser, IncorrectPassword, PasswordAuthenticationProvider, UserNotFound
from app.auth_server.interfaces.password_hash_provider import PasswordHashProvider
from app.user.service import UserService
from nordic_realm.decorators.controller import Implement
from nordic_realm.mongo.exceptions import DocumentNotFound


@Implement(base_class=PasswordAuthenticationProvider)
class PasswordAuthenticationProviderImpl:
    
    password_hash_provider : PasswordHashProvider
    user_service : UserService

    def authenticate(self, username : str, password : str):
        try:
            user = self.user_service.get_user_by_email(username)
            assert user.id is not None
        except DocumentNotFound:
            raise UserNotFound()
        
        if(not self.password_hash_provider.verify(user.password, password)):
            raise IncorrectPassword()
        
        return AuthUser(user.id, user.email)