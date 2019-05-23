import asyncio
import concurrent.futures
import functools
import logging
import threading
from typing import Collection
import os

import boto3
from botocore.exceptions import ClientError
from rx.subjects import Subject
from rx.operators import subscribe_on
from rx.concurrency.mainloopscheduler.asyncioscheduler import AsyncIOScheduler

from core.cloud import CloudProvider, UploadData
from core.utils import format_bytes
from core.rx_utils import to_async_iterable
from player import PlayerApp
from ui.components.progress import ProgressComponent

logger = logging.getLogger("cloud.s3")


class ProgressCallback:
    def __init__(self, upload_data: UploadData):
        self._filename = upload_data.source_path
        self._size = float(os.path.getsize(self._filename))
        self._size_formatted = format_bytes(int(self._size))
        self._seen_so_far = 0
        self._lock = threading.Lock()
        with self._lock:
            app: PlayerApp = PlayerApp.get_instance()
            self.progress_component = ProgressComponent()
            self.progress_component.left_text = upload_data.target_path
            app.ui.stack_layout.add(self.progress_component)

    def __call__(self, bytes_amount: int):
        with self._lock:
            self._seen_so_far += bytes_amount
            seen_formatter = format_bytes(self._seen_so_far)
            self.progress_component.progress = self._seen_so_far / self._size
            self.progress_component.right_text = (
                f"{seen_formatter} / {self._size_formatted}"
            )
            if self._seen_so_far == self._size:
                self.progress_component.detach()


class S3Provider(CloudProvider):
    def __init__(self, config: dict):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=config["access_key"],
            aws_secret_access_key=config["secret_access_key"],
        )
        self.bucket_name = config["bucket_name"]

    def push_files(self, uris: Collection[UploadData]):
        subject = Subject()
        asyncio.get_event_loop().run_in_executor(
            None, functools.partial(self._upload_many, uris, subject)
        )
        return subject.pipe(
            subscribe_on(AsyncIOScheduler()), to_async_iterable()
        )

    async def pull_files(self, items: Collection[str]):
        raise NotImplementedError

    def _upload_many(self, items: Collection[UploadData], subject: Subject):
        items_count = len(items)
        finished_items_count = 0
        app: PlayerApp = PlayerApp.get_instance()
        pc = ProgressComponent()
        pc.left_text = "uploading to cloud"
        pc.right_text = f"0 / {items_count}"
        app.ui.stack_layout.add(pc)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(self._upload, item) for item in items]
            for future in concurrent.futures.as_completed(futures):
                finished_items_count += 1
                pc.progress = finished_items_count / items_count
                pc.right_text = f"{finished_items_count} / {items_count}"
                subject.on_next(future.result())
        subject.on_completed()
        pc.detach()

    def _upload(self, item: UploadData):
        try:
            self.s3.upload_file(
                item.source_path,
                self.bucket_name,
                item.target_path,
                Callback=ProgressCallback(item),
            )
            return item.track
        except ClientError as e:
            logger.error(e)
