import uvicorn

from nordic_realm.application.context import ApplicationContext
from nordic_realm.di.scanner import DIScanner
from nordic_realm.fastapi_server.filters.security_middleware import (
    AuthenticationMiddleware, OAuthSecurityBackend)
from nordic_realm.log import Log

from .fastapi_server.add_controllers import add_controllers
from .fastapi_server.app import app

Log()
started = False
ApplicationContext(app, True)

DIScanner().scan("app")
add_controllers()
ApplicationContext.get().singleton_store.register(ApplicationContext.get().mongo_conns.get(None))
app.add_middleware(AuthenticationMiddleware, backend=OAuthSecurityBackend())

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
            log_config=Log()._config
        )
        