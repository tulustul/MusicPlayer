from collections import defaultdict
import logging


from commands import registry
import commands_runner
import config
import keyboard
import ui

logger = logging.getLogger('keybindings')

general_keybindings = {}
context_keybindings = defaultdict(dict)

config_keybindings = config.get_keybindings()

for binding in config_keybindings:
    for key in binding['keys']:
        command_name = binding['command']
        command = registry.get_by_name(command_name)
        if command is None:
            raise ValueError('Unknown command {}'.format(command_name))
        args = binding.get('args', [])

        keybinding = (command, args)

        context = binding.get('context')
        if context:
            context_keybindings[context][key] = keybinding
        else:
            general_keybindings[key] = keybinding


def get_binding(key):
    context = context_keybindings.get(ui.win.current_view) or {}
    return context.get(key) or general_keybindings.get(key)


def handle_keys(key):
    logger.debug('key pressed: {}'.format(key))
    binding = get_binding(key)
    if binding:
        command, args = binding
        commands_runner.run_command(command, *args)


def init():
    keyboard.keys.subscribe(handle_keys)
