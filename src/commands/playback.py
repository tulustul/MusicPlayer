import logging

from core.audio.audio_backend import AudioBackend
from ui.window import Window

from .decorator import command

logger = logging.getLogger('commands')

@command()
def play_track(window: Window, audio: AudioBackend):
    audio.play_track(window.active_component.value)


@command()
def pause_track(audio: AudioBackend):
    audio.toggle_pause()


@command()
def rewind(audio: AudioBackend, offset: int):
    audio.rewind(offset)
