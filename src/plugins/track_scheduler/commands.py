import random

from player_ui import PlayerUI
from commands.decorator import command
from ui.window import Window
from core.audio import AudioBackend


@command()
def next_track(ui: PlayerUI, audio: AudioBackend):
    skip_tracks_by(ui, audio, 1)


@command()
def previous_track(ui: PlayerUI, audio: AudioBackend):
    skip_tracks_by(ui, audio, -1)


@command()
def random_track(ui: PlayerUI, audio: AudioBackend):
    new_index = random.randrange(len(ui.tracks_view.filtered_data))
    ui.tracks_view.set_index(new_index)
    audio.play_track(ui.tracks_view.value)


@command()
def find_playing_track(ui: PlayerUI):
    current_item = ui.tracks_view.distinguished_item
    if current_item:
        index = ui.tracks_view.filtered_data.index(current_item)
        ui.tracks_view.set_index(index)


def skip_tracks_by(ui: PlayerUI, audio: AudioBackend, offset: int):
    current_item = ui.tracks_view.distinguished_item
    if current_item:
        index = ui.tracks_view.filtered_data.index(current_item)
        new_index = ui.tracks_view.wrap_index(index + offset)
        track = ui.tracks_view.filtered_data[new_index]
    elif ui.tracks_view.filtered_data:
        track = ui.tracks_view.filtered_data[0]

    if track:
        ui.tracks_view.distinguished_item = track
        audio.play_track(track)
