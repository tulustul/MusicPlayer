from core.app import App
from plugins.library.views import LibraryComponent
from plugins.bar.views import BarComponent
from ui import colors
from ui.components.layout import Layout
from ui.components.table import TableComponent
from ui.components.label import LabelComponent
from ui.components.input import InputComponent


class PlayerUI:

    def __init__(self, app: App):
        self.root = app.window.root_component

        self.tracks_view = LibraryComponent(context='tracks')
        app.window.focus(self.tracks_view)

        self.bar_component = BarComponent(app.audio)

        # sidebar = Layout(size=30)

        self.top_layout = Layout()
        self.root.add(self.top_layout)

        self.top_layout.direction = Layout.Direction.horizontal
        # self.top_layout.add(sidebar)
        self.top_layout.add(self.tracks_view)

        self.stack_layout = Layout()

        app.window.input_container = self.stack_layout
        self.root.add(self.stack_layout)
        self.root.add(self.bar_component)

        for component in app.window.root_component.get_descendants():
            component.mark_for_redraw()

    def show_error(self, text: str):
        error_component = LabelComponent(
            text,
            align=LabelComponent.Align.left,
            color=colors.colors['error'],
            context='error',
            size=1,
        )
        self.stack_layout.add(error_component)
        self.focus(error_component)
