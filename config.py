import codecs
import subprocess
import os
from functools import lru_cache, cache
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    MYEXAM_SECRET_KEY: str = codecs.encode(os.urandom(32), "hex").decode()
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
    return get_config("MYEXAM_SECRET_KEY")


@lru_cache()
def get_config(item: Optional[str] = None):
    if item:
        return Settings()[item]
    return Settings()


@cache
def get_version() -> str:
    cmd = "git rev-parse --short HEAD"
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    return proc.stdout.decode().strip()
