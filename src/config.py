from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "RAG Demo"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/rag_demo"
    test_database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/rag_demo_test"


@lru_cache
def get_settings() -> Settings:
    return Settings()
