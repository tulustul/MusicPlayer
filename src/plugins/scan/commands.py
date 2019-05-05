import asyncio
import functools
import glob
import logging
import os
from typing import List, Sequence

import mutagen
from mutagen.id3 import ID3
from sqlalchemy import exists

from core import db
from commands.decorator import command
from plugins import library
from player_ui import PlayerUI
from ui.components.progress import ProgressComponent
from ui.window import Window

logger = logging.getLogger('plugins.scan')


@command()
async def scan_local_files(window: Window, ui: PlayerUI):
    path = await window.input('path:')

    if not path:
        return

    progress_component = ProgressComponent()
    progress_component.set_text('listing files...')

    ui.stack_layout.add(progress_component)

    files = glob.iglob(f'{path}/**/*.*', recursive=True)

    files = (f for f in files if not os.path.isdir(f))

    progress_component.set_text('scanning...')

    result = await asyncio.get_event_loop().run_in_executor(
        None, functools.partial(create_tracks, progress_component, list(files)),
    )

    progress_component.detach()

    logger.info('Scan done')


def create_tracks(progress_component: ProgressComponent, files: List[str]):
    total = len(files)
    tracks: List[library.models.Track] = []
    for f in files:
        track = create_track(f)
        if track:
            tracks.append(track)
        progress_component.progress += 1 / total

    progress_component.set_text('saving to library...')

    add_tracks(tracks)


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
            uri=f'file://{filepath}',
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
