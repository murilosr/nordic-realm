from pathlib import Path
from typing import List

from fastapi import FastAPI

from .context import ApplicationContext
from ..fastapi_server.ws_connection_manager import WebsocketConnectionManager


def _get_mongo_connection_config(application_context: ApplicationContext):
    _config = application_context.config_store.get("mongodb")
    if not isinstance(_config, dict):
        raise ValueError("mongodb not found in secrets.yaml")
    _config = _config.copy()
    _config.pop("db", None)

    return _config


def _bootstrap_mongo_connections(application_context: ApplicationContext):
    application_context.mongo_conns.register(
        name=None,
        params=_get_mongo_connection_config(application_context)
    )


def bootstrap_application_context(
        config_files: List[str | Path] | None = None,
        fastapi_app: FastAPI | None = None,
        set_global: bool = True
):
    from ..mongo.connections import MongoConnections
    from ..di import ConfigStore, ComponentStore, SingletonStore

    if fastapi_app is None:
        from nordic_realm.fastapi_server.app import create_app
        fastapi_app = create_app()

    config_store = ConfigStore(config_files)
    component_store = ComponentStore()
    singleton_store = SingletonStore()
    mongo_conns = MongoConnections()
    websocket_conns = WebsocketConnectionManager(config_store)

    application_context = ApplicationContext(
        fastapi_app,
        config_store,
        component_store,
        singleton_store,
        mongo_conns,
        websocket_conns
    )

    if set_global:
        application_context.set_global()

    _bootstrap_mongo_connections(application_context)
    return application_context
