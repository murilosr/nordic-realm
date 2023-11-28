from app.user.service import UserService
from nordic_realm.decorators.controller import Controller


@Controller("/user")
class UserController:

    service : UserService

    pass