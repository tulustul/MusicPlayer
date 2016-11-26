from commands.decorator import command
import commands_runner
import context
from . import palette_view


@command()
def open_palette():
    context.push('palette')


@command()
def run_command():
    context.pop()
    commands_runner.run_text_command(palette_view.value)
