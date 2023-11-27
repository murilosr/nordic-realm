from random import randint
from typing import Any
from typing_extensions import Annotated
from fastapi.params import Depends
from app.repositories.test_repository import TestRepository
from app.services.test_service import TestService
from nordic_realm.decorators.controller import Controller, Get, Post
from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm

def get_request(request : Request):
    return request

@Controller(path="/hello")
class HelloWorld:
    test_service : TestService
    
    def __init__(self):
        self.y = randint(0,10)
    
    @Get(path="/world")
    def get(self, x : Request):
        return self.test_service.get()