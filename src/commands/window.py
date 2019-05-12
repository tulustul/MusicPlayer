import logging

from core import context
from player_ui import PlayerUI
from ui.window import Window

from .decorator import command

logger = logging.getLogger('commands')


@command()
def focus_next_view(ui: PlayerUI, window: Window):
    if len(window.active_component_stack) > 1:
        component = window.active_component_stack.pop()
        window.active_component_stack.insert(0, component)
    elif ui.tabs_layout.displayed_tab:
        tab_index = ui.tabs_layout.tabs.index(ui.tabs_layout.displayed_tab)
        if tab_index != -1:
            new_index = tab_index + 1
            tabs_len = len(ui.tabs_layout.tabs)
            if new_index >= tabs_len:
                new_index = 0
            ui.tabs_layout.switch_to_tab_index(new_index)

            component = ui.tabs_layout.displayed_tab.component
            window.active_component_stack.pop()
            window.active_component_stack.append(component)
