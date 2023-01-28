from uuid import uuid4
import random
from typing import Callable, Iterable


def gen_id() -> str:
    return str(uuid4())


def gen_jid() -> str:
    d = ""
    for _ in range(6):
        d += str(random.randint(0, 9))
    return d


def find_item(item: Iterable, func: Callable, target) -> int:
    for i in range(len(item)):
        if func(item[i]) == target:
            return i

    return -1
