import math
from collections import namedtuple
import logging

from rx.subjects import Subject, ReplaySubject

import audio
import ui

logger = logging.getLogger('playback')

current_position = 0
current_duration = 1
current_state = 'paused'

TimeTrack = namedtuple(
    'TimeTrack',
    ['elapsed', 'total', 'progress_percentage'],
)


def format_seconds(seconds):
    seconds = int(seconds)

    hours = math.floor(seconds / 3600)
    seconds -= hours * 3600

    minutes = math.floor(seconds / 60)
    seconds -= minutes * 60

    formatted = '{}:{}'.format(minutes, str(seconds).zfill(2))
    if hours:
        formatted = '{}:{}'.format(hours, minutes)

    return formatted


def make_time_tracking(position):
    return TimeTrack(
        elapsed=format_seconds(position),
        total=format_seconds(current_duration),
        progress_percentage=position * 100 / current_duration,
    )


def set_position(p):
    global current_position
    current_position = p


def set_duration(d):
    global current_duration
    current_duration = d


def set_state(s):
    global current_state
    current_state = s


def play_track(track):
    audio.set_track(track)
    audio.play()


def next_track(_=None):
    set_track_by(1)


def previous_track(_=None):
    set_track_by(-1)


def set_track_by(offset):
    view = ui.win.current_view()
    view.index += offset
    view.refresh()
    current_track.on_next(view.value)


def rewind(offset):
    new_position = current_position + offset
    new_position = min(current_duration, max(0, new_position))
    audio.seek(new_position)


def toggle_pause():
    if current_state == 'playing':
        audio.pause()
    elif current_state == 'paused':
        audio.play()
    else:
        logger.error('Unknown playback state "{}"'.format(current_state))


state = ReplaySubject(1)
current_track = ReplaySubject(1)
progress = ReplaySubject(1)
duration = ReplaySubject(1)
end_of_track = Subject()

current_track.subscribe(play_track)
end_of_track.subscribe(next_track)

state.subscribe(set_state)
progress.subscribe(set_position)
duration.subscribe(set_duration)

time_tracking = progress.map(make_time_tracking)
