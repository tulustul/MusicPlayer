import asyncio
import concurrent.futures
import functools
import logging
from typing import Sequence

import boto3
from botocore.exceptions import ClientError

from core.cloud import CloudProvider

logger = logging.getLogger("cloud.s3")


class S3Provider(CloudProvider):

    PROVIDER_KEY = "S3"

    def __init__(self, config: dict):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=config["access_key"],
            aws_secret_access_key=config["secret_access_key"],
        )
        self.bucket_name = config["bucket_name"]

    async def push_files(self, uris: Sequence[str]):
        await asyncio.get_event_loop().run_in_executor(
            None, functools.partial(self._upload_many, uris)
        )

    async def pull_files(self, uris: Sequence[str]):
        raise NotImplementedError

    def _upload_many(self, uris: Sequence[str]):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self._upload, uri) for uri in uris]
            for future in concurrent.futures.as_completed(futures):
                # todo mark progress
                pass

    def _upload(self, uri: str):
        try:
            self.s3.upload_file(uri, self.bucket_name)
        except ClientError as e:
            logger.error(e)
