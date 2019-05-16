import logging
from typing import Optional

from ui.colors import colors
from ui.components.progress import ProgressComponent
from core.config import theme
from core import audio
from core.audio.audio_backend import TimeTrack

logger = logging.getLogger('ui')


class BarComponent(ProgressComponent):

    def __init__(self, audio: audio.AudioBackend, **kwargs):
        super().__init__(**kwargs)

        self.audio = audio

        self.playing_indicator = theme['strings']['playing']
        self.paused_indicator = theme['strings']['paused']

        self.time_track: Optional[TimeTrack] = None
        self.state = None

        self.track = None

        self.subscriptions = [
            self.audio.current_track.subscribe(self.on_track_changed),
            self.audio.time_tracking.subscribe(self.on_time_track_changed),
            self.audio.state.subscribe(self.on_state_changed),
        ]

        self.color = colors['bar']
        self.elapsed_color = colors['bar-elapsed']

    # def __del__(self):
    #     for subscription in self.subscriptions:
    #         subscription()

    def draw_content(self):
        self.right_text = '{}/{}'.format(
            self.time_track.elapsed if self.time_track else '-',
            self.time_track.total if self.time_track else '-',
        )

        self.left_text = f'{self.state_indicator} {self.track_name}'

        super().draw_content()

    def on_track_changed(self, track):
        if self.track != track:
            self.track = track
            self.mark_for_redraw()

    def on_time_track_changed(self, time_track: audio.audio_backend.TimeTrack):
        if (
            not self.time_track or
            self.time_track.elapsed != time_track.elapsed
        ):
            self.time_track = time_track
            self.progress = (
                self.time_track.progress_percentage if self.time_track else 0
            )

    def on_state_changed(self, state):
        if self.state != state:
            self.state = state
            self.mark_for_redraw()

    @property
    def track_name(self):
        return '{} - {}'.format(
            self.track.title,
            self.track.artist,
        ) if self.track else '---'

    @property
    def state_indicator(self):
        if self.state == self.audio.State.playing:
            return self.playing_indicator
        elif self.state == self.audio.State.paused:
            return self.paused_indicator
        else:
            return ''
