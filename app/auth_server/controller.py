
from app.auth_server.service import AuthServerService
from nordic_realm.decorators.controller import Controller, Get
from fastapi import Request


@Controller("/auth")
class AuthServerController:
    service : AuthServerService
    
    @Get("/u", public=True)
    def root(self, r : Request):
        print(r.scope.get("user"))
        return self.service.get()