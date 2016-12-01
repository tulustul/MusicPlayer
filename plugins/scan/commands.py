import glob
import logging
import os

import mutagen
from mutagen.id3 import ID3
from sqlalchemy import exists

import db
from commands.decorator import command
# from plugins import playlist
from plugins import library

logger = logging.getLogger('scan')


@command()
def scan_local_files(path):
    files = glob.iglob('{}/**/*.*'.format(path), recursive=True)

    files = (f for f in files if not os.path.isdir(f))

    tracks = (create_track(f) for f in files)
    tracks = (track for track in tracks if track)

    add_tracks(tracks)

    library.load_library()

    logger.info('Scan done')


def get_field(metadata, field):
    return metadata[field].text[0] if field in metadata else ''


def create_track(filepath):
    try:
        metadata = mutagen.File(filepath)
    except mutagen.MutagenError:
        logger.warn('Cannot process file "{}"'.format(filepath))
        return None

    if metadata:
        return library.models.Track(
            uri='file://{}'.format(filepath),
            source='local_disk',
            length=metadata.info.length,
            title=get_field(metadata, 'TIT2') or os.path.basename(filepath),
            album=get_field(metadata, 'TALB'),
            artist=get_field(metadata, 'TPE1'),
            album_artist=get_field(metadata, 'TPE2'),
            track_number=get_field(metadata, 'TRCK'),
            year=get_field(metadata, 'TYER'),
        )
    else:
        return None

def add_tracks(tracks):
    for track in tracks:
        tracks_exists = db.session.query(
            exists().where(library.models.Track.uri == track.uri)
        ).scalar()
        if not tracks_exists:
            db.session.add(track)
    db.session.commit()