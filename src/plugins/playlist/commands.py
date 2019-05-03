from core import db
from commands.decorator import command
from core.commands_runner import CommandsRunner
from plugins import commands_palette
from ui.window import Window
from player_ui import PlayerUI

from ui.components.label import LabelComponent

from .controller import PlaylistController
from .models import Playlist


@command()
def toggle_playlists(controller: PlaylistController):
    controller.toggle_playlists()


@command()
async def create_playlist(window: Window):
    playlists_count = db.session.query(Playlist).count()
    default_name = f'playlist {playlists_count + 1}'
    playlist_name = await window.input('new playlist name:', default_name)

    playlist = Playlist(name=playlist_name)
    db.session.add(playlist)
    db.session.commit()
