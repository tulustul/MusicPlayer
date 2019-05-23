import logging
from typing import List, Iterable, Dict, Type

from core.errors import errors
from core.config import config
from core.track import Track

logger = logging.getLogger("cloud")


class CloudProvider:

    PROVIDER_KEY = None

    def __init__(self, config: dict):
        pass

    async def push_files(self, uris: Iterable[str]):
        raise NotImplementedError

    async def pull_files(self, uris: Iterable[str]):
        raise NotImplementedError


class CloudSynchronizer:

    PROVIDERS_REGISTRY: Dict[str, Type[CloudProvider]] = {}

    def __init__(self):
        cloud_config = config.get("cloud", [])

        self.providers: List[CloudProvider] = [
            self._make_provider(c) for c in cloud_config
        ]

    @classmethod
    def _make_provider(cls, provider_config: dict):
        provider_key = provider_config["provider"]
        if provider_key not in cls.PROVIDERS_REGISTRY:
            raise ValueError(f'Unknown cloud provider: "{provider_key}"')

        return cls.PROVIDERS_REGISTRY[provider_key](provider_config)

    async def push_library(self):
        ...

    async def pull_library(self):
        ...

    async def push_tracks(self, tracks: Iterable[Track]):
        uris = [t.local_uri for t in tracks]

        if not all(uris):
            errors.on_next("Rip track before pushing it to cloud.")
            return

        for provider in self.providers:
            await provider.push_files(uris)

        Track.__table__.update().where(
            Track.id.in_(t.id for t in tracks)
        ).values(cloud_synced=True)

    async def pull_tracks(self, tracks: Iterable[Track]):
        ...
