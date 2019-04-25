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


def setup(app: App):
    root = app.window.root_component

    list_component = LibraryComponent(context='tracks')
    app.window.focus(list_component)

    bar_component = BarComponent(app.audio)

    sidebar = LabelComponent('sidebar')
    sidebar.desired_size = 30

    layout2 = Layout()
    root.add(layout2)

    layout2.direction = Layout.Direction.horizontal
    # layout2.add(sidebar)
    layout2.add(list_component)

    commands = PaletteComponent()
    commands.desired_size = 6
    commands.visible = False

    root.add(commands)

    input_component = InputComponent()
    input_component.visible = False

    notifications = Layout()

    app.window.notifications_layout = notifications
    components = [
        notifications,
        input_component,
        bar_component,
    ]
    for c in components:
        c.desired_size = 1
        root.add(c)

    app.window.input_component = input_component

    for component in app.window.root_component.get_descendants():
        component.mark_for_redraw()


if __name__ == '__main__':
    app = App()
    setup(app)
    app.run_forever()
