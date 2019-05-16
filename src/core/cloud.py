from typing import List, Sequence

from core.errors import errors
from plugins.library.models import Track


class CloudProvider:

    async def push_files(self, uris: Sequence[str]):
        raise NotImplementedError

    async def pull_files(self, uris: Sequence[str]):
        raise NotImplementedError


class Cloud:

    def __init__(self):
        self.providers: List[CloudProvider] = []

    async def push_library(self):
        ...

    async def pull_library(self):
        ...

    async def push_tracks(self, tracks: Sequence[Track]):
        uris = [t.local_uri for t in tracks if t.local_uri]

        if not all(uris):
            errors.on_next('Rip track before pushing it to cloud.')
            return

        for provider in self.providers:
            await provider.push_files(uris)

        Track.__table__.update().where(
            Track.id.in_(t.id for t in tracks)
        ).values(cloud_synced=True)

    async def pull_tracks(self, tracks: Sequence[Track]):
        ...
