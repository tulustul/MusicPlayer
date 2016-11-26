from commands.decorator import command
import ui
import commands_runner
import context


@command()
def open_palette():
    context.push('palette')
    # ui.win.show_view('palette')


@command()
def run_command():
    ui.win.hide_view('palette')
    commands_runner.run_text_command(ui.win.views['palette'].value)


@command()
def cancel_palette():
    ui.win.hide_view('palette')
