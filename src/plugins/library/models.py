from sqlalchemy import Column, Integer, String, Boolean

from core import db


class Track(db.Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True)

    source = Column(String(64), nullable=False)

    uri = Column(String(), nullable=False)

    local_uri = Column(String(), nullable=True)

    cloud_synced = Column(Boolean, default=False)

    # track metadata below

    title = Column(String(250), nullable=False)

    album = Column(String(250), nullable=True)

    artist = Column(String(250), nullable=True)

    album_artist = Column(String(250), nullable=True)

    track_number = Column(Integer, nullable=True)

    year = Column(Integer, nullable=True)

    genre = Column(String(250), nullable=True)

    length = Column(Integer, nullable=True)
