from commands.decorator import command
from core.cloud import CloudSynchronizer
from core.db import get_session
from core.track import Track
from ui.components.tracks import TracksComponent


@command()
async def push_all_tracks(tracks_component: TracksComponent, force=False):
    all_tracks = get_session().query(Track).all()
    await CloudSynchronizer().push_tracks(all_tracks, force)


@command()
async def push_tracks(tracks_component: TracksComponent, force=False):
    await CloudSynchronizer().push_tracks(tracks_component.marked_items, force)


@command()
async def push_tracks_force(tracks_component: TracksComponent):
    await push_tracks(tracks_component, True)
