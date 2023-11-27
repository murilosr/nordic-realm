from fastapi import FastAPI
from nordic_realm.di.component_store import ComponentStore
from nordic_realm.di.singleton_store import SingletonStore
from nordic_realm.mongo.connections import MongoConnections

_global_app_context : "ApplicationContext" = None # type: ignore

class ApplicationContext:
    
    fastapi_app : FastAPI
    component_store : ComponentStore
    
    @staticmethod
    def get():
        if(_global_app_context is None):
            raise Exception("Global ApplicationContext not initialized")
        return _global_app_context
    
    def __init__(self, fastapi_app : FastAPI, set_global : bool = False):
        self.fastapi_app = fastapi_app
        self.component_store = ComponentStore()
        self.singleton_store = SingletonStore()
        self.mongo_conns = MongoConnections()
        self.mongo_conns.register(None, {"host" : "mongodb://root:murilo@rs1.mongodb.local:27017/?retryWrites=true&serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1"})
        
        if(set_global):
            global _global_app_context
            _global_app_context = self