from ui.components.listview import ListComponent
from ui.window import Window

from .dependency_injection import Injector

def register_core_providers(injector: Injector, window: Window):
    injector.provide(Window, lambda: window)

    injector.provide(ListComponent, lambda: _get_list_component(window))


def _get_list_component(window: Window):
    if issubclass(window.current_view.__class__, ListComponent):
        return window.current_view
    return None
