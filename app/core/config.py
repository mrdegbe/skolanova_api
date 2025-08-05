# app/core/config.py

from functools import lru_cache
import os
from typing import List
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(".env")
env_mode = os.getenv("ENVIRONMENT", "dev").lower()
load_dotenv(f".env.{env_mode}")


class Settings(BaseSettings):
    ENVIRONMENT: str = env_mode

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 710
    ALLOWED_ORIGINS: str = ""

    class Config:
        env_file = None  # We've already loaded with dotenv


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
