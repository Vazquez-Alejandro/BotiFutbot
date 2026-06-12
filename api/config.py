from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://localhost:5432/botifutbol"
    TELEGRAM_TOKEN: str = ""
    API_FOOTBALL_KEY: str = ""
    JWT_SECRET: str = "botifutbol-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    CORS_ORIGINS: list = ["http://localhost:3000"]

    class Config:
        env_file = "../.env"


@lru_cache
def get_settings():
    return Settings()
