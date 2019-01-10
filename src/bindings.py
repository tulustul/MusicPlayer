from collections import defaultdict
import logging

import commands
import commands_runner
import config
import keyboard
import context


logger = logging.getLogger('keybindings')

general_keybindings: dict = {}

context_keybindings: dict = defaultdict(dict)


def get_binding(key: str):
    logger.info(context.current_context.name)
    binding_context = context_keybindings.get(
        context.current_context.name,
    ) or {}
    return binding_context.get(key) or general_keybindings.get(key)


def handle_keys(key: str):
    logger.debug('key pressed: {}'.format(key))
    binding = get_binding(key)
    if binding:
        command, args = binding
        commands_runner.run_command(command, *args)


def init():
    config_keybindings = config.get_keybindings()

    for binding in config_keybindings:
        for key in binding['keys']:
            command_name = binding['command']
            command = commands.registry.get_by_name(command_name)
            if command is None:
                raise ValueError('Unknown command {}'.format(command_name))
            args = binding.get('args', [])

            keybinding = (command, args)

            binding_context = binding.get('context')
            if binding_context:
                context_keybindings[binding_context][key] = keybinding
            else:
                general_keybindings[key] = keybinding

    keyboard.keys.subscribe(handle_keys)