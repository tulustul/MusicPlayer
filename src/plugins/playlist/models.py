from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core import db
from plugins.library.models import Track


class PlaylistTrack(db.Base):
    __tablename__ = 'playlist_tracks'

    id = Column(Integer, primary_key=True)
    order = Column(Integer)

    playlist = Column(Integer, ForeignKey('playlist.id'))
    track = Column(Integer, ForeignKey(Track.id))


class Playlist(db.Base):
    __tablename__ = 'playlist'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    tracks = relationship(PlaylistTrack)
