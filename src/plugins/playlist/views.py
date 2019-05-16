import logging
from typing import List

from core import db
from core.app import App
from ui.components.listview import ListComponent
from plugins.library.models import Track
from plugins.library.views import TracksComponent

from .models import Playlist, PlaylistTrack

logger = logging.getLogger("plugins.playlist")


class PlaylistsComponent(ListComponent[str]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_playlists()

    def load_playlists(self):
        self.data = self.query(db.session.query(Playlist.name).all())

    def filter(self, query: str):
        session = db.get_session()

        query = f"%{query}%"
        self.data = self.query(
            session.query(Playlist.name)
            .filter(Playlist.name.ilike(query))
            .scalar()
        )

        self.mark_for_redraw()

    def query(self, query):
        return list(zip(*query))[0]

    async def on_delete(self, playlists_names: List[str]):
        session = db.get_session()
        app = App.get_instance()
        yesno = (
            await app.window.input("Delete selected playlists? (y/n)") == "y"
        )
        if yesno:
            session.query(Playlist).filter(
                Playlist.name.in_(playlists_names)
            ).delete(synchronize_session=False)
            session.commit()
            self.load_playlists()


class PlaylistTracksComponent(TracksComponent):
    def __init__(self, playlist: Playlist, **kwargs):
        super().__init__(**kwargs)
        self.playlist = playlist
        self.load_playlist()

    def get_query(self):
        session = db.get_session()
        return session.query(PlaylistTrack).filter(
            PlaylistTrack.playlist_id == self.playlist.id
        )

    def load_playlist(self):
        tracks = self.get_query().order_by(PlaylistTrack.order.asc())
        self.data = [t.track for t in tracks]

    def on_paste(self, tracks: List[Track]):
        session = db.get_session()

        start_index = self.get_query().count()

        playlist_tracks = [
            PlaylistTrack(
                playlist_id=self.playlist.id,
                track_id=track.id,
                order=start_index + index,
            )
            for index, track in enumerate(tracks)
        ]

        session.bulk_save_objects(playlist_tracks)
        session.commit()

        self.load_playlist()

    def on_delete(self, tracks: List[Track]):
        session = db.get_session()

        self.get_query().filter(
            PlaylistTrack.track_id.in_(t.id for t in tracks)
        ).delete(synchronize_session=False)

        session.commit()

        self.load_playlist()
