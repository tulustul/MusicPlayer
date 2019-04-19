#! /usr/bin/env python3
import asyncio
from dataclasses import dataclass
import logging

from core.app import App
from plugins.commands_palette.components import PaletteComponent
from ui.components.layout import Layout
from ui.components.table import TableComponent
from ui.components.label import LabelComponent
from ui.components.input import InputComponent

logger = logging.getLogger('player')


def setup(app: App):
    root = app.window.root_component

    list_component = TableComponent()
    app.window.focus(list_component)

    # list_component.data = [f'option {i}' for i in range(100)]
    from dataclasses import dataclass

    @dataclass
    class Data:
        option: str
        value: str

    list_component.data = [
        Data(f'option {i}', f'value {i}')
        for i in range(100)
    ]
    list_component.columns = [
        {
            "field": "option",
            "name": "Option",
            "priority": 1,
            "size": 10,
        },
        {
            "field": "value",
            "name": "Value",
            "priority": 2,
            "size": 20,
        },
        {
            "field": "__class__",
            "name": "class",
            "priority": 10,
        },
    ]

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
