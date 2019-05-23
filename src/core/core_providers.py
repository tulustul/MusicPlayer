from ui.window import Window

from .commands_runner import CommandsRunner
from .audio.audio_backend import AudioBackend


def register_core_providers(app):
    from ui.components.listview import ListComponent
    from ui.components.tracks import TracksComponent

    app.injector.provide(Window, lambda: app.window)

    app.injector.provide(
        ListComponent,
        lambda: _get_component_by_class(app.window, ListComponent),
    )

    app.injector.provide(
        TracksComponent,
        lambda: _get_component_by_class(app.window, TracksComponent),
    )

    app.injector.provide(CommandsRunner, lambda: app.commander)
    app.injector.provide(AudioBackend, lambda: app.audio)


def _get_component_by_class(window: Window, cls: type):
    active_component = window.active_component
    if issubclass(active_component.__class__, cls):
        return window.active_component
    return None
