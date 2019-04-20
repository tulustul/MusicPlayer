from sqlalchemy import Column, Integer, String

from core import db


class Track(db.Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True)

    uri = Column(String(), nullable=False)
    source = Column(String(64), nullable=False)

    title = Column(String(250), nullable=False)
    album = Column(String(250), nullable=True)
    artist = Column(String(250), nullable=True)
    album_artist = Column(String(250), nullable=True)
    track_number = Column(Integer, nullable=True)
    year = Column(Integer, nullable=True)
    genre = Column(String(250), nullable=True)

    length = Column(Integer, nullable=True)
