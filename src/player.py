#! /usr/bin/env python3
import asyncio
import logging

from commands import core_commands
from core.app import App
from player_ui import PlayerUI

logger = logging.getLogger('player')


class PlayerApp(App):

    def setup(self):
        self.ui = PlayerUI(self)
        self.injector.provide(PlayerUI, lambda: self.ui)


if __name__ == '__main__':
    PlayerApp().run_forever()
