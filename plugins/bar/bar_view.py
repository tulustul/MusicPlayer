import logging

from config import theme
from ui.toolkit.component import Component
from ui.colors import colors
import playback
import context

logger = logging.getLogger('ui')


class Bar(Component):

    def __init__(self):
        super().__init__()

        self.playing_indicator = theme['strings']['playing']
        self.paused_indicator = theme['strings']['paused']

        self.time_track = None
        self.state = None

        self.track = None

        self.context_name = None

        self.subscriptions = [
            playback.current_track.subscribe(self.on_track_changed),
            playback.time_tracking.subscribe(self.on_time_track_changed),
            playback.state.subscribe(self.on_state_changed),
            context.switch.subscribe(self.on_context_changed),
        ]

        self.color = colors['bar']
        self.elapsed_color = colors['bar-elapsed']

    # def __del__(self):
    #     for subscription in self.subscriptions:
    #         subscription()

    def draw_content(self):
        progress_percentage = (
            self.time_track.progress_percentage if self.time_track else 0
        )

        right_text = '{}/{} {}%  {}'.format(
            self.time_track.elapsed if self.time_track else '-',
            self.time_track.total if self.time_track else '-',
            int(progress_percentage) if self.time_track else '-',
            self.context_name,
        )

        left_text = '{} {}'.format(
            self.state_indicator,
            self.track_name,
        )

        max_left_text_length = self.cols - len(right_text) - 1
        if len(left_text) >= max_left_text_length:
            left_text = left_text[:max_left_text_length - 2] + '… '

        text = '{}{}{}'.format(
            left_text,
            ' ' * (self.cols - len(left_text) - 1 - len(right_text)),
            right_text,
        )

        progress_div = int(self.cols * (progress_percentage / 100))
        progress_div = min(self.cols - 1, progress_div)


        self.win.addstr(0, 0, text[:progress_div], self.elapsed_color)
        self.win.addstr(0, progress_div, text[progress_div:], self.color)

    def on_track_changed(self, track):
        if self.track != track:
            self.track = track
            self.refresh()

    def on_time_track_changed(self, time_track):
        if (
            not self.time_track or
            self.time_track.elapsed != time_track.elapsed
        ):
            self.time_track = time_track
            self.refresh()

    def on_state_changed(self, state):
        if self.state != state:
            self.state = state
            self.refresh()

    def on_context_changed(self, context):
        self.context_name = context.name
        self.refresh()

    @property
    def track_name(self):
        return '{} - {}'.format(
            self.track.title,
            self.track.artist,
        ) if self.track else '---'

    @property
    def state_indicator(self):
        if self.state == 'playing':
            return self.playing_indicator
        elif self.state == 'paused':
            return self.paused_indicator
        else:
            return ''
