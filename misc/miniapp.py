import requests
from functools import cache
from typing import Tuple
from datetime import datetime, timedelta
from config import get_config
import base64


@cache
def fetch_access_token() -> Tuple[str, int]:
    app_id = get_config("MINIAPP_APP_ID")
    app_secret = get_config("MINIAPP_APP_SECRET")

    response = requests.get(
        "https://api.weixin.qq.com/cgi-bin/token",
        {"grant_type": "client_credential", "appid": app_id, "secret": app_secret},
    )

    data = response.json()
    access_token = data["access_token"]
    expires = datetime.now() + timedelta(seconds=data["expires_in"])

    return access_token, expires


def get_access_token() -> str:
    token, expires = fetch_access_token()

    if expires <= datetime.now():
        fetch_access_token.cache_clear()
        token, expires = fetch_access_token()

    return token


def get_miniapp_code(id) -> str:
    token = get_access_token()
    data = {
        "page": "pages/jump/jump",
        "scene": "id=" + str(id),
        "check_path": True,
        "env_version": "release",
    }

    response = requests.post(
        "https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=" + token,
        json=data,
    )

    return base64.b64encode(response.content)
