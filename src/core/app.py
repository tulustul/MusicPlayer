#! /usr/bin/env python3

import asyncio
import sys
import traceback
import logging
import curses
from typing import Optional

import setproctitle

from core.errors import errors
from ui.window import Window

from .config import config
from . import (
    plugging,
    audio,
    bindings,
    context,
    keyboard,
    db,
    dependency_injection,
    core_providers,
    commands_runner,
)

logger = logging.getLogger('app')

errors.subscribe(lambda e: logger.error(e))

def log_exception(window=None):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error = ''.join(traceback.format_exception(
        exc_type, exc_value, exc_traceback,
    ))
    logger.error(error)

    if window:
        window.destroy()

    print(error)


class App:

    def __init__(self):
        self.crashed = False
        self.loop = None
        self.window = None

        try:
            setproctitle.setproctitle('music-player')

            self.loop = asyncio.get_event_loop()

            if config['log_level'] == 'DEBUG':
                self.loop.set_debug(True)

            # audio.init(loop)
            plugging.load_plugins(self.loop)
            # db.init()
            self.window = Window(self.loop)
            self.injector = dependency_injection.Injector()

            self.commander = commands_runner.CommandsRunner(
                self.loop, self.injector,
            )
            self.binding_controller = bindings.BindingsController(
                self.commander, self.window,
            )
            plugging.init_plugins()

            context.push(config['default_context'])

            core_providers.register_core_providers(self)
        except Exception as e:
            self.crashed = True
            log_exception(self.window)
            self.destroy()
            raise e

    def run_forever(self):
        try:
            running = True
            while running:
                try:
                    running = False
                    self.loop.run_until_complete(self.window.process_input())
                except KeyboardInterrupt:
                    running = True
                    keyboard.raw_keys.on_next(curses.KEY_EXIT)
        except Exception as e:
            self.crashed = True
            log_exception(self.window)
        finally:
            self.destroy()

    def destroy(self):
        plugging.destroy()
        if self.window:
            self.window.destroy()
        # audio.destroy()
        for task in asyncio.Task.all_tasks():
            task.cancel()
        try:
            if self.loop:
                self.loop.run_until_complete(
                    asyncio.gather(*asyncio.Task.all_tasks())
                )
        except asyncio.CancelledError:
            pass
        finally:
            if self.loop:
                self.loop.close()
            if self.crashed:
                sys.exit(1)
