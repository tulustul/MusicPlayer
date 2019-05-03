from core.app import App

from . import commands


class TrackSchedulerController:

    def __init__(self):
        app = App.get_instance()

        app.audio.end_of_track.subscribe(
          lambda _: commands.next_track(app.window, app.audio),
        )

controller = TrackSchedulerController
