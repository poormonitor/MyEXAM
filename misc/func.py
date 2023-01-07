from uuid import uuid4


def gen_id() -> str:
    return str(uuid4())
