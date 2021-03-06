from dataclasses import dataclass
import logging
from enum import Enum

from rx.subjects import Subject, ReplaySubject
from rx.operators import map

from core import utils
from core.track import Track

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
        self.position = ReplaySubject(1)
        self.duration = ReplaySubject(1)
        self.end_of_track = Subject()

        self.end_of_track.subscribe(lambda _: logger.debug('END OF TRACK'))

        self.state.subscribe(self.set_state)
        self.position.subscribe(self.set_position)
        self.duration.subscribe(self.set_duration)

        self.time_tracking = self.position.pipe(map(self.make_time_tracking))

    def destroy(self) -> None:
        raise NotImplementedError

    def set_track(self, track: Track) -> None:
        raise NotImplementedError

    def seek(self, position: int) -> None:
        raise NotImplementedError

    def play(self) -> None:
        raise NotImplementedError

    def pause(self) -> None:
        raise NotImplementedError

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

    def rewind_by_seconds(self, offset: int):
        new_position = self.current_position + offset
        new_position = min(self.current_duration, max(0, new_position))
        self.seek(new_position)

    def rewind_by_percentage(self, offset: float):
        self.rewind_by_seconds(self.current_duration * offset)

    def toggle_pause(self):
        if self.current_state == self.State.playing:
            self.pause()
        elif self.current_state == self.State.paused:
            self.play()
        else:
            logger.error(f'Unknown playback state "{self.current_state}"')
