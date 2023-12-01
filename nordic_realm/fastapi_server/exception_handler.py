from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from http import HTTPStatus
from typing import Type
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, InvalidTokenError
from starlette.authentication import AuthenticationError

from nordic_realm.application.context import ApplicationContext

def http_exception_proxy(status_code : int):

    def _internal_proxy(request : Request, exception : Exception):
        nonlocal status_code

        message = str(exception)
        classname = exception.__class__.__name__

        if isinstance(exception, HTTPException):
            status_code = exception.status_code
            message = exception.detail

        return JSONResponse({
                    "status_code": status_code,
                    "exception": classname,
                    "detail": message
                },
                status_code=status_code)

    return _internal_proxy

class FastAPIExceptionHandler():
    
    @staticmethod
    def install_exception_handler():
        FastAPIExceptionHandler()

    def __init__(self, app_context : ApplicationContext | None = None):
        self.app_context = app_context if app_context is not None else ApplicationContext.get()
        
        self.app = self.app_context.fastapi_app

        self._add_generic_errors()
        self._add_jwt_errors()

    def _add_batch(self, exceptions : list[Type[Exception]], status_code : int):
        for _e in exceptions:
            self.app.add_exception_handler(_e, http_exception_proxy(status_code))
    
    def _add_generic_errors(self):
        self._add_batch([Exception, HTTPException], HTTPStatus.INTERNAL_SERVER_ERROR)
    
    def _add_jwt_errors(self):
        self._add_batch([AuthenticationError, ExpiredSignatureError, InvalidSignatureError, InvalidTokenError], HTTPStatus.UNAUTHORIZED)