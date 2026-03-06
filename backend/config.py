from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Hospital Appointment System"
    debug: bool = False
    database_url: str = ""
    api_prefix: str = "/graphql"
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()