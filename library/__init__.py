import logging

from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker

from .models import *
import stream

logger = logging.getLogger('library')

session = None


def init():
    global session
    engine = create_engine('sqlite:///music.db')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    tracks = session.query(Track)

    stream.get('playlist.tracks').on_next(list(tracks))


def add_tracks(tracks):
    for track in tracks:
        tracks_exists = session.query(
            exists().where(Track.uri == track.uri)
        ).scalar()
        if not tracks_exists:
            session.add(track)
    session.commit()
