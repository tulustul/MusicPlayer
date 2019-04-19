import logging

from ui.components.listview import ListComponent
import commands

logger = logging.getLogger('commands_palette')


class PaletteComponent(ListComponent):

    def __init__(self):
        super().__init__()

        self._search_enabled = True

        self.data = commands.registry.get_names()
