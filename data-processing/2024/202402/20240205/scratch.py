import argparse
import asyncio
import os

import aioboto3

# import pandas as pd
from dotenv import load_dotenv
from tqdm.asyncio import trange


class S3:
    def __init__(self):
        self.session = aioboto3.Session()

    def get_object(self, bucket, key):
        obj = self.s3.get_object(Bucket=bucket, Key=key)
        return obj["Body"]

    def put_object(self, bucket, key, data):
        self.s3.put_object(Bucket=bucket, Key=key, Body=data)

    def copy_object(self, bucket, key, new_key):
        self.s3.copy_object(
            Bucket=bucket,
            CopySource={"Bucket": bucket, "Key": key},
            Key=new_key,
        )


async def main(start, end):
    load_dotenv()

    BUCKET = os.getenv("BUCKET_NAME")
    ORIGINAL_KEY = os.getenv("ORIGINAL_KEY")
    PREP_KEY = os.getenv("PREP_KEY")

    s3_object = S3()

    async with s3_object.session.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    ) as s3:
        async for itr in trange(start, end, 100):
            await s3.copy_object(
                Bucket=BUCKET,
                CopySource={
                    "Bucket": BUCKET,
                    "Key": os.path.join(ORIGINAL_KEY, f"{itr}-{itr+100}.csv"),
                },
                Key=os.path.join(
                    PREP_KEY, str((itr // 100_000_000) + 1), f"{itr}-{itr+100}.csv"
                ),
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--start", type=int, help="start range")
    parser.add_argument("--end", type=int, help="end range")

    args = parser.parse_args()
    asyncio.run(main(args.start, args.end))
