from dataclasses import dataclass
import logging
from enum import Enum

from rx.subjects import Subject, ReplaySubject
from rx.operators import map

from core import utils
from plugins.library.models import Track

logger = logging.getLogger('audio')


@dataclass
class TimeTrack:
    elapsed: int
    total: int
    progress_percentage: float


class AudioBackend:

    class State(Enum):
        paused = 1
        playing = 2

    def __init__(self):
        self.playing = False

        self.current_position = 0
        self.current_duration = 1
        self.current_state = self.State.paused

        self.state = ReplaySubject(1)
        self.current_track = ReplaySubject(1)
        self.progress = ReplaySubject(1)
        self.duration = ReplaySubject(1)
        self.end_of_track = Subject()

        self.end_of_track.subscribe(lambda _: logger.debug('END OF TRACK'))

        self.state.subscribe(self.set_state)
        self.progress.subscribe(self.set_position)
        self.duration.subscribe(self.set_duration)

        self.time_tracking = self.progress.pipe(map(self.make_time_tracking))

    def destroy(self) -> None:
        raise NotImplemented

    def set_track(self, track: Track) -> None:
        raise NotImplemented

    def seek(self, position: int) -> None:
        raise NotImplemented

    def play(self) -> None:
        raise NotImplemented

    def pause(self) -> None:
        raise NotImplemented

    def make_time_tracking(self, position: int):
        return TimeTrack(
            elapsed=utils.format_seconds(position),
            total=utils.format_seconds(self.current_duration),
            progress_percentage=position / self.current_duration,
        )

    def set_position(self, position: int):
        self.current_position = position

    def set_duration(self, duration: int):
        self.current_duration = duration

    def set_state(self, state):
        self.current_state = state

    def play_track(self, track: Track):
        self.current_track.on_next(track)
        self.set_track(track)
        self.play()

    def rewind(self, offset: int):
        new_position = self.current_position + offset
        new_position = min(self.current_duration, max(0, new_position))
        self.seek(new_position)

    def toggle_pause(self):
        if self.current_state == self.State.playing:
            audio.pause()
        elif self.current_state == self.State.paused:
            audio.play()
        else:
            logger.error(f'Unknown playback state "{self.current_state}"')
