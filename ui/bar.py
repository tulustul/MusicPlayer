import logging

from .widget import Widget
from playback import current_track, duration, progress

logger = logging.getLogger('ui')


class Bar(Widget):

    HEIGHT = 1

    def __init__(self):
        super().__init__()

        self.duration = 1
        self.progress = 0

        self.track = None
        current_track.subscribe(self.on_track_changed)
        duration.subscribe(self.on_duration_changed)
        progress.subscribe(self.on_progress_changed)

    def refresh(self):
        self.win.clear()
        self.win.addstr(0, 0, 'now playing: {}'.format(self.track_name))

        progress = int((self.progress * 100) / self.duration)
        text = 'progress: {}%'.format(progress)
        self.win.addstr(0, self.cols - len(text) - 1, text)
        super().refresh()

    def on_track_changed(self, track):
        self.track = track
        self.refresh()

    def on_duration_changed(self, duration):
        self.duration = duration
        self.refresh()

    def on_progress_changed(self, progress):
        self.progress = progress
        self.refresh()

    @property
    def track_name(self):
        return self.track.name if self.track else ''
