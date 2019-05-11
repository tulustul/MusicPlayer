from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core import db
from plugins.library.models import Track


class Playlist(db.Base):
    __tablename__ = 'playlist'

    id = Column(Integer, primary_key=True)

    name = Column(String(250), nullable=False)

    tracks = relationship('PlaylistTrack', lazy='raise')


class PlaylistTrack(db.Base):
    __tablename__ = 'playlist_track'

    id = Column(Integer, primary_key=True)

    order = Column(Integer)

    playlist_id = Column(Integer, ForeignKey(Playlist.id))
    playlist = relationship(Playlist, back_populates='tracks')

    track_id = Column(Integer, ForeignKey(Track.id))
    track = relationship(Track, lazy='joined')
