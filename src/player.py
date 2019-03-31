#! /usr/bin/env python3
import asyncio
from dataclasses import dataclass
import logging

from core.app import App
from ui.components.layout import Layout
from ui.components.table import TableComponent
from ui.components.label import LabelComponent
from ui.components.progress import ProgressComponent
from ui.components.input import InputComponent

logger = logging.getLogger('player')


def setup(app: App):
    layout = app.window.root_component
    layout.direction = Layout.Direction.vertical

    list_component = TableComponent()
    app.window.current_view = list_component

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
    layout2.direction = Layout.Direction.horizontal
    layout2.add(sidebar)
    layout2.add(list_component)

    layout.add(layout2)

    commands = LabelComponent('commands')
    commands.desired_size = 6

    layout.add(commands)

    progress_component = ProgressComponent()
    progress_component.set_text('progress', '')

    input_component = InputComponent()
    input_component.visible = False

    components = [
        input_component,
        progress_component,
        LabelComponent('errors'),
        LabelComponent('playback'),
    ]
    for c in components:
        c.desired_size = 1
        layout.add(c)

    app.window.input_component = input_component

    asyncio.get_event_loop().create_task(test_progress(progress_component))


async def test_progress(progress_component: ProgressComponent):
    while True:
        await asyncio.sleep(0.2)
        progress_component.progress += 0.01
        if progress_component.progress > 1:
            progress_component.progress = 0


if __name__ == '__main__':
    app = App()
    setup(app)
    app.run_forever()
