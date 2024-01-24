import pytest
from fastapi import FastAPI
from starlette.responses import PlainTextResponse
from starlette.testclient import TestClient


def mount_app():
    app = FastAPI()

    @app.get("/")
    def root():
        return PlainTextResponse("hello world")

    return app


@pytest.fixture
def test_client():
    _app = mount_app()
    with TestClient(_app) as _test_client:
        yield _test_client


def test_root_path(test_client):
    response = test_client.get("/")
    assert response.text == "hello world"


def test_root_path_2(test_client):
    response = test_client.get("/")
    assert response.text == "hello world"
