# noinspection PyUnresolvedReferences
from nordic_realm.test import *


def test_fastapi_app(test_client):
    assert test_client is not None


def test_auth_middleware_should_block_unauthenticated_requests(test_client):
    response = test_client.get("/auth/test")
    assert response.status_code == 401
    assert response.json()["detail"] == "Missing Authorization header"


def test_auth_middleware_should_block_invalid_authorization_header(test_client):
    response = test_client.get("/auth/test", headers={"Authorization": "Bearer"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Bad Authorization header"

    response = test_client.get("/auth/test", headers={"Authorization": "Bearer 123"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Bad Authorization token"


def test_auth_middleware_should_block_expired_authorization_header(test_client):
    response = test_client.get("/auth/test", headers={
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwic2lkIjoiNjVhZTc5NDdiNDExOGE1OTcyOGE0MmU3IiwidGlkIjoiNGYzZDY1ODE1MDQwNGMxZmJkYzA5NjE4YzZmMTg3YTM0YWU5MWM0N2YzNjU0NjgyYjQ0ODQxZTAyYmI5ZjViNSIsImV4cCI6MTcwODUyNTEyN30.dYwc7EFZU5HE6E8eEUDSXLVX49PkiFXpAZVCD5yuqg0"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Session revoked"
