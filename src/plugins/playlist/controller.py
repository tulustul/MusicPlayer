import logging
from typing import Optional

from core import db
from player import PlayerApp
from ui.components.tabs_layout import Tab

from .models import Playlist
from .views import PlaylistsComponent, PlaylistTracksComponent

logger = logging.getLogger('plugins.playlist')


class PlaylistController:

    def __init__(self):
        self.app: PlayerApp = PlayerApp.get_instance()
        self.playlist_container = self.app.ui.top_layout

        self.playlists_view: Optional[LabelComponent] = None

        self.app.injector.provide(PlaylistController, lambda: self)

    def toggle_playlists(self):
        if self.playlists_view:
            self.app.window.blur_active_component()
            self.playlists_view.detach()
            self.playlists_view = None
            if self.subscription:
                self.subscription.dispose()
                self.subscription = None
        else:
            self.playlists_view = PlaylistsComponent(size=40)
            self.playlist_container.insert(0, self.playlists_view)
            self.app.window.focus(self.playlists_view)

            self.subscription = self.playlists_view.selected_item.subscribe(self.open_playlist)

    def open_playlist(self, playlist_name: str):
        playlist = db.session.query(Playlist).filter(
            Playlist.name == playlist_name,
        ).one()

        if not playlist:
            logger.error(f'Unable to open playlist {playlist_name}')
            return

        tabs_layout = self.app.ui.tabs_layout
        tab = tabs_layout.get_tab(playlist.name)
        if tab:
            tabs_layout.switch_to_tab(tab)
        else:
            tracks_view = PlaylistTracksComponent(playlist)
            self.app.ui.tabs_layout.add_tab(Tab(
                title=playlist.name,
                component=tracks_view,
            ))
