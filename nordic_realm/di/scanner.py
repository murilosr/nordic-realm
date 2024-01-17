from importlib import import_module
from pathlib import Path

from typing_extensions import Optional

from nordic_realm.application import ApplicationContext


class DIScanner:

    def __init__(self, app_context: Optional[ApplicationContext] = None):
        self.app_context = app_context if app_context is not None else ApplicationContext.get()

    def scan(self, package: str):
        _root_abspath = Path(".").joinpath(package).absolute()
        for _file in _root_abspath.rglob("**/*.py"):
            _module_name = f"{package}.{str(_file.relative_to(_root_abspath)).replace('/', '.').replace('.py', '')}"
            if _module_name.endswith("__init__"):
                _module_name = _module_name.replace(".__init__", "")
            # _module = __import__(_module_name, _g, _l, ["*"])
            _module = import_module(_module_name)
            for _i in _module.__dict__.values():
                if getattr(_i, "_NR_component", False) and isinstance(_i, type):
                    self.app_context.component_store.register(_i)
