from dataclasses import dataclass
import logging
from typing import List, Collection, Dict, Type

from rx.core.observable import Observable

from core.db import get_session
from core.errors import errors
from core.config import config
from core.track import Track
from core.utils import async_log_time

logger = logging.getLogger("cloud")


@dataclass
class UploadData:
    track: Track
    source_path: str
    target_path: str


class CloudProvider:

    PROVIDERS_REGISTRY: Dict[str, Type["CloudProvider"]] = {}

    def __init__(self, config: dict):
        pass

    @classmethod
    def register_provider(cls, name: str, provider: Type["CloudProvider"]):
        cls.PROVIDERS_REGISTRY[name] = provider

    def push_files(self, uris: Collection[UploadData]) -> Observable:
        raise NotImplementedError

    async def pull_files(self, uris: Collection[str]):
        raise NotImplementedError


class CloudSynchronizer:
    def __init__(self):
        cloud_config = config.get("cloud", [])

        self.providers: List[CloudProvider] = [
            self._make_provider(c) for c in cloud_config
        ]

    @staticmethod
    def make_upload_data(track: Track):
        if not track.local_uri:
            return None

        target = "library/"
        if track.artist:
            target += f"{track.artist}/"
        if track.album:
            target += f"{track.album}/"
        target += track.title

        source = track.local_uri.lstrip("file:")

        # adding extension
        tokens = source.rsplit(".", 1)
        if len(tokens) > 1:
            target += f".{tokens[-1]}"

        return UploadData(source_path=source, target_path=target, track=track)

    @classmethod
    def _make_provider(cls, provider_config: dict):
        provider_key = provider_config["provider"]
        if provider_key not in CloudProvider.PROVIDERS_REGISTRY:
            raise ValueError(f'Unknown cloud provider: "{provider_key}"')

        return CloudProvider.PROVIDERS_REGISTRY[provider_key](provider_config)

    async def push_library(self):
        ...

    async def pull_library(self):
        ...

    @async_log_time
    async def push_tracks(self, tracks: Collection[Track], force=False):
        if any(not t.local_uri for t in tracks):
            errors.on_next("Rip track before pushing it to cloud.")
            return

        upload_data = [
            self.make_upload_data(t)
            for t in tracks
            if not t.cloud_synced or force
        ]

        for provider in self.providers:
            async for track in provider.push_files(upload_data):
                self._mark_as_synced(track)

    async def pull_tracks(self, tracks: Collection[Track]):
        ...

    def _mark_as_synced(self, track: Track):
        track.cloud_synced = True
        get_session().commit()
