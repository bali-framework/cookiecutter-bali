import threading
from typing import Optional


class LoginUser:
    class _LoginUser(threading.local):
        {{cookiecutter.business_key}}: Optional[str] = None

    _login_user = _LoginUser()

    @classmethod
    def set_login_user_{{cookiecutter.business_key}}(cls, user_{{cookiecutter.business_key}}: Optional[str]) -> None:
        cls._login_user.{{cookiecutter.business_key}} = user_{{cookiecutter.business_key}}

    @classmethod
    def get_login_user_{{cookiecutter.business_key}}(cls) -> str:
        assert cls._login_user.{{cookiecutter.business_key}} is not None, "login user {{cookiecutter.business_key}} is unset"
        return cls._login_user.{{cookiecutter.business_key}}

    def __init__(self, user):
        self.user = user

    def __enter__(self):
        self.set_login_user_{{cookiecutter.business_key}}(self.user)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.set_login_user_{{cookiecutter.business_key}}(None)
