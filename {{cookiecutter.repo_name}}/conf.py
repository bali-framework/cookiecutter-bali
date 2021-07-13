import locale

from bali.db import db
from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = '.env'

    TITLE: str = "{{cookiecutter.repo_name}}"
    LOCALE: str
    TZ: str
    DATABASE: str
    RPC_PORT: int
    RPC_THREAD_POOL_SIZE: int
    MQ_HOST: str
    MQ_ACCESS_ID: str
    MQ_ACCESS_KEY: str
    MQ_INSTANCE: str


settings = Settings()
db.connect(settings.DATABASE)
locale.setlocale(locale.LC_ALL, settings.LOCALE)
