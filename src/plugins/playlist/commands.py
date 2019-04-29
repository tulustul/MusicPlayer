from commands.decorator import command
from core.commands_runner import CommandsRunner
from plugins import commands_palette
from ui.window import Window
from player_ui import PlayerUI

from ui.components.label import LabelComponent


@command()
async def open_playlists(ui: PlayerUI, window: Window):
    playlists_view = LabelComponent(
      'Playlists',
      align=LabelComponent.Align.center,
      size=40,
    )

    ui.top_layout.insert(0, playlists_view)
