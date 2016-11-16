import logging

from .decorator import command
import audio
import playback
import playlist
import ui

logger = logging.getLogger('commands')


@command()
def play_track():
    playback.current_track.on_next(ui.win.get_focused_view().value)


@command()
def seek():
    audio.seek()


@command()
def next_track():
    playback.next_track()



@command()
def previous_track():
    playback.previous_track()
