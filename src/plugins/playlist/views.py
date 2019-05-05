import logging

from core import db
from ui.components.listview import ListComponent
from plugins.library.views import TracksComponent

from .models import Playlist

logger = logging.getLogger('plugins.playlist')


class PlaylistsComponent(ListComponent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = self.query(db.session.query(Playlist.name).all())

    def filter(self, query: str):
        if not db.session:
            return

        query = f'%{query}%'
        self.data = self.query(db.session.query(Playlist.name).filter(
            Playlist.name.ilike(query),
        ).scalar())

        self.mark_for_redraw()

    def query(self, query):
        return list(zip(*query))[0]


class PlaylistTracksComponent(TracksComponent):

    def __init__(self, playlist: Playlist, **kwargs):
        super().__init__(**kwargs)
        self.playlist = playlist
