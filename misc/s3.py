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


def get_presigned_post_url(ext: str, id: str) -> str:
    key = config["S3_PREFIX"] + "/" + id + "." + ext
    key = key.strip("/")

    url = minioClient.get_presigned_url(
        "POST", config["S3_BUCKET"], key, expires=timedelta(hours=1)
    )

    return url, key


def get_presigned_get_url(
    ext: str, id: str, file: str = None, download: bool = False
) -> str:
    key = config["S3_PREFIX"] + "/" + id + "." + ext
    key = key.strip("/")

    filename = file if file else id + "." + ext
    extra = {"response-content-disposition": "attachment; filename=%s" % filename}

    url = minioClient.get_presigned_url(
        "GET",
        config["S3_BUCKET"],
        key,
        expires=timedelta(hours=1),
        response_headers=extra if download else {},
    )

    return url


def delete_object_from_s3(ext: str, fid: str):
    key = config["S3_PREFIX"] + "/" + fid + "." + ext
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


def get_file_local(ext: str, fid: str):
    new_file = NamedTemporaryFile("w", delete=False, suffix="." + ext)
    new_file.close()

    key = config["S3_PREFIX"] + "/" + fid + "." + ext
    key = key.strip("/")

    minioClient.fget_object(config["S3_BUCKET"], key, new_file.name)

    return new_file.name