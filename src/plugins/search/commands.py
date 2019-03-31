import logging

from sqlalchemy import exists, or_

import db
from commands.decorator import command
from plugins import library
from plugins.library.models import Track
import stream

logger = logging.getLogger('search')


@command()
def search(query: str):
    query = f'%{query}%'
    tracks = db.session.query(Track).filter(or_(
        Track.title.ilike(query),
        Track.album.ilike(query),
        Track.artist.ilike(query),
        Track.album_artist.ilike(query),
        Track.genre.ilike(query),
    )).all()
    stream.get('library.tracks').on_next(tracks)
