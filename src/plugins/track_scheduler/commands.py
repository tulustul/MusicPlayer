import random

from commands.decorator import command
from plugins import playlist
import playback


@command()
def next_track():
    playlist.playlist_view.go_by(1)
    playback.current_track.on_next(playlist.playlist_view.value)


@command()
def previous_track():
    playlist.playlist_view.go_by(-1)
    playback.current_track.on_next(playlist.playlist_view.value)


@command()
def random_track():
    new_index = random.randrange(len(playlist.playlist_view.filtered_data))
    playlist.playlist_view.set_index(new_index)
    playback.current_track.on_next(playlist.playlist_view.value)
