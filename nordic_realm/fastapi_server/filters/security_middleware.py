import base64
import binascii
from re import Pattern

from fastapi import FastAPI
from starlette.authentication import (AuthCredentials, AuthenticationBackend,
                                      AuthenticationError, SimpleUser,
                                      UnauthenticatedUser)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware


class OAuthSecurityBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        app = conn.scope["app"] # type: FastAPI
        
        path = conn.scope["path"]
        slash_normalized_path : str
        if path.endswith("/"):
            slash_normalized_path = path.rstrip("/")
        else:
            slash_normalized_path = path + "/"
        
        for _path_re in app._NR_public_paths: # type: ignore
            _path_re : Pattern
            if(_path_re.match(path) or _path_re.match(slash_normalized_path)):
                return AuthCredentials(), UnauthenticatedUser()
        
        if "Authorization" not in conn.headers:
            raise AuthenticationError('Invalid basic auth credentials')

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        # TODO: You'd want to verify the username and password here.
        return AuthCredentials(["authenticated"]), SimpleUser(username)

OAuthMiddleware = Middleware(AuthenticationMiddleware, backend=OAuthSecurityBackend())