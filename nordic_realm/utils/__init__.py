import os

from jwt.utils import base64url_encode


def _gen_bytes():
    return (
        base64url_encode(os.urandom(32))
        .replace(b'_', b'')
        .replace(b'-', b'')
        .replace(b'=', b'')
    )


def generate_id(length: int = 24):
    _curr_bytes: bytes = bytes()

    while len(_curr_bytes) < length:
        _curr_bytes += _gen_bytes()

    return _curr_bytes[:length].decode()
