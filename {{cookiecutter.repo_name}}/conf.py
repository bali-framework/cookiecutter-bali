from bali.db import db
from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        case_sensitive = True
        env_file = '.env'

    TITLE: str = "{{cookiecutter.repo_name}}"
    DATABASE: str


settings = Settings()
db.connect(settings.DATABASE)
