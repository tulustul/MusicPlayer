#! /usr/bin/env python3
import asyncio
from dataclasses import dataclass
import logging

from core.app import App
from plugins.commands_palette.components import PaletteComponent
from plugins.library.views import LibraryComponent
from plugins.bar.views import BarComponent
from ui.components.layout import Layout
from ui.components.table import TableComponent
from ui.components.label import LabelComponent
from ui.components.input import InputComponent

logger = logging.getLogger('player')


class PlayerUI:

    def __init__(self, app: App):
        self.root = app.window.root_component

        self.tracks_view = LibraryComponent(context='tracks')
        app.window.focus(self.tracks_view)

        self.bar_component = BarComponent(app.audio, desired_size=1)

        # sidebar = Layout(desired_size=30)

        top_layout = Layout()
        self.root.add(top_layout)

        top_layout.direction = Layout.Direction.horizontal
        # top_layout.add(sidebar)
        top_layout.add(self.tracks_view)

        self.stack_layout = Layout()

        app.window.input_container = self.stack_layout
        self.root.add(self.stack_layout)
        self.root.add(self.bar_component)

        for component in app.window.root_component.get_descendants():
            component.mark_for_redraw()


class PlayerApp(App):

    def setup(self):
        self.ui = PlayerUI(self)
        self.injector.provide(PlayerUI, lambda: self.ui)


if __name__ == '__main__':
    PlayerApp().run_forever()
