from .decorator import command
import ui


@command()
def navigate_list_top():
    ui.win.get_focused_view().go_top()


@command()
def navigate_list_bottom():
    ui.win.get_focused_view().go_bottom()


@command()
def navigate_list_by(offset):
    ui.win.get_focused_view().go_by(offset)


@command()
def navigate_next_page():
    ui.win.get_focused_view().next_page()


@command()
def navigate_previous_page():
    ui.win.get_focused_view().previous_page()


@command()
def autocomplete_input():
    ui.win.get_focused_view().autocomplete_input()
