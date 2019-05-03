from typing import Optional

from player import PlayerApp

from .views import PlaylistComponent


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
        else:
            self.playlists_view = PlaylistComponent(size=40)
            self.playlist_container.insert(0, self.playlists_view)
            self.app.window.focus(self.playlists_view)
