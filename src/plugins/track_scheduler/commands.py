import random

from commands.decorator import command
from ui.window import Window
from core.audio import AudioBackend


@command()
def next_track(window: Window, audio: AudioBackend):
    if window.active_component.is_last:
      window.active_component.set_index(0)
    else:
      window.active_component.go_by(1)

    audio.play_track(window.active_component.value)


@command()
def previous_track(window: Window, audio: AudioBackend):
    if window.active_component.is_first:
        window.active_component.set_index(len(window.active_component.filtered_data))
    else:
        window.active_component.go_by(-1)
    audio.play_track(window.active_component.value)


@command()
def random_track(window: Window, audio: AudioBackend):
    new_index = random.randrange(len(window.active_component.filtered_data))
    window.active_component.set_index(new_index)
    audio.play_track(window.active_component.value)
