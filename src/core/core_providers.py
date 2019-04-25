from ui.components.listview import ListComponent
from ui.window import Window

from .commands_runner import CommandsRunner
from .audio.audio_backend import AudioBackend

def register_core_providers(app):
    app.injector.provide(Window, lambda: app.window)

    app.injector.provide(ListComponent, lambda: _get_list_component(app.window))

    app.injector.provide(CommandsRunner, lambda: app.commander)
    app.injector.provide(AudioBackend, lambda: app.audio)


def _get_list_component(window: Window):
    active_component = window.active_component
    if issubclass(active_component.__class__, ListComponent):
        return window.active_component
    return None