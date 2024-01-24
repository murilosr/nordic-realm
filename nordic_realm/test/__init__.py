import logging

import pytest
from pymongo.errors import ServerSelectionTimeoutError
from starlette.testclient import TestClient

from auth_server.middleware.security_middleware import OAuthSecurityMiddleware
from auth_server.service import AuthServerService
from nordic_realm.application.bootstrap import bootstrap_application_context
from nordic_realm.application.context import ApplicationContext
from nordic_realm.di.injector import DIInjector
from nordic_realm.fastapi_server.app import create_app
from nordic_realm.fastapi_server.exception_handler import FastAPIExceptionHandler
from nordic_realm.log import Log
from nordic_realm.utils import generate_id

log = logging.getLogger("Test")
Log()


@pytest.fixture
def app_context():
    return bootstrap_application_context(
        config_files=["./config.yaml", "./secrets_test.yaml"],
        fastapi_app=create_app(),
        set_global=True
    )


@pytest.fixture
def before_init(request, app_context):
    from nordic_realm.di.scanner import DIScanner
    from nordic_realm.fastapi_server.add_controllers import add_controllers

    db_name = ApplicationContext.get().config_store.get("mongodb.db") + "_" + generate_id(8)
    ApplicationContext.get().config_store.register_override("mongodb.db", db_name)

    DIScanner().scan("auth_server")
    DIScanner().scan("app")
    add_controllers(app_context)
    app_context.singleton_store.register(app_context.mongo_conns.get(None))

    OAuthSecurityMiddleware.install_middleware(app_context)
    FastAPIExceptionHandler.install_exception_handler(app_context)


@pytest.fixture(autouse=True)
def reset_database(before_init):
    db_name = ApplicationContext.get().config_store.get("mongodb.db")

    try:
        ApplicationContext.get().mongo_conns.get().drop_database(db_name)
        logging.info(f"Before_init executed. Using db: {db_name}")
    except ServerSelectionTimeoutError:  # pragma: nocover
        pytest.exit("Can't connect to MongoDB. Check your secrets_test.yaml parameters")

    yield

    # ApplicationContext.get().mongo_conns.get().drop_database(db_name)
    logging.info(f"Before_init ended. Dropping db: {db_name}\n\n")


@pytest.fixture
def test_client(reset_database):
    with TestClient(ApplicationContext.get().fastapi_app) as _test_client:
        yield _test_client


@pytest.fixture
def use_session():
    def _internal(user_id: str, user_agent: str = "test_agent"):
        auth_service = DIInjector().instance(AuthServerService)
        _session = auth_service.create_session(user_id, user_agent)
        return auth_service.create_access_token(_session)

    return _internal
