from sqlalchemy import (
    Column,
    Integer,
    String,
)

import db


class Track(db.Base):
    __tablename__ = 'track'

    id: int = Column(Integer, primary_key=True)

    uri: str = Column(String(), nullable=False)
    source: str = Column(String(64), nullable=False)

    title: str = Column(String(250), nullable=False)
    album: str = Column(String(250), nullable=True)
    artist: str = Column(String(250), nullable=True)
    album_artist: str = Column(String(250), nullable=True)
    track_number: int = Column(Integer, nullable=True)
    year: int = Column(Integer, nullable=True)
    genre: str = Column(String(250), nullable=True)

    length: int = Column(Integer, nullable=True)
