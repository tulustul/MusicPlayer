from core import db
from commands.decorator import command
from ui.window import Window

from .controller import PlaylistController
from .models import Playlist


@command()
def toggle_playlists(controller: PlaylistController):
    controller.toggle_playlists()


@command()
async def create_playlist(window: Window):
    playlists_count = db.get_session().query(Playlist).count()
    default_name = f'playlist {playlists_count + 1}'
    playlist_name = await window.input('new playlist name:', default_name)

    playlist = Playlist(name=playlist_name)
    db.get_session().add(playlist)
    db.get_session().commit()
