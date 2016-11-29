from commands.decorator import command
import commands_runner
import context
from plugins import commands_palette


@command()
def open_palette():
    context.push('palette')


@command()
def run_command():
    context.pop()
    commands_runner.run_text_command(commands_palette.palette_view.value)
