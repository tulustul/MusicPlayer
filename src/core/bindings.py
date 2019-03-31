from collections import defaultdict
import logging
from typing import cast

import commands
from core import (
    commands_runner,
    config,
    keyboard,
    context,
)

logger = logging.getLogger('keybindings')


class BindingsController:

    general_keybindings: dict = {}

    context_keybindings: dict = defaultdict(dict)

    def __init__(self, commander: commands_runner.CommandsRunner):
        self.commander = commander

        config_keybindings = config.get_keybindings()

        for binding in config_keybindings:
            for key in binding['keys']:
                command_name = binding['command']
                command = commands.registry.get_by_name(command_name)
                if command is None:
                    logger.error('Unknown command {}'.format(command_name))

                args = binding.get('args', [])

                keybinding = (command, args)

                binding_context = binding.get('context')
                if binding_context:
                    self.context_keybindings[binding_context][key] = keybinding
                else:
                    self.general_keybindings[key] = keybinding

        keyboard.keys.subscribe(self.handle_keys)

    def get_binding(self, key: str):
        current_context = cast(context.Context, context.current_context)
        logger.info(current_context.name)
        binding_context = self.context_keybindings.get(
            current_context.name,
        ) or {}
        return binding_context.get(key) or self.general_keybindings.get(key)


    def handle_keys(self, key: str):
        logger.debug('key pressed: {}'.format(key))
        binding = self.get_binding(key)
        if binding:
            command, args = binding
            self.commander.run_command(command, *args)
