import logging

import pytest
from pymongo.errors import ServerSelectionTimeoutError
from starlette.testclient import TestClient

from nordic_realm.application.bootstrap import bootstrap_application_context
from nordic_realm.application.context import ApplicationContext
from nordic_realm.fastapi_server.exception_handler import FastAPIExceptionHandler
from nordic_realm.log import Log
from nordic_realm.utils import generate_id

log = logging.getLogger("Test")
Log()


@pytest.fixture(scope="session", autouse=True)
def before_init(request):
    print("")

    bootstrap_application_context(["./config.yaml", "./secrets_test.yaml"])

    from nordic_realm.di.scanner import DIScanner
    from nordic_realm.fastapi_server.add_controllers import add_controllers
    DIScanner().scan("auth_server")
    DIScanner().scan("app")
    add_controllers()
    ApplicationContext.get().singleton_store.register(ApplicationContext.get().mongo_conns.get(None))

    from auth_server.middleware.security_middleware import OAuthSecurityMiddleware
    OAuthSecurityMiddleware.install_middleware()
    FastAPIExceptionHandler.install_exception_handler()


@pytest.fixture(scope="function", autouse=True)
def reset_database():
    db_name = ApplicationContext.get().config_store.get("mongodb.db") + f"_{generate_id(8)}"
    log.info(f"using db: {db_name}")
    ApplicationContext.get().config_store.register_override("mongodb.db", db_name)

    for _clazz in ApplicationContext.get().component_store._store.values():
        _clazz._DB = db_name

    logging.info("before_init executed")
    try:
        ApplicationContext.get().mongo_conns.get().drop_database(db_name)
    except ServerSelectionTimeoutError:  # pragma: nocover
        pytest.exit("Can't connect to MongoDB. Check your secrets_test.yaml parameters")

    yield

    print("")
    logging.info("ended")
    ApplicationContext.get().mongo_conns.get().drop_database(db_name)


@pytest.fixture(scope="session")
def test_client():
    yield TestClient(ApplicationContext.get().fastapi_app)
