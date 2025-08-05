# app/core/config.py

from functools import lru_cache
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "prod"  # 'dev' or 'prod'

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 710
    ALLOWED_ORIGINS: str = ""

    class Config:
        env_file = f".env.{os.getenv('ENVIRONMENT', 'dev')}"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
