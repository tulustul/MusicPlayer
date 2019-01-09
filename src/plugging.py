import os
import sys
import logging
import importlib

import pyinotify
from rx.subjects import Subject

import ui
from config import config

logger = logging.getLogger('plugins')

STANDARD_MODULES = [
    'models',
    'views',
    'commands',
]

modules = []

notifier = None

plugins_changes = Subject()


def load_plugin(module):
    for standart_module in STANDARD_MODULES:
        module_name = '{}.{}'.format(module.__name__, standart_module)
        logger.info(module_name)
        logger.info(importlib.util.find_spec(module_name))
        if importlib.util.find_spec(module_name):
            importlib.import_module(module_name)


def init_plugin(module):
    if hasattr(module, 'init'):
        module.init()


def destroy_module(module):
    if hasattr(module, 'destroy'):
        module.destroy()


def reload_plugin(module):
    logger.info('Reloading plugin: {}'.format(module.__name__))
    importlib.invalidate_caches()

    destroy_module(module)

    importlib.reload(module)

    submodules = (
        m for name, m in sys.modules.items()
        if name.startswith(module.__name__)
    )
    for submodule in submodules:
        importlib.reload(submodule)

    init_plugin(module)

    # ui.reinitialize()


plugins_changes.subscribe(reload_plugin)


class ChangeWatcher(pyinotify.ProcessEvent):

    def __init__(self, module):
        super().__init__()
        self.module = module

    def process_default(self, event):
        plugins_changes.on_next(self.module)


def init_plugins_watchers(loop):
    global notifier

    WATCH_FLAGS = (
        pyinotify.IN_CREATE |
        pyinotify.IN_DELETE |
        pyinotify.IN_DELETE_SELF |
        pyinotify.IN_MODIFY
    )

    wm = pyinotify.WatchManager()
    notifier = pyinotify.AsyncioNotifier(wm, loop)

    for module in modules:
        path = os.path.dirname(module.__file__)

        exclude = [os.path.join(path, '__pycache__')]
        # exclude = pyinotify.ExcludeFilter(os.path.join(path, '__pycache__'))

        wm.add_watch(
            path,
            WATCH_FLAGS,
            rec=True,
            proc_fun=ChangeWatcher(module),
            exclude_filter=pyinotify.ExcludeFilter(exclude),
        )


def load_plugins(loop):
    for plugins_path in config['plugins_paths']:
        sys.path.append(plugins_path)

    for plugin_name in config['plugins']:
        logger.info('Loading plugin: {}'.format(plugin_name))
        module = importlib.import_module('plugins.{}'.format(plugin_name))
        load_plugin(module)
        modules.append(module)

    if config['debug']:
        init_plugins_watchers(loop)


def init_plugins():
    for module in modules:
        init_plugin(module)


def destroy():
    if notifier:
        notifier.stop()

    for module in modules:
        destroy_module(module)
