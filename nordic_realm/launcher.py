import logging
from pymongo import MongoClient
from nordic_realm.application.context import ApplicationContext
from nordic_realm.di.injector import DIInjector
from nordic_realm.di.scanner import DIScanner
from nordic_realm.fastapi_server.filters.security_middleware import AuthenticationMiddleware, OAuthSecurityBackend
from .fastapi_server.app import app
from .fastapi_server.add_controllers import add_controllers
import uvicorn
from app.controllers import HelloWorld

started = False
ApplicationContext(app, True)

DIScanner().scan("app")
add_controllers()
ApplicationContext.get().singleton_store.register(ApplicationContext.get().mongo_conns.get(None))
app.add_middleware(AuthenticationMiddleware, backend=OAuthSecurityBackend())

def run_app():
    global started
    if not started:
        uvicorn.run(f"nordic_realm.launcher:app", host="127.0.0.1", port=8080, reload=True, workers=1)
        started = True