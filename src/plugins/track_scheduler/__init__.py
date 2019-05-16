from player import PlayerApp

from . import commands


class TrackSchedulerController:
    def __init__(self):
        app = PlayerApp.get_instance()

        app.audio.end_of_track.subscribe(
            lambda _: commands.next_track(app.ui, app.audio)
        )


controller = TrackSchedulerController
