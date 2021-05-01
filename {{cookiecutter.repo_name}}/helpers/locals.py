import threading
from typing import Optional


class LoginUser:
    class _LoginUser(threading.local):
        uuid: Optional[str] = None

    _login_user = _LoginUser()

    @classmethod
    def set_login_user_uuid(cls, user_uuid: Optional[str]) -> None:
        cls._login_user.uuid = user_uuid

    @classmethod
    def get_login_user_uuid(cls) -> str:
        assert cls._login_user.uuid is not None, "login user uuid is unset"
        return cls._login_user.uuid

    def __init__(self, user):
        self.user = user

    def __enter__(self):
        self.set_login_user_uuid(self.user)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.set_login_user_uuid(None)
