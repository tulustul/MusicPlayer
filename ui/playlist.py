from .listview import List
import playlist


class Playlist(List):

    def __init__(self):
        super().__init__()

        playlist.tracks.subscribe(self.set_tracks)

    def set_tracks(self, tracks):
        self.data = tracks
        self.refresh()

    def entry_value(self, entry):
        return entry.name
