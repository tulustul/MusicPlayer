import logging

from .decorator import command
import core.playback
import ui

logger = logging.getLogger('commands')

@command()
def play_track():
    playback.current_track.on_next(ui.win.current_view.value)


@command()
def pause_track():
    playback.toggle_pause()


@command()
def rewind(offset):
    playback.rewind(offset)
