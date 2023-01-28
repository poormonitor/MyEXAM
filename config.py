import codecs
import json
import os
import subprocess
import sys
from functools import cache, lru_cache
from typing import Dict, List, Optional

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
    MINIAPP_APP_ID: str = ""
    MINIAPP_APP_SECRET: str = ""
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


@cache
def get_dependencies() -> List[Dict[str, str]]:
    cmd = [sys.executable, "-m", "pip", "list", "--format", "json"]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE)
    dep = json.loads(proc.stdout.decode())
    return dep
