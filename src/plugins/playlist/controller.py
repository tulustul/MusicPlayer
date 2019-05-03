from typing import Optional

from player import PlayerApp
from ui.components.label import LabelComponent

from .views import PlaylistComponent


class PlaylistController:

    def __init__(self):
        app: PlayerApp = PlayerApp.get_instance()
        self.playlist_container = app.ui.top_layout

        self.playlists_view: Optional[LabelComponent] = None

        app.injector.provide(PlaylistController, lambda: self)

    def toggle_playlists(self):
        if self.playlists_view:
            self.playlists_view.detach()
            self.playlists_view = None
        else:
            self.playlists_view = LabelComponent(
                'Playlist1',
                align=LabelComponent.Align.center,
                size=40,
            )
            self.playlist_container.insert(0, self.playlists_view)
