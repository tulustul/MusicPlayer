import logging

from sqlalchemy import or_

from ui.components.table import TableComponent
from core.app import App
from core.config import config
from core import db

from .models import Track

logger = logging.getLogger('plugins.library')


class TracksComponent(TableComponent[Track]):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.columns = config['playlist']['columns']

        app = App.get_instance()

        app.audio.current_track.subscribe(self.set_distinguished_item)

    def on_select(self, track: Track):
        App.get_instance().audio.play_track(track)


class LibraryComponent(TracksComponent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        session = db.get_session()

        self.data = list(session.query(Track))

    def filter(self, query: str):
        if not db.session:
            return

        query = f'%{query}%'
        self.data = list(db.session.query(Track).filter(or_(
            Track.title.ilike(query),
            Track.album.ilike(query),
            Track.artist.ilike(query),
            Track.album_artist.ilike(query),
            Track.genre.ilike(query),
        )).all())

        self.mark_for_redraw()
