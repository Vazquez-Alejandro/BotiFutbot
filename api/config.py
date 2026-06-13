from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///data/botifutbol.db"
    TELEGRAM_TOKEN: str = ""
    API_FOOTBALL_KEY: str = ""
    NEWS_API_KEY: str = ""
    JWT_SECRET: str = "botifutbol-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "https://botifutbol.vercel.app",
        "https://botifutbol-alejandro.vercel.app",
    ]

    class Config:
        env_file = "../.env"


@lru_cache
def get_settings():
    return Settings()
