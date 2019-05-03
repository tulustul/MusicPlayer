import random

from player_ui import PlayerUI
from commands.decorator import command
from ui.window import Window
from core.audio import AudioBackend


@command()
def next_track(ui: PlayerUI, audio: AudioBackend):
    if ui.tracks_view.is_last:
      ui.tracks_view.set_index(0)
    else:
      ui.tracks_view.go_by(1)

    audio.play_track(ui.tracks_view.value)


@command()
def previous_track(ui: PlayerUI, audio: AudioBackend):
    if ui.tracks_view.is_first:
        ui.tracks_view.set_index(len(ui.tracks_view.filtered_data))
    else:
        ui.tracks_view.go_by(-1)
    audio.play_track(ui.tracks_view.value)


@command()
def random_track(ui: PlayerUI, audio: AudioBackend):
    new_index = random.randrange(len(ui.tracks_view.filtered_data))
    ui.tracks_view.set_index(new_index)
    audio.play_track(ui.tracks_view.value)
