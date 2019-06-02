from collections import defaultdict
import logging

import commands
from core import (
    commands_runner,
    config,
    keyboard,
)
from ui.window import Window

logger = logging.getLogger('keybindings')


class BindingsController:

    general_keybindings: dict = {}

    context_keybindings: dict = defaultdict(dict)

    def __init__(
        self,
        commander: commands_runner.CommandsRunner,
        window: Window,
    ):
        self.commander = commander
        self.window = window

        for binding in config.keybindings:
            keys = binding['keys']
            if isinstance(keys, str):
                keys = [keys]

            for key in keys:
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
        current_context = self.window.active_component.context
        binding_context = self.context_keybindings.get(current_context) or {}
        return binding_context.get(key) or self.general_keybindings.get(key)

    def handle_keys(self, key: str):
        if not self.window.input_mode or key in ('<up>', '<down>'):
            binding = self.get_binding(key)
            if binding:
                command, args = binding
                self.commander.run_command(command, *args)
