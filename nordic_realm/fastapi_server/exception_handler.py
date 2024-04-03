from http import HTTPStatus
from typing import Type, TYPE_CHECKING

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, InvalidTokenError
from starlette.authentication import AuthenticationError

from nordic_realm.mongo import DocumentNotFound, MultipleDocumentFound

if TYPE_CHECKING:
    from nordic_realm.application.context import ApplicationContext

cors_origins = [
    "http://localnet.thorson.tech:3000",
    "http://localhost:3000",
    "http://localnet.thorson.tech:8080",
    "http://localhost:8080",
]


def http_exception_proxy(status_code: int):
    def _internal_proxy(request: Request, exception: Exception):
        nonlocal status_code

        message = str(exception)
        classname = exception.__class__.__name__

        if isinstance(exception, HTTPException):
            status_code = exception.status_code
            message = exception.detail

        request_origin = request.headers.get("origin", None)
        headers = {}
        if request_origin and request_origin in cors_origins:
            headers = {
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Origin": request_origin,
                "Access-Control-Allow-Methods": ", ".join(("DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT",))
            }

        return JSONResponse(
            content={
                "status_code": status_code,
                "exception": classname,
                "detail": message
            },
            status_code=status_code,
            headers=headers
        )

    return _internal_proxy


class FastAPIExceptionHandler:

    @staticmethod
    def install_exception_handler(app_context: "ApplicationContext"):
        FastAPIExceptionHandler(app_context)

    def __init__(self, app_context: "ApplicationContext"):
        self.app_context = app_context
        self.app = self.app_context.fastapi_app

        self._add_jwt_errors()
        self._add_db_errors()
        self._add_generic_errors()

    def _add_batch(self, exceptions: list[Type[Exception]], status_code: int):
        for _e in exceptions:
            self.app.add_exception_handler(_e, http_exception_proxy(status_code))

    def _add_generic_errors(self):
        self._add_batch([Exception, HTTPException], HTTPStatus.INTERNAL_SERVER_ERROR)

    def _add_db_errors(self):
        self._add_batch([DocumentNotFound], HTTPStatus.NOT_FOUND)
        self._add_batch([MultipleDocumentFound], HTTPStatus.BAD_REQUEST)

    def _add_jwt_errors(self):
        self._add_batch([AuthenticationError, ExpiredSignatureError, InvalidSignatureError, InvalidTokenError],
                        HTTPStatus.UNAUTHORIZED)
