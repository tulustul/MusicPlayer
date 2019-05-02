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
def rewind_by_seconds(audio: AudioBackend, offset: int):
    audio.rewind_by_seconds(offset)


@command()
def rewind_by_percentage(audio: AudioBackend, offset: float):
    audio.rewind_by_percentage(offset)


@command()
def rewind_to_percentage(audio: AudioBackend, offset: float):
    audio.seek(audio.current_duration * offset)
