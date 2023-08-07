import os
from datetime import timedelta
from tempfile import NamedTemporaryFile
from typing import List, Tuple

from minio import Minio
from minio.deleteobjects import DeleteObject

from config import get_config

config = get_config()
minioClient = Minio(
    config["S3_ENDPOINT"],
    access_key=config["S3_SECRET_ID"],
    secret_key=config["S3_SECRET_KEY"],
    region=config["S3_REGION"],
    secure=True,
)


def get_presigned_post_url(ext: str, id: str) -> Tuple[str, str]:
    key = config["S3_PREFIX"] + "/" + id + "." + ext
    key = key.strip("/")

    url = minioClient.get_presigned_url(
        "POST", config["S3_BUCKET"], key, expires=timedelta(hours=1)
    )

    return url, key


def get_presigned_get_url(ext: str, id: str) -> str:
    key = config["S3_PREFIX"] + "/" + id + "." + ext
    key = key.strip("/")

    if config["S3_DOMAIN"]:
        url = config["S3_DOMAIN"] + key
    else:
        url = "https://%s/%s/%s/%s" % (
            config["S3_ENDPOINT"],
            config["S3_BUCKET"],
            config["S3_PREFIX"],
            key,
        )

    return url


def delete_object_from_s3(ext: str, id: str):
    key = config["S3_PREFIX"] + "/" + id + "." + ext
    key = key.strip("/")

    minioClient.remove_object(config["S3_BUCKET"], key)


def delete_objects_from_s3(lst: List[Tuple[str, str]]):
    keys = map(
        lambda x: DeleteObject(
            (config["S3_PREFIX"] + "/" + x[0] + "." + x[1]).strip("/")
        ),
        lst,
    )

    minioClient.remove_objects(config["S3_BUCKET"], keys)


def get_file_local(ext: str, id: str):
    new_file = NamedTemporaryFile("w", delete=False, suffix="." + ext)
    new_file.close()

    key = config["S3_PREFIX"] + "/" + id + "." + ext
    key = key.strip("/")

    minioClient.fget_object(config["S3_BUCKET"], key, new_file.name)

    return new_file.name


def list_object_hash() -> List[str]:
    objects = minioClient.list_objects(
        config["S3_BUCKET"], prefix=config["S3_PREFIX"] + "/", recursive=True
    )
    sp = lambda x: os.path.splitext(os.path.split(x)[1])[0]
    return [sp(obj.object_name) for obj in objects]


def list_object_names() -> List[Tuple[str, str]]:
    objects = minioClient.list_objects(
        config["S3_BUCKET"], prefix=config["S3_PREFIX"] + "/", recursive=True
    )
    sp = lambda x: os.path.splitext(os.path.split(x)[1])
    return [sp(obj.object_name) for obj in objects]
