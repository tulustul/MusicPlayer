import math
from collections import namedtuple
import logging

from rx.subjects import Subject, ReplaySubject
from rx.operators import map

from core import audio, utils
import ui

logger = logging.getLogger('playback')



TimeTrack = namedtuple(
    'TimeTrack',
    ['elapsed', 'total', 'progress_percentage'],
)


