from datetime import datetime

import pytz

UTC = pytz.timezone("UTC")


class DateUtils:
    @staticmethod
    def utc_midnight() -> datetime:
        return datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def now_midnight() -> datetime:
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
