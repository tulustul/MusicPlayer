from typing import Sequence

import boto3

from core.cloud import CloudProvider


class S3Provider(CloudProvider):

    PROVIDER_KEY = "S3"

    def __init__(self, config: dict):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=config['access_key'],
            aws_secret_access_key=config['secret_access_key'],
        )
        self.bucket_name = config['bucket_name']

    async def push_files(self, uris: Sequence[str]):
        raise NotImplementedError

    async def pull_files(self, uris: Sequence[str]):
        raise NotImplementedError
