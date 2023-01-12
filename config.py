from functools import lru_cache

from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DB_PATH: str = "sqlite:///data.sqlite"
    S3_ENDPOINT: str = ""
    S3_SECRET_ID: str = ""
    S3_SECRET_KEY: str = ""
    S3_REGION: str = ""
    S3_BUCKET: str = ""
    S3_PREFIX: str = ""
    REGISTER: int = 1

    class Config:
        env_file = ".env"

    def __getitem__(self, item: str):
        return getattr(self, item)


def get_secret_key() -> str:
    from os import environ

    secret_key = environ.get("MyEXAMSecretKey", None)
    if not secret_key:
        from base64 import b64encode
        from secrets import token_bytes

        secret_key = b64encode(token_bytes(32)).decode()
    return secret_key


@lru_cache()
def get_config(item: Optional[str] = None) -> BaseSettings:
    if item:
        return Settings()[item]
    return Settings()