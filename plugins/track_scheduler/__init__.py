import playback
from plugins import playlist


def play_next_track(_):
    playlist.playlist_view.go_by(1)
    playback.current_track.on_next(playlist.playlist_view.value)


def init():
    playback.end_of_track.subscribe(play_next_track)
