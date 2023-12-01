from fastapi import FastAPI
from nordic_realm.fastapi_server.app import app

from nordic_realm.di import ComponentStore, ConfigStore, SingletonStore
from nordic_realm.mongo import MongoConnections

_global_app_context : "ApplicationContext" = None # type: ignore

class ApplicationContext:
    
    @staticmethod
    def get():
        if(_global_app_context is None):
            raise Exception("Global ApplicationContext not initialized")
        return _global_app_context
    
    def __init__(self, fastapi_app : FastAPI, set_global : bool = False):
        self.fastapi_app = fastapi_app
        self.config_store = ConfigStore()
        self.component_store = ComponentStore()
        self.singleton_store = SingletonStore()
        self.mongo_conns = MongoConnections()
        
        if(set_global):
            global _global_app_context
            _global_app_context = self
        
        self._start_modules()
    
    def _get_mongo_connection_config(self):
        _config = self.config_store.get("mongodb")
        if not isinstance(_config, dict):
            raise ValueError("mongodb not found in secrets.yaml")
        _config = _config.copy()
        _config.pop("db", None)

        return _config

    def _start_modules(self):
        self.mongo_conns.register(
            name=None,
            params=self._get_mongo_connection_config()
        )

ApplicationContext(app, True)