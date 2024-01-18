import re


class ValidationUtil:
    email_regex: re.Pattern = re.compile(r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,5})+$")

    @classmethod
    def isEmail(cls, value: str):
        return cls.email_regex.match(value) is not None
