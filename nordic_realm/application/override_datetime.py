import datetime
import os
import time

import pytz

os.environ["TZ"] = "America/Sao_Paulo"
time.tzset()
_default_tz = pytz.timezone("America/Sao_Paulo")


class _DatetimeSP(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return super().now(tz=tz or _default_tz)


datetime.datetime = _DatetimeSP  # type: ignore
