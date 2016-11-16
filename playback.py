import logging

from rx.subjects import Subject

import audio
import playlist
import ui

logger = logging.getLogger('playback')


def play_track(track):
    audio.set_track(track)
    audio.play()


def next_track(_=None):
    set_track_by(1)


def previous_track(_=None):
    set_track_by(-1)


def set_track_by(offset):
    view = ui.win.get_focused_view()
    view.index += offset
    view.refresh()
    current_track.on_next(view.value)


current_track = Subject()
progress = Subject()
duration = Subject()
end_of_track = Subject()

current_track.subscribe(play_track)
end_of_track.subscribe(next_track)
