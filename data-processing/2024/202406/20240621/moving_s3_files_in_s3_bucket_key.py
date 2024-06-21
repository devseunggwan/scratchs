import os
from typing import List, Tuple

import boto3
from dotenv import load_dotenv


def list_objects(s3_client, bucket_name, prefix):
    paginator = s3_client.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    object_keys = []
    for page in page_iterator:
        if "Contents" in page:
            object_keys.extend([obj["Key"] for obj in page["Contents"]])

    return object_keys


def move_objects(s3_client, bucket_name, source_prefix, destination_prefix):
    objects_to_move = list_objects(s3_client, bucket_name, source_prefix)

    for obj_key in objects_to_move:
        copy_source = {"Bucket": bucket_name, "Key": obj_key}
        destination_key = obj_key.replace(source_prefix, destination_prefix, 1)

        # 객체 복사
        s3_client.copy_object(
            CopySource=copy_source, Bucket=bucket_name, Key=destination_key
        )

        # 원본 객체 삭제
        s3_client.delete_object(Bucket=bucket_name, Key=obj_key)

        print(f"Moved {obj_key} to {destination_key}")


if __name__ == "__main__":
    load_dotenv()

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # variables
    bucket_name: str = ""
    # [(source_prefix, destination_prefix), ...]
    source_destination_prefixs: List[Tuple[str, str]] = []

    for source_prefix, destination_prefix in source_destination_prefixs:
        # 객체 이동 실행
        move_objects(s3_client, bucket_name, source_prefix, destination_prefix)
