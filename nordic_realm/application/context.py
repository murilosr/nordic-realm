from fastapi import FastAPI

from nordic_realm.di import ComponentStore, ConfigStore, SingletonStore
from nordic_realm.fastapi_server.ws_connection_manager import WebsocketConnectionManager
from nordic_realm.mongo.connections import MongoConnections

_global_app_context: "ApplicationContext" = None  # type: ignore


class ApplicationContext:

    @staticmethod
    def get():
        global _global_app_context
        if _global_app_context is None:
            raise Exception("Global ApplicationContext not initialized")
        return _global_app_context

    def __init__(self,
                 fastapi_app: FastAPI,
                 config_store: ConfigStore,
                 component_store: ComponentStore,
                 singleton_store: SingletonStore,
                 mongo_conns: MongoConnections,
                 websocket_conns: WebsocketConnectionManager):
        self.fastapi_app = fastapi_app
        self.config_store = config_store
        self.component_store = component_store
        self.singleton_store = singleton_store
        self.mongo_conns = mongo_conns
        self.websocket_conns = websocket_conns

    def set_global(self):
        global _global_app_context
        _global_app_context = self
