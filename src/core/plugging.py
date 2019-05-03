import asyncio
import os
import sys
import logging
import importlib
from typing import Any, List, Optional
from types import ModuleType

import ui
from core.config import config

logger = logging.getLogger('plugging')


class Plugin:

    STANDARD_MODULES = [
        'models',
        'commands',
    ]

    def __init__(self, module: ModuleType):
        self.module: ModuleType = module
        self.controller: Optional[Any] = None
        self.load()

    def load(self):
        logger.info(f'Loading plugin: {self.module.__name__}')
        for standart_module in self.STANDARD_MODULES:
            module_name = '{}.{}'.format(self.module.__name__, standart_module)
            if importlib.util.find_spec(module_name):
                importlib.import_module(module_name)

    def start(self):
        if hasattr(self.module, 'controller'):
            self.controller = self.module.controller()

    def destroy(self):
        if self.controller and hasattr(self.controller, 'destroy'):
            self.controller.destroy()
        plugins.remove(self)

    def __repr__(self):
        return repr(self.module)


plugins: List[Plugin] = []


def load_plugins():
    for plugins_path in config['plugins_paths']:
        sys.path.append(plugins_path)

    for plugin_name in config['plugins']:
        module = importlib.import_module('plugins.{}'.format(plugin_name))
        plugins.append(Plugin(module=module))


def start_plugins():
    for plugin in plugins:
        plugin.start()


def destroy():
    for plugin in plugins:
        plugin.destroy()
