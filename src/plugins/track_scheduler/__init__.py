from core.app import App

from . import commands


def init():
    app = App.get_instance()

    app.audio.end_of_track.subscribe(
      lambda _: commands.next_track(app.window, app.audio),
    )
