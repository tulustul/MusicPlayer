from ui.components.table import TableComponent
from core.app import App
from core.config import config

from core.track import Track


class TracksComponent(TableComponent[Track]):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.columns = config['playlist']['columns']

        app = App.get_instance()

        app.audio.current_track.subscribe(self.set_distinguished_item)

    def on_select(self, track: Track):
        App.get_instance().audio.play_track(track)
