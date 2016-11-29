import math
from collections import namedtuple
import logging

from rx.subjects import Subject, ReplaySubject

import audio
import ui
import utils

logger = logging.getLogger('playback')

current_position = 0
current_duration = 1
current_state = 'paused'

TimeTrack = namedtuple(
    'TimeTrack',
    ['elapsed', 'total', 'progress_percentage'],
)


def make_time_tracking(position):
    return TimeTrack(
        elapsed=utils.format_seconds(position),
        total=utils.format_seconds(current_duration),
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
end_of_track.subscribe(lambda _: logger.debug('END OF TRACK'))

state.subscribe(set_state)
progress.subscribe(set_position)
duration.subscribe(set_duration)

time_tracking = progress.map(make_time_tracking)
