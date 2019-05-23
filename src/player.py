#! /usr/bin/env python3
import logging
from typing import cast

from core.app import App
from player_ui import PlayerUI

logger = logging.getLogger('player')


class PlayerApp(App):

    def setup(self):
        self.ui = PlayerUI(self)
        self.injector.provide(PlayerUI, lambda: self.ui)

    @classmethod
    def get_instance(cls) -> 'PlayerApp':
        return cast(PlayerApp, cls._instance)


if __name__ == '__main__':
    PlayerApp().run_forever()
