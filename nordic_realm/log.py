import logging.config
from typing import Any

from yaml import safe_load

orig_factory : Any = None

class Log:
    
    def __init__(self):
        with open('./config.yaml', 'rt') as f:
            self._config = safe_load(f.read())["logging"]
        logging.config.dictConfig(self._config)
        global orig_factory
        if(orig_factory is None):
            orig_factory = logging.getLogRecordFactory()

            def record_factory(*args, **kwargs):
                global orig_factory
                record = orig_factory(*args, **kwargs)
                record.name = record.name[-20:] if len(
                    record.name) > 20 else record.name
                return record

            logging.setLogRecordFactory(record_factory)