from datetime import timedelta
from tempfile import NamedTemporaryFile

from minio import Minio

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


def get_presigned_get_url(ext: str, id: str, file: str = None) -> str:
    key = config["S3_PREFIX"] + "/" + id + "." + ext
    key = key.strip("/")

    filename = file if file else id + "." + ext
    extra = {"response-content-disposition": "attachment; filename=%s" % filename}

    url = minioClient.get_presigned_url(
        "GET",
        config["S3_BUCKET"],
        key,
        expires=timedelta(hours=1),
        response_headers=extra,
    )

    return url


def delete_from_s3(ext: str, fid: str):
    key = config["S3_PREFIX"] + "/" + fid + "." + ext
    key = key.strip("/")

    minioClient.remove_object(config["S3_BUCKET"], key)


def get_file_local(ext: str, fid: str):
    new_file = NamedTemporaryFile("w", delete=False)

    key = config["S3_PREFIX"] + "/" + fid + "." + ext
    key = key.strip("/")

    minioClient.fget_object(config["S3_BUCKET"], key, new_file.name)

    return new_file.name
