from commands.decorator import command
from core.commands_runner import CommandsRunner
from plugins import commands_palette
from ui.window import Window
from player import PlayerUI

from .components import PaletteComponent


@command()
async def open_palette(commands_runner: CommandsRunner, ui: PlayerUI, window: Window):
    palette = PaletteComponent(desired_size=6)

    ui.stack_layout.add(palette)

    window.focus(palette)

    input_coroutine = window.input('>')

    if window.input_component:
        subscription = window.input_component.value.subscribe(
            lambda value: palette.filter(value),
        )

    result = await input_coroutine

    window.blur_active_component()
    palette.detach()

    if result is not None:
        commands_runner.run_text_command(palette.value)

    if subscription:
        subscription.dispose()
