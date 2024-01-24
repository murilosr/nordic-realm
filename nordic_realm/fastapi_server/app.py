from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app():
    _app = FastAPI()

    origins = [
        "http://localnet.thorson.tech:3000",
        "http://localhost:3000",
        "http://localnet.thorson.tech:8080",
        "http://localhost:8080",
    ]

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app
