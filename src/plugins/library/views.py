import logging

from sqlalchemy import or_

from ui.components.table import TableComponent
from core.config import config
from core import db

from .models import Track

logger = logging.getLogger('ui')


class LibraryComponent(TableComponent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.data = list(db.session.query(Track))

        self.columns = config['playlist']['columns']

    def set_tracks(self, tracks):
        logger.info('tracks: {}'.format(len(tracks)))
        self.data = tracks
        self.refresh()

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
