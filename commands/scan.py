import glob
import logging
import os

from .decorator import command
import playlist
from library.models import Track
import library

logger = logging.getLogger('scan')


@command()
def scan_local_files(path):
    files = glob.iglob('{}/**/*.*'.format(path), recursive=True)

    tracks = [create_track(f) for f in files]
    library.add_tracks(tracks)

    files = [os.path.basename(track.name) for track in tracks]

    playlist.tracks.on_next(files)


def create_track(filepath):
    return Track(
        name=os.path.basename(filepath),
        uri='file://{}'.format(filepath),
    )
