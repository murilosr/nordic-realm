from datetime import datetime, UTC


class DateUtils:

    @staticmethod
    def utc_midnight() -> datetime:
        return datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=UTC)

