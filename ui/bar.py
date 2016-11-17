import logging

from config import theme
from .colors import colors
from .widget import Widget
import playback

logger = logging.getLogger('ui')


class Bar(Widget):

    HEIGHT = 1

    def __init__(self):
        super().__init__()

        self.playing_indicator = theme['strings']['playing']
        self.paused_indicator = theme['strings']['paused']

        self.time_track = None
        self.state = None

        self.track = None
        playback.current_track.subscribe(self.on_track_changed)
        playback.time_tracking.subscribe(self.on_time_track_changed)
        playback.state.subscribe(self.on_state_changed)

        self.color = colors['bar']

    def refresh(self):
        self.win.clear()
        self.win.bkgd(' ', self.color)
        text = '{} {}'.format(self.state_indicator, self.track_name)
        self.win.addstr(0, 0, text)

        if self.time_track:
            text = '{}/{} {}%'.format(
                self.time_track.elapsed,
                self.time_track.total,
                int(self.time_track.progress_percentage),
            )
            self.win.addstr(0, self.cols - len(text) - 1, text, self.color)
        super().refresh()

    def on_track_changed(self, track):
        self.track = track
        self.refresh()

    def on_time_track_changed(self, time_track):
        self.time_track = time_track
        self.refresh()

    def on_state_changed(self, state):
        self.state = state
        self.refresh()

    @property
    def track_name(self):
        return self.track.name if self.track else ''

    @property
    def state_indicator(self):
        if self.state == 'playing':
            return self.playing_indicator
        elif self.state == 'paused':
            return self.paused_indicator
        else:
            return ''
