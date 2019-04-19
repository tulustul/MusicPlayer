import logging

# from .components import PaletteComponent
# from config import config
# import context
# import ui

logger = logging.getLogger('palette')

palette_view = None


# def show_palette(_):
#     ui.win.open_view_in(palette_view, config['palette']['open_in'])


# def hide_palette(_):
#     logger.debug('hide_palette')
#     ui.win.remove_view_from(palette_view, config['palette']['open_in'])


def init():
    pass
    # global palette_view

    # palette_view = Palette()
    # palette_context = context.register('palette')
    # palette_context.on_enter.subscribe(show_palette)
    # palette_context.on_exit.subscribe(hide_palette)


def destroy():
    ...
