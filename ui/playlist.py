from .listview import List
from config import config
import playlist


class Playlist(List):

    def __init__(self):
        super().__init__()

        self.columns = config['playlist']['columns']

        playlist.tracks.subscribe(self.set_tracks)

    def set_tracks(self, tracks):
        self.data = tracks
        self.refresh()
