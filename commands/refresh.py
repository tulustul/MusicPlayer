from .decorator import command
import ui


@command()
def refresh():
    ui.win.refresh()
