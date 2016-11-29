from rx.subjects import ReplaySubject

import stream
import db
from . import models

tracks = ReplaySubject(1)


def load_library():
    track_models = db.session.query(models.Track)
    tracks.on_next(list(track_models))


def init():
    stream.register('library.tracks', tracks)
    load_library()
