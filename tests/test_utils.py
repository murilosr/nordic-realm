import re
from datetime import datetime

from nordic_realm.utils import generate_id
from nordic_realm.utils.pydantic_validators import PydanticValidators


def _assert_datetime(dt: datetime):
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.second == 0
    assert dt.microsecond == 0
    assert dt.day == 1
    assert dt.month == 1
    assert dt.year == 2024
    assert dt.tzname() == "UTC"


def test_to_midnight_with_tz_aware():
    dt_test = datetime.fromisoformat("2024-01-01T00:00:00.000000Z")
    dt_test_midnight = PydanticValidators.to_midnight(dt_test, None)
    _assert_datetime(dt_test_midnight)


def test_generate_id_should_include_only_alphanumeric():
    pattern = re.compile(r"[^a-zA-Z0-9]")
    for i in range(1000):
        _id = generate_id()
        assert pattern.match(_id) is None


def test_generate_id_should_respect_length_parameter():
    for i in range(256):
        _id = generate_id(i)
        assert len(_id) == i
