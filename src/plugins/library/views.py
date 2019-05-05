import logging

from sqlalchemy import or_

from ui.components.table import TableComponent
from core.app import App
from core.config import config
from core import db

from .models import Track

logger = logging.getLogger('plugins.library')


class TracksComponent(TableComponent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.columns = config['playlist']['columns']

    def select(self):
        super().select()
        App.get_instance().audio.play_track(self.value)


class LibraryComponent(TracksComponent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = list(db.session.query(Track))

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
