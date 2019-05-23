from commands.decorator import command
from core.cloud import CloudSynchronizer
from ui.components.tracks import TracksComponent


@command()
async def push_tracks(tracks_component: TracksComponent):
    cloud = CloudSynchronizer()
    await cloud.push_tracks(tracks_component.marked_items)
