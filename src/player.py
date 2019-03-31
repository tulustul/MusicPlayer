#! /usr/bin/env python3
from dataclasses import dataclass

from core.app import App
from ui.components.layout import Layout
from ui.components.table import TableComponent
from ui.components.label import LabelComponent


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

    layout.add(list_component)
    layout.add(LabelComponent('2'))

    layout2 = Layout()
    layout2.add(LabelComponent('3'))
    layout2.add(LabelComponent('4'))
    layout2.add(LabelComponent('5'))

    l = LabelComponent('bottom')
    l.desired_size = 1

    layout.add(layout2)
    layout.add(l)

    # app.window.set_root_component(layout)

if __name__ == '__main__':
    app = App()
    setup(app)
    app.run_forever()
