from bali.db import db
from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = '.env'

    TITLE: str = "Financial"
    DATABASE: str


settings = Settings()
db.connect(settings.DATABASE)
