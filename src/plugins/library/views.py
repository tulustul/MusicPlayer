import logging

from sqlalchemy import or_

from ui.components.tracks import TracksComponent
from core import db

from core.track import Track

logger = logging.getLogger('plugins.library')


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
