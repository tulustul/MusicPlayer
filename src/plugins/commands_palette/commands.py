from commands.decorator import command
from core.commands_runner import CommandsRunner
from ui.window import Window
from player_ui import PlayerUI

from .components import PaletteComponent


@command()
async def open_palette(
    commands_runner: CommandsRunner, ui: PlayerUI, window: Window
):
    palette = PaletteComponent(size=6)

    ui.stack_layout.add(palette)
    window.root_component.update_layout()

    window.focus(palette)

    subscription = window.input_component.value.subscribe(
        lambda value: palette.filter(value)
    )

    result = await window.input(">")

    window.blur_active_component()
    palette.detach()

    if result is not None:
        commands_runner.run_text_command(palette.value)

    if subscription:
        subscription.dispose()
