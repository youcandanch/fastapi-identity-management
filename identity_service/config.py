from functools import lru_cache

from pydantic import BaseSettings


@lru_cache()
def get_current_settings():
    return Settings()


class Settings(BaseSettings):
    db_filename: str = "identity_service.db"
    jwt_expiration_time_in_seconds: int = 3600
    password_hash_algorithm: str = "HS256"
    password_hash_secret_key: str

    class Config:
        env_file = ".env"
