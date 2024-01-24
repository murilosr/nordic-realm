import uvicorn

from auth_server.middleware.security_middleware import OAuthSecurityMiddleware
from nordic_realm.application import ApplicationContext, bootstrap_application_context
from nordic_realm.di.scanner import DIScanner
from nordic_realm.fastapi_server.exception_handler import FastAPIExceptionHandler
from nordic_realm.log import Log
from .fastapi_server.add_controllers import add_controllers

Log()
started = False

global_context = bootstrap_application_context()

DIScanner().scan("auth_server")
DIScanner().scan("app")
add_controllers(global_context)
ApplicationContext.get().singleton_store.register(ApplicationContext.get().mongo_conns.get(None))

OAuthSecurityMiddleware.install_middleware(global_context)
FastAPIExceptionHandler.install_exception_handler(global_context)

app = global_context.fastapi_app


def run_app():
    global started
    if not started:
        started = True

        uvicorn.run(
            app=f"nordic_realm.launcher:app",
            host="0.0.0.0",
            port=8080,
            reload=True,
            workers=1,
            log_config=Log().config
        )
