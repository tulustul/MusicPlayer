import playback
from . import commands


def init():
    playback.end_of_track.subscribe(lambda _: commands.next_track())
