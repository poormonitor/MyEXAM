from datetime import datetime, timedelta
from functools import cache
from typing import Tuple

import requests

from config import get_config


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


def get_access_token(refresh: bool = False) -> str:
    token, expires = fetch_access_token()

    if refresh or expires <= datetime.now():
        fetch_access_token.cache_clear()
        token, expires = fetch_access_token()

    return token


def request_code(id, token):
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

    return response

def get_miniapp_code(id) -> bytes:
    token = get_access_token()
    response = request_code(id, token)
    
    try:
        err = response.json()
        if err["errcode"] == 40001:
            token = get_access_token(True)
            response = request_code(id, token)
    except:
        pass


    return response.content
