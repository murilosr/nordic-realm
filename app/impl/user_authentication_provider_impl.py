from auth_server.dtos.open_id_profile import OpenIdProfile
from auth_server.interfaces.user_authentication_provider import AuthUser, IncorrectPassword, UserAuthenticationProvider, UserNotFound
from auth_server.interfaces.password_hash_provider import PasswordHashProvider
from app.user.service import UserService
from app.user.user import User
from nordic_realm.decorators.controller import Implement
from nordic_realm.mongo.exceptions import DocumentNotFound


@Implement(base_class=UserAuthenticationProvider)
class UserAuthenticationProviderImpl:
    
    password_hash_provider : PasswordHashProvider
    user_service : UserService

    def authenticate_by_password(self, username : str, password : str):
        try:
            user = self.user_service.get_user_by_email(username)
            assert user.id is not None
        except DocumentNotFound:
            raise UserNotFound("User not found")
        
        if(not self.password_hash_provider.verify(user.password, password)):
            raise IncorrectPassword("Incorrect password")
        
        return AuthUser(user.id, user.email)
    
    def get_user_by_email(self, email : str) -> User:
        return self.user_service.get_user_by_email(email)
    
    def create_user(self, profile : OpenIdProfile) -> User:
        return self.user_service.create(profile.name, profile.email)