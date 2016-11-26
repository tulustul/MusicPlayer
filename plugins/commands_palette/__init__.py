from .views import Palette
from config import config
import context
import ui

palette_view = None


def show_palette(_):
    ui.win.open_view_in(palette_view, config['palette']['open_in'])


def init():
    global palette_view

    palette_view = Palette()
    context.register('palette')
    context.switch.filter(lambda s: s == 'palette').subscribe(show_palette)


def destroy():
    ...
