from commands.decorator import command
from core.commands_runner import CommandsRunner
from plugins import commands_palette
from ui.window import Window
from player_ui import PlayerUI

from ui.components.label import LabelComponent

from .controller import PlaylistController


class PlaylistCommands:

    @command()
    async def toggle_playlists(controller: PlaylistController):
        controller.toggle_playlists()
